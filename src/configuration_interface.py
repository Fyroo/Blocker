import tkinter as tk
from tkinter import ttk, messagebox

class DNSConfigApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Configuration")
        self.root.geometry("500x600")

        self.auto_update = tk.BooleanVar(value=False)
        self.upstream_dns = tk.StringVar(value="Google")
        self.custom_dns = tk.StringVar()
        self.whitelist = []
        self.blacklist = []

        self.create_ui()

    def create_ui(self):
        # Title
        ttk.Label(self.root, text="DNS Configuration", font=("Arial", 16, "bold")).pack(pady=10)

        # Upstream DNS Providers
        ttk.Label(self.root, text="Select Upstream DNS Provider:", font=("Arial", 12)).pack(pady=5)
        providers = ["Google", "Cloudflare", "Quad9", "OpenDNS", "Custom"]
        self.provider_menu = ttk.Combobox(self.root, values=providers, textvariable=self.upstream_dns, state="readonly")
        self.provider_menu.pack(pady=5)

        # Custom DNS Server Entry
        self.custom_dns_frame = ttk.Frame(self.root)
        self.custom_dns_frame.pack(pady=5, fill=tk.X)
        ttk.Label(self.custom_dns_frame, text="Custom DNS Server:", font=("Arial", 12)).pack(side=tk.LEFT, padx=5)
        self.custom_dns_entry = ttk.Entry(self.custom_dns_frame, textvariable=self.custom_dns, state="disabled")
        self.custom_dns_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)

        # Enable custom DNS when selected
        self.upstream_dns.trace("w", self.toggle_custom_dns)

        # Whitelist Management
        ttk.Label(self.root, text="Whitelist Domains:", font=("Arial", 12)).pack(pady=5)
        self.whitelist_box = tk.Listbox(self.root, height=5)
        self.whitelist_box.pack(pady=5, fill=tk.X)
        self.create_list_controls(self.whitelist_box, self.whitelist)

        # Blacklist Management
        ttk.Label(self.root, text="Blacklist Domains:", font=("Arial", 12)).pack(pady=5)
        self.blacklist_box = tk.Listbox(self.root, height=5)
        self.blacklist_box.pack(pady=5, fill=tk.X)
        self.create_list_controls(self.blacklist_box, self.blacklist)

        # Auto-Update Settings
        self.auto_update_check = ttk.Checkbutton(self.root, text="Enable Auto-Update for Domain Lists", variable=self.auto_update)
        self.auto_update_check.pack(pady=5)

        # Buttons
        ttk.Button(self.root, text="Update Domain List Manually", command=self.update_domain_list).pack(pady=5)
        ttk.Button(self.root, text="Save Configuration", command=self.save_configuration).pack(pady=5)

    def create_list_controls(self, listbox, domain_list):
        """Create controls for managing whitelist/blacklist."""
        frame = ttk.Frame(self.root)
        frame.pack(pady=5, fill=tk.X)

        entry = ttk.Entry(frame)
        entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)

        ttk.Button(frame, text="Add", command=lambda: self.add_to_list(entry, listbox, domain_list)).pack(side=tk.LEFT, padx=5)
        ttk.Button(frame, text="Remove Selected", command=lambda: self.remove_from_list(listbox, domain_list)).pack(side=tk.LEFT, padx=5)

    def toggle_custom_dns(self, *args):
        """Enable or disable the custom DNS entry field."""
        state = "normal" if self.upstream_dns.get() == "Custom" else "disabled"
        self.custom_dns_entry.config(state=state)

    def add_to_list(self, entry, listbox, domain_list):
        """Add a domain to the list."""
        domain = entry.get().strip()
        if domain:
            domain_list.append(domain)
            listbox.insert(tk.END, domain)
            entry.delete(0, tk.END)

    def remove_from_list(self, listbox, domain_list):
        """Remove selected domains from the list."""
        selected_indices = listbox.curselection()
        for index in reversed(selected_indices):
            listbox.delete(index)
            domain_list.pop(index)

    def update_domain_list(self):
        """Manually update the domain list."""
        messagebox.showinfo("Update", "Domain list updated manually!")

    def save_configuration(self):
        """Save the configuration."""
        config = {
            "upstream_dns": self.upstream_dns.get(),
            "custom_dns": self.custom_dns.get() if self.upstream_dns.get() == "Custom" else None,
            "whitelist": self.whitelist,
            "blacklist": self.blacklist,
            "auto_update": self.auto_update.get()
        }
        print("Configuration saved:", config)
        messagebox.showinfo("Save", "Configuration saved successfully!")

if __name__ == "__main__":
    root = tk.Tk()
    app = DNSConfigApp(root)
    root.mainloop()
