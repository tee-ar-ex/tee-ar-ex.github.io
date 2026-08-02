# Timeline of TRX

## Origins

File formats that store the results of computational tractography were
traditionally developed within specific software packages. This approach has
facilitated a myriad of applications, but this development approach has also
generated insularity within software packages, and has limited standardization.
Moreover, because tractography file formats were developed to solve immediate
challenges, only a limited breadth of applications within a single software
package was envisioned, sometimes also neglecting computational performance.

Given the growing interest in tractography methods and applications, and the
increasing size and complexity of datasets, a community-driven standardization
of tractography have become a priority
{cite:p}`Legarreta2026Gigascience, Descoteaux2025Millenium`.

The TRX format emerged in 2020
following [this discussion](https://github.com/nipy/nibabel/issues/942) on the nibabel
repository, where the tractography community began conversations about a shared
data format.

## Community adoption and dissemination

TRX has been developed and advocated by researchers across many institutions
and geographies. The format has been presented at conferences, workshops, and
through technical developments.

### Conferences and workshops

- **OHBM 2021** (online) — initial presentation of the format
- **OHBM 2022** (Glasgow) — in-person poster presentation
- **OHBM 2023** — progress presented at the Open Science Room
- **Tract Anat Retreat, Corsica, 2024** — presented and discussed at length
- **DIPY online workshops, 2025 and 2026** — presented to trainees
- **BRAIN CONNECTS gathering, Austin TX, 2025** — presented to the project

### Institutional adoption

- The NIH-funded **BIDS Connectivity project** incorporated TRX into its
  proposal for extensions of BIDS to represent brain tractography.
- The **International Society for Tractography Standardization Unit** has been
  carrying this work forward.

### Community note

For a community service project that is not currently funded by any agency, the
community around TRX has been exceptionally active in disseminating knowledge
about the format. Technical developments to ease the burden of TRX adoption
have also been remarkable, with the format now supported by many platforms and
languages, as described in the [Software](software.md) page.

### Adoption of TRX in BIDS

The [Brain Imaging Data Structure (BIDS)](https://bids.neuroimaging.io/) is a
widely-used standard for organizing and describing data collected during
neuroimaging experiments. As BIDS has evolved, it has shifted from a standard
that covers only experimental data to one that also covers the outputs of
processing pipelines.

The proposal for standardization of tractography outputs (or, in BIDS jargon,
"tractography derivatives") currently being discussed as
[BIDS Enhancement Proposal \#46](https://github.com/bids-standard/bids-specification/pull/2333)
focuses on making TRX the only file format that will be accepted by the
standard. This means that standards-compliant experiments and projects will
eventually need to adopt TRX.
