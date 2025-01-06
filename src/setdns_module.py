import os
import subprocess
import threading

class DNSManager:
    def __init__(self,logger):
        self.system_logger = logger.system_logger  
        os_type = os.name
        self.os_type = os_type
        self.dns_ready_event = threading.Event()

    def set_dns_linux(self):
        resolv_conf = "/etc/resolv.conf"
        backup = f"{resolv_conf}.backup"

        try:
            if not os.path.exists(backup):
                os.rename(resolv_conf, backup)
                self.system_logger.info(f"Backup created at {backup}")

            with open(resolv_conf, "w") as file:
                file.write("nameserver 127.0.0.1\n")
            self.system_logger.info("DNS server set to 127.0.0.1 in /etc/resolv.conf.")

        except PermissionError:
            self.system_logger.warn("Permission denied. Please run this script as root.")
        except Exception as e:
            self.system_logger.error(f"An error occurred: {e}")
        finally:
            self.dns_ready_event.set()

    def get_connected_interfaces(self):
        if self.os_type != 'nt':
            return [] 

        try:
            process = subprocess.run('netsh interface show interface', stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
            if process.returncode != 0:
                self.system_logger.error('Error fetching interfaces, aborting.')
                self.system_logger.error(process.stderr.decode())  
                exit(1)
            
            output = process.stdout.decode()
            lines = output.split('\r\n')[3:-2]
            connected_interfaces = []
            for line in lines:
                properties = line.split()
                interface_admin_state = properties[0]
                interface_state = properties[1]
                interface_name = properties[3]
                if interface_state == 'Connected':
                    connected_interfaces.append(interface_name)
            return connected_interfaces
        except Exception as e:
            self.system_logger.error(f"Error fetching interfaces: {e}")
            return []

    def set_dns_windows(self):
        connected_interfaces = self.get_connected_interfaces()
        if len(connected_interfaces) == 0:
            self.system_logger.warn('No network connected interfaces present, aborting.')
            exit(1)
        
        first_connected_interface = connected_interfaces[0]
        try:

            subprocess.run([f'netsh', 'interface', 'ip', 'set', 'dns', f'name={first_connected_interface}', 'static', '127.0.0.1'], check=True, shell=True)
            self.system_logger.info(f"DNS server set to 127.0.0.1 on interface {first_connected_interface} in Windows.")
        except subprocess.CalledProcessError as e:
            self.system_logger.error(f"Failed to set DNS server on Windows for interface {first_connected_interface}. Error: {e}")
        except Exception as e:
            self.system_logger.error(f"An error occurred while setting DNS on Windows: {e}")
        finally:
            self.dns_ready_event.set()

    def set_dns(self):
        try:
            if self.os_type == 'posix':
                self.set_dns_linux()
            elif self.os_type == 'nt':
                self.set_dns_windows()
            else:
                self.system_logger.warn("Unsupported operating system.")
        except Exception as e:
            self.system_logger.error(f"An error occurred while setting DNS: {e}")

    def wait_for_dns_ready(self):
        self.dns_ready_event.wait()

    def reset_default_server_on_destroy_linux(self):
        self.system_logger.info('Resetting DNS on Linux...')
        try:
            subprocess.run(['sudo', 'systemctl', 'restart', 'NetworkManager'], check=True)
            self.system_logger.info("Network manager restarted successfully.")
        except subprocess.CalledProcessError as e:
            self.system_logger.error(f"Error restarting network manager: {e}")
        except Exception as e:
            self.system_logger.error(f"An unexpected error occurred while restarting the network manager: {e}")

    def reset_default_server_on_destroy_windows(self):
        connected_interfaces = self.get_connected_interfaces()
        if len(connected_interfaces) == 0:
            self.system_logger.warn('No network connected interfaces present, aborting.')
            exit(1)

        first_connected_interface = connected_interfaces[0]
        try:
            process = subprocess.run(
                f'netsh interface ip set dns name="{first_connected_interface}" dhcp',
                stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True
            )
            if process.returncode != 0:
                self.system_logger.error(process.stdout.decode())
                self.system_logger.error(f"Error while resetting DNS on {first_connected_interface}, aborting.")
                exit(1)
            self.system_logger.info(f"DNS reset to DHCP on {first_connected_interface} in Windows.")
        except subprocess.CalledProcessError as e:
            self.system_logger.error(f"Failed to reset DNS on Windows: {e}")
        except Exception as e:
            self.system_logger.error(f"An error occurred while resetting DNS on Windows: {e}")

    def reset_dns(self):
        try:
            self.system_logger.info('Resetting DNS...')
            if self.os_type == 'posix':
                self.reset_default_server_on_destroy_linux()
            elif self.os_type == 'nt':
                self.reset_default_server_on_destroy_windows()
            else:
                self.system_logger.warn("Unsupported operating system.")
        except Exception as e:
            self.system_logger.error(f"An error occurred while resetting DNS: {e}")
