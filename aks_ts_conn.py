import subprocess

def test_connectivity(resource_group, vmss_name, instance_id):
    log_file = "connectivity_test.log"

    try:
        # Test connectivity with mcr.microsoft.com on port 443 using netcat
        netcat_command = f"az vmss run-command invoke -g {resource_group} -n {vmss_name} --command-id RunShellScript --instance-id {instance_id} --scripts 'nc -zv mcr.microsoft.com 443'"
        netcat_result = subprocess.run(netcat_command, shell=True, capture_output=True, text=True)

        # Write netcat command output to log file
        with open(log_file, "a") as f:
            f.write("Connectivity Test:\n")
            f.write(f"Resource Group: {resource_group}\n")
            f.write(f"VMSS Name: {vmss_name}\n")
            f.write(f"Instance ID: {instance_id}\n")
            f.write(netcat_result.stdout)
            f.write("\n")

        # Check kubelet service status using systemctl
        systemctl_command = f"az vmss run-command invoke -g {resource_group} -n {vmss_name} --command-id RunShellScript --instance-id {instance_id} --scripts 'systemctl status kubelet'"
        systemctl_result = subprocess.run(systemctl_command, shell=True, capture_output=True, text=True)

        # Write systemctl command output to log file
        with open(log_file, "a") as f:
            f.write("Kubelet Status:\n")
            f.write(f"Resource Group: {resource_group}\n")
            f.write(f"VMSS Name: {vmss_name}\n")
            f.write(f"Instance ID: {instance_id}\n")
            f.write(systemctl_result.stdout)
            f.write("\n")

        # Retrieve kubelet logs using journalctl
        journalctl_command = f"az vmss run-command invoke -g {resource_group} -n {vmss_name} --command-id RunShellScript --instance-id {instance_id} --scripts 'journalctl -u kubelet --no-pager'"
        journalctl_result = subprocess.run(journalctl_command, shell=True, capture_output=True, text=True)

        # Write journalctl command output to log file
        with open(log_file, "a") as f:
            f.write("Kubelet Logs:\n")
            f.write(f"Resource Group: {resource_group}\n")
            f.write(f"VMSS Name: {vmss_name}\n")
            f.write(f"Instance ID: {instance_id}\n")
            f.write(journalctl_result.stdout)
            f.write("\n")

    except KeyboardInterrupt:
        print("Connectivity test interrupted. Exiting gracefully...")
        exit(0)

    print(f"Connectivity test completed. Results saved in {log_file}")
    exit(0)  # Gracefully exit with success code

# Example usage
resource_group = input("Enter the resource group name: ")
vmss_name = input("Enter the VMSS name: ")
instance_id = input("Enter the instance ID: ")

test_connectivity(resource_group, vmss_name, instance_id)
