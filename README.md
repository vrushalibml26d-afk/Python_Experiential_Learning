Contact Book Application
Project Overview
The Contact Book is a desktop application developed using Python and Tkinter. It provides a graphical user interface (GUI) to manage contact information in one place.
Features
- Add new contacts
- View all saved contacts in a table
- Search contacts by name, mobile number, email, or organization
- Update existing contact details
- Delete contacts with confirmation
- Store contacts in a JSON file so they remain available after restarting the application
- Clear input fields and display all contacts
Technologies Used
- Python 3
- Tkinter for the graphical user interface
- JSON for local data storage
Requirements
- Python 3 installed on your computer
- Tkinter (usually included with Python on Windows)
Project Files
ContactBook/
├── contact_book_gui.py
├── contacts.json       # Created automatically when contacts are saved
└── README.md
How to Run
1. Download or clone this project.
2. Open the project folder in VS Code, IDLE, or a terminal.
3. Run the application:
   python contact_book_gui.py
4. The Contact Book window will open.
How to Use
1. Add Contact: Enter the name and mobile number, optionally enter email and organization, then click Add Contact.
2. Select a Contact: Click a row in the table to load its details into the form.
3. Update Contact: Select a contact, edit its details, and click Update.
4. Delete Contact: Select a contact and click Delete. Confirm the deletion when prompted.
5. Search Contact: Enter a name, phone number, email, or organization in the search box and click Search.
6. Show All: Click Show All to display all saved contacts.
7. Clear: Click Clear to clear the form and search box.
Data Storage
Contact details are stored locally in contacts.json. This file is created automatically when a contact is added. Keep this file private because it may contain personal contact information.
Testing Checklist
- [ ] Add a new contact
- [ ] View all contacts
- [ ] Search by name, mobile number, email, and organization
- [ ] Update contact details
- [ ] Delete a contact and test the confirmation prompt
- [ ] Restart the application and verify saved contacts
Limitations
- Contact names are used as unique identifiers, so two contacts cannot have exactly the same name.
- The current version does not support renaming a contact through the Update button.
- Data is stored locally on the computer; it is not synchronized online.
Future Enhancements
- Support editing a contact's name
- Add input validation for phone numbers and email addresses
- Add export/import and backup options
- Add password protection
Conclusion
The Contact Book application demonstrates the use of Python functions, Tkinter widgets, event handling, dictionaries, and JSON file handling to create a simple desktop contact management system.
