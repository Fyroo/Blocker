import tkinter as tk
from tkinter import ttk
import threading
from setdns_module import DNSManager
from dns_resolver_interface import DomainBlockerApp
from sniffer_interface import PacketSnifferApp
from domain_fetch_module import DomainUpdater
from configuration_module import ConfigHandler
from configuration_interface import ConfigurationInterface
from dns_resolver_module import DNSServer
from dashboard_interface import DashboardApp

def main():
    dns_manager = DNSManager()
    dns_thread = threading.Thread(target=dns_manager.set_dns, daemon=True)
    dns_thread.start()
    dns_manager.wait_for_dns_ready()

    config_handler = ConfigHandler()
    
    dns_server = DNSServer(config_handler)
    dns_server.update_blocklist([])

    auto_update = config_handler.config.get("auto_update", True)
    domain_updater = DomainUpdater(auto_update=auto_update)

    if auto_update:
        update_thread = threading.Thread(target=domain_updater.update_loop, daemon=True)
        update_thread.start()

    root = tk.Tk()
    root.title("Blocker")
    root.config(bg="#F4F6F9")

    sidebar = tk.Frame(root, width=250, bg="#4CAF50")
    sidebar.pack(side="left", fill="y", padx=5, pady=5)

    content_frame = tk.Frame(root, bg="#F4F6F9")
    content_frame.pack(side="right", fill="both", expand=True, padx=10, pady=10)

    frames = {}

    def switch_frame(frame_name):
        for name, frame in frames.items():
            frame.pack_forget()
        frames[frame_name].pack(fill="both", expand=True)

    dashboard_frame = tk.Frame(content_frame, bg="#F4F6F9")
    DashboardApp(dashboard_frame, config_handler, dns_server)
    frames["Dashboard"] = dashboard_frame

    sniffer_frame = tk.Frame(content_frame, bg="#F4F6F9")
    PacketSnifferApp(sniffer_frame)
    frames["Live Packet View"] = sniffer_frame

    blocker_frame = tk.Frame(content_frame, bg="#F4F6F9")
    DomainBlockerApp(blocker_frame, dns_server)
    frames["Domain Blocker"] = blocker_frame

    config_frame = tk.Frame(content_frame, bg="#F4F6F9")
    ConfigurationInterface(config_frame, config_handler)
    frames["Configuration"] = config_frame

    def create_button(text, command):
        button = ttk.Button(sidebar, text=text, command=command, style="Sidebar.TButton")
        button.pack(fill="x", pady=15, padx=20)
        return button

    buttons = {
        "Dashboard": lambda: switch_frame("Dashboard"),
        "Live Packet View": lambda: switch_frame("Live Packet View"),
        "Domain Blocker": lambda: switch_frame("Domain Blocker"),
        "Configuration": lambda: switch_frame("Configuration"),
    }

    for text, command in buttons.items():
        create_button(text, command)

    style = ttk.Style()
    style.configure("Sidebar.TButton", font=("Segoe UI", 14), padding=8, relief="flat", background="#4CAF50", foreground="white")
    style.map("Sidebar.TButton", background=[("active", "#45a049")])

    switch_frame("Dashboard")

    
    def on_closing():
        print("Closing application...")
        dns_manager.reset_dns() 
        root.destroy()

    root.protocol("WM_DELETE_WINDOW", on_closing)
    root.mainloop()
if __name__ == "__main__":
    main()
