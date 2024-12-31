import tkinter as tk
from tkinter import ttk, messagebox
import threading
from dns_resolver_module import DNSServer  # Import your DNS server class


class DomainBlockerApp:
    def __init__(self, root, dns_server):
        self.root = root
        self.dns_server = dns_server

        self.root.title("Domain Blocker")
        self.root.geometry("400x400")
        self.auto_update = tk.BooleanVar(value=False)
        self.selected_filters = set()

        self.server_running = True  # The server is always running

        self.init_ui()

        # Start the DNS server in a separate thread when the app starts
        threading.Thread(target=self.dns_server.run, daemon=True).start()

    def init_ui(self):
        # Title
        ttk.Label(self.root, text="Domain Blocker", font=("Arial", 16, "bold")).pack(pady=10)

        # Filters
        ttk.Label(self.root, text="Select Filters:", font=("Arial", 12)).pack(pady=5)

        self.ads_var = tk.BooleanVar(value=False)
        self.nsfw_var = tk.BooleanVar(value=False)

        ttk.Checkbutton(
            self.root, text="Block Advertisments", variable=self.ads_var,
            command=self.update_filters
        ).pack(anchor=tk.W, padx=20)

        ttk.Checkbutton(
            self.root, text="Block NSFW", variable=self.nsfw_var,
            command=self.update_filters
        ).pack(anchor=tk.W, padx=20)

        # Counters
        self.counter_label = ttk.Label(self.root, text="", font=("Arial", 12))
        self.counter_label.pack(pady=10)

        self.daily_blocks_label = ttk.Label(self.root, text=f"Domains Blocked Today: {self.dns_server.daily_blocks}", font=("Arial", 10))
        self.daily_blocks_label.pack(pady=5)

        self.monthly_blocks_label = ttk.Label(self.root, text=f"Domains Blocked This Month: {self.dns_server.monthly_blocks}", font=("Arial", 10))
        self.monthly_blocks_label.pack(pady=5)

        self.update_counters()

        # Start/Stop Server Buttons
        ttk.Button(self.root, text="Start Blocking", command=self.start_blocking).pack(pady=5)
        ttk.Button(self.root, text="Stop Blocking", command=self.stop_blocking).pack(pady=5)

    def update_filters(self):
        self.selected_filters = set()
        if self.ads_var.get():
            self.selected_filters.add("ADS")
        if self.nsfw_var.get():
            self.selected_filters.add("NSFW")

        self.dns_server.update_blocklist(self.selected_filters)
        self.update_counters()

    def update_counters(self):
        total = len(self.dns_server.blocked_domains)
        self.counter_label.config(text=f"Total Domains to Block: {total}")
        self.daily_blocks_label.config(text=f"Domains Blocked Today: {self.dns_server.daily_blocks}")
        self.monthly_blocks_label.config(text=f"Domains Blocked This Month: {self.dns_server.monthly_blocks}")
        self.root.after(1000, self.update_counters)  # Update counters every second

    def start_blocking(self):
        self.dns_server.blocking_enabled = True
        messagebox.showinfo("Info", "Blocking Enabled!")

    def stop_blocking(self):
        self.dns_server.blocking_enabled = False
        messagebox.showinfo("Info", "Blocking Disabled. All queries will resolve through upstream DNS.")


if __name__ == "__main__":
    server = DNSServer()
    server.blocklist_files = {
        "ADS": "Blocker/data/ads_domains.txt",
        "NSFW": "Blocker/data/nsfw_domains.txt",
    }
    server.update_blocklist([])  # Start with no filters

    root = tk.Tk()
    app = DomainBlockerApp(root, server)
    root.mainloop()
