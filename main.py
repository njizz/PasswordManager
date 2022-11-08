from tkinter import *
from tkinter import messagebox
from random import choice, randint, shuffle
from pyperclip import copy
import json

FONT = ("Arial", 10)


# ---------------------------- PASSWORD GENERATOR ------------------------------- #
def gen_pwd():
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    password_list = [choice(letters) for _ in range(randint(8, 10))]
    password_list += [choice(symbols) for _ in range(randint(2, 4))]
    password_list += [choice(numbers) for _ in range(randint(2, 4))]

    shuffle(password_list)

    password = "".join(password_list)

    pwd_entry.delete(0, END)
    pwd_entry.insert(0, password)
    copy(password)


# ---------------------------- SAVE PASSWORD ------------------------------- #
def save_pwd():

    website = website_entry.get()
    email = email_entry.get()
    pwd = pwd_entry.get()
    new_data = {
        website: {
            "email": email,
            "password": pwd
        }
    }

    if len(website) == 0 or len(pwd) == 0:
        messagebox.showinfo(title="Oops", message="Please make sure you haven't left any fields empty")
    else:
        try:
            with open("data.json", "r") as data_file:
                # Read old data
                data = json.load(data_file)
        except FileNotFoundError:
            with open("data.json", "w") as data_file:
                # Save updated data
                json.dump(new_data, data_file, indent=4)
        else:
            # Update old data with new data
            data.update(new_data)
            with open("data.json", "w") as data_file:
                # Save updated data
                json.dump(data, data_file, indent=4)
        finally:
            website_entry.delete(0, END)
            pwd_entry.delete(0, END)


# ---------------------------- PASSWORD SEARCH ------------------------------- #
def pwd_search():
    website = website_entry.get()
    if len(website) == 0:
        messagebox.showinfo(title="Oops", message="Please enter a website.")
    else:
        try:
            with open("data.json", "r") as data_file:
                data = json.load(data_file)
        except FileNotFoundError:
            messagebox.showinfo(title="No password found", message="You have not saved any passwords.")
        else:
            if website in data:
                pwd_entry.insert(0, data[website]["password"])
            else:
                messagebox.showinfo(title="No password found",
                                    message=f"There is no password saved for {website}.")


# ---------------------------- UI SETUP ------------------------------- #
window = Tk()
window.title("Password Manager")
window.config(padx=50, pady=50)

# Logo
canvas = Canvas(height=200, width=200)
logo_img = PhotoImage(file="logo.png")
canvas.create_image(100, 100, image=logo_img)
canvas.grid(row=0, column=1)

# Website Label
website_label = Label(text="Website:", font=FONT)
website_label.grid(column=0, row=1)

# Website Entry
website_entry = Entry(width=34)
website_entry.grid(column=1, row=1)

# Website Search
search_button = Button(text="Search", width=14, command=pwd_search)
search_button.grid(column=2, row=1)

# Email/Username Label
email_label = Label(text="Email/Username:", font=FONT)
email_label.grid(column=0, row=2)

# Email/Username Entry
email_entry = Entry(width=52)
email_entry.grid(column=1, row=2, columnspan=2)
email_entry.insert(0, "njizzard@gmail.com")

# Password label
pwd_label = Label(text="Password:", font=FONT)
pwd_label.grid(column=0, row=3)

# Password Entry
pwd_entry = Entry(width=34)
pwd_entry.grid(column=1, row=3)

# Generate Password Button
gen_pwd_button = Button(text="Generate Password", command=gen_pwd)
gen_pwd_button.grid(column=2, row=3)

# Add Button
add_button = Button(text="Add", width=44, command=save_pwd)
add_button.grid(column=1, row=4, columnspan=2)


window.mainloop()
