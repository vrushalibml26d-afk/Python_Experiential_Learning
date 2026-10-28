
import json
import os

FILE = "contacts.json"


def load_contacts():
    if os.path.exists(FILE):
        with open(FILE, "r") as f:
            return json.load(f)
    return {}


def save_contacts(contacts):
    with open(FILE, "w") as f:
        json.dump(contacts, f, indent=4)


def add_contact(contacts):
    name = input("Enter name: ").strip()

    if not name:
        print("Name cannot be empty!")
        return

    if name in contacts:
        print("Contact already exists!")
        return

    mobile = input("Enter mobile number: ")
    email = input("Enter email address: ")
    organization = input("Enter organization: ")

    contacts[name] = {
        "mobile": mobile,
        "email": email,
        "organization": organization
    }

    save_contacts(contacts)
    print("Contact added successfully!")


def view_contacts(contacts):
    if not contacts:
        print("No contacts found.")
        return

    for name, details in contacts.items():
        print("\nName:", name)
        print("Mobile:", details["mobile"])
        print("Email:", details["email"])
        print("Organization:", details["organization"])


def search_contact(contacts):
    name = input("Enter name to search: ").strip()

    if name in contacts:
        print("Contact Found:", name)
        for key, value in contacts[name].items():
            print(key.title() + ":", value)
    else:
        print("Contact not found.")


def update_contact(contacts):
    name = input("Enter name to update: ").strip()

    if name not in contacts:
        print("Contact not found.")
        return

    details = contacts[name]
    details["mobile"] = input(
        f"Mobile [{details['mobile']}]: "
    ) or details["mobile"]

    details["email"] = input(
        f"Email [{details['email']}]: "
    ) or details["email"]

    details["organization"] = input(
        f"Organization [{details['organization']}]: "
    ) or details["organization"]

    save_contacts(contacts)
    print("Contact updated successfully!")


def delete_contact(contacts):
    name = input("Enter name to delete: ").strip()

    if name in contacts:
        del contacts[name]
        save_contacts(contacts)
        print("Contact deleted successfully!")
    else:
        print("Contact not found.")


def main():
    contacts = load_contacts()

    while True:
        print("\n===== CONTACT BOOK =====")
        print("1. Add Contact")
        print("2. View Contacts")
        print("3. Search Contact")
        print("4. Update Contact")
        print("5. Delete Contact")
        print("6. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            add_contact(contacts)
        elif choice == "2":
            view_contacts(contacts)
        elif choice == "3":
            search_contact(contacts)
        elif choice == "4":
            update_contact(contacts)
        elif choice == "5":
            delete_contact(contacts)
        elif choice == "6":
            print("Thank you for using Contact Book!")
            break
        else:
            print("Invalid choice! Try again.")


if __name__ == "__main__":
    main()
