
import tkinter as tk
from tkinter import ttk, messagebox
import json
import os

FILE = "contacts.json"
contacts = {}


# Load saved contacts
def load_contacts():
    global contacts
    if os.path.exists(FILE):
        try:
            with open(FILE, "r") as f:
                contacts = json.load(f)
        except (json.JSONDecodeError, OSError):
            contacts = {}
    refresh_table()


# Save contacts
def save_contacts():
    with open(FILE, "w") as f:
        json.dump(contacts, f, indent=4)


# Clear input fields
def clear_fields():
    name_entry.delete(0, tk.END)
    mobile_entry.delete(0, tk.END)
    email_entry.delete(0, tk.END)
    org_entry.delete(0, tk.END)
    search_entry.delete(0, tk.END)
    refresh_table()


# Refresh contact table
def refresh_table(data=None):
    for item in table.get_children():
        table.delete(item)

    records = contacts if data is None else data

    for name, details in records.items():
        table.insert("", tk.END, values=(
            name,
            details.get("mobile", ""),
            details.get("email", ""),
            details.get("organization", "")
        ))


# Add contact
def add_contact():
    name = name_entry.get().strip()
    mobile = mobile_entry.get().strip()
    email = email_entry.get().strip()
    org = org_entry.get().strip()

    if not name or not mobile:
        messagebox.showwarning(
            "Required", "Name and mobile number are required!"
        )
        return

    if name in contacts:
        messagebox.showwarning(
            "Duplicate", "Contact already exists!"
        )
        return

    contacts[name] = {
        "mobile": mobile,
        "email": email,
        "organization": org
    }

    save_contacts()
    refresh_table()
    clear_inputs()
    messagebox.showinfo("Success", "Contact added successfully!")


def clear_inputs():
    for entry in (name_entry, mobile_entry,
                  email_entry, org_entry):
        entry.delete(0, tk.END)


# Select contact from table
def select_contact(event):
    selected = table.selection()
    if not selected:
        return

    values = table.item(selected[0], "values")
    clear_inputs()

    name_entry.insert(0, values[0])
    mobile_entry.insert(0, values[1])
    email_entry.insert(0, values[2])
    org_entry.insert(0, values[3])


# Update contact
def update_contact():
    old_name = name_entry.get().strip()

    if old_name not in contacts:
        messagebox.showwarning(
            "Error", "Select an existing contact first!"
        )
        return

    new_name = old_name
    mobile = mobile_entry.get().strip()
    email = email_entry.get().strip()
    org = org_entry.get().strip()

    if not mobile:
        messagebox.showwarning(
            "Required", "Mobile number is required!"
        )
        return

    if new_name != old_name and new_name in contacts:
        messagebox.showwarning(
            "Duplicate", "This name already exists!"
        )
        return

    contacts[new_name] = {
        "mobile": mobile,
        "email": email,
        "organization": org
    }

    save_contacts()
    refresh_table()
    clear_inputs()
    messagebox.showinfo("Success", "Contact updated!")


# Delete contact
def delete_contact():
    name = name_entry.get().strip()

    if name not in contacts:
        messagebox.showwarning(
            "Error", "Select a contact to delete!"
        )
        return

    if messagebox.askyesno(
        "Confirm Delete", f"Delete {name}?"
    ):
        del contacts[name]
        save_contacts()
        refresh_table()
        clear_inputs()
        messagebox.showinfo(
            "Success", "Contact deleted!"
        )


# Search contact
def search_contact():
    query = search_entry.get().strip().lower()

    results = {
        name: details
        for name, details in contacts.items()
        if query in name.lower()
        or query in details.get("mobile", "").lower()
        or query in details.get("email", "").lower()
        or query in details.get("organization", "").lower()
    }

    refresh_table(results)


# Main window
root = tk.Tk()
root.title("Contact Book Application")
root.geometry("950x650")
root.minsize(800, 550)
root.configure(bg="#eef2f7")

# Heading
heading = tk.Label(
    root,
    text="CONTACT BOOK",
    font=("Arial", 24, "bold"),
    bg="#243b55",
    fg="white",
    pady=15
)
heading.pack(fill="x")

# Input frame
form = tk.LabelFrame(
    root,
    text="Contact Details",
    font=("Arial", 12, "bold"),
    bg="#eef2f7",
    padx=15,
    pady=10
)
form.pack(fill="x", padx=20, pady=15)

labels = ["Name", "Mobile Number", "Email Address", "Organization"]
entries = []

for i, label in enumerate(labels):
    tk.Label(
        form, text=label, font=("Arial", 10),
        bg="#eef2f7"
    ).grid(row=i // 2 * 2, column=(i % 2) * 2,
           sticky="w", padx=8, pady=5)

    entry = tk.Entry(form, font=("Arial", 11), width=28)
    entry.grid(row=i // 2 * 2, column=(i % 2) * 2 + 1,
               padx=8, pady=5)
    entries.append(entry)

name_entry, mobile_entry, email_entry, org_entry = entries

# Action buttons
buttons = tk.Frame(root, bg="#eef2f7")
buttons.pack(pady=5)

tk.Button(
    buttons, text="Add Contact", command=add_contact,
    bg="#198754", fg="white", width=13
).grid(row=0, column=0, padx=5)

tk.Button(
    buttons, text="Update", command=update_contact,
    bg="#0d6efd", fg="white", width=12
).grid(row=0, column=1, padx=5)

tk.Button(
    buttons, text="Delete", command=delete_contact,
    bg="#dc3545", fg="white", width=12
).grid(row=0, column=2, padx=5)

tk.Button(
    buttons, text="Clear", command=clear_fields,
    width=12
).grid(row=0, column=3, padx=5)

# Search section
search_frame = tk.Frame(root, bg="#eef2f7")
search_frame.pack(fill="x", padx=25, pady=10)

tk.Label(
    search_frame, text="Search Contact:",
    font=("Arial", 11, "bold"), bg="#eef2f7"
).pack(side="left", padx=5)

search_entry = tk.Entry(search_frame, font=("Arial", 11))
search_entry.pack(side="left", fill="x", expand=True, padx=5)

tk.Button(
    search_frame, text="Search",
    command=search_contact, width=10
).pack(side="left", padx=4)

tk.Button(
    search_frame, text="Show All",
    command=lambda: refresh_table(), width=10
).pack(side="left", padx=4)

# Contact table
table_frame = tk.Frame(root)
table_frame.pack(fill="both", expand=True, padx=20, pady=10)

columns = ("Name", "Mobile", "Email", "Organization")

table = ttk.Treeview(
    table_frame, columns=columns,
    show="headings", height=12
)

for col in columns:
    table.heading(col, text=col)
    table.column(col, width=180, anchor="center")

scrollbar = ttk.Scrollbar(
    table_frame, orient="vertical",
    command=table.yview
)
table.configure(yscrollcommand=scrollbar.set)

table.pack(side="left", fill="both", expand=True)
scrollbar.pack(side="right", fill="y")

table.bind("<<TreeviewSelect>>", select_contact)

# Footer
tk.Label(
    root,
    text="Python Tkinter | Contact Management System",
    bg="#243b55", fg="white", pady=8
).pack(fill="x")

load_contacts()
root.mainloop()
