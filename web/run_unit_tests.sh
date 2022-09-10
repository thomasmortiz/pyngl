#!/bin/bash
if [ -e $PWD/tests.py ]
    then
        python -m unittest tests.py
fi

if [ -e $PWD/thermo ]
    then
        cd thermo
fi

if [ -e $PWD/tests.py ]
    then
        python -m unittest tests.py
fi

echo "Finished running unit tests"
