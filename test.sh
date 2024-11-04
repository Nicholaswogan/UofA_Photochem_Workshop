CMD='jupyter nbconvert --execute --to notebook --inplace'

mamba create -n workshop -c conda-forge -y photochem=0.6.2 matplotlib jupyter
mamba activate workshop # Activate the environment
python -c "import photochem; print('Photochem version:', photochem.__version__)"

cd 3_ModernEarthPhotochemistry
$CMD ModernEarth_COMPLETED.ipynb &
cd ..

cd 4_ClimateTutorial
$CMD ClimateTutorial_COMPLETED.ipynb &
cd ..

cd 5_TRAPPIST1e
$CMD TRAPPIST1e_COMPLETED.ipynb &
cd ..

wait

cd ExtraTutorials

cd ArcheanEarthPhotochemistry
$CMD ArcheanEarth_COMPLETED.ipynb &
cd ..

cd ChangingModelData
$CMD ModelData.ipynb &
cd ..

cd GasGiantsAndBrownDwarfs
$CMD GasGiants.ipynb &
cd ..

wait

cd InstallingFromSourceAndContributing
mamba create -n test -c conda-forge -y photochem_clima_data=0.2.0 python numpy scipy pyyaml numba astropy h5py threadpoolctl scikit-build cmake ninja cython fypp pip clang gfortran wget git jupyter matplotlib
mamba activate test
if [ -d "photochem" ]; then
  rm -rf "photochem"
fi
git clone https://github.com/Nicholaswogan/photochem.git
cd photochem
git checkout v0.6.2
export CC="$(which clang)"
export CXX="$(which clang)"
export FC="$(which gfortran)"
unset CMAKE_ARGS
export CMAKE_ARGS="-DCMAKE_PREFIX_PATH=$CONDA_PREFIX -DCMAKE_POSITION_INDEPENDENT_CODE=ON"
export CONDA_PREFIX_SAVE=$CONDA_PREFIX
unset CONDA_PREFIX
python -m pip install --no-deps --no-build-isolation . -v
export CONDA_PREFIX=$CONDA_PREFIX_SAVE
cd ..

cd ..

