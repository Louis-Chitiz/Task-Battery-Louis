@ECHO OFF
cd %~dp0
call conda env create -f environment.yml
pause
call conda activate psytask
conda install pip
pause
