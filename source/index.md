---
bibliography:
  - references.bib
---

# TRX: A community-oriented file format for tractography

Welcome to the documentation of the TRX file format (pronounced "tee-ar-ex" or
"tracks"). The goal of TRX is to support use of computational tractography by
providing a simple, computationally-efficient and extensible standard. It is
designed to be future-proof, with very large datasets and high-resolution
acqusitions in mind. It is designed to provide a minimal container for simple
applications, as well as to support sophisticated data analysis workflows.

We believe that TRX will serve the tractography research community and the
growing computational needs of our field well into the future.

:::{note} Join us!
  We are currently [working](https://github.com/bids-standard/bids-specification/pull/2333)
  to integrate TRX within the [Brain Imaging Data Structure (BIDS)](https://bids.neuroimaging.io/) ecosystem {cite:p}`Gorgolewski2016BIDS`. We would appreciate suggestions and comments from
  members of the community.
:::

::::{grid} 2
:::{grid-item-card}  TRX fundamentals
```{toctree}
:maxdepth: 1
specification
concepts
```
:::
:::{grid-item-card}  Examples and software support
```{toctree}
:maxdepth: 2
showcase
software
```
:::
::::


::::{grid} 2
:::{grid-item-card} Benchmarks
```{toctree}
:maxdepth: 2
benchmarks
```
:::
:::{grid-item-card} Motivation design and history
```{toctree}
:maxdepth: 2
design
history
```
:::
::::

````{dropdown} Bibliography
```{toctree}
bib
```
````