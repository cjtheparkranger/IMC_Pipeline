# IMC_Pipeline

This is a python based pipeline composed of preexisting modules developed for IMC analysis. First, please clone this directory. Then, with /IMC_Pipeline as your root directory, use the set up script, the script will attempt to provide instructions for installation 
of other necesasry directories and packages. If those fail, please direct your attention to the documentation for the various packages, listed below:

IMC Denoise: https://github.com/PENGLU-WashU/IMC_Denoise
IMC Segmentation Pipeline: https://github.com/BodenmillerGroup/ImcSegmentationPipeline/tree/main
Squidpy: https://squidpy.readthedocs.io/en/latest/installation.html
Ilastik: https://www.ilastik.org/documentation/basics/installation.html
CellProfiler: https://cellprofiler.org/releases


Steinbock will need to be installed manually, with instructions at this URL: https://bodenmillergroup.github.io/steinbock/latest/install-docker/


After installation, your directory should look like this:
<img width="729" alt="Screenshot 2023-07-20 at 2 55 26 PM" src="https://github.com/cjtheparkranger/IMC_Pipeline/assets/76821785/874404a3-71a7-4664-bd5a-e3e3584d9008">

After running the mcd_to_tiff.py script, a folder named 'analysis' should appear in your ImcSegmentationPipeline folder, which will the base of all image process and storage.
