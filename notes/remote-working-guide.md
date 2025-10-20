# Remote Working Guide 

This guide helps you access School computers from home for the Machine Learning Practical course.

The School supports multiple access methods:
- [Remote desktop service](http://computing.help.inf.ed.ac.uk/remote-desktop)
- [Virtual DICE Machine](http://computing.help.inf.ed.ac.uk/vdice) 
- **SSH External Login** (recommended)

We recommend SSH External Login as it provides fast, reliable access to DICE systems. If you prefer other options, follow the links above.

## Connecting via SSH

Connect to the Informatics student server using a terminal:

```bash
ssh [dice-username]@student.ssh.inf.ed.ac.uk
```

*Note: This assumes you have an SSH client and are familiar with SSH. If not, see "How to use an SSH gateway" in the [external login guide](http://computing.help.inf.ed.ac.uk/external-login).*

Once connected, set up your environment following the [environment setup instructions](environment-set-up.md). 

**Windows users:** Skip to the [Windows SSH setup section](#ssh-setup-for-windows) for detailed PuTTY instructions. 

# Running Jupyter Notebooks over SSH

This guide shows how to run Jupyter notebooks on remote `student.compute` servers and connect to them from your local machine using SSH port forwarding.

## Securing Your Notebook Server

**Important:** Before running Jupyter on shared servers, you **must** secure your server with password authentication and HTTPS.

Run the provided security script in your `mlpractical` directory:

```bash
cd ~/mlpractical
bash scripts/secure-notebook-server.sh
```

This script:
- Sets up password authentication
- Creates a self-signed SSL certificate for HTTPS
- Configures Jupyter to use secure connections

*Note: You'll see a security warning in your browser due to the self-signed certificate - this is expected and safe to ignore.*

## Connecting to a Remote Server

1. **Connect to the SSH gateway:**
   ```bash
   ssh [dice-username]@student.ssh.inf.ed.ac.uk
   ```

2. **Connect to a compute server:**
   ```bash
   ssh student.compute
   ```
   
   Note the server name shown in your prompt (e.g., `ashbury:~$`) - you'll need this later.

## Starting the Notebook Server

1. **Activate your environment:**
   ```bash
   conda activate mlp
   ```

2. **Navigate to your repository:**
   ```bash
   cd ~/mlpractical
   ```

3. **Start the notebook server:**
   ```bash
   nice -n 19 jupyter notebook --no-browser
   ```
   
   The `nice -n 19` command runs Jupyter at low priority to keep shared servers responsive for all users.
   
   **Important:** Note the port number from the output: `The Jupyter Notebook is running at: https://localhost:[port]/`

## Setting Up Port Forwarding

In a **new terminal window** on your local machine, create an SSH tunnel to forward the remote port to your local machine:

```bash
ssh -N -o ProxyCommand="ssh -q [dice-username]@student.ssh.inf.ed.ac.uk nc [remote-server-name] 22" \
    -L [local-port]:localhost:[remote-port] [dice-username]@[remote-server-name]
```

Replace:
- `[remote-port]`: Port number from the Jupyter server output
- `[local-port]`: An unused port on your local machine (e.g., 8888)
- `[remote-server-name]`: Server name from your prompt (e.g., ashbury)

You'll be prompted for your DICE password twice (once for the gateway, once for the compute server).

## Accessing the Notebook

1. Open your browser and go to `https://localhost:[local-port]`
2. Accept the security warning about the self-signed certificate
3. Enter the notebook password you set up earlier
4. You should now see the Jupyter dashboard

## Shutting Down

When finished:
1. Stop the notebook server: Press `Ctrl+C` twice in the terminal running Jupyter
2. Stop port forwarding: Press `Ctrl+C` in the terminal running the SSH tunnel


# SSH Setup for Windows

Windows users can access School computers using [PuTTY](http://computing.help.inf.ed.ac.uk/installing-putty). 

**Prerequisites:** First install PuTTY and Kerberos following the [official computing instructions](http://computing.help.inf.ed.ac.uk/installing-putty).

## Configuring PuTTY with SSH Tunneling

### 1. Basic Session Setup

1. Run PuTTY and navigate to **Session**
2. Enter hostname: `student.ssh.inf.ed.ac.uk`
3. Save the session with a descriptive name for future use

<center><img src="./figures/putty1.png" width="400" height="300"></center>

### 2. Auto-Login Configuration

1. Navigate to **Connection** → **Data**
2. Enter your student ID (e.g., `s1234567`) in **Auto-login username**

<center><img src="./figures/putty2.png" width="400" height="300"></center>

### 3. Authentication and X11 Setup

Follow steps 3-5 from the [PuTTY installation guide](http://computing.help.inf.ed.ac.uk/installing-putty) to configure:
- **Auth** settings
- **X11 Forwarding**

### 4. SSH Tunnel Configuration

1. Navigate to **Connection** → **SSH** → **Tunnels**
2. Enter a local port number (e.g., `8888`) in **Source port**
3. Enter `localhost:8888` in **Destination** 
4. Click **Add**

<center><img src="./figures/putty3.png" width="400" height="300"></center>

You should see your tunnel listed:

<center><img src="./figures/putty4.png" width="400" height="300"></center>

### 5. Save Configuration

1. Return to **Session**
2. Click **Save** to store your configuration

<center><img src="./figures/putty5.png" width="400" height="300"></center>

## Using Your PuTTY Session

### 6. Connect to Compute Server

1. Click **Open** to start your session
2. Enter your DICE password when prompted
3. Connect to a compute server:
   ```bash
   ssh student.compute
   ```
   Note the server name in your prompt (e.g., `ashbury:~$`)

### 7. Set Up and Start Jupyter

1. Follow the [environment setup guide](environment-set-up.md) if needed
2. Secure your notebook server:
   ```bash
   cd ~/mlpractical
   bash scripts/secure-notebook-server.sh
   ```
3. Start Jupyter:
   ```bash
   conda activate mlp
   cd ~/mlpractical
   nice -n 19 jupyter notebook --no-browser
   ```
   Note the port number from the Jupyter output.

### 8. Create SSH Tunnel

1. Open a **second PuTTY session** using your saved configuration
2. Log in to the SSH gateway (enter password)
3. **Do NOT** run `ssh student.compute` in this session
4. Run the tunnel command:
   ```bash
   ssh -N -f -L localhost:[local-port]:localhost:[jupyter-port] [dice-username]@[remote-server-name]
   ```
   Where:
   - `[local-port]`: Port from step 4 (e.g., 8888)
   - `[jupyter-port]`: Port from Jupyter output
   - `[remote-server-name]`: Server name from step 6

### 9. Access Jupyter

1. Open your browser and go to `https://localhost:[local-port]`
2. Accept the security warning
3. Enter your notebook password
4. Start working with your notebooks!

### Cleanup

When finished:
- Stop Jupyter: `Ctrl+C` twice in the first terminal
- Stop tunneling: `Ctrl+C` in the second terminal
   
   
