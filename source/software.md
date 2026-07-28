# Software

TRX is integrated into several software libraries:

## TRXViz

[TRXViz](https://github.com/tee-ar-ex/TRXViz) is a tool for visualization and
processing of diffusion-MRI based tractography. Implemented in Rust, it
supports fast visualization and basic processing of TRX-based tractography.

## pyAFQ

[pyAFQ](https://tractometry.org/pyAFQ) is a Python library for automated
white matter tractography and tractometry. It uses TRX to parallelize and
accelerate tractography, as well as to perform batched operations over
groups of streamlines in ways that allow handling very large tractograms
(>100M streamlines) on standard hardware.

## Trekker

Trekker implements parallel transport tractography for generating geometrically
smooth streamlines {cite:p}`Aydogan2021-ug`. It uses TRX

## DIPY

[DIPY](https://dipy.org/) is a library for the analysis of diffusion MRI
data {cite:p}`Garyfallidis2014-el`. DIPY supports I/O in many different
file formats, including TRX.

## QSIPrep & QSIRecon

QSIPrep is an integrative platform for preprocessing and reconstructing
diffusion MRI data {cite:p}`Cieslak2021-ic`. QSIPrep and its post-processing
pipelines, implemented in QSIRecon advance the use of TRX as an interchange
format, because they knit together functionality from many different software
libraries.

## Surfice

Surfice is a tool for visualizing neuroimaging meshes, tractography
streamlines, and connectomes {cite:p}`Rorden2025-zq`.

## SlicerDMRI

SlicerDMRI is an open source diffusion MRI software, implemented as an
extension of 3D Slicer {cite:p}`Norton2017-yz`. It now supports use of TRX,
through its C++ implementation.

## FSL

[FSL](https://fsl.fmrib.ox.ac.uk/fsl/) is a comprehensive library of tools
for functional MRI, structural MRI, and diffusion MRI analysis. The FSLeyes
viewer includes support for TRX as of its 1.20 version release.

## COMMIT

COMMIT (Convex Optimization Modeling for Microstructure Informed Tractography)
is a framework for microstructure-informed tractography. TRX support in
COMMIT using its C++ implementation is currently work-in-progress.

## brainlife.io

[brainlife.io](https://brainlife.io) is a decentralized and open-source cloud
platform to support neuroscience research {cite:p}`Hayashi2024-zm`. It uses
TRX for streamline I/O.

## Niivue

[Niivue](https://niivue.com/) is a WebGL-based visualization library for
neuroimaging data, including tractography streamlines. It uses the TRX
features of TRX to display different groups (e.g., tracts) and their distinct
properties.

## DWI2TRX

The [DWI2TRX](https://tee-ar-ex.github.io/dwi2trx/) web application uses
WASM-based dcm2niix and niimath as well as WebGPU-based NiiVue, mindgrab and
GPUstreamlines to perform a minimal processing pipeline that generates a TRX
tractography from NiFTI/bval/bvec files or from a directory of dicoms. All
computations are conducted client-side on the users computer, and no data is
uploaded to any remote server. It works on any web enabled device that supports
the full WebGPU standard.

## Insight ToolKit (ITK)

ITK is an open-source framework for image analysis. TRX has been integrated as
an external module, making it available for users of the ANTS registration
framework {cite:p}`Avants2014-ci`.

## MRtrix

[MRtrix3](https://www.mrtrix.org/) is a fast, flexible and open software
framework for medical image processing and visualisation {cite:p}`Tournier2019-cq`.
Integration of TRX support is currently in progress.
