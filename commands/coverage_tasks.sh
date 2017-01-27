#!/bin/bash

coverage run setup.py test
coverage report --fail-under=100
RESULT=$?
if [ $RESULT -eq 2 ]; then
  coverage annotate
fi
if [ $RESULT -eq 0 ]; then
  ./commands/delete_cover_files.sh
fi
