@ECHO OFF
REM setlocal enabledelayedexpansion
if not defined in_subprocess (cmd /k set in_subprocess=y ^& %0 %*) & exit )
md Internal_Logs
(
call conda activate psytask
python Tasks/mainscript.py
)> "Internal_Logs/log_file_%RANDOM%.txt"