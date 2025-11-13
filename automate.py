import getpass # Module to securely prompt for the user's password
from netmiko import ConnectHandler # Main class used to establish SSH connections

# Define the device connection parameters
router = {
    "device_type": "cisco_ios",
    "host": "192.168.33.2",
    "username": "admin",
    "password": "1234",
    "secret": "1234",
}

# Prompt the user for the router password securely
router["password"] = getpass.getpass("Enter router password: ")

print(f"\n--- Connecting to {router['host']} ---")

try:
    # Establishes the SSH connection; the 'with' statement handles automatic closing
    with ConnectHandler(**router) as net_connect:
        print("--- Connection Successful! ---")

        # Ensure we are in privileged exec mode (required for config mode)
        # net_connect.check_enable_mode() returns True if in enable; net_connect.enable() will attempt to enter it.
        if not net_connect.check_enable_mode():
            print("-> Not in enable mode: attempting to enter enable mode...")
            net_connect.enable()   # enters privileged exec; uses router['secret'] if set
            if not net_connect.check_enable_mode():
                raise Exception("Failed to enter enable (privileged exec) mode. Check the enable password or user privileges.")

        # Optional: disable paging so send_config_from_file output is not paged
        # net_connect.send_command("terminal length 0")  # brief: disables paging

        # === TASK 1: Get active interfaces ===
        print("\n--- TASK 1: Getting active interfaces ---")
        
        # Executes the 'show' command and returns the output string
        command = "show ip interface brief | include up"
        output = net_connect.send_command(command)
        
        # Opens a local file on the VM for writing
        with open("interface_list.txt", "w") as f:
            f.write(output) # Writes the retrieved data into the local file
        
        print(f"-> Successfully saved active interfaces to 'interface_list.txt'")

        # === TASK 2: Configure Loopback 111 ===
        print("\n--- TASK 2: Sending loopback configuration from file ---")
        
        config_file = "commands_file.txt"
        # Reads commands from the file and pushes them to the router in config mode
        output = net_connect.send_config_from_file(config_file)
        
        print(f"-> Configuration from '{config_file}' sent.")

        # === Verification Step ===
        print("\n--- Verifying Loopback111 configuration ---")
        verify_cmd = "show run interface Loopback111"
        # Executes a final 'show' command to confirm the changes
        verify_output = net_connect.send_command(verify_cmd)
        print(verify_output)

except Exception as e:
    print(f"\n*** AN ERROR OCCURRED: {e} ***")