"""
Managing Pre-Allocated Memory Maps, Dynamic Resizing, and Compaction.

Requirements:
    pip install trx-python dipy

Usage:
    python showcase_resizing.py
"""
import logging
from trx.trx_file_memmap import load, save

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%H:%M:%S",
)

logging.info("Loading reference tractogram 'complete_tractogram.trx'...")
trx = load("complete_tractogram.trx")

# Create an independent, writable deepcopy of the memory maps
logging.info("Creating independent deepcopy of the tractogram...")
new_trx = trx.deepcopy()
logging.info(
    "Initial state: streamline_count = %d, vertex_count = %d",
    len(new_trx.streamlines),
    len(new_trx.streamlines._data),
)

# Step 1: Downsize streamline count and buffer to 100,000
logging.info("Step 1: Downsizing to 100,000 streamlines...")
new_trx.resize(nb_streamlines=100_000)
logging.info(
    "After downsizing: streamline_count = %d, vertex_count = %d",
    len(new_trx.streamlines),
    len(new_trx.streamlines._data),
)

# Step 2: Expand buffer capacity to 1,000,000 without altering existing valid data
logging.info("Step 2: Expanding buffer capacity to 1,000,000 streamlines...")
new_trx.resize(nb_streamlines=1_000_000)
real_strs, real_pts = new_trx._get_real_len()
logging.info(
    "After capacity expansion: allocated buffer capacity = %d, valid data count = %d",
    new_trx.header["NB_STREAMLINES"],
    real_strs,
)

# Step 3: Trim buffer to exact occupied content
logging.info("Step 3: Trimming buffer to exact data content...")
new_trx.resize()
logging.info(
    "After final trim: streamline_count = %d, vertex_count = %d",
    len(new_trx.streamlines),
    len(new_trx.streamlines._data),
)

# Step 4: Persist trimmed tractogram and export to StatefulTractogram
save_path = "resized_tractogram.trx"
save(new_trx, save_path)
logging.info("Persisted resized tractogram to '%s'", save_path)

sft = new_trx.to_sft()
logging.info(
    "Converted to StatefulTractogram: %d streamlines in %s space",
    len(sft),
    sft.space,
)
