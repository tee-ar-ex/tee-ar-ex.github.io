# Design Rationale

This page explains the motivation and design decisions behind the TRX file
format. The TRX emerged from a
[community discussion initiated in 2020](https://github.com/nipy/nibabel/issues/942)
to address long-standing limitations in existing tractography file formats.

## Motivation

File formats that store the results of computational tractography were
traditionally developed within specific software packages. While this approach
facilitated many applications, it also generated insularity and limited
standardization. As tractography datasets grew in size and complexity, the need
for a community-driven standard became clear.

## Limitations of existing formats

The existing tractography file formats have several limitations:

- **Lack of community-based development.** Formats were tied to specific
  toolboxes rather than developed through community consensus.
- **Lack of efficiency in I/O and storage.** Many formats do not support
  efficient memory mapping or compression.
- **Limited partial loading.** Most formats require loading all streamlines
  at once, making it difficult to work with subsets.
- **Non-standard spatial transformations.** For example, the TRK format uses a
  complex and non-standard spatial mapping based on voxel corners rather than
  world coordinates.

## Design goals

The community identified several key features for a new tractography format:

- **Community-based development.** The format should be developed by the
  community, not tied to any single toolbox.
- **Cross-platform compatibility.** The format should work across Python, C++,
  JavaScript, and other programming languages.
- **Simplicity.** The format should be easy to implement in any language
  without relying on external tooling. As few elements as possible should be
  required, and conventions should be explicit.
- **I/O and storage efficiency.** The format should support memory mapping and
  allow direct access to data without conversion. IEEE floating-point
  little-endian storage is preferred since it is the native format on all
  commonly used CPUs.
- **Independence.** The format should be self-contained and not require external
  references. Storing streamlines in world coordinates (RAS+ millimeters)
  eliminates the need for a user-supplied reference image.
- **Extensibility.** The format should allow additional metadata to be stored
  and for new fields to become part of the standard as their use becomes
  commonplace.
- **Seamless spatial transformation.** Intuitive metadata handling at any scale
  — vertices, streamlines, and bundles.

## Streamline storage trade-offs

A key design decision is how to store streamlines, which are "jagged arrays",
i.e., each streamline has a different number of vertices.

**Approaches considered:**

- **VTK-style** (explicit vertex indexing) — allows vertex sharing, efficient
  for triangulated meshes, but leads to much larger files for streamlines where
  each vertex is used once.
- **Single array with separators** (TCK, TRK, PDB style) — stores vertex
  positions and end-of-streamline markers in one array. Good for writing during
  streamline creation, but less efficient for random access.
- **Separate arrays for positions and offsets** (TRX approach) — stores vertex
  positions in one array and a prefix-sum index in another. This enables
  efficient memory mapping, random access, and block reads. Each data type
  (float positions, integer offsets) can be read with a single block read.

The TRX format adopts the **positions + offsets** approach because it provides:

- Memory-mapped access to arbitrary streamline subsets
- Efficient random access without reading the entire file
- Clean separation of data types for SIMD and GPU compatibility

**Vertex storage layout:**

- **Array of Structures (AoS):** `x0, y0, z0, x1, y1, z1, ...` — intuitive,
  matches how vertices are sent to GPUs.
- **Structure of Arrays (SoA):** `x0, x1, ..., y0, y1, ..., z0, z1, ...` —
  can benefit from CPU-based SIMD programming.

TRX uses AoS layout for positions, matching the convention used by MRtrix3
`.tck` and OpenGL polyline rendering.

## Metadata hierarchy

TRX organizes metadata into four levels:

- **Per-vertex (DPV):** scalar or vector values at each streamline vertex
  (e.g., FA along a tract, RGB colors).
- **Per-streamline (DPS):** one value per streamline (e.g., mean FA, cluster
  labels, algorithm weights).
- **Groups:** named index sets of streamlines enabling sparse, overlapping
  labeling (e.g., bundle assignments, connectivity subsets).
- **Per-group (DPG):** metadata attached to groups (e.g., mean FA across a
  bundle, display colors, volume estimates).

This hierarchy covers the metadata needs of existing formats (TRK's
per-vertex/per-streamline values, TCK's bundle labels) while adding the
flexibility of group-level properties that no predecessor format provided.

## Spatial coordinates

TRX stores streamline vertices in **RAS+ world coordinates** (millimeters)
rather than voxel space. This decision was motivated by:

- **Independence from external data.** The file is self-contained — no
  reference image is needed to interpret vertex positions.
- **Consistency with MRtrix3.** The `.tck` format already uses world
  coordinates, and TRX maintains compatibility.
- **Reduced errors.** Requiring a user-supplied reference image to convert
  between voxel and world coordinates creates opportunities for mistakes.

The `header.json` includes a `VOXEL_TO_RASMM` affine for tools that need to
convert to voxel space, but this field is optional to use — the data on disk
is already in world coordinates.

## Compression

TRX supports optional ZIP compression:

- **Whole-archive compression** (`ZIP_DEFLATE`) is simple and widely supported.
- **Per-array compression** is possible within the ZIP structure, allowing
  random access to uncompressed arrays while compressing others.
- **Byte shuffling** before compression can improve ratios for structured data
  like offset arrays, where neighboring values share most-significant bytes.

The format does not mandate a specific compression strategy, leaving this as
an implementation choice.
