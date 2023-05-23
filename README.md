![CI-status](https://github.com/preangelleo/ai_avartar/actions/workflows/ci.yml/badge.svg?branch=main)
# AI Avatar
Create your own cross-platform AI Avatar in a few seconds

## Env Setup

### Do it Once:
1. install anaconda from https://www.anaconda.com/
2. Go to the top folder of this repo and do `conda create -n env python=3.10; pip install -e .`

### To install a new packages 
1. `conda activate env`
2. `pip install pkg_name`
3. Add the `pkg_name` to `requirements.txt` file.

### Do it Everytime before you develop anything (including Jupyter Notebook)
`conda activate env`
`pip install -e .` every time we have new dependencies in `requirements.txt`.

With `-e`, the package is installed in the dev mode which exposes `src/alpha/`
as a symlink, meaning that you can edit the source code in-place and the changes will be reflected in the installed package without having to reinstall it.
