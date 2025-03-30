from tkinter import *
from tkinter import messagebox
from random import randint, choice, shuffle
import pyperclip
import json
from cryptography.fernet import Fernet
# ---------------------------- PASSWORD GENERATOR ------------------------------- #


def generate_password():
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
               'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P',
               'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']
    password_letters = [choice(letters) for _ in range(randint(8, 10))]
    password_symbols = [choice(symbols) for _ in range(randint(2, 4))]
    password_numbers = [choice(numbers) for _ in range(randint(2, 4))]
    password_list = password_letters + password_symbols + password_numbers
    shuffle(password_list)
    pwd = "".join(password_list)
    passwordEntry.insert(0, pwd)
    pyperclip.copy(pwd)

# ---------------------------- SAVE PASSWORD ------------------------------- #


def encrypt_password(password_data):
    key = Fernet.generate_key()
    f = Fernet(key)
    return key.decode('utf-8'), f.encrypt(bytes(password_data, 'utf-8')).decode('utf-8')


def decrypt_password(key, encrypted_password):
    f = Fernet(key.encode('utf-8'))
    return f.decrypt(encrypted_password.encode('utf-8')).decode('utf-8')


def save_data():
    website_data = websiteEntry.get()
    username_data = emailEntry.get()
    password_data = passwordEntry.get()
    if bool(not website_data.strip()) or bool(not username_data.strip()) or bool(not password_data.strip()):
        messagebox.showinfo("Error", "Please fill all fields")
    else:
        key, encrypted_password = encrypt_password(password_data)
        data = {website_data.lower(): {"username": username_data, "key": key, "password": encrypted_password}}
        try:
            with open("data.json", "r") as f:
                existing_data = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            with open("data.json", "w") as f:
                json.dump(data, f, indent=4)
        else:
            existing_data.update(data)
            with open("data.json", "w") as f:
                json.dump(existing_data, f, indent=4)
        finally:
            websiteEntry.delete(0, END)
            passwordEntry.delete(0, END)


# --------------------------- SEARCH PASSWORD ---------------------------#


def search_password():
    website_data = websiteEntry.get()

    try:
        with open("data.json", "r") as f:
            existing_data = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        messagebox.showinfo("Error", "No File Found")
    else:
        specific_data = existing_data.get(website_data.lower(), None)
        if specific_data is not None:
            password_retrieved = decrypt_password(specific_data.get("key"), specific_data.get("password"))

            messagebox.showinfo(f"{website_data}", f"Email: {specific_data.get("username")}\n Password: {password_retrieved}")
        else:
            messagebox.showinfo("Error", "No password found")


# ---------------------------- UI SETUP ------------------------------- #


window = Tk()
window.title("Password Manager")
window.config(padx=50, pady=50)

canvas = Canvas(width=200, height=200)
image = PhotoImage(file='logo.png')
canvas.create_image(100, 100, image=image)
canvas.grid(column=1, row=0)

# Labels
website = Label(text="Website:", )
website.grid(column=0, row=1)

username = Label(text="Email/Username:")
username.grid(column=0, row=2)

password = Label(text="Password:")
password.grid(column=0, row=3)

# Entries
websiteEntry = Entry(width=35)
websiteEntry.grid(column=1, row=1, columnspan=2, sticky="w")
websiteEntry.focus()

emailEntry = Entry(width=35)
emailEntry.grid(column=1, row=2, columnspan=3, sticky="w")
emailEntry.insert(0, "yadavrajesh5612@gmail.com")

passwordEntry = Entry(width=35)
passwordEntry.grid(column=1, row=3, sticky="w")

# Buttons
# Search button
search_button = Button(text="Search", width=14, command=search_password)
search_button.grid(column=2, row=1)

generateButton = Button(text="Generate Password", width=14, command=generate_password)
generateButton.grid(column=2, row=3)

addButton = Button(text="Add", width=45, command=save_data)
addButton.grid(column=1, row=4, columnspan=2)

window.mainloop()
