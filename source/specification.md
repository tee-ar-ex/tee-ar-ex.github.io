# TRX Specification

This page defines the TRX file format specification. The authoritative
specification is maintained in the
[trx-spec](https://github.com/tee-ar-ex/trx-spec) repository.

## General

- Uncompressed ZIP file or simple folder architecture
- File architecture describes the data
- Each file basename is the metadata's name
- Each file extension is the metadata's dtype
- Each file dimension is in the value between basename and metadata
- 1-dimensional arrays do not have to follow this convention for readability
- All arrays have a C-style memory layout (row-major)
- All arrays have a little-endian byte order
- Compression is optional
  - Use `ZIP_STORE` if no compression is desired
  - Use `ZIP_DEFLATE` if compression is desired
  - Compressed TRX files will have to be decompressed before being loaded

## Header

The header is primarily for human readability, read-time checks, and broader
compatibility.

- Dictionary in JSON
  - `VOXEL_TO_RASMM` — 4 lists of 4 floats (4x4 transformation matrix)
  - `DIMENSIONS` — list of 3 uint16
  - `NB_STREAMLINES` — uint32
  - `NB_VERTICES` — uint64

## Arrays

### positions

- Written in world space (RASMM), like TCK files
- Always float16, float32, or float64 (default: float16)
- Stored as contiguous 3D array `(NB_VERTICES, 3)`

### offsets

- Always uint32 or uint64
- Contains the index where each streamline starts in the positions array,
  beginning at 0
- Two ways of knowing how many vertices there are:
  - Check the header
  - Positions array size / dtype / 3
- To get streamline lengths: append the total number of vertices to the end of
  offsets and take the differences between consecutive elements
  (`numpy.ediff1d`)

### dpv (data per vertex)

- Always of size `(NB_VERTICES, 1)` or `(NB_VERTICES, N)`

### dps (data per streamline)

- Always of size `(NB_STREAMLINES, 1)` or `(NB_STREAMLINES, N)`

### groups

Groups are tables of indices that allow sparse and overlapping representation
(clusters, connectomics, bundles).

- All indices must satisfy `0 <= id < NB_STREAMLINES`
- Datatype should be uint32
- Allow efficient extraction of a predefined streamline subset from memmaps
- Variable sizes across groups

### dpg (data per group)

- Each subfolder is named after its corresponding group
- Not all metadata need be present in all groups
- Always of size `(1,)` or `(N,)`

## Accepted datatypes

- int8, int16, int32, int64
- uint8, uint16, uint32, uint64
- float16, float32, float64
- bit (for binary/boolean arrays)

## Example structure

```
OHBM_demo.trx
├── dpg
│   ├── AF_L
│   │   ├── mean_fa.float16
│   │   ├── shuffle_colors.3.uint8
│   │   └── volume.uint32
│   ├── AF_R
│   │   ├── mean_fa.float16
│   │   ├── shuffle_colors.3.uint8
│   │   └── volume.uint32
│   ├── CC
│   │   ├── mean_fa.float16
│   │   ├── shuffle_colors.3.uint8
│   │   └── volume.uint32
│   ├── CST_L
│   │   └── shuffle_colors.3.uint8
│   ├── CST_R
│   │   └── shuffle_colors.3.uint8
│   ├── SLF_L
│   │   ├── mean_fa.float16
│   │   ├── shuffle_colors.3.uint8
│   │   └── volume.uint32
│   └── SLF_R
│       ├── mean_fa.float16
│       ├── shuffle_colors.3.uint8
│       └── volume.uint32
├── dpv
│   ├── color_x.uint8
│   ├── color_y.uint8
│   ├── color_z.uint8
│   └── fa.float16
├── dps
│   ├── algo.uint8
│   ├── algo.json
│   ├── clusters_QB.uint16
│   ├── commit_colors.3.uint8
│   └── commit_weights.float32
├── groups
│   ├── AF_L.uint32
│   ├── AF_R.uint32
│   ├── CC.uint32
│   ├── CST_L.uint32
│   ├── CST_R.uint32
│   ├── SLF_L.uint32
│   └── SLF_R.uint32
├── header.json
├── offsets.uint64
└── positions.3.float16
```

## Example code

```python
from trx.trx_file_memmap import TrxFile, load, save
import numpy as np

trx = load('complete_tractogram.trx')

# Access the header (dict) / streamlines (ArraySequences)
trx.header
trx.streamlines

# Access the dpv (dict) / dps (dict)
trx.data_per_vertex
trx.data_per_streamline

# Access the groups (dict) / dpg (dict)
trx.groups
trx.data_per_group

# Get a random subset of 10000 streamlines
indices = np.arange(len(trx.streamlines._lengths))
np.random.shuffle(indices)
sub_trx = trx.select(indices[0:10000])
save(sub_trx, 'random_1000.trx')

# Get sub-groups only, from the random subset
for key in sub_trx.groups.keys():
    group_trx = sub_trx.get_group(key)
    save(group_trx, '{}.trx'.format(key))

# Pre-allocate memmaps and append 100x the random subset
alloc_trx = TrxFile(nb_streamlines=1500000, nb_vertices=500000000, init_as=trx)
for i in range(100):
    alloc_trx.append(sub_trx)

# Resize to remove the unused portion of the memmap
alloc_trx.resize()
```
