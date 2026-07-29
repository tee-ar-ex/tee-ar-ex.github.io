---
bibliography:
  - references.bib
---

# TRX: A community-oriented file format for tractography

Welcome to the documentation of the TRX file format (pronounced "tee-ar-ex" or
"tracks").

The goal of TRX is to become the standard file format. As with other file
formats like NIfTI, we believe that TRX will serve the community well and the
growing computational needs of our field. We encourage community members to
consider early contributions to our proposal so as to ensure the new standard
will cover the needs of the wider audience of software developers, toolboxes,
and scientists. Our long-term plan is to integrate TRX within the [Brain
Imaging Data Structure (BIDS)](https://bids.neuroimaging.io/) ecosystem
{cite:p}`Gorgolewski2016BIDS`.

## Table of Contents

* **[Core Concepts](concepts.md)**: Understanding the data structures and hierarchies.
  <details><summary><em>Show sections</em></summary>
  
  * [The TRX format](concepts.md#the-trx-format)
  * [Positions array](concepts.md#positions-array)
  * [Offsets and the sentinel](concepts.md#offsets-and-the-sentinel)
  * [Data per vertex (DPV)](concepts.md#data-per-vertex-dpv)
  * [Data per streamline (DPS)](concepts.md#data-per-streamline-dps)
  * [Groups](concepts.md#groups)
  * [Data per group (DPG)](concepts.md#data-per-group-dpg)
  * [Header](concepts.md#header)
  </details>

* **[Specification](specification.md)**: The technical details of the TRX file format.
  <details><summary><em>Show sections</em></summary>
  
  * [General](specification.md#general)
  * [Header](specification.md#header)
  * [Arrays](specification.md#arrays)
  * [Accepted datatypes](specification.md#accepted-datatypes)
  * [Example structure](specification.md#example-structure)
  * [Example code](specification.md#example-code)
  </details>

* **[Design Rationale](design.md)**: The motivation and design choices behind TRX.
  <details><summary><em>Show sections</em></summary>
  
  * [Motivation](design.md#motivation)
  * [Limitations of existing formats](design.md#limitations-of-existing-formats)
  * [Design goals](design.md#design-goals)
  * [Streamline storage trade-offs](design.md#streamline-storage-trade-offs)
  * [Metadata hierarchy](design.md#metadata-hierarchy)
  * [Spatial coordinates](design.md#spatial-coordinates)
  * [Compression](design.md#compression)
  </details>

* **[Software Ecosystem](software.md)**: Tools and libraries that support TRX.
  <details><summary><em>Show sections</em></summary>
  
  * [TRXViz](software.md#trxviz)
  * [pyAFQ](software.md#pyafq)
  * [Trekker](software.md#trekker)
  * [DIPY](software.md#dipy)
  * [QSIPrep & QSIRecon](software.md#qsiprep-qsirecon)
  * [Surfice](software.md#surfice)
  * [SlicerDMRI](software.md#slicerdmri)
  * [FSL](software.md#fsl)
  * [COMMIT](software.md#commit)
  * [brainlife.io](software.md#brainlife-io)
  * [Niivue](software.md#niivue)
  * [DWI2TRX](software.md#dwi2trx)
  * [Insight ToolKit (ITK)](software.md#insight-toolkit-itk)
  * [MRtrix](software.md#mrtrix)
  </details>

* **[History & Origins](history.md)**: How the format evolved and its community adoption.
  <details><summary><em>Show sections</em></summary>
  
  * [Origins](history.md#origins)
  * [Community adoption and dissemination](history.md#community-adoption-and-dissemination)
  </details>

* **[Bibliography](bib.md)**: Academic references.

```{toctree}
:hidden:

concepts
specification
design
software
history
bib
```