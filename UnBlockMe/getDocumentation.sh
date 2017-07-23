#!/bin/bash

# remove current directories
rm -r documentation
rm -r coverage

# get new ones
mv ../../UnBlockMeSolver/UnBlockMeSolver/docs/documentation .
mv ../../UnBlockMeSolver/UnBlockMeSolver/docs/htmlcov .

# rename htmlcov
mv htmlcov coverage
