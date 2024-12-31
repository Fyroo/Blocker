import tkinter as tk
from tkinter import ttk
import threading
from blocker_interface import DomainBlockerApp
from sniffer_interface import PacketSnifferApp
from domain_fetch_module import DomainUpdater

def main():
    # Initialize domain updater
    domain_updater = DomainUpdater(auto_update=True)
    update_thread = threading.Thread(target=domain_updater.update_loop, daemon=True)
    update_thread.start()

    # Initialize applications
    root = tk.Tk()
    root.title("Network Tools")

    # Tabs for different applications
    notebook = ttk.Notebook(root)


    root.mainloop()

if __name__ == "__main__":
    main()
