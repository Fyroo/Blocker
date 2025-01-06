import os
import subprocess
import threading

class DNSManager:
    def __init__(self):
        os_type = os.name
        self.os_type = os_type
        self.dns_ready_event = threading.Event()

    def set_dns_linux(self):
        resolv_conf = "/etc/resolv.conf"
        backup = f"{resolv_conf}.backup"

        try:
            if not os.path.exists(backup):
                os.rename(resolv_conf, backup)
                print(f"Backup created at {backup}")

            with open(resolv_conf, "w") as file:
                file.write("nameserver 127.0.0.1\n")
            print("DNS server set to 127.0.0.1 in /etc/resolv.conf.")

        except PermissionError:
            print("Permission denied. Please run this script as root.")
        except Exception as e:
            print(f"An error occurred: {e}")
        finally:
            self.dns_ready_event.set()

    def get_connected_interfaces():
        process = subprocess.run('netsh interface show interface', stdout=subprocess.PIPE)
        if process.returncode != 0:
            print('Error fetching interfaces, aborting.')
            exit(1)
        output = process.stdout.decode()
        lines = output.split('\r\n')[3:-2]
        connected_interfaces = []
        for line in lines:
            properties = line.split()
            interface_admin_state = properties[0]
            interface_state = properties[1]
            interface_type = properties[2]
            interface_name = properties[3]
            if interface_state == 'Connected':
                connected_interfaces.append(interface_name)
        return connected_interfaces
   
    def set_dns_windows(self):
        connected_interfaces = get_connected_interfaces()
        if len(connected_interfaces) == 0:
            print('No network connected interfaces present, aborting.')
            exit(1)
        try:
            subprocess.run([f'netsh interface ip set dns name="{first_connected_interface}" static 127.0.0.1'], check=True)
            print("DNS server set to 127.0.0.1 on Windows.")
        except subprocess.CalledProcessError:
            print("Failed to set DNS server on Windows. Please ensure you have the necessary permissions.")
        except Exception as e:
            print(f"An error occurred: {e}")
        finally:
            self.dns_ready_event.set()

    def set_dns(self):

        if self.os_type == 'posix':
            self.set_dns_linux()
        elif self.os_type == 'nt':
            self.set_dns_windows()
        else:
            print("Unsupported operating system.")

    def wait_for_dns_ready(self):
        self.dns_ready_event.wait()

    def reset_default_server_on_destroy_linux(self):
        print('destroy')
        try:
            subprocess.run(['sudo', 'systemctl', 'restart', 'NetworkManager'], check=True)
            print("Network manager restarted successfully.")
        except subprocess.CalledProcessError as e:
            print(f"Error restarting network manager: {e}")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")

    def reset_default_server_on_destroy_windows(self):
        connected_interfaces = get_connected_interfaces()
        if len(connected_interfaces) == 0:
            print('No network connected interfaces present, aborting.')
            exit(1)
        first_connected_interface = connected_interfaces[0]
        process = subprocess.run(f'netsh interface ip set dns name="{first_connected_interface}" dhcp', stdout=subprocess.PIPE)
        if process.returncode != 0:
            print(process.stdout.decode())
            print('Error while resetting DNS, aborting.')
            exit(1)
        
    def reset_dns(self):
        try:
            print('Resetting DNS on Windows...')
            if self.os_type == 'posix':
                self.reset_default_server_on_destroy_linux()
            elif self.os_type == 'nt':
                self.reset_default_server_on_destroy_windows()
            else:
                print("Unsupported operating system.")
        except Exception as e:
            print(f"An error occurred: {e}")