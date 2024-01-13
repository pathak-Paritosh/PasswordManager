from tkinter import *
from tkinter import messagebox
import random
import pyperclip
import json

# ---------------------------- PASSWORD GENERATOR ------------------------------- #
def generate_password():
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    nr_letters = random.randint(8, 10)
    nr_symbols = random.randint(2, 4)
    nr_numbers = random.randint(2, 4)

    password_list = []

    for char in range(nr_letters):
        password_list.append(random.choice(letters))

    for char in range(nr_symbols):
        password_list += random.choice(symbols)

    for char in range(nr_numbers):
        password_list += random.choice(numbers)

    random.shuffle(password_list)
    password = "".join(password_list)
    password_entry.insert(0, password)
    pyperclip.copy(password)

    


# ---------------------------- SAVE PASSWORD ------------------------------- #

def save_password():
    website = website_entry.get()
    email = email_entry.get()
    password = password_entry.get()

    new_data = {
        website: {
            "email" : email,
            "password" : password,
        }
    }

    if len(website)==0 or len(password)==0 or len(email)==0:
        messagebox.showinfo(title="oops!", message="Please do not leave any field empty.")
    else:
        try:
            with open("data.json", "r") as file:
                data = json.load(file)
        except FileNotFoundError:
            with open("data.json", "w") as file:
                json.dump(new_data, file, indent=4)
        else:
            data.update(new_data)
            with open("data.json", "w") as file:
                json.dump(data, file, indent=4)

        website_entry.delete(0, END)
        password_entry.delete(0, END)
        email_entry.delete(0, END)
        website_entry.focus()




# -----------------------------  FIND PASSWORD  ----------------------------#
def  find_password():
    try:
        file = open("data.json", "r")
    except FileNotFoundError:
        messagebox.showinfo(title="error", message="Data file not found")
    else:
        data = json.load(file)
        website_to_search = website_entry.get()
        info = {}

        for (k, v) in data.items():
            if k.upper() == website_to_search.upper():
                info = v

        if bool(info) == False:
            messagebox.showinfo(title="error", message=f"No website having name '{website_to_search}' found")
        else:
            messagebox.showinfo(title=website_to_search, message=f"Email/Username: {info['email']}\nPassword: {info['password']}")
            pyperclip.copy(info['password'])
        file.close()
        



# ---------------------------- UI SETUP ------------------------------- #
window = Tk()

window.title("Password Manager")

window.config(padx=50, pady=50)

canvas = Canvas(width=200, height=200)
logo_image = PhotoImage(file="logo.png")
canvas.create_image(100, 100, image=logo_image)
canvas.grid(column=1, row=0)

website_label = Label(text="Website:")
website_label.grid(column=0, row=1)
website_label.config(pady=5)

email_label = Label(text="Email/Username:")
email_label.grid(column=0, row=2)
email_label.config(pady=5)

password_label = Label(text="Password:")
password_label.grid(column=0, row=3)
password_label.config(pady=5)

website_entry = Entry(width=30)
website_entry.grid(column=1, row=1, sticky="W")
website_entry.focus()

email_entry = Entry(width=35)
email_entry.grid(column=1, row=2, columnspan=2, sticky="EW")

password_entry = Entry(width=30)
password_entry.grid(column=1, row=3, sticky="W")

search_btn = Button(text="Search", command=find_password)
search_btn.grid(column=2, row=1, sticky="EW")

generate_password_btn = Button(text="Generate Password", command=generate_password)
generate_password_btn.grid(column=2, row=3, sticky="EW")

add_btn = Button(text="Add", width=36, command=save_password)
add_btn.grid(column=1, row=4, columnspan=2, sticky="EW")

window.mainloop()