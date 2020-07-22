# csgy-9163-unit1-spell
Repository For Unit 1 of CSGY-9163 Application Security

Build Status: [![Build Status](https://travis-ci.org/ab7289-tandon-nyu/csgy-9163-unit1-spell.svg?branch=master)](https://travis-ci.org/ab7289-tandon-nyu/csgy-9163-unit1-spell)

Code Coverage: [![Coverage Status](https://coveralls.io/repos/github/ab7289-tandon-nyu/csgy-9163-unit1-spell/badge.svg?branch=master)](https://coveralls.io/github/ab7289-tandon-nyu/csgy-9163-unit1-spell?branch=master)

# Usage

This project requires the following dependencies in order to build and run.

1. Cmake
2. Check
3. pkg-config
4. cpp-coveralls (for code-coverage)
5. gcovr (for code-coverage)

## Install Dependencies

On Linux, install dependencies with (on MacOS use homebrew)
`sudo apt-get update && sudo apt-get install build-essential pkg-config check cmake`

Then install the python dependencies (you may need to install python and pip):
`pip install --user cpp-coveralls gcovr`


## Build

Clone the repo and cd into the project directory, then create bin and build folders.

`mkdir build`
and 
`mkdir bin`

Then cd into the build directory and build with:
`cmake .. && make`

Test can be run with:
`make test`

Coverage reports can be generated with:
`make coverage`

## Usage

The binary file 'spell_check' will be created in the {project_dir}/bin folder. It can be run with:

`./spell_check [path_to_words] [path_to_dictionary]`

for example: `./spell_check ../res/test1.txt ../res/wordlist.txt`
