import tkinter as tk
from tkinter import messagebox
from tkinter import ttk

def auto_update_filters():
    # Placeholder for auto-update logic
    messagebox.showinfo("Mise à jour", "Les listes de filtres ont été mises à jour automatiquement.")

def filter_by_category(category):
    blocklist_listbox.delete(0, tk.END)
    for item in blocklist:
        if category.lower() in item.lower():
            blocklist_listbox.insert(tk.END, item)

def start_blocking():
    selected_domain = blocklist_listbox.get(tk.ACTIVE)
    if selected_domain:
        messagebox.showinfo("Blocage", f"Blocage du domaine '{selected_domain}' démarré.")
        # Add logic for blocking the domain here (e.g., adding it to a blocklist)
    else:
        messagebox.showwarning("Avertissement", "Veuillez sélectionner un domaine à bloquer.")

def stop_blocking():
    selected_domain = blocklist_listbox.get(tk.ACTIVE)
    if selected_domain:
        messagebox.showinfo("Blocage", f"Blocage du domaine '{selected_domain}' arrêté.")
        # Add logic for stopping the blocking here (e.g., removing it from a blocklist)
    else:
        messagebox.showwarning("Avertissement", "Veuillez sélectionner un domaine à débloquer.")

# Initialisation de la fenêtre principale
root = tk.Tk()
root.title("Gestion des Listes de Blocage")
root.geometry("600x600")
root.configure(bg="#f5f5f5")

# Liste de blocage
blocklist = ["", "", ""]

# Styles
style = ttk.Style()
style.configure("TButton", font=("Arial", 10), padding=5)
style.configure("TLabel", font=("Arial", 12), background="#f5f5f5")

# Bouton Auto-update
ttk.Label(root, text="Gestion des filtres", font=("Arial", 16, "bold"), background="#f5f5f5").pack(pady=10)
ttk.Button(root, text="Auto-update filter lists", command=auto_update_filters).pack(pady=10)

# Liste affichée
ttk.Label(root, text="domain blocked :").pack(pady=5)
blocklist_listbox = tk.Listbox(root, width=70, height=15, font=("Arial", 10), bg="#ffffff", bd=1, relief="solid")
blocklist_listbox.pack(pady=10)

# Remplir la liste de blocage
for domain in blocklist:
    blocklist_listbox.insert(tk.END, domain)

# Filtres
ttk.Label(root, text="Filtres :").pack(pady=5)
filter_frame = tk.Frame(root, bg="#f5f5f5")
filter_frame.pack(pady=10)

# Variables pour les filtres
nsfw_var = tk.BooleanVar(value=False)
ads_var = tk.BooleanVar(value=False)

# Checkbuttons pour les filtres
nsfw_checkbox = tk.Checkbutton(filter_frame, text="NSFW", variable=nsfw_var,
                               command=lambda: filter_by_category("NSFW") if nsfw_var.get() else filter_by_category("Aucun"))
nsfw_checkbox.pack(anchor=tk.W, padx=10)
ads_checkbox = tk.Checkbutton(filter_frame, text="ADS", variable=ads_var,
                              command=lambda: filter_by_category("ADS") if ads_var.get() else filter_by_category("Aucun"))
ads_checkbox.pack(anchor=tk.W, padx=10)

# Boutons de blocage
button_frame = tk.Frame(root, bg="#f5f5f5")
button_frame.pack(pady=10)

start_button = ttk.Button(button_frame, text="Start Block Domain", command=start_blocking)
start_button.pack(side=tk.LEFT, padx=10)

stop_button = ttk.Button(button_frame, text="Stop Block Domain", command=stop_blocking)
stop_button.pack(side=tk.LEFT, padx=10)

# Bouton pour quitter
ttk.Button(root, text="Quitter", command=root.quit).pack(pady=20)

# Lancement de la boucle principale
root.mainloop()
