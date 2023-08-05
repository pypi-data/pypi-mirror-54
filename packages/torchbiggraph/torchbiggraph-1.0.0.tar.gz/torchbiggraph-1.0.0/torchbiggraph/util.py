#!/usr/bin/env python3

# Copyright (c) Facebook, Inc. and its affiliates.
# All rights reserved.
#
# This source code is licensed under the BSD-style license found in the
# LICENSE.txt file in the root directory of this source tree.

import logging
import multiprocessing as mp
import multiprocessing.pool  # noqa: F401
import os
import os.path
import sys
from collections import defaultdict
from functools import partial
from typing import Any, Callable, Dict, Iterable, List, Optional, Set, Tuple, TypeVar

import torch
import torch.multiprocessing
from torch.optim import Optimizer

from torchbiggraph.config import ConfigSchema
from torchbiggraph.types import Bucket, EntityName, FloatTensorType, Side


logger = logging.getLogger("torchbiggraph")


def tag_logs_with_process_name(process_name: str) -> None:
    def filter_(record: logging.LogRecord) -> bool:
        record.processName = process_name
        return True
    logger.addFilter(filter_)


def hide_distributed_logging() -> None:
    def filter_(record: logging.LogRecord) -> bool:
        return not getattr(record, "distributed", False)
    logger.addFilter(filter_)


def set_logging_verbosity(verbosity_level: int) -> None:
    if verbosity_level == 0:
        logger.setLevel(logging.INFO)
    elif verbosity_level == 1:
        logger.setLevel(logging.DEBUG)
    else:
        raise ValueError(f"Unknown verbosity level: {verbosity_level}")


# This function is only intended for internal usage by PBG's own cmdline scripts.
def setup_logging(verbosity_level: int = 0) -> None:
    set_logging_verbosity(verbosity_level)
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(CustomLoggingFormatter())
    logging.basicConfig(handlers=[handler])


class BucketLogger(logging.LoggerAdapter):

    def __init__(self, logger_: logging.Logger, bucket: Bucket) -> None:
        super().__init__(logger_, extra={"bucket": bucket})

    def process(self, msg: str, kwargs: Dict[str, Any]) -> Tuple[str, Dict[str, Any]]:
        bucket: Bucket = self.extra["bucket"]
        msg = f"{bucket}: {msg}"
        return msg, kwargs


class CustomLoggingFormatter(logging.Formatter):

    def usesTime(self) -> bool:
        return True

    def formatMessage(self, record: logging.LogRecord) -> str:
        msg = record.message
        if record.levelname not in ("DEBUG", "INFO"):
            msg = f"{record.levelname}: {msg}"
        process_name = getattr(record, "processName", None)
        if process_name is not None:
            process_name = f"[{process_name[-10:]}]"
        else:
            process_name = ""
        msg = f"{record.asctime}  {process_name:>12} {msg}"
        return msg


class SubprocessInitializer:

    def __init__(self) -> None:
        self.initializers: List[Callable[[], None]] = []

    def register(
        self,
        init_function: Callable[[], None],
        *args: Any,
        **kwargs: Any,
    ) -> None:
        # A check in case anyone *calls* the function when passing it.
        if init_function is None:
            raise ValueError("init_function must be a callable, got None")
        self.initializers.append(partial(init_function, *args, **kwargs))

    def __call__(self) -> None:
        for f in self.initializers:
            f()


def call_one_after_the_other(*funcs: Optional[Callable[[], None]]) -> None:
    for f in funcs:
        if f is not None:
            f()


class CouldNotLoadData(Exception):
    pass


def split_almost_equally(size: int, *, num_parts: int) -> Iterable[slice]:
    """Split an interval of the given size into the given number of subintervals

    The sizes of the subintervals will be between the floor and the ceil of the
    "exact" fractional size, with larger intervals preceding smaller ones.

    """
    size_per_part = size // num_parts
    num_larger_parts = size % num_parts
    prev = 0
    for i in range(num_parts):
        next_ = prev + size_per_part + (1 if i < num_larger_parts else 0)
        yield slice(prev, next_)
        prev = next_


def round_up_to_nearest_multiple(value: int, factor: int) -> int:
    return ((value - 1) // factor + 1) * factor


def fast_approx_rand(numel: int) -> FloatTensorType:
    if numel < 1_000_003:
        tensor = torch.randn(numel)
        # share_memory_ does return the tensor but its type annotation says it
        # doesn't, thus we do this in two separate steps.
        tensor.share_memory_()
        return tensor
    # construct the tensor storage in shared mem so we don't have to copy it
    storage = torch.FloatStorage._new_shared(numel)
    tensor = torch.FloatTensor(storage)
    rand = torch.randn(1_000_003)
    excess = numel % 1_000_003
    # Using just `-excess` would give bad results when excess == 0.
    tensor[:numel - excess].view(-1, 1_000_003)[...] = rand
    tensor[numel - excess:] = rand[:excess]
    return tensor


class DummyOptimizer(Optimizer):

    def __init__(self) -> None:
        # This weird dance makes Optimizer accept an empty parameter list.
        super().__init__([{'params': []}], {})

    def step(self, closure: None = None) -> None:
        pass

    def state_dict(self) -> Dict[str, Any]:
        return {}

    def load_state_dict(self, state_dict: Dict[str, Any]) -> None:
        pass

    def share_memory(self) -> None:
        pass


# HOGWILD

def _pool_init(
    subprocess_name: Optional[str] = None,
    subprocess_init: Optional[Callable[[], None]] = None,
) -> None:
    torch.set_num_threads(1)
    torch.manual_seed(os.getpid())
    # FIXME Add the rank to the name of each process.
    if subprocess_name is not None:
        tag_logs_with_process_name(subprocess_name)
    if subprocess_init is not None:
        subprocess_init()


def create_pool(
    num_workers: int,
    subprocess_name: Optional[str] = None,
    subprocess_init: Optional[Callable[[], None]] = None,
) -> mp.Pool:
    # PyTorch relies on OpenMP, which by default parallelizes operations by
    # implicitly spawning as many threads as there are cores, and synchronizing
    # them with each other. This interacts poorly with Hogwild!-style subprocess
    # pools as if each child process spawns its own OpenMP threads there can
    # easily be thousands of threads that mostly wait in barriers. Calling
    # set_num_threads(1) in both the parent and children prevents this.
    # OpenMP can also lead to deadlocks if it gets initialized in the parent
    # process before the fork (this bit us in unit tests, due to the generation
    # of the test input data). Using the "spawn" context (i.e., fork + exec)
    # solved the issue in most cases but still left some deadlocks. See
    # https://github.com/pytorch/pytorch/issues/17199 for some more information
    # and discussion.
    torch.set_num_threads(1)
    return mp.get_context("spawn").Pool(
        num_workers, initializer=_pool_init, initargs=(subprocess_name, subprocess_init,)
    )


T = TypeVar("T")


def get_async_result(
    future_res: "mp.pool.AsyncResult[T]",
    pool: mp.Pool,
    health_check_interval: float = 1.0,
) -> T:
    """Wait for an AsyncResult while checking the health of the pool.

    If the processes of an mp.Pool die unexpectedly, the pool will respawn them
    over and over (https://bugs.python.org/issue22393). This hacky function
    (which accesses a private attribute) tries to make up for that by storing
    the initial set of processes and repeatedly polling their health.
    In Python 3.7 we can switch to concurrent.futures.ProcessPoolExecutor, where
    this issue has already been fixed (https://bugs.python.org/issue9205). We
    can't use it now because we need the mp_context and initializer arguments.
    """
    processes = list(pool._pool)
    while True:
        try:
            res = future_res.get(health_check_interval)
        except mp.TimeoutError:
            pass
        else:
            return res
        for p in processes:
            if not p.is_alive():
                raise RuntimeError(
                    f"A subprocess exited unexpectedly with status {p.exitcode}")


# config routines

def get_partitioned_types(
    config: ConfigSchema,
    side: Side,
) -> Tuple[int, Set[EntityName]]:
    """Return the number of partitions on a given side and the partitioned entity types

    Each of the entity types that appear on the given side (LHS or RHS) of a relation
    type is split into some number of partitions. The ones that are split into one
    partition are called "unpartitioned" and behave as if all of their entities
    belonged to all buckets. The other ones are the "properly" partitioned ones.
    Currently, they must all be partitioned into the same number of partitions. This
    function returns that number and the names of the properly partitioned entity
    types.

    """
    entity_names_by_num_parts: Dict[int, Set[EntityName]] = defaultdict(set)
    for relation_config in config.relations:
        entity_name = side.pick(relation_config.lhs, relation_config.rhs)
        entity_config = config.entities[entity_name]
        entity_names_by_num_parts[entity_config.num_partitions].add(entity_name)

    if 1 in entity_names_by_num_parts:
        del entity_names_by_num_parts[1]

    if len(entity_names_by_num_parts) == 0:
        return 1, set()
    if len(entity_names_by_num_parts) > 1:
        raise RuntimeError("Currently num_partitions must be a single "
                           "value across all partitioned entities.")

    (num_partitions, partitioned_entity_names), = entity_names_by_num_parts.items()
    return num_partitions, partitioned_entity_names


# compute a randomized AUC using a fixed number of sample points
# NOTE: AUC is the probability that a randomly chosen positive example
# has a higher score than a randomly chosen negative example
def compute_randomized_auc(
    pos_: FloatTensorType,
    neg_: FloatTensorType,
    num_samples: int,
) -> float:
    pos_, neg_ = pos_.view(-1), neg_.view(-1)
    diff = (pos_[torch.randint(len(pos_), (num_samples,))]
            > neg_[torch.randint(len(neg_), (num_samples,))])
    return float(diff.float().mean())


def get_num_workers(override: Optional[int]) -> int:
    if override is not None:
        return override
    cpu_count = os.cpu_count()
    if cpu_count is not None:
        return cpu_count
    result = 40
    logger.warning(
        f"The number of workers was left unspecified and the CPU count "
        f"couldn't be auto-detected; defaulting to {result} workers.")
    return result
