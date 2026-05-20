# Launch Open Shop Quote (OSQ) launcher with the correct conda env.
& "C:\Users\eadsl\miniconda3\shell\condabin\conda-hook.ps1"
conda activate quotetool
Set-Location $PSScriptRoot
python ui/launcher.py
