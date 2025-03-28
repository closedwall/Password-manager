from tkinter import *
from tkinter import messagebox
from random import randint, choice, randint, shuffle
import pyperclip
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


def save_to_file(data):
    with open('password.txt', 'a') as f:
        f.write(data + "\n")


def save_data():
    website_data = websiteEntry.get()
    username_data = emailEntry.get()
    password_data = passwordEntry.get()
    if bool(not website_data.strip()) or bool(not username_data.strip()) or bool(not password_data.strip()):
        messagebox.showinfo("Error", "Please fill all fields")
    else:
        is_ok = messagebox.askokcancel(title=website_data, message=f"These are the details entered:"
                                                                   f" \nEmail: {username_data}\nPassword:"
                                                                   f" {password_data} \n Is it ok to save?")
        if is_ok:
            data = f"{website_data} | {username_data} | {password_data}"
            save_to_file(data)
            print("Password saved")
            websiteEntry.delete(0, END)
            passwordEntry.delete(0, END)

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
websiteEntry.grid(column=1, row=1, columnspan=2)
websiteEntry.focus()

emailEntry = Entry(width=35)
emailEntry.grid(column=1, row=2, columnspan=2)
emailEntry.insert(0, "yadavrajesh5612@gmail.com")

passwordEntry = Entry(width=21)
passwordEntry.grid(column=1, row=3)

# Buttons
generateButton = Button(text="Generate Password", command=generate_password)
generateButton.grid(column=2, row=3)

addButton = Button(text="Add", width=36, command=save_data)
addButton.grid(column=1, row=4, columnspan=2)

window.mainloop()
