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
            # Backup the existing resolv.conf if not already backed up
            if not os.path.exists(backup):
                os.rename(resolv_conf, backup)
                print(f"Backup created at {backup}")

            # Write the new DNS server
            with open(resolv_conf, "w") as file:
                file.write("nameserver 127.0.0.1\n")
            print("DNS server set to 127.0.0.1 in /etc/resolv.conf.")

        except PermissionError:
            print("Permission denied. Please run this script as root.")
        except Exception as e:
            print(f"An error occurred: {e}")
        finally:
            self.dns_ready_event.set()

    def set_dns_windows(self):
        try:
            # Set the DNS server using netsh
            subprocess.run(['netsh', 'interface', 'ipv4', 'set', 'dns', 'name="Ethernet"', 'static', '127.0.0.1'], check=True)
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
    def reset_default_server_on_destroy_windows(self):
        print('destroy')
    def reset_default_server_on_destroy_linux(self):
        print('destroy')