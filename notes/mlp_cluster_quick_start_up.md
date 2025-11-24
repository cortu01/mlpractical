# MLP GPU Cluster Usage Tutorial

This guide is intended to guide students into the basics of using the charles GPU cluster. It is not intended to be
an exhaustive guide that goes deep into micro-details of the Slurm ecosystem. For an exhaustive guide please visit 
[the Slurm Documentation page.](https://slurm.schedmd.com/)


##### For info on clusters and some tips on good cluster ettiquete please have a look at the complementary lecture slides https://docs.google.com/presentation/d/1SU4ExARZLbenZtxm3K8Unqch5282jAXTq0CQDtfvtI0/edit?usp=sharing

## Getting Started

### Accessing the Cluster:
1. If you are not on a DICE machine, then ssh into your dice home using ```ssh sxxxxxx@student.ssh.inf.ed.ac.uk``` 
2. Then ssh into either mlp1 or mlp2 which are the headnodes of the GPU cluster - it does not matter which you use. To do that
 run ```ssh mlp1``` or ```ssh mlp2```.
3. You are now logged into the MLP gpu cluster. If this is your first time logging in you'll need to build your environment.  This is because your home directory on the GPU cluster is separate to your usual AFS home directory on DICE.
- Note: Alternatively you can just ```ssh sxxxxxxx@mlp.inf.ed.ac.uk``` to get there in one step.

### Installing requirements:
1. Start by downloading the miniconda3 installation file using 
 ```wget https://repo.continuum.io/miniconda/Miniconda3-latest-Linux-x86_64.sh```.
2. Now run the installation using ```bash Miniconda3-latest-Linux-x86_64.sh```. At the first prompt reply yes. 
    ```
    Do you accept the license terms? [yes|no]
    [no] >>> yes
    ```
3. At the second prompt simply press enter.
    ```
    Miniconda3 will now be installed into this location:
    /home/sxxxxxxx/miniconda3
    
      - Press ENTER to confirm the location
      - Press CTRL-C to abort the installation
      - Or specify a different location below
    ```
4. At the last prompt to initialise conda reply 'yes':
    ```
    Do you wish the installer to initialize Miniconda3
    by running conda init [yes|no]
    [no] >>> yes
    ```
5. Now you need to activate your environment by first running:
```source .bashrc```.
This reloads .bashrc which includes the new miniconda path.
6. Run ```source activate``` to load miniconda root.
7. Now run ```conda create -n mlp python=3``` this will create the mlp environment. At the prompt choose y.
8. Now run ```source activate mlp```.
9. Install git using```conda install git```. Then config git using: 
```git config --global user.name "[your name]"; git config --global user.email "[matric-number]@sms.ed.ac.uk"```
10. Now clone the mlpractical repo using ```git clone https://github.com/cortu01/mlpractical.git```.
11. ```cd mlpractical```
12. Checkout the mlp_cluster_tutorial branch using ```git checkout mlp2025-26/mlp_compute_engines```.
13. Install the required packages using ```bash install.sh```.

> Note: Check that you can use the GPU version of PyTorch by running ```python -c "import torch; print(torch.cuda.is_available())"``` in a `bash` script (see the example below). If this returns `True`, then you are good to go. If it returns `False`, then you need to install the GPU version of PyTorch manually. To do this, run ```conda uninstall pytorch``` and then ```pip install torch torchvision --index-url https://download.pytorch.org/whl/cu118``` or ```pip install torch torchvision```. This will install the latest version of PyTorch with CUDA support. This version is also compatible with older CUDA versions installed on the cluster.

14. This includes all of the required installations. Proceed to the next section outlining how to use the slurm cluster
 management software. Please remember to clean your setup files using ```conda clean -t```
 
### Using Slurm
Slurm provides us with some commands that can be used to submit, delete, view, explore current jobs, nodes and resources among others.
To submit a job one needs to use ```sbatch script.sh``` which will automatically find available nodes and pass the job,
 resources and restrictions required. The script.sh is the bash script containing the job that we want to run. Since we will be using the NVIDIA CUDA and CUDNN libraries 
 we have provided a sample script which should be used for your job submissions. The script is explained in detail below:
 
```bash
#!/bin/sh
#SBATCH -N 1	  # nodes requested
#SBATCH -n 1	  # tasks requested
#SBATCH --partition=Teach-Standard
#SBATCH --gres=gpu:1
#SBATCH --mem=12000  # memory in Mb
#SBATCH --time=0-08:00:00

export CUDA_HOME=/opt/cuda-9.0.176.1/

export CUDNN_HOME=/opt/cuDNN-7.0/

export STUDENT_ID=$(whoami)

export LD_LIBRARY_PATH=${CUDNN_HOME}/lib64:${CUDA_HOME}/lib64:$LD_LIBRARY_PATH

export LIBRARY_PATH=${CUDNN_HOME}/lib64:$LIBRARY_PATH

export CPATH=${CUDNN_HOME}/include:$CPATH

export PATH=${CUDA_HOME}/bin:${PATH}

export PYTHON_PATH=$PATH

mkdir -p /disk/scratch/${STUDENT_ID}


export TMPDIR=/disk/scratch/${STUDENT_ID}/
export TMP=/disk/scratch/${STUDENT_ID}/

mkdir -p ${TMP}/datasets/
export DATASET_DIR=${TMP}/datasets/
# Activate the relevant virtual environment:

source /home/${STUDENT_ID}/miniconda3/bin/activate mlp
cd ..
python train_evaluate_emnist_classification_system.py --filepath_to_arguments_json_file experiment_configs/emnist_tutorial_config.json
```

To actually run this use ```sbatch emnist_single_gpu_tutorial.sh```. When you do this, the job will be submitted and you will be given a job id.
```bash
[burly]sxxxxxxx: sbatch emnist_single_gpu_tutorial.sh 
Submitted batch job 147

```

To view a list of all running jobs use ```squeue``` for a minimal presentation and ```smap``` for a more involved presentation. Furthermore to view node information use ```sinfo```.
```bash
squeue
             JOBID PARTITION     NAME     USER ST       TIME  NODES NODELIST(REASON)
               143 interacti     bash    iainr  R       8:00      1 landonia05
               147 interacti gpu_clus sxxxxxxx  R       1:05      1 landonia02

```
Also in case you want to stop/delete a job use ```scancel job_id``` where job_id is the id of the job.

Furthermore in case you want to test some of your code interactively to prototype your solution before you submit it to
 a node you can use ```srun -p interactive  --gres=gpu:2 --pty python my_code_exp.py```.

## Slurm Cheatsheet
For a nice list of most commonly used Slurm commands please visit [here](https://bitsanddragons.wordpress.com/2017/04/12/slurm-user-cheatsheet/).

## Syncing or copying data over to DICE

At some point you will need to copy your data to DICE so you can analyse them and produce charts, write reports, store for future use etc.
1. If you are on a terminal within I.F/A.T, then skip to step 2, if you are not, then, you'll first have to open a VPN into the university network using the instructions found [here](http://computing.help.inf.ed.ac.uk/openvpn).
2. From your local machine:
    1. To send data from a local machine to the cluster: ```rsync -ua --progress <local_path_of_data_to_transfer> <studentID>@mlp.inf.ed.ac.uk:/home/<studentID>/path/to/folder```
    2. To receive data from the cluster to your local machine ```rsync -ua --progress <studentID>@mlp.inf.ed.ac.uk:/home/<studentID>/path/to/folder <local_path_of_data_to_transfer> ```

## Running an experiment
To run a default image classification experiment using the template models provided:
1. Sign into the cluster using ssh sxxxxxxx@mlp1.inf.ed.ac.uk
2. Activate your conda environment using, source miniconda3/bin/activate ; conda activate mlp
3. cd mlpractical
4. cd cluster_experiment_scripts
5. Find which experiment(s) you want to run (make sure the experiment ends in 'gpu_cluster.sh'). Decide if you want to run a single experiment or multiple experiments in parallel.
    1. For a single experiment: ```sbatch experiment_script.sh```
    2. To run multiple experiments using the "hurdle-reducing" script that automatically submits jobs, makes sure the jobs are always in queue/running:
        1. Make sure the cluster_experiment_scripts folder contains ***only*** the jobs you want to run. 
        2. Run the command: 
        ```
        python run_jobs.py --num_parallel_jobs <number of jobs to keep in the slurm queue at all times> --num_epochs <number of epochs to run each job>
        ```

## Additional Help

If you require additional help please post on piazza or if you are experiencing technical problems (actual system/hardware problems) then please submit a [computing support ticket](https://www.inf.ed.ac.uk/systems/support/form/).

## List of very useful slurm commands:
- squeue: Shows all jobs from all users currently in the queue/running
- squeue -u <user_id>: Shows all jobs from user <user_id> in the queue/running 
- sprio: Shows the priority score of all of your current jobs that are not yet running
- scontrol show job <job_id>: Shows all information about job <job_id>
- scancel <job_id>: Cancels job with id <job_id>
- scancel -u <user_id>: Cancels all jobs, belonging to user <user_id>, that are currently in the queue/running
- sinfo: Provides info about the cluster/partitions
- sbatch <job_script>: Submit a job that will run the script <job_script> to the slurm scheduler.

## Overview of code:
- [arg_extractor.py](arg_extractor.py): Contains an array of utility methods that can parse python arguments or convert
 a json config file into an argument NamedTuple.
- [data_providers.py](data_providers.py): A sample data provider, of the same type used in the MLPractical course.
- [experiment_builder.py](experiment_builder.py): Builds and executes a simple image classification experiment, keeping track
of relevant statistics, taking care of storing and re-loading pytorch models, as well as choosing the best validation-performing model to evaluate the test set on.
- [model_architectures.py](model_architectures.py): Provides a fully connected network and convolutional neural network 
sample models, which have a number of moving parts indicated as hyperparameters.
- [storage_utils.py](storage_utils.py): Provides a number of storage/loading methods for the experiment statistics.
- [train_evaluated_emnist_classification_system.py](train_evaluate_emnist_classification_system.py): Runs an experiment 
given a data provider, an experiment builder instance and a model architecture