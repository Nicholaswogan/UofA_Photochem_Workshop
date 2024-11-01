# Building Photochem from source

Building Photochem from source can be challenging, which is why `conda` is the preferred installation route. But in order to change the underlying Fortran, you need to be able to build the code from source.

First, lets create a new conda environment called `test` with all the photochem dependencies

```sh
conda create -n test -c conda-forge photochem_clima_data=0.2.0 python numpy scipy pyyaml numba astropy h5py threadpoolctl scikit-build cmake ninja cython fypp pip clang gfortran wget git jupyter matplotlib

conda activate test
```

Here is a breakdown of the dependencies:
- `photochem_clima_data=0.2.0` - All model data (e.g., photolysis cross sections etc.) 
- `python numpy scipy pyyaml numba astropy h5py threadpoolctl` - Packages needed to run Photochem
- `scikit-build cmake ninja cython fypp pip clang gfortran` - Packages needed to build Photochem. Critically, this includes the clang and gfortran C and Fortran compilers.
- `wget git` - Needed to download the Photochem source from the internet
- `jupyter matplotlib` - Only needed later for running notebooks/plotting

Next, we need to download Photochem from the internet with `git`. Also, here we checkout the version v0.6.1. This is necessary because future Photochem versions might have slightly different build instructions

```sh
git clone https://github.com/Nicholaswogan/photochem.git
cd photochem
git checkout v0.6.1
```

We need to set some environment variables to help the build find compilers and libraries.

```sh
export CC="$(which clang)"
export CXX="$(which clang)"
export FC="$(which gfortran)"

unset CMAKE_ARGS
export CMAKE_ARGS="-DCMAKE_PREFIX_PATH=$CONDA_PREFIX -DCMAKE_POSITION_INDEPENDENT_CODE=ON"
export CONDA_PREFIX_SAVE=$CONDA_PREFIX
unset CONDA_PREFIX
```

Finally, we can install the code

```sh
python -m pip install --no-deps --no-build-isolation . -v

# Reset your conda-prefix, if you want.
export CONDA_PREFIX=$CONDA_PREFIX_SAVE
```

A common issue is that the hdf5 libraries can not be found. Here are some commands below to hopefully fix that problem.

```sh
# MacOS (Homebrew) 
brew install hdf5

# Linux
sudo apt install libhdf5-dev

# Build HDF5 from source
wget https://github.com/geospace-code/h5fortran/archive/refs/tags/v4.5.0.tar.gz
tar -xvzf v4.5.0.tar.gz
rm v4.5.0.tar.gz
cmake -S h5fortran-4.5.0/scripts -B h5fortran-4.5.0/scripts/build -DCMAKE_INSTALL_PREFIX=mylibs
cmake --build h5fortran-4.5.0/scripts/build -j
rm -r h5fortran-4.5.0
export CMAKE_PREFIX_PATH="$(pwd)/mylibs"
```

## Building in place without `pip`

It is also useful to build the code without installing it to your Python installation. Below are the commands for accomplishing this.

```sh
mkdir build
cd build

export CC="$(which clang)"
export CXX="$(which clang)"
export FC="$(which gfortran)"

export CONDA_PREFIX_SAVE=$CONDA_PREFIX
unset CONDA_PREFIX

# Configure
cmake .. -DCMAKE_PREFIX_PATH=$CONDA_PREFIX_SAVE -DBUILD_PYTHON_PHOTOCHEM=ON -DBUILD_WITH_OPENMP=ON -DCMAKE_POSITION_INDEPENDENT_CODE=ON -DCMAKE_BUILD_TYPE=Release -DSKBUILD_CMAKE_MODULE_DIR=$(python -c "from skbuild import __file__; print(__file__.strip('__init__.py')+'resources/cmake')")

# Build and install
cmake --build . -j && cmake --install .
```

So now, you can run python code at the root of the `photochem` directory, and it will use the code that you just installed.
