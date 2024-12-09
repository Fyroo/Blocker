import tkinter as tk
from tkinter import ttk
import threading
from queue import Queue
from sniffer_module import start_sniffing
from interface_list_module import list_interfaces  
from threading import Event

class PacketSnifferApp:
    def __init__(self, root):
        self.root = root
        self.root.geometry('600x600')
        self.root.title('Packet Analyzer')
        
        self.should_we_stop = Event()
        self.packet_queue = Queue()
        
        # Apply styles
        style = ttk.Style()
        style.theme_use('clam')
        style.configure("Treeview", font=('Helvetica', 12), rowheight=25)
        style.configure("Treeview.Heading", font=('Helvetica', 14, 'bold'))
        style.configure("TButton", font=('Helvetica', 14), padding=5)
        style.configure("Title.TLabel", font=('Helvetica', 24, 'bold'), foreground="#333")

        header_label = ttk.Label(root, text='Packet Sniffer', style="Title.TLabel")
        header_label.pack(pady=10)

        # Dropdown for network interfaces
        self.interface_label = ttk.Label(root, text="Select Network Interface:", font=('Helvetica', 12))
        self.interface_label.pack(pady=5)

        self.interface_var = tk.StringVar()
        self.interface_dropdown = ttk.Combobox(root, textvariable=self.interface_var, state="readonly", font=('Helvetica', 12))
        self.interface_dropdown.pack(pady=5)


        self.populate_interfaces()

        self.treev = ttk.Treeview(root, height=10, columns=("Domain IP", "Domain Name"), show='headings')
        self.treev.heading("Domain IP", text="Domain IP")
        self.treev.heading("Domain Name", text="Domain Name")
        self.treev.column("Domain IP", width=200, anchor="center")
        self.treev.column("Domain Name", width=300, anchor="center")
        self.treev.pack(pady=10, padx=20, fill=tk.BOTH, expand=True)

        button_frame = ttk.Frame(root)
        button_frame.pack(pady=10, side=tk.BOTTOM)

        tk.Button(button_frame, text="Start Sniffing", command=self.start_sniffing, width=15, font="Helvetica 7 bold").pack(side=tk.LEFT, padx=10)
        tk.Button(button_frame, text="Stop Sniffing", command=self.stop_sniffing, width=15, font="Helvetica 7 bold").pack(side=tk.LEFT, padx=10)

    def populate_interfaces(self):
        try:
            interfaces = list_interfaces()  
            self.interface_dropdown['values'] = interfaces
            if interfaces:
                self.interface_dropdown.current(0)  
        except Exception as e:
            print(f"Error fetching interfaces: {e}")

    def start_sniffing(self):
        selected_interface = self.interface_var.get()
        if not selected_interface:
            print("Please select a network interface.")
            return
        print(f"Start Sniffing clicked on interface: {selected_interface}")
        self.should_we_stop.clear()
        self.sniffing_thread = threading.Thread(target=start_sniffing, args=(self.packet_queue, self.should_we_stop, selected_interface), daemon=True)
        self.sniffing_thread.start()
        self.root.after(100, self.update_treeview)

    def stop_sniffing(self):
        print("Stop Sniffing clicked")
        self.should_we_stop.set()

    def update_treeview(self):
        while not self.packet_queue.empty():
            packet = self.packet_queue.get()
            self.treev.insert('', 'end', values=(packet["domain_ip"], packet["domain_name"]))
        if not self.should_we_stop.is_set():
            self.root.after(100, self.update_treeview)


if __name__ == "__main__":
    root = tk.Tk()
    app = PacketSnifferApp(root)
    root.mainloop()
