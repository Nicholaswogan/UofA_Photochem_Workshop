# Installing Photochem

You can install Photochem, and the other packages needed for this workshop, by following the steps below.

**Note for Windows computers:** For Windows, you need to use the "Windows Subsystem for Linux" (i.e., WSL), which is a way to run Linux commands on Windows. The following website contains instructions for installing WSL: https://learn.microsoft.com/en-us/windows/wsl/install. Once WSL is installed then carry out the steps below using a WSL terminal.

## Step 1: Install the `conda` package manager

**If you already have `conda`, skip to Step 2.**

To install Photochem, you will need the `conda` package manager. There are many ways to install `conda`, but the following is my preferred method. Open a terminal, run the following commands, and accept every prompt:

```sh
curl -L -O "https://github.com/conda-forge/miniforge/releases/latest/download/Miniforge3-$(uname)-$(uname -m).sh"
bash Miniforge3-$(uname)-$(uname -m).sh
```

Note: if you are using a Linux machine or WSL, and you don't have `curl` installed, then first install it with `sudo apt-get install curl`.

To ensure the installation worked, open up a new terminal window and run the command `conda --version`.

## Step 2: Install photochem with conda

The below command creates a new Python environment called `workshop` with Photochem v0.6.2 installed. The command also installs `matplotlib` and `jupyter` which are needed to make plots and run notebooks.

```sh
conda create -n workshop -c conda-forge photochem=0.6.2 matplotlib jupyter
conda activate workshop # Activate the environment
```

Check that your installation worked by running the following

```sh
python -c "import photochem; print('Photochem version:', photochem.__version__)"
```