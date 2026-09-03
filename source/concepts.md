# Core Concepts

This page describes the TRX file format specification. The authoritative (and dry!) text of the specification is maintained in the [trx-spec](https://github.com/tee-ar-ex/trx-spec) repository, and can be read [there](https://tee-ar-ex.github.io/trx-spec). To learn more about the motivation for TRX, refer to {doc}`design`.

## The TRX format

### Layout
A TRX file is a ZIP archive (or on-disk directory) whose layout directly
encodes its data model:

- `header.json` — spatial metadata
- `positions.<dim>.<dtype>` — all streamline vertices in a single flat array
- `offsets.<dtype>` — prefix-sum index from streamlines into positions
- `dpv/<name>.<dtype>` — per-vertex metadata arrays
- `dps/<name>.<dtype>` — per-streamline metadata arrays
- `groups/<name>.uint32` — named index sets of streamlines
- `dpg/<group>/<name>.<dtype>` — per-group metadata arrays

Coordinates are stored in **RAS+ world space** (millimeters), matching the
convention used by MRtrix3 `.tck` and NIfTI qform outputs.

### Header

`header.json` stores:

- `VOXEL_TO_RASMM` — 4x4 affine mapping voxel indices to RAS+ world
  coordinates (mm)
- `DIMENSIONS` — reference image grid dimensions as three `uint16` values
- `NB_STREAMLINES` — number of streamlines (`uint32`)
- `NB_VERTICES` — total number of vertices across all streamlines (`uint64`)

The header is primarily for human readability and downstream compatibility. The
authoritative sizes come from the array dimensions themselves.

### Arrays

#### Positions array

All streamline vertices are stored in a single flat matrix of shape
`(NB_VERTICES, 3)`. Keeping all vertices contiguous enables efficient memory
mapping and avoids per-streamline allocations.

#### Offsets and the sentinel

`offsets` is a prefix-sum index of length `NB_STREAMLINES + 1`. Element *i* is
the offset in `positions` of the first vertex of streamline *i*. The final
element is a **sentinel** equal to `NB_VERTICES`, which makes length
computation trivial without special-casing the last streamline:

```
length_i = offsets[i + 1] - offsets[i]
```

This design avoids per-streamline allocations and makes slicing the global
positions array fast and uniform.

#### Data per vertex (DPV)

A DPV array stores one value per vertex in `positions`. It has shape
`(NB_VERTICES, 1)` for scalar fields or `(NB_VERTICES, N)` for vector-valued
fields. Typical uses:

- FA values along the tract
- Per-point RGB colors
- Confidence or weight measures per vertex

DPV arrays live under `dpv/` and are memory-mapped in the same way as
`positions`.

#### Data per streamline (DPS)

A DPS array stores one value per streamline. It has shape
`(NB_STREAMLINES, 1)` or `(NB_STREAMLINES, N)`. Typical uses:

- Mean FA or average curvature per tract
- Per-streamline cluster labels
- Tractography algorithm weights

DPS arrays live under `dps/` and are loaded as typed matrix fields. If the
on-disk dtype differs from the requested typed reader dtype, values are
converted during load.

### Groups

A group is a named list of streamline indices stored as a `uint32` array under
`groups/`. Groups enable sparse, overlapping labeling: a streamline can belong
to multiple groups, and groups can have different sizes. Typical uses:

- Bundle labels (`CST_L`, `CC`, `SLF_R`, ...)
- Cluster assignments from QuickBundles or similar algorithms
- Connectivity subsets (streamlines connecting two ROIs)

#### Data per group (DPG)

DPG attaches metadata to a group. Each group folder `dpg/<name>/` can contain
any number of scalar or vector arrays. Typical uses:

- Mean FA across the bundle
- Per-bundle display color
- Volume or surface-area estimates

### Accepted datatypes

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

For a much more extensive example, please see {doc}`showcase` or visit the
examples provided in each of the language-specific implementations (linked in the
sidebar to the left).

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
