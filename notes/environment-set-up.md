# Environment Setup

*The instructions below are intentionally detailed to explain the reasoning behind our environment setup and what each command does. If you're already confident using bash, Conda environments, and Git, you can use the much shorter [minimal setup instructions](#minimal-setup-instructions-for-dice) at the end.*

This course uses [Python 3](https://www.python.org/) for all labs and coursework assignments. We'll make heavy use of the numerical computing libraries [NumPy](https://numpy.org/) and [SciPy](https://scipy.org/), and the interactive notebook application [Jupyter](https://jupyter.org/).

A common challenge in software projects is managing correct versions of dependencies across different systems and projects. You may be working on multiple projects with conflicting dependencies, across different machines with different operating systems, or on systems where you don't have root access (like DICE).

To solve these issues, we use project-specific *virtual environments* - isolated development environments where dependencies can be installed and managed independently of system-wide versions.

We'll use [Conda](https://docs.conda.io/) for environment management. Unlike pip and virtualenv, Conda is language-agnostic and can handle complex dependencies including optimized numerical computing libraries. Conda works across Linux, macOS, and Windows, making it easy to set up consistent environments wherever you work.

We'll use [Miniconda](https://www.anaconda.com/docs/getting-started/installation), which installs just Conda and its dependencies (rather than the full Anaconda distribution), to save disk space on DICE.

## Installing Miniconda

We provide instructions for setting up the environment on [DICE desktop](http://computing.help.inf.ed.ac.uk/dice-platform) computers. These instructions should work on other Linux distributions (Ubuntu, Linux Mint) with minimal adjustments.

**For Windows or macOS:** Select the appropriate Miniconda installer from the [official installation page](https://www.anaconda.com/docs/getting-started/installation) and follow the [Conda installation instructions](https://docs.conda.io/projects/conda/en/latest/user-guide/install/index.html). The commands below target DICE and other Linux systems using Bash; package installation and paths may differ on other operating systems.

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

Recent Miniconda installers may require accepting Terms of Service before using the default Anaconda channels. If Conda prompts you, accept the terms in the prompt. If your installer includes the `conda-anaconda-tos` plugin and you need to accept the terms explicitly, run:

```bash
conda tos accept --override-channels --channel https://repo.anaconda.com/pkgs/main
conda tos accept --override-channels --channel https://repo.anaconda.com/pkgs/r
```

If `conda tos` is not a recognised command, your installer predates this plugin; skip these commands. This is expected, and the remaining setup commands are unchanged.

## Creating the Conda Environment

Test that Conda is working:

```bash
conda --help
```

If you see the Conda help page, you're ready to proceed. If you get a `No command 'conda' found` error, check your PATH setup.

Create the Conda environment with Python 3.12:

```bash
conda create -n mlp python=3.12 pip -y
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
conda install numpy=2.3.4 scipy matplotlib jupyter ipywidgets -y
```

This will take several minutes and installs NumPy, SciPy, [matplotlib](https://matplotlib.org/) (for plotting) and Jupyter.

Install the CPU version of PyTorch and torchvision:

```bash
python -m pip install torch torchvision --index-url https://download.pytorch.org/whl/cpu
```

The course notebooks also run on computers without a GPU. For optional GPU acceleration, choose the Linux installation command for your hardware from the [PyTorch installation guide](https://pytorch.org/get-started/locally/).

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

[Git](https://git-scm.com/) is a version control system, and [GitHub](https://github.com) hosts Git repositories. We use Git to distribute code for labs and assignments. For Git beginners, see [this guide](https://rogerdudler.github.io/git-guide/) or [this longer tutorial](https://www.atlassian.com/git/tutorials/).

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

We use Git branches to organize course content. Each lab has its own branch (e.g., `mlp2026-27/lab1`, `mlp2026-27/lab2`). This lets us release content progressively while preserving your work.

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
git checkout mlp2026-27/lab1
```

**Important:** Make sure you're on the correct lab branch before starting each week's work.

## Installing the MLP Python Package

The `mlp` directory contains a custom NumPy-based neural network framework for this course. We need to install it so Python can import the modules.

Install the package in development mode (so changes are automatically available):

```bash
cd ~/mlpractical
python -m pip install -e .
```

This installs the package in "editable" mode, meaning any changes to the source code are immediately available without reinstalling.

## Data directory

The data providers use the repository's `data` directory automatically. Set
`MLP_DATA_DIR` only when keeping the datasets elsewhere (for example, on a
shared filesystem):

```bash
export MLP_DATA_DIR=/path/to/mlpractical/data
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
4. Open `01_introduction.ipynb` to start the first lab

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
   If `conda tos` is not a recognised command, skip this step; older Miniconda installers do not include the Terms of Service plugin.

4. **Create and activate environment:**
```bash
conda create -n mlp python=3.12 pip -y
conda activate mlp
```

5. **Install packages:**
```bash
# Use a NumPy build compatible with older DICE CPUs.
conda install numpy=2.3.4 scipy matplotlib jupyter ipywidgets -y
python -m pip install torch torchvision --index-url https://download.pytorch.org/whl/cpu
conda clean -t -y
```

6. **Get course code:**
```bash
git clone https://github.com/cortu01/mlpractical.git ~/mlpractical
cd ~/mlpractical
git checkout mlp2026-27/lab1
```

7. **Install MLP package:**
```bash
cd ~/mlpractical
python -m pip install -e .
```

8. **Optional data directory:** Set `MLP_DATA_DIR` only if the datasets are
   stored outside the repository (see the section above).

9. **Start working:**
```bash
cd ~/mlpractical
jupyter notebook
```
   Then open `notebooks/01_introduction.ipynb`

**Remember:** Run `conda activate mlp` at the start of each session!
