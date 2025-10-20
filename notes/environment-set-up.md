# Environment Setup

*The instructions below are intentionally detailed to explain the reasoning behind our environment setup and what each command does. If you're already confident using bash, Conda environments, and Git, you can use the much shorter [minimal setup instructions](#minimal-setup-instructions-for-dice) at the end.*

This course uses [Python 3](https://www.python.org/) for all labs and coursework assignments. We'll make heavy use of the numerical computing libraries [NumPy](http://www.numpy.org/) and [SciPy](http://www.scipy.org/), and the interactive notebook application [Jupyter](http://jupyter.org/).

A common challenge in software projects is managing correct versions of dependencies across different systems and projects. You may be working on multiple projects with conflicting dependencies, across different machines with different operating systems, or on systems where you don't have root access (like DICE).

To solve these issues, we use project-specific *virtual environments* - isolated development environments where dependencies can be installed and managed independently of system-wide versions.

We'll use [Conda](http://conda.pydata.org/docs/) for environment management. Unlike pip and virtualenv, Conda is language-agnostic and can handle complex dependencies including optimized numerical computing libraries. Conda works across Linux, macOS, and Windows, making it easy to set up consistent environments wherever you work.

We'll use [Miniconda](http://conda.pydata.org/miniconda.html), which installs just Conda and its dependencies (rather than the full Anaconda distribution), to save disk space on DICE.

## Installing Miniconda

We provide instructions for setting up the environment on [DICE desktop](http://computing.help.inf.ed.ac.uk/dice-platform) computers. These instructions should work on other Linux distributions (Ubuntu, Linux Mint) with minimal adjustments.

**For Windows or macOS:** Select the appropriate installer from [here](https://docs.conda.io/en/latest/miniconda.html) and follow the installation instructions from [here](https://conda.io/projects/conda/en/latest/user-guide/install/index.html). After Conda is installed, the [remaining instructions](#creating-the-conda-environment) should be the same across different systems.

*Note: While you're welcome to set up an environment on a personal machine, you should still set up a DICE environment as you'll need access to shared computing resources later in the course. These instructions have only been tested on DICE, and we cannot provide support for non-DICE systems during labs.*

---

**For DICE systems:**

If using SSH to connect to the student server, proceed to the next step. If using a DICE computer with a graphical interface, open a bash terminal (`Applications > Terminal`). 

Download the latest 64-bit Python 3 Miniconda installer:

```bash
wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh
```

Run the installer:

```bash
bash Miniconda3-latest-Linux-x86_64.sh
```

You'll be asked to:
1. Review the software license agreement
2. Choose an install location (default: `~/miniconda3` - we recommend using this)
3. Whether to initialize Miniconda in your shell

**Important for DICE users:** When asked whether to initialize Miniconda, respond `no` as we'll set up the PATH manually for DICE's bash configuration.

On DICE, add Miniconda to your PATH manually:

```bash
echo ". /afs/inf.ed.ac.uk/user/${USER:0:3}/$USER/miniconda3/etc/profile.d/conda.sh" >> ~/.bashrc
echo ". /afs/inf.ed.ac.uk/user/${USER:0:3}/$USER/miniconda3/etc/profile.d/conda.sh" >> ~/.benv
```

Verify the paths are correct:

```bash
vim ~/.bashrc
vim ~/.benv 
```

Update your current session:

```bash
source ~/.benv
```

**Accept Conda Terms of Service (if required):**

Newer versions of Miniconda may require accepting Terms of Service before using certain channels. If you encounter TOS-related errors, run these commands:

```bash
conda tos accept --override-channels --channel https://repo.anaconda.com/pkgs/main
conda tos accept --override-channels --channel https://repo.anaconda.com/pkgs/r
```

*Note: These commands may or may not be required depending on your Miniconda version and configuration.*

## Creating the Conda Environment

Test that Conda is working:

```bash
conda --help
```

If you see the Conda help page, you're ready to proceed. If you get a `No command 'conda' found` error, check your PATH setup.

Create the Conda environment with Python 3.12:

```bash
conda create -n mlp python=3.12 -y
```

Activate the environment:

```bash
conda activate mlp
```

*Note: On Windows, use `activate mlp` instead.*

When activated, your prompt should show `(mlp)` at the beginning. **You need to run `conda activate mlp` every time you start a new terminal session for this course.**

To deactivate an environment, run `conda deactivate` (or just `deactivate` on Windows).

Install the required packages:

```bash
conda install numpy scipy matplotlib jupyter -y
```

This will take several minutes and installs NumPy, SciPy, [matplotlib](http://matplotlib.org/) (for plotting), and Jupyter.

Install PyTorch:

```bash 
conda install pytorch torchvision torchaudio cpuonly -c pytorch -y
```

*Note: This installs the CPU-only version. If you have a CUDA-enabled GPU, replace `cpuonly -c pytorch` with your CUDA version (e.g., `pytorch-cuda=12.1 -c pytorch -c nvidia`). See [PyTorch installation guide](https://pytorch.org/get-started/locally/) for details.*

Clean up installation files to save disk space:

```bash
conda clean -t -y
```

***ANLP and IAML students only:***
To have normal access to your ANLP and IAML environments please do the following:

1. ```nano .condarc```
2. Add the following lines in the file:

```yml
envs_dirs:
- /group/teaching/conda/envs

pkgs_dirs:
- /group/teaching/conda/pkgs
- ~/miniconda3/pkgs
```

3. Exit by using control + x and then choosing 'yes' at the exit prompt.

## Getting the Course Code

The course code is available in a Git repository on GitHub: https://github.com/cortu01/mlpractical

[Git](https://git-scm.com/) is a version control system, and [GitHub](https://github.com) hosts Git repositories. We use Git to distribute code for labs and assignments. For Git beginners, see [this guide](http://rogerdudler.github.io/git-guide/) or [this longer tutorial](https://www.atlassian.com/git/tutorials/).

**Non-DICE systems:** Git is pre-installed on DICE. If needed, install it with: `conda install git`

### Cloning the Repository

**Advanced Git users:** You may create a private fork of `cortu01/mlpractical` for syncing work between machines. **Do NOT create a public fork** as this risks plagiarism.

Clone the repository to your home directory:

```bash
git clone https://github.com/cortu01/mlpractical.git ~/mlpractical
```

Navigate to the directory:

```bash
cd ~/mlpractical
ls -a  # Windows: dir /a
```

You'll see:
- `data`: Data files for labs and assignments
- `mlp`: The custom Python package for this course  
- `notebooks`: Jupyter notebook files for each lab
- `.git`: Git repository data (don't modify directly)

Configure Git with your details (optional but recommended):

```bash
git config --global user.name "Your Name"
git config --global user.email "your-email@sms.ed.ac.uk"
```

### Understanding Branches

We use Git branches to organize course content. Each lab has its own branch (e.g., `mlp2025-26/lab1`, `mlp2025-26/lab2`). This lets us release content progressively while preserving your work.

Check current branch:

```bash
git status
```

List all branches:

```bash
git branch
```

Switch to the first lab branch:

```bash
git checkout mlp2025-26/lab1
```

**Important:** Make sure you're on the correct lab branch before starting each week's work.

## Installing the MLP Python Package

The `mlp` directory contains a custom NumPy-based neural network framework for this course. We need to install it so Python can import the modules.

Install the package in development mode (so changes are automatically available):

```bash
cd ~/mlpractical
pip install -e .
```

This installs the package in "editable" mode, meaning any changes to the source code are immediately available without reinstalling.

## Setting Up the Data Directory

The `data` directory contains files used in labs and assignments. We need to set an environment variable so the data loaders can find these files.

**For Linux/macOS:**

```bash
cd ~/miniconda3/envs/mlp
mkdir -p ./etc/conda/activate.d
mkdir -p ./etc/conda/deactivate.d
echo -e '#!/bin/sh\n' >> ./etc/conda/activate.d/env_vars.sh
echo "export MLP_DATA_DIR=$HOME/mlpractical/data" >> ./etc/conda/activate.d/env_vars.sh
echo -e '#!/bin/sh\n' >> ./etc/conda/deactivate.d/env_vars.sh
echo 'unset MLP_DATA_DIR' >> ./etc/conda/deactivate.d/env_vars.sh
export MLP_DATA_DIR=$HOME/mlpractical/data
```

**For Windows:**

```bash
cd [path-to-conda-root]\envs\mlp
mkdir .\etc\conda\activate.d
mkdir .\etc\conda\deactivate.d
echo "set MLP_DATA_DIR=[path-to-local-repository]\data" >> .\etc\conda\activate.d\env_vars.bat
echo "set MLP_DATA_DIR="  >> .\etc\conda\deactivate.d\env_vars.bat
set MLP_DATA_DIR=[path-to-local-repository]\data
```

## Starting Jupyter Notebooks

Your environment is now ready! To start working with the lab notebooks:

1. Make sure you're in the `mlpractical` directory with the `mlp` environment activated
2. Launch Jupyter:

```bash
cd ~/mlpractical
jupyter notebook
```

3. In the browser interface, navigate to the `notebooks` directory
4. Open `01_Introduction.ipynb` to start the first lab

The notebook interface combines formatted text, runnable code, and visualizations in a web browser. If you're new to Jupyter notebooks, the first lab will introduce you to the interface.

# Minimal Setup Instructions for DICE

*Quick setup for experienced users. If you don't understand a command, use the detailed instructions above.*

1. **Download and install Miniconda:**
```bash
wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh
bash Miniconda3-latest-Linux-x86_64.sh
```
   - Accept license, use default location (`~/miniconda3`)
   - Say **no** when asked to initialize

2. **Setup PATH for DICE:**
```bash
echo ". /afs/inf.ed.ac.uk/user/${USER:0:3}/$USER/miniconda3/etc/profile.d/conda.sh" >> ~/.bashrc
echo ". /afs/inf.ed.ac.uk/user/${USER:0:3}/$USER/miniconda3/etc/profile.d/conda.sh" >> ~/.benv
source ~/.benv
```

3. **Accept Conda Terms of Service (if needed):**
```bash
conda tos accept --override-channels --channel https://repo.anaconda.com/pkgs/main
conda tos accept --override-channels --channel https://repo.anaconda.com/pkgs/r
```

4. **Create and activate environment:**
```bash
conda create -n mlp python=3.12 -y
conda activate mlp
```

5. **Install packages:**
```bash
conda install numpy scipy matplotlib jupyter -y
conda install pytorch torchvision torchaudio cpuonly -c pytorch -y
conda clean -t -y
```

6. **Get course code:**
```bash
git clone https://github.com/cortu01/mlpractical.git ~/mlpractical
cd ~/mlpractical
git checkout mlp2025-26/lab1
```

7. **Install MLP package:**
```bash
cd ~/mlpractical
pip install -e .
```

8. **Setup data directory:**
```bash
cd ~/miniconda3/envs/mlp
mkdir -p ./etc/conda/activate.d ./etc/conda/deactivate.d
echo -e '#!/bin/sh\n' >> ./etc/conda/activate.d/env_vars.sh
echo "export MLP_DATA_DIR=$HOME/mlpractical/data" >> ./etc/conda/activate.d/env_vars.sh
echo -e '#!/bin/sh\n' >> ./etc/conda/deactivate.d/env_vars.sh
echo 'unset MLP_DATA_DIR' >> ./etc/conda/deactivate.d/env_vars.sh
export MLP_DATA_DIR=$HOME/mlpractical/data
```

9. **Start working:**
```bash
cd ~/mlpractical
jupyter notebook
```
   Then open `notebooks/01_Introduction.ipynb`

**Remember:** Run `conda activate mlp` at the start of each session!
