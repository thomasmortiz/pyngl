@echo off
rem Usage: run_unit_tests.bat <path to top level test file>
set testpath=%1
echo %testpath%

if exist %testpath%\tests.py (
    echo running excel tests
    python -m unittest tests.py
)

if exist %testpath%\thermo\ (
    if exist %testpath%\thermo\tests.py (
        echo running thermo tests
        pushd %testpath%\thermo
        python -m unittest tests.py
        popd
    )
)
