#!/usr/bin/env python3
"""
Render Showcase tractography figures using FURY.

Reproduces:
1. The hero whole-brain ensemble tractogram (`whole_brain.png`).
2. The four tracking algorithm bundle figures (`DTI.png`, `EUDX.png`, `DET.png`, `prob.png`).

Features:
- Streamlines loaded from TRX (whole-brain and bundle groups).
- Non-transparent streamlines (opacity=1.0) with endpoint-based orientation coloring.
- Axial and mid-sagittal reference anatomy slices (FA) rendered with FURY slicers.
- Programmatic camera configuration matching the oblique lateral view.
- Clean offscreen rendering to PNG.

Requirements:
    pip install trx-python dipy fury nibabel numpy

Usage:
    python generate_showcase_figure.py in_trx in_img [--out_dir OUT_DIR] [--nb_streamlines NB]
"""

import argparse
import logging
import os
import nibabel as nib
import numpy as np

from fury import actor, window
from trx.trx_file_memmap import load

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%H:%M:%S",
)

CAMERA_CONFIG = {
    "position": (-300, 38, 72),
    "focal_point": (0, -16, 5),
    "view_up": (0, 0, 1),
}


def create_base_scene(
    fa_data: np.ndarray,
    affine: np.ndarray,
    z_slice: int = 55,
    x_slice: int = 58,
):
    """Create a FURY scene with axial and mid-sagittal anatomical slices."""
    axial_slicer = actor.slicer(fa_data, affine=affine, opacity=0.7)
    axial_slicer.display(z=z_slice)

    sagittal_slicer = actor.slicer(fa_data, affine=affine, opacity=0.6)
    sagittal_slicer.display(x=x_slice)

    scene = window.Scene()
    scene.background((0.2, 0.2, 0.2))
    scene.add(axial_slicer)
    scene.add(sagittal_slicer)
    scene.set_camera(**CAMERA_CONFIG)
    return scene


def render_whole_brain(
    trx,
    fa_data: np.ndarray,
    affine: np.ndarray,
    output_path: str,
    nb_streamlines: int = 40000,
    z_slice: int = 55,
    x_slice: int = 58,
    resolution: tuple = (1068, 755),
):
    """Render the whole-brain ensemble tractogram with opaque streamlines."""
    logging.info("Preparing whole-brain tractogram...")
    streamlines = [
        s.astype(np.float32) for s in trx.streamlines[:nb_streamlines]
    ]
    logging.info(
        "Rendering %d non-transparent streamlines (opacity=1.0)...",
        len(streamlines),
    )
    streamlines_actor = actor.line(streamlines, opacity=1.0, linewidth=0.7)

    scene = create_base_scene(fa_data, affine, z_slice=z_slice, x_slice=x_slice)
    scene.add(streamlines_actor)

    logging.info("Saving whole-brain snapshot to: %s", output_path)
    window.snapshot(scene, fname=output_path, size=resolution, offscreen=True)


def render_algo_bundles(
    trx,
    algo_code: int,
    algo_name: str,
    fa_data: np.ndarray,
    affine: np.ndarray,
    output_path: str,
    z_slice: int = 55,
    x_slice: int = 58,
    resolution: tuple = (1068, 755),
):
    """Render bundle groups for a tracking algorithm using endpoint coloring."""
    logging.info("Extracting %s bundle streamlines (algo code %d)...", algo_name, algo_code)

    all_grp_indices = np.concatenate(
        [trx.groups[k] for k in trx.groups.keys() if len(trx.groups[k]) > 0]
    )
    unique_grp_indices = np.unique(all_grp_indices)

    algo = trx.data_per_streamline["algo"]
    idx_algo = np.where(algo == algo_code)[0]
    sub_indices = np.intersect1d(unique_grp_indices, idx_algo)

    if len(sub_indices) == 0:
        logging.warning("No bundle streamlines found for algo %d (%s).", algo_code, algo_name)
        return

    sub_trx = trx.select(sub_indices)
    streamlines = [s.astype(np.float32) for s in sub_trx.streamlines]
    logging.info(
        "Rendering %d %s bundle streamlines (endpoint coloring, opacity=1.0)...",
        len(streamlines),
        algo_name,
    )

    # In FURY, colors=None automatically uses endpoint-based line_colors(streamlines)
    streamlines_actor = actor.line(streamlines, opacity=1.0, linewidth=1.0)

    scene = create_base_scene(fa_data, affine, z_slice=z_slice, x_slice=x_slice)
    scene.add(streamlines_actor)

    logging.info("Saving %s snapshot to: %s", algo_name, output_path)
    window.snapshot(scene, fname=output_path, size=resolution, offscreen=True)


def _build_arg_parser():
    p = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawTextHelpFormatter,
    )
    p.add_argument(
        "in_trx",
        help="Path to input TRX tractogram file (e.g. complete_tractogram.trx).",
    )
    p.add_argument(
        "in_img",
        help="Path to reference FA / anatomical NIfTI image (e.g. fa.nii.gz).",
    )
    p.add_argument(
        "--out_dir",
        default=".",
        help="Directory to save generated PNG images [%(default)s].",
    )
    p.add_argument(
        "--nb_streamlines",
        type=int,
        default=40000,
        help="Number of streamlines to display for whole brain [%(default)s].",
    )
    p.add_argument(
        "--z_slice",
        type=int,
        default=55,
        help="Axial slice voxel index [%(default)s].",
    )
    p.add_argument(
        "--x_slice",
        type=int,
        default=58,
        help="Mid-sagittal slice voxel index [%(default)s].",
    )
    return p


def main():
    parser = _build_arg_parser()
    args = parser.parse_args()

    if not os.path.isfile(args.in_trx):
        parser.error(f"Input TRX file not found: {args.in_trx}")
    if not os.path.isfile(args.in_img):
        parser.error(f"Input image file not found: {args.in_img}")

    os.makedirs(args.out_dir, exist_ok=True)

    logging.info("Loading reference anatomy from: %s", args.in_img)
    img = nib.load(args.in_img)
    fa_data = img.get_fdata()
    affine = img.affine

    logging.info("Loading tractogram from: %s", args.in_trx)
    trx = load(args.in_trx)

    # 1. Whole-brain hero figure
    wb_out = os.path.join(args.out_dir, "whole_brain.png")
    render_whole_brain(
        trx,
        fa_data,
        affine,
        wb_out,
        nb_streamlines=args.nb_streamlines,
        z_slice=args.z_slice,
        x_slice=args.x_slice,
    )

    # 2. Four algorithm bundle figures (if groups and algo metadata are present)
    if len(trx.groups) > 0 and "algo" in trx.data_per_streamline:
        algos = [
            (1, "DTI", "DTI.png"),
            (2, "EuDX", "EUDX.png"),
            (3, "Deterministic", "DET.png"),
            (4, "Probabilistic", "prob.png"),
        ]
        for code, name, png_name in algos:
            out_png = os.path.join(args.out_dir, png_name)
            render_algo_bundles(
                trx,
                code,
                name,
                fa_data,
                affine,
                out_png,
                z_slice=args.z_slice,
                x_slice=args.x_slice,
            )

    logging.info("Showcase figures successfully generated!")


if __name__ == "__main__":
    main()
