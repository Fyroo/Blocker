import tkinter as tk
from tkinter import ttk
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
    root.title("DNS Filter")
    root.geometry("1300x800")
    root.config(bg="#F4F6F9")  # Light background for the entire app

    # Sidebar Frame
    sidebar = tk.Frame(root, width=250, bg="#4CAF50")
    sidebar.pack(side="left", fill="y", padx=5, pady=5)

    # Content Frame
    content_frame = tk.Frame(root, bg="#F4F6F9")
    content_frame.pack(side="right", fill="both", expand=True, padx=10, pady=10)

    frames = {}

    def switch_frame(frame_name):
        for name, frame in frames.items():
            frame.pack_forget()
        frames[frame_name].pack(fill="both", expand=True)

    # Initialize the individual frame content
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

    # Create buttons for sidebar
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

    # Sidebar Button Style
    style = ttk.Style()
    style.configure("Sidebar.TButton", font=("Segoe UI", 14), padding=8, relief="flat", background="#4CAF50", foreground="white")
    style.map("Sidebar.TButton", background=[("active", "#45a049")])

    # Start with the Dashboard frame
    switch_frame("Dashboard")

    root.mainloop()

if __name__ == "__main__":
    main()
