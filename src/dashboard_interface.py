import tkinter as tk
from tkinter import ttk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import random
from dns_resolver_module import DNSServer 


class DashboardApp:
    def __init__(self, root, config_handler, dns_server):
        self.root = root
        label = tk.Label(self.root, text="Dashboard", font=("Arial", 16, "bold"))
        label.pack()
        self.config_handler = config_handler
        self.dns_server = dns_server

        self.total_queries = self.dns_server.total_monthly_queries
        self.blocked_queries = self.dns_server.monthly_blocks
        self.total_domains_blocked = len(self.dns_server.blocked_domains)
        if self.total_queries == 0 :
            self.percentage_blocked =100
        else:
            self.percentage_blocked = (self.blocked_queries / self.total_queries) * 100

        self.upstream_server = tk.StringVar(value=self.config_handler.config["upstream_dns"]["name"])
        self.server_state = self.dns_server.is_run
        self.blocker_state = self.dns_server.blocking_enabled

        self.create_header()
        self.create_summary_boxes()
        self.create_pie_charts()

        self.update_stats()

    def create_header(self):
        header_frame = ttk.Frame(self.root, padding=10)
        header_frame.pack(fill=tk.X)

        ttk.Label(header_frame, text="This Month Statistics:", font=("Arial", 24, "bold")).pack(side=tk.LEFT)

        self.server_status_label = ttk.Label(
            header_frame, text=self.get_server_status_text()[0], font=("Arial", 14)
        )
        self.server_status_label.pack(side=tk.RIGHT)

    def create_summary_boxes(self):
        summary_frame = ttk.Frame(self.root, padding=10)
        summary_frame.pack(fill=tk.X, pady=10)

        blocker_frame = ttk.Frame(summary_frame, relief=tk.RIDGE, padding=10)
        blocker_frame.grid(row=0, column=0, padx=10, sticky=tk.W)
        ttk.Label(blocker_frame, text="Blocker", font=("Arial", 14, "bold")).pack()
        self.blocker_state_label = ttk.Label(
            blocker_frame, text=self.get_blocker_state_text()[0], font=("Arial", 12)
        )
        self.blocker_state_label.pack()

        upstream_frame = ttk.Frame(summary_frame, relief=tk.RIDGE, padding=10)
        upstream_frame.grid(row=0, column=1, padx=10, sticky=tk.W)
        ttk.Label(upstream_frame, text="Upstream Server", font=("Arial", 14, "bold")).pack()
        self.upstream_server_label = ttk.Label(
            upstream_frame, text=self.upstream_server.get(), font=("Arial", 12), foreground="purple"
        )
        self.upstream_server_label.pack()

        domains_frame = ttk.Frame(summary_frame, relief=tk.RIDGE, padding=10)
        domains_frame.grid(row=0, column=2, padx=10, sticky=tk.W)
        ttk.Label(domains_frame, text="Total Domains on Blocklist", font=("Arial", 14, "bold")).pack()
        self.total_domains_label = ttk.Label(
            domains_frame, text=f"{self.total_domains_blocked:,}", font=("Arial", 12), foreground="red"
        )
        self.total_domains_label.pack()

    def create_pie_charts(self):
        pie_frame = ttk.Frame(self.root, padding=10)
        pie_frame.pack(fill=tk.BOTH, expand=True, pady=10)

        figure1 = Figure(figsize=(6, 6), dpi=100)
        self.pie1 = figure1.add_subplot(1, 1, 1)
        self.update_pie1()

        canvas1 = FigureCanvasTkAgg(figure1, master=pie_frame)
        canvas1.get_tk_widget().grid(row=0, column=0, padx=20, pady=10)

        figure2 = Figure(figsize=(6, 6), dpi=100)
        self.pie2 = figure2.add_subplot(1, 1, 1)
        self.update_pie2()

        canvas2 = FigureCanvasTkAgg(figure2, master=pie_frame)
        canvas2.get_tk_widget().grid(row=0, column=1, padx=20, pady=10)

    def update_pie1(self):
        blocked = self.blocked_queries
        allowed = self.total_queries - blocked
        labels = ["Blocked Queries", "Allowed Queries"]
        sizes = [0, 1]
        if blocked != 0 or allowed != 0 :
            sizes = [blocked, allowed]
        colors = ["red", "green"]

        self.pie1.clear()
        self.pie1.pie(
            sizes,
            labels=labels,
            autopct='%1.1f%%',
            startangle=90,
            colors=colors,
            wedgeprops={"edgecolor": "black"},
        )
        self.pie1.set_title("Query Distribution", fontsize=14)

    def update_pie2(self):
        categories = ["ADS", "NSFW", "Other"]
        blocked_domains = [50000, 30000, max(self.total_domains_blocked - 80000, 0)]  # Ensure non-negative values
        colors = ["blue", "orange", "purple"]

        self.pie2.clear()
        self.pie2.pie(
            blocked_domains,
            labels=categories,
            autopct='%1.1f%%',
            startangle=90,
            colors=colors,
            wedgeprops={"edgecolor": "black"},
        )
        self.pie2.set_title("Blocklist Distribution", fontsize=14)

    def update_stats(self):
        self.total_queries = self.dns_server.total_monthly_queries
        self.blocked_queries = self.dns_server.monthly_blocks
        if self.total_queries > 0:
            self.percentage_blocked = (self.blocked_queries / self.total_queries) * 100

        self.update_pie1()
        self.update_pie2()

        self.total_domains_blocked = len(self.dns_server.blocked_domains)
        self.total_domains_label.config(text=f"{self.total_domains_blocked:,}")

        self.blocker_state_label.config(
            text=self.get_blocker_state_text()[0], foreground=self.get_blocker_state_text()[1]
        )

        self.server_status_label.config(
            text=self.get_server_status_text()[0], foreground=self.get_server_status_text()[1]
        )

        self.root.after(1000, self.update_stats)

    def get_server_status_text(self):
        if self.dns_server.is_run:
            return "DNS Server: ON", "green"
        else:
            return "DNS Server: OFF", "red"

    def get_blocker_state_text(self):
        if self.dns_server.blocking_enabled:
            return "Enabled", "green"
        else:
            return "Disabled", "red"


#if __name__ == "__main__":
#    root = tk.Tk()
#    app = DashboardApp(root)
#    root.mainloop()
