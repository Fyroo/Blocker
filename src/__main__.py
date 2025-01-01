import tkinter as tk
from tkinter import ttk, messagebox
import threading
from dns_resolver_interface import DomainBlockerApp
from sniffer_interface import PacketSnifferApp
from domain_fetch_module import DomainUpdater
from configuration_module import ConfigHandler
from configuration_interface import ConfigurationInterface
from dns_resolver_module import DNSServer  
from dashboard_interface import DashboardApp

def main():
    config_handler = ConfigHandler()
    
    dns_server = DNSServer(config_handler)
    dns_server.update_blocklist([])

    auto_update = config_handler.config.get("auto_update", True)
    domain_updater = DomainUpdater(auto_update=auto_update)

    if auto_update:
        update_thread = threading.Thread(target=domain_updater.update_loop, daemon=True)
        update_thread.start()

    root = tk.Tk()
    root.title("Network Tools")
    root.geometry("1300x700")

    sidebar = tk.Frame(root, width=200, bg="lightgray")
    sidebar.pack(side="left", fill="y")

    content_frame = tk.Frame(root)
    content_frame.pack(side="right", fill="both", expand=True)

    frames = {}

    def switch_frame(frame_name):
        for name, frame in frames.items():
            frame.pack_forget()  
        frames[frame_name].pack(fill="both", expand=True)

    dashboard_frame = tk.Frame(content_frame)
    DashboardApp(dashboard_frame, config_handler, dns_server)
    frames["Dashboard"] = dashboard_frame

    sniffer_frame = tk.Frame(content_frame)
    PacketSnifferApp(sniffer_frame)  
    frames["Packet Sniffer"] = sniffer_frame

    blocker_frame = tk.Frame(content_frame)
    DomainBlockerApp(blocker_frame, dns_server) 
    frames["Domain Blocker"] = blocker_frame

    config_frame = tk.Frame(content_frame)
    ConfigurationInterface(config_frame, config_handler) 
    frames["Configuration"] = config_frame



    buttons = {
        "Dashboard": lambda: switch_frame("Dashboard"),
        "Packet Sniffer": lambda: switch_frame("Packet Sniffer"),
        "Domain Blocker": lambda: switch_frame("Domain Blocker"),
        "Configuration": lambda: switch_frame("Configuration"),
    }

    for idx, (text, command) in enumerate(buttons.items()):
        btn = tk.Button(sidebar, text=text, command=command, bg="white", fg="black")
        btn.pack(fill="x", pady=5, padx=10)



    switch_frame("Dashboard")

    root.mainloop()

if __name__ == "__main__":
    main()
