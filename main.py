from tkinter import *
from tkinter import messagebox
from string import ascii_letters, digits
from random import choice, sample, randint
import pyperclip
import json

PASSWORD_CHARS = (list(ascii_letters), list(digits), ["!", "#", "$", "*", "%", "&", "+", "(", ")"])


# ---------------------------- PASSWORD GENERATOR ------------------------------- #
def generate_password():
    passw_entry.delete(0, END)
    generated = []
    for index, num in enumerate([randint(8, 10), randint(2, 4), randint(2, 4)]):
        for _ in range(num):
            generated.append(choice(PASSWORD_CHARS[index]))
    passw_entry.insert(END, string="".join(sample(generated, len(generated))))


# ---------------------------- SAVE PASSWORD ------------------------------- #
def save_info():

    website = webs_entry.get()
    username = user_entry.get()
    password = passw_entry.get()

    new_data = {
        website: {
            "Email/Username": username,
            "Password": password,
        }
    }

    if "" in [website, username, password]:
        is_retry = messagebox.askretrycancel(title="Whoops!", message="Fields were left open. Try again.")
        if is_retry:
            return
        else:
            reset_ui()
            return

    pyperclip.copy(password)

    is_ok = messagebox.askokcancel(title=webs_entry.get(), message=f"These are the details you have entered:\n"
                                                                   f"\nEmail: {username}\n"
                                                                   f"Password: {password}\n"
                                                                   f"\nIs it okay to save?")
    if is_ok:
        try:
            with open(file="data.json", mode="r") as data_file:
                data = json.load(data_file)
                data.update(new_data)
            reset_ui()
        except FileNotFoundError:
            with open(file="data.json", mode="w") as data_file:
                json.dump(new_data, data_file, indent=4)
        else:
            with open(file="data.json", mode="w") as data_file:
                json.dump(data, data_file, indent=4)
            reset_ui()
    else:
        return


# ---------------------------- SEARCH DETAILS ------------------------------- #
def search_details():
    website = webs_entry.get()
    try:
        with open(file="data.json", mode="r") as data_file:
            data = json.load(data_file)
        retrieved_data = [data[key] for key in data.keys() if key == website][0]
    except FileNotFoundError:
        messagebox.showerror(title="No entries made.",
                             message="We could not find any website names matching your entry.")
    except IndexError:
        messagebox.showerror(title="No entries made.",
                             message="We could not find any website names matching your entry.")
    else:
        pyperclip.copy(retrieved_data['Password'])
        messagebox.showinfo(title=f"Details saved under {website}:",
                            message=f"Username/Email: {retrieved_data['Email/Username']}\n"
                                    f"Password: {retrieved_data['Password']}")


# ---------------------------- UI SETUP ------------------------------- #
def reset_ui():
    passw_entry.delete(0, END)
    webs_entry.delete(0, END)
    webs_entry.focus()


window = Tk()
window.title("MyPass: Password Manager")
window.config(width=300, height=300, padx=20, pady=20)

canvas = Canvas(width=200, height=200, highlightthickness=0)
logo = PhotoImage(file="logo.png")
canvas.create_image(100, 100, image=logo)
canvas.grid(column=1, row=0)

# Labels
website_text = Label(text="Website:", font=("Arial", 10, "bold"))
website_text.grid(column=0, row=1)

username_text = Label(text="Email/Username:", font=("Arial", 10, "bold"))
username_text.grid(column=0, row=2)

password_text = Label(text="Password:", font=("Arial", 10, "bold"))
password_text.grid(column=0, row=3)

# entries
webs_entry = Entry(width=25)
webs_entry.grid(column=1, row=1, padx=(38, 4.49))

user_entry = Entry(width=44)
user_entry.grid(column=1, row=2, columnspan=2)

passw_entry = Entry(width=25)
passw_entry.grid(column=1, row=3, padx=(38, 4.49))

# buttons
generate_passw = Button(text="Generate Password", highlightthickness=0, command=generate_password)
generate_passw.grid(column=2, row=3, padx=(0, 40))

search_login = Button(text="Search", highlightthickness=0, command=search_details, width=14)
search_login.grid(column=2, row=1, padx=(0, 40))

add_saved = Button(text="Add", width=37, command=save_info)
add_saved.grid(column=1, row=4, columnspan=2)

window.mainloop()
