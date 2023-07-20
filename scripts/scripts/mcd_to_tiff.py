# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import shutil
from pathlib import Path
from tempfile import TemporaryDirectory
from typing import List
import pandas as pd
import os

import imcsegpipe
from imcsegpipe.utils import sort_channels_by_mass

cwd = os.getcwd()

#paths to zipped files
raw_dirs = [cwd+"/raw"]
raw_dirs = [Path(raw_dir) for raw_dir in raw_dirs]

# select files with data in name
file_regex = "*BS17*.zip"

# panel information

panel_file = cwd+"/raw/panel.csv"
panel_channel_col = "channel"
panel_keep_col = "keep"
panel_ilastik_col = "ilastik"

# working directory storing all outputs
work_dir = cwd+"/analysis"
work_dir = Path(work_dir)
work_dir.mkdir(exist_ok=True)

# general output directories
acquisitions_dir = work_dir / "ometiff"
ilastik_dir = work_dir / "ilastik"
crops_dir = work_dir / "crops"
cellprofiler_input_dir = work_dir / "cpinp"
cellprofiler_output_dir = work_dir / "cpout"
histocat_dir = work_dir / "histocat_raw"

# Final output directories
final_images_dir = cellprofiler_output_dir / "images"
final_masks_dir = cellprofiler_output_dir / "masks"
final_probabilities_dir = cellprofiler_output_dir / "probabilities"

acquisitions_dir.mkdir(exist_ok=True)
crops_dir.mkdir(exist_ok=True)
ilastik_dir.mkdir(exist_ok=True)
cellprofiler_input_dir.mkdir(exist_ok=True)
cellprofiler_output_dir.mkdir(exist_ok=True)
histocat_dir.mkdir(exist_ok=True)

final_images_dir.mkdir(exist_ok=True)
final_masks_dir.mkdir(exist_ok=True)
final_probabilities_dir.mkdir(exist_ok=True)

temp_dirs: List[TemporaryDirectory] = []

try:
    for raw_dir in raw_dirs:
        zip_files = list(raw_dir.rglob(file_regex))
        if len(zip_files) > 0:
            temp_dir = TemporaryDirectory()
            temp_dirs.append(temp_dir)
            for zip_file in sorted(zip_files):
                imcsegpipe.extract_zip_file(zip_file, temp_dir.name)
    acquisition_metadatas = []
    for raw_dir in raw_dirs + [Path(temp_dir.name) for temp_dir in temp_dirs]:
        mcd_files = list(raw_dir.rglob("*.mcd"))
        mcd_files=[(i) for i in mcd_files if not i.stem.startswith('.')]
        if len(mcd_files) > 0:
            txt_files = list(raw_dir.rglob("*.txt"))
            txt_files=[(i) for i in txt_files if not i.stem.startswith('.')]
            matched_txt_files = imcsegpipe.match_txt_files(mcd_files, txt_files)
            for mcd_file in mcd_files:
                acquisition_metadata = imcsegpipe.extract_mcd_file(
                    mcd_file,
                    acquisitions_dir / mcd_file.stem,
                    txt_files=matched_txt_files[mcd_file],
                )
                acquisition_metadatas.append(acquisition_metadata)
    acquisition_metadata = pd.concat(acquisition_metadatas, copy=False)
    acquisition_metadata.to_csv(cellprofiler_input_dir / "acquisition_metadata.csv")
finally:
    for temp_dir in temp_dirs:
        temp_dir.cleanup()
    del temp_dirs
    
shutil.copy2(panel_file, cellprofiler_output_dir / "panel.csv")

for acquisition_dir in acquisitions_dir.glob("[!.]*"):
    if acquisition_dir.is_dir():
        imcsegpipe.export_to_histocat(acquisition_dir, histocat_dir)
        
panel: pd.DataFrame = pd.read_csv(panel_file)

# for acquisition_dir in acquisitions_dir.glob("[!.]*"):
#     if acquisition_dir.is_dir():
#         # Write full stack
#         imcsegpipe.create_analysis_stacks(
#             acquisition_dir=acquisition_dir,
#             analysis_dir=final_images_dir,
#             analysis_channels=sort_channels_by_mass(
#                 panel.loc[panel[panel_keep_col] == 1, panel_channel_col].tolist()
#             ),
#             suffix="_full",
#             hpf=50.0,
#         )
#         # Write ilastik stack
#         imcsegpipe.create_analysis_stacks(
#             acquisition_dir=acquisition_dir,
#             analysis_dir=ilastik_dir,
#             analysis_channels=sort_channels_by_mass(
#                 panel.loc[panel[panel_ilastik_col] == 1, panel_channel_col].tolist()
#             ),
#             suffix="_ilastik",
#             hpf=50.0,
#         )

# first_channel_order_file = next(final_images_dir.glob("[!.]*_full.csv"))
# shutil.copy2(first_channel_order_file, cellprofiler_input_dir / "full_channelmeta.csv")

# probab_meta = ["CellCenter", "CellBorder", "Background"]
# with open(cellprofiler_input_dir / "probab_channelmeta_manual.csv", "w") as f:
#     f.write("\n".join(probab_meta))
    
