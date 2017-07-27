#!/bin/bash

# remove current directories
rm -r documentation
rm -r coverage

# get new ones
mv ../../UnBlockMeSolver/UnBlockMe/docs/documentation .
mv ../../UnBlockMeSolver/UnBlockMe/docs/htmlcov .

# rename htmlcov
mv htmlcov coverage
