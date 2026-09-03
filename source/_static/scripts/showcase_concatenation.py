"""
Assembling Tractograms: Batch Concatenation vs Incremental vs Pre-allocated.

Requirements:
    pip install trx-python numpy

Usage:
    python showcase_concatenation.py
"""
import logging
from time import time
import numpy as np

from trx.trx_file_memmap import TrxFile, load, concatenate

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%H:%M:%S",
)

filename = "groups/CC.trx"
iteration = 100

logging.info("Loading reference tractogram '%s'...", filename)
trx = load(filename)
chunk_len = len(trx.streamlines)
chunk_pts = len(trx.streamlines._data)
logging.info(
    "Reference chunk: %d streamlines, %d vertices", chunk_len, chunk_pts
)

# --- Strategy 1: Batch concatenation (known input list) ---
logging.info("--- Strategy 1: Batch concatenation (known input list) ---")
timer = time()
concat_trx = concatenate([trx for _ in range(iteration)])
concat_time = time() - timer
logging.info(
    "Concatenated %dx chunks (%d streamlines) in %.3fs (%.1f streamlines/s)",
    iteration,
    len(concat_trx.streamlines),
    concat_time,
    len(concat_trx.streamlines) / concat_time,
)

# --- Strategy 2: Naive incremental append (dynamic reallocation) ---
logging.info(
    "--- Strategy 2: Naive incremental append (dynamic reallocation) ---"
)
append_trx = load(filename)
timer = time()
append_durations = []
for i in range(iteration - 1):
    step_timer = time()
    append_trx.append(trx)
    append_durations.append(time() - step_timer)

total_naive_time = time() - timer
logging.info(
    "Naive append %dx chunks: total %.3fs (avg per call: %.4fs)",
    iteration,
    total_naive_time,
    np.mean(append_durations),
)

# --- Strategy 3: Pre-allocated memory map append (recommended) ---
logging.info(
    "--- Strategy 3: Pre-allocated memory map append (recommended) ---"
)
max_streamlines = 10_000_000
max_vertices = 500_000_000

# 1. Pre-allocate buffer capacity on disk (RAM overhead is ~0 MB via mmap)
timer = time()
alloc_trx = TrxFile(
    nb_streamlines=max_streamlines,
    nb_vertices=max_vertices,
    init_as=trx,
)
alloc_init_time = time() - timer
logging.info(
    "Pre-allocated buffer capacity: %d streamlines, %d vertices "
    "(init: %.4fs, RAM: ~0 MB)",
    max_streamlines,
    max_vertices,
    alloc_init_time,
)

# 2. Append chunks directly into pre-allocated memory-mapped arrays
timer = time()
prealloc_durations = []
for i in range(iteration):
    step_timer = time()
    alloc_trx.append(trx)
    prealloc_durations.append(time() - step_timer)

total_prealloc_time = time() - timer
real_strs, real_pts = alloc_trx._get_real_len()

logging.info(
    "Pre-allocated append %dx chunks: total %.3fs (avg per call: %.4fs)",
    iteration,
    total_prealloc_time,
    np.mean(prealloc_durations),
)
logging.info(
    "Buffer state before resize: allocated = %d, real data count = %d",
    max_streamlines,
    real_strs,
)

# 3. Truncate trailing unused storage back to exact written content
timer = time()
alloc_trx.resize()
resize_time = time() - timer
logging.info(
    "Trimmed buffer to exact content (%d streamlines, %d vertices) in %.4fs",
    len(alloc_trx.streamlines),
    len(alloc_trx.streamlines._data),
    resize_time,
)
