#!/bin/bash
rm -rf '__pycache__'
find -name '*.pyc' -delete
find -name '*.pyo' -delete
find -name '*.swp' -delete
find -name '*~' -delete
echo 'Done'
exit 0

