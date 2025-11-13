# 📜 README: NetDevOps GNS3 Automation Project

# DEMO
![demo gif](ss/demo.gif "Demo GIF")

# Topology
![topology](ss/0.gif "Topology")

## 🎯 Project Goal

This project demonstrates foundational **Network Automation** using Python and the **Netmiko** library. The primary goal is to manage a Cisco router (IOSv-Router) programmatically from a Linux control node (`Control-Node`) via SSH.

### Key Use Cases
1.  **Data Retrieval:** Programmatically collect operational data (active interfaces) and save it locally.
2.  **Configuration Deployment:** Push standard configuration commands (Loopback interface setup) from a local file.

***

### 📁 File Descriptions

| File Name | Description |
| :--- | :--- |
| `IOSv-Router1_config.txt` | The complete running configuration required for IOSv-Router (includes SSH, management IP, and user credentials). |
| `gns3_portable_project.gns3project` | The topology file containing the Router, EtherSwitch, and VM nodes with correct interconnectivity. |
| `automate.py` | The script that handles SSH connection, executes `show` commands, saves output, and pushes configuration commands. |
| `commands_file.txt` | Configuration commands to create `Loopback111` (`10.111.111.111/24`). |
| `requirements.txt` | Contains `netmiko`. Used to quickly install dependencies on the VM. |

***

## 🚀 Setup & Execution Guide

### Step 1: Topology Setup (GNS3)

1.  **Load Project:** Open GNS3 and go to **File > Open portable project...**
2.  Select `gns3_portable_project.gns3project`.
3.  Ensure the necessary appliance images (Cisco IOSv and Ubuntu/Arch VM) are linked and available in your GNS3 setup.
4.  **Start all nodes** (IOSv-Router, EtherSwitch, Control-Node).

### Step 2: Configure the Router (IOSv-Router)

The easiest way to configure IOSv-Router is to paste the prepared configuration.

1.  Open the console for **IOSv-Router**.
2.  Enter privileged EXEC mode:
    ```bash
    enable
    configure terminal
    ```
3.  Copy all content from the provided **`IOSv-Router1_config.txt`** file.
4.  Paste the entire content into the IOSv-Router console and wait for the commands to process.
5.  Save the configuration:
    ```bash
    end
    write memory
    ```

### Step 3: Prepare the Control-Node (IPs, secrets, passwords and other valuez can vary depending on your case!)

1.  Open the console for the **Control-Node**.
2.  Configure the static IP (`192.168.1.10/24`) and ensure connectivity to IOSv-Router (`192.168.1.1`).
    * **Verification:** `ping 192.168.1.1` should succeed.
3.  Install Dependencies: Use the `requirements.txt` file to install Netmiko.
    ```bash
    # Install pip and update packages first (if not already done)
    sudo apt update
    sudo apt install python3-pip -y

    # Install Netmiko using the requirements file
    pip install -r requirements.txt
    ```
4.  Copy the script files (`automate.py` and `commands_file.txt`) from your host machine into a directory on the Control-Node.

### Step 4: Execute the Script

1.  Navigate to the directory containing the Python script on the **Control-Node**.
2.  Execute the automation script:
    ```bash
    python3 automate.py
    ```
3.  When prompted, enter the router password (e.g., `1234`).

***

## ✅ Verification

| Task | Command to Verify | Expected Result |
| :--- | :--- | :--- |
| **Data Retrieval** | On the VM: `cat interface_list.txt` | File contains the output of `show ip interface brief \| include up`. |
| **Config Deployment** | On IOSv-Router: `show run interface Loopback111` | Interface exists with IP `10.111.111.111/24` and the correct description. |
| **Connectivity** | On the VM: `ping 10.111.111.111` | Ping should succeed, confirming the loopback is configured and reachable. |
