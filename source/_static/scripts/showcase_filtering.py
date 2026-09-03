"""
Metadata-Driven Filtering and Anatomical Bundle Extraction.

Requirements:
    pip install trx-python dipy numpy

Usage:
    python showcase_filtering.py
"""
import logging
import os
from time import time
import numpy as np

from trx.trx_file_memmap import load, save
from dipy.io.streamline import save_tractogram

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%H:%M:%S",
)

# 1. Load whole-brain tractogram with metadata
logging.info("Loading whole-brain tractogram with metadata...")
trx = load("complete_tractogram.trx")
logging.info(
    "Loaded tractogram: %d streamlines, %d vertices",
    len(trx.streamlines),
    len(trx.streamlines._data),
)

# 2. Vectorized filtering on microstructure and tracking algorithm
# Filtering criteria:
# - commit_weights > 0: streamlines contributing non-zero signal in COMMIT
# - algo == 4: probabilistic tracking (1: DTI, 2: EuDX, 3: Det, 4: Prob)
logging.info(
    "Filtering streamlines by microstructure weight and tracking algorithm..."
)
timer = time()
ind_commit = np.argwhere(trx.data_per_streamline["commit_weights"] > 0).T[0]
ind_prob = np.argwhere(trx.data_per_streamline["algo"] == 4).T[0]
indices = np.intersect1d(ind_prob, ind_commit)
filtering_time = time() - timer

logging.info(
    "Identified %d / %d valid streamlines in %.3fs",
    len(indices),
    len(trx.streamlines),
    filtering_time,
)

# Subsetting via .select() preserves groups and group metadata (DPG)
timer = time()
sub_trx = trx.select(indices)
logging.info("Created sub-tractogram via .select() in %.3fs", time() - timer)

# Save filtered sub-tractogram directly
save(sub_trx, "filtered_prob_commit.trx")
logging.info("Saved filtered sub-tractogram to 'filtered_prob_commit.trx'")

# 3. Extract each anatomical bundle as an independent tractogram
groups_dir = "groups"
if not os.path.isdir(groups_dir):
    os.mkdir(groups_dir)

logging.info("Extracting and saving individual bundle groups...")
for key in sub_trx.groups.keys():
    group_trx = sub_trx.get_group(key)
    logging.info(
        "  Bundle '%s': %d streamlines", key, len(group_trx.streamlines)
    )
    sft = group_trx.to_sft()
    save_tractogram(sft, os.path.join(groups_dir, f"{key}.trk"))
    save(group_trx, os.path.join(groups_dir, f"{key}.trx"))

logging.info("Group extraction and export complete.")
