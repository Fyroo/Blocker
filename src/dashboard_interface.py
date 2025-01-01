import tkinter as tk
from tkinter import ttk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import random


class DNSDashboardApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Dashboard")
        self.root.geometry("1200x700")  # Wider screen

        # Sample Data
        self.total_queries = 1000
        self.blocked_queries = 200
        self.total_domains_blocked = 109599
        self.percentage_blocked = (self.blocked_queries / self.total_queries) * 100
        self.upstream_server = "Google DNS"
        self.server_state = "Active"
        self.blocker_state = "Enabled"

        # Layout
        self.create_header()
        self.create_summary_boxes()
        self.create_pie_charts()

        # Simulate updates
        self.update_stats()

    def create_header(self):
        header_frame = ttk.Frame(self.root, padding=10)
        header_frame.pack(fill=tk.X)

        ttk.Label(header_frame, text="DNS Statistics Dashboard", font=("Arial", 24, "bold")).pack(side=tk.LEFT)

        self.server_status_label = ttk.Label(
            header_frame, text=f"DNS Server: {self.server_state}", font=("Arial", 14), foreground="green"
        )
        self.server_status_label.pack(side=tk.RIGHT)

    def create_summary_boxes(self):
        summary_frame = ttk.Frame(self.root, padding=10)
        summary_frame.pack(fill=tk.X, pady=10)

        # Box for Blocker State
        blocker_frame = ttk.Frame(summary_frame, relief=tk.RIDGE, padding=10)
        blocker_frame.grid(row=0, column=0, padx=10, sticky=tk.W)
        ttk.Label(blocker_frame, text="Blocker State", font=("Arial", 14, "bold")).pack()
        self.blocker_state_label = ttk.Label(blocker_frame, text=self.blocker_state, font=("Arial", 12), foreground="blue")
        self.blocker_state_label.pack()

        # Box for Upstream Server
        upstream_frame = ttk.Frame(summary_frame, relief=tk.RIDGE, padding=10)
        upstream_frame.grid(row=0, column=1, padx=10, sticky=tk.W)
        ttk.Label(upstream_frame, text="Upstream Server", font=("Arial", 14, "bold")).pack()
        self.upstream_server_label = ttk.Label(upstream_frame, text=self.upstream_server, font=("Arial", 12), foreground="purple")
        self.upstream_server_label.pack()

        # Box for Total Domains Blocked
        domains_frame = ttk.Frame(summary_frame, relief=tk.RIDGE, padding=10)
        domains_frame.grid(row=0, column=2, padx=10, sticky=tk.W)
        ttk.Label(domains_frame, text="Total Domains on Blocklist", font=("Arial", 14, "bold")).pack()
        self.total_domains_label = ttk.Label(domains_frame, text=f"{self.total_domains_blocked:,}", font=("Arial", 12), foreground="red")
        self.total_domains_label.pack()

    def create_pie_charts(self):
        pie_frame = ttk.Frame(self.root, padding=10)
        pie_frame.pack(fill=tk.BOTH, expand=True, pady=10)

        # Total vs Blocked Queries Pie Chart
        figure1 = Figure(figsize=(6, 6), dpi=100)
        self.pie1 = figure1.add_subplot(1, 1, 1)
        self.update_pie1()  # Initialize chart

        canvas1 = FigureCanvasTkAgg(figure1, master=pie_frame)
        canvas1.get_tk_widget().grid(row=0, column=0, padx=20, pady=10)

        # Blocklist Distribution Pie Chart
        figure2 = Figure(figsize=(6, 6), dpi=100)
        self.pie2 = figure2.add_subplot(1, 1, 1)
        self.update_pie2()  # Initialize chart

        canvas2 = FigureCanvasTkAgg(figure2, master=pie_frame)
        canvas2.get_tk_widget().grid(row=0, column=1, padx=20, pady=10)

    def update_pie1(self):
        # Data for the first pie chart
        blocked = self.blocked_queries
        allowed = self.total_queries - blocked
        labels = ["Blocked Queries", "Allowed Queries"]
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
        # Data for the second pie chart
        categories = ["ADS", "NSFW", "Other"]
        blocked_domains = [50000, 30000, self.total_domains_blocked - 80000]
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
        # Simulate dynamic updates
        self.total_queries += random.randint(10, 50)
        self.blocked_queries += random.randint(0, 20)
        if self.total_queries > 0:
            self.percentage_blocked = (self.blocked_queries / self.total_queries) * 100

        # Update pie charts
        self.update_pie1()
        self.update_pie2()

        # Schedule the next update
        self.root.after(1000, self.update_stats)


# Run the app
if __name__ == "__main__":
    root = tk.Tk()
    app = DNSDashboardApp(root)
    root.mainloop()
