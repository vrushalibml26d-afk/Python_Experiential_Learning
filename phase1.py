
# Contact Book Using Python
# Phase I: Basic Logic Design

contacts = {}

while True:
    print("\n--- CONTACT BOOK ---")
    print("1. Add Contact")
    print("2. View Contacts")
    print("3. Search Contact")
    print("4. Update Contact")
    print("5. Delete Contact")
    print("6. Exit")

    choice = input("Enter your choice: ")

    if choice == "1":
        name = input("Enter name: ")
        mobile = input("Enter mobile number: ")
        email = input("Enter email: ")
        organization = input("Enter organization: ")

        contacts[name] = {
            "mobile": mobile,
            "email": email,
            "organization": organization
        }
        print("Contact added successfully!")

    elif choice == "2":
        for name, details in contacts.items():
            print(name, details)

    elif choice == "3":
        name = input("Enter name to search: ")
        if name in contacts:
            print(name, contacts[name])
        else:
            print("Contact not found!")

    elif choice == "4":
        print("Update logic will be implemented in Phase II.")

    elif choice == "5":
        print("Delete logic will be implemented in Phase II.")

    elif choice == "6":
        print("Exiting Contact Book.")
        break

    else:
        print("Invalid choice!")
