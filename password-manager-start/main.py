from tkinter import *
from tkinter import messagebox
import random
import pyperclip
import json


# ---------------------------- PASSWORD GENERATOR ------------------------------- #
def generate_password():

    password_input.delete(0, END)

    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
               'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P',
               'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    nr_letters = random.randint(8, 10)
    nr_symbols = random.randint(2, 4)
    nr_numbers = random.randint(2, 4)

    password_list = [random.choice(letters) for _ in range(nr_letters)]
    password_list += [random.choice(symbols) for _ in range(nr_symbols)]
    password_list += [random.choice(numbers) for _ in range(nr_numbers)]

    random.shuffle(password_list)

    password = "".join(password_list)

    password_input.insert(0, f"{password}")
    pyperclip.copy(password)


# --------------------------- SEARCH FUNCTION ------------------------------ #
def find_password():

    website = website_input.get()
    try:
        with open("data.json") as data_file:
            data = json.load(data_file)
    except FileNotFoundError:
        messagebox.showerror(title="Error", message="No data file found.")
    else:
        if website in data:
            email = data[website]["email"]
            password = data[website]["password"]
            messagebox.showinfo(title=website, message=f"Email: {email}\nPassword: {password}")
        else:
            messagebox.showerror(title="Error", message=f"No details for {website} exists.")


# ---------------------------- SAVE PASSWORD ------------------------------- #
def save():

    website = website_input.get()
    email = email_input.get()
    password = password_input.get()
    new_data = {
        website: {
            "email": email,
            "password": password,
        }
    }

    if len(website) == 0 or len(password) == 0:
        messagebox.showerror(title="Error", message="Please don't leave any fields empty!")

    else:
        is_ok = messagebox.askokcancel(title=website, message=f"These are the details entered:\n Email: {email}\n "
                                                              f"Password: {password}\n Is this okay?")

        if is_ok:
            try:
                with open("data.json", "r") as data_file:
                    data = json.load(data_file)
            except FileNotFoundError:
                with open("data.json", "w") as data_file:
                    json.dump(new_data, data_file, indent=4)
            else:
                data.update(new_data)
                with open("data.json", "w") as data_file:
                    json.dump(data, data_file, indent=4)
            finally:
                website_input.delete(0, END)
                password_input.delete(0, END)


# ---------------------------- UI SETUP ------------------------------- #
window = Tk()
window.title("Password Manager")
window.config(padx=50, pady=50, bg="white")

canvas = Canvas(width=200, height=200, bg="white", highlightthickness=0)
logo_img = PhotoImage(file="logo.png")
canvas.create_image(100, 100, image=logo_img)
canvas.grid(column=1, row=0)

website_label = Label(text="Website:", bg="white", highlightthickness=0)
website_label.grid(column=0, row=1)

username_label = Label(text="Email/Username:", bg="white", highlightthickness=0)
username_label.grid(column=0, row=2)

password_label = Label(text="Password:", bg="white", highlightthickness=0)
password_label.grid(column=0, row=3)

website_input = Entry(width=35)
website_input.grid(column=1, row=1, sticky="EW")
website_input.focus()

email_input = Entry(width=35)
email_input.grid(column=1, row=2, columnspan=2, sticky="EW")
email_input.insert(0, "email@gmail.com")

password_input = Entry(width=21)
password_input.grid(column=1, row=3, columnspan=1, sticky="EW")

generate_pw_button = Button(text="Generate Password", bg="White", width=14, command=generate_password)
generate_pw_button.grid(column=2, row=3, sticky="EW")

add_button = Button(text="Add", bg="White", width=43, command=save)
add_button.grid(column=1, row=4, columnspan=2)

search_button = Button(text="Search", bg="White", width=14, command=find_password)
search_button.grid(column=2, row=1, sticky="EW")

window.mainloop()
