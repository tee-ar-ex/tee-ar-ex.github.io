# TRX: A community-oriented file format for tractography

### Rationale

File formats that store the results of computational tractography were typically
developed within specific software packages. This approach has facilitated a
myriad of applications, but this development approach has also generated
insularity within software packages, and has limited standardization. Moreover,
because tractography file formats were developed to solve immediate challenges,
only a limited breadth of applications within a single software package was
envisioned, sometimes also neglecting computational performance. Given the
growing interest in tractography methods and applications, and the increasing
size and complexity of datasets, a community-driven standardization of
tractography have become a priority. To address these challenges, our community
initiated a discussion to design a new file format and agreed to participate in
its conception, development, and, if successful, its adoption.

The goal of TRX is to become the standard amongst tractography file formats. As
with other file formats like NiFTI, we believe that TRX will serve the
community well and the growing computational needs of our field. We encourage
community members to consider early contributions to our proposal so as to
ensure the new standard will cover the needs of the wider audience of software
developers, toolboxes, and scientists. Our long-term plan is to integrate TRX
within the [Brain Imaging Data Structure (BIDS)](https://bids.neuroimaging.io/)
ecosystem.

## Implementations

[*Python*](https://tee-ar-ex/trx-python)

[*C++*](https://tee-ar-ex/trx-cpp)

```{note}

The TRX file-format started following [this discussion](https://github.com/nipy/nibabel/issues/942)

```


```{eval-rst}

.. toctree::
   :maxdepth: 2
   :caption: Contents:

```