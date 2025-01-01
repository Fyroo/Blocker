import tkinter as tk
from tkinter import ttk, messagebox
from domain_fetch_module import DomainUpdater

class ConfigurationInterface:

    providers_names = ["Google", "Cloudflare", "Quad9", "OpenDNS", "Custom"]
    providers_map = {
        "Google": "8.8.8.8",
        "Cloudflare": "1.1.1.1",
        "Quad9": "9.9.9.9",
        "OpenDNS": "208.67.222.222",
    }

    def __init__(self, root, config_handler):
        self.root = root
        self.config_handler = config_handler
        label = tk.Label(self.root, text="Configuration", font=("Arial", 16, "bold"))
        label.pack()
        self.DomainUpdater = DomainUpdater()
        self.auto_update = tk.BooleanVar(value=self.config_handler.config.get("auto_update", True))
        self.upstream_dns_name = tk.StringVar(value=self.config_handler.config["upstream_dns"]["name"])
        self.upstream_dns_address = tk.StringVar(value=self.config_handler.config["upstream_dns"]["address"])
        self.custom_dns = tk.StringVar(value=self.config_handler.config.get("custom_dns", ""))
        self.whitelist = self.config_handler.config.get("whitelist", [])
        self.blacklist = self.config_handler.config.get("blacklist", [])

        self.create_ui()

    def create_ui(self):
        ttk.Label(self.root, text="Select Upstream DNS Provider:", font=("Arial", 12)).pack(pady=5)

        self.provider_menu = ttk.Combobox(self.root, values=self.providers_names, textvariable=self.upstream_dns_name, state="readonly")
        self.provider_menu.pack(pady=5)

        self.custom_dns_frame = ttk.Frame(self.root)
        self.custom_dns_frame.pack(pady=5, fill=tk.X)
        ttk.Label(self.custom_dns_frame, text="Custom DNS Server:", font=("Arial", 12)).pack(side=tk.LEFT, padx=5)
        self.custom_dns_entry = ttk.Entry(self.custom_dns_frame, textvariable=self.custom_dns, state="disabled")
        self.custom_dns_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)

        self.upstream_dns_name.trace("w", self.toggle_custom_dns)

        ttk.Label(self.root, text="Whitelist Domains:", font=("Arial", 12)).pack(pady=5)
        self.whitelist_box = tk.Listbox(self.root, height=5)
        self.whitelist_box.pack(pady=5, fill=tk.X)
        self.populate_listbox(self.whitelist_box, self.whitelist)
        self.create_list_controls(self.whitelist_box, "whitelist")

        ttk.Label(self.root, text="Blacklist Domains:", font=("Arial", 12)).pack(pady=5)
        self.blacklist_box = tk.Listbox(self.root, height=5)
        self.blacklist_box.pack(pady=5, fill=tk.X)
        self.populate_listbox(self.blacklist_box, self.blacklist)
        self.create_list_controls(self.blacklist_box, "blacklist")

        self.auto_update_check = ttk.Checkbutton(self.root, text="Enable Auto-Update for Domain Lists", variable=self.auto_update)
        self.auto_update_check.pack(pady=5)

        ttk.Button(self.root, text="Update Domain List Manually", command=self.update_domain_list).pack(pady=5)
        ttk.Button(self.root, text="Save Configuration", command=self.save_configuration).pack(pady=5)

    def create_list_controls(self, listbox, key):
        frame = ttk.Frame(self.root)
        frame.pack(pady=5, fill=tk.X)

        entry = ttk.Entry(frame)
        entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)

        ttk.Button(frame, text="Add", command=lambda: self.add_to_list(entry, listbox, key)).pack(side=tk.LEFT, padx=5)
        ttk.Button(frame, text="Remove Selected", command=lambda: self.remove_from_list(listbox, key)).pack(side=tk.LEFT, padx=5)

    def toggle_custom_dns(self, *args):
        state = "normal" if self.upstream_dns_name.get() == "Custom" else "disabled"
        self.custom_dns_entry.config(state=state)

    def add_to_list(self, entry, listbox, key):
        domain = entry.get().strip()
        if domain:
            self.config_handler.add_to_list(key, domain)
            listbox.insert(tk.END, domain)
            entry.delete(0, tk.END)

    def remove_from_list(self, listbox, key):
        selected_indices = listbox.curselection()
        for index in reversed(selected_indices):
            domain = listbox.get(index)
            self.config_handler.remove_from_list(key, domain)
            listbox.delete(index)

    def populate_listbox(self, listbox, items):
        for item in items:
            listbox.insert(tk.END, item)

    def save_configuration(self):
        selected_provider = self.upstream_dns_name.get()
        if selected_provider != "Custom":
            address = self.providers_map.get(selected_provider, "")
        else:
            address = self.custom_dns.get()

        self.config_handler.update_upstream_dns(selected_provider, address)
        self.config_handler.update_config("auto_update", self.auto_update.get())
        self.config_handler.update_config("custom_dns", self.custom_dns.get())

        messagebox.showinfo("Save", "Configuration saved successfully!")


    def update_domain_list(self):
        try:
            self.DomainUpdater.fetch_domains()
            messagebox.showinfo("Update Success", "Domain list updated successfully!")
        except Exception as e:
            messagebox.showerror("Update Failed", f"Error updating domain list: {e}")


if __name__ == "__main__":
    from config_handler import ConfigHandler

    root = tk.Tk()
    config_handler = ConfigHandler()
    app = ConfigurationInterface(root, config_handler)
    root.mainloop()



if __name__ == "__main__":
    from config_handler import ConfigHandler

    root = tk.Tk()
    config_handler = ConfigHandler()
    app = ConfigurationInterface(root, config_handler)
    root.mainloop()
