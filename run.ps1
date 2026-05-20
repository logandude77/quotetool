# Launch quotetool STEP viewer (Phase 1 scaffold).
& "C:\Users\eadsl\miniconda3\shell\condabin\conda-hook.ps1"
conda activate quotetool
Set-Location $PSScriptRoot
python -m src.main
