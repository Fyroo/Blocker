import tkinter as tk
from tkinter import ttk

should_we_stop = False  # Global variable to control sniffing state

def start_button():
    print("Start Sniffing clicked")
    # Logic to start sniffing
    print("Sniffing started")
    treev.insert('', 'end', values=("192.168.1.1", "example.com"))
    treev.insert('', 'end', values=("8.8.8.8", "google.com"))
    #insert live sniffing output

def stop_button():
    global should_we_stop
    print("Stop Sniffing clicked")
    should_we_stop = True
    # Logic to stop sniffing
    print("Sniffing stopped")

# Main application window
root = tk.Tk()
root.geometry('600x400')
root.title('Packet Analyzer')

# Apply a theme to the application
style = ttk.Style()
style.theme_use('clam')  # Use a clean, modern theme

# Styling for Treeview and buttons
style.configure("Treeview", font=('Helvetica', 12), rowheight=25)
style.configure("Treeview.Heading", font=('Helvetica', 14, 'bold'))
style.configure("TButton", font=('Helvetica', 14), padding=5)
style.configure("Title.TLabel", font=('Helvetica', 24, 'bold'), foreground="#333")

# Header Label
header_label = ttk.Label(root, text='Packet Sniffer', style="Title.TLabel")
header_label.pack(pady=10)

# Treeview widget to display IPs and domains
treev = ttk.Treeview(root, height=10, columns=("IP", "Domain"), show='headings')
treev.heading("IP", text="IP Address")
treev.heading("Domain", text="Domain")
treev.column("IP", width=150, anchor="center")
treev.column("Domain", width=300, anchor="center")
treev.pack(pady=10, padx=20, fill=tk.BOTH, expand=True)

# Adding some dummy data to Treeview for testing


# Button frame
button_frame = ttk.Frame(root)
button_frame.pack(pady=10, side=tk.BOTTOM)

# Start Sniffing Button
tk.Button(button_frame, text="Start Sniffing", command=start_button, width=15, font="Helvetica 7 bold").pack(side=tk.LEFT, padx=10)

# Stop Sniffing Button
tk.Button(button_frame, text="Stop Sniffing", command=stop_button, width=15, font="Helvetica 7 bold").pack(side=tk.LEFT, padx=10)

# Run the application
root.mainloop()
