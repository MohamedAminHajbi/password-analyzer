import string
import getpass
import random
import math
import tkinter as tk
from tkinter import ttk

def generate_suggested_password():
    # Define character sets for password generation
    lowercase_chars = string.ascii_lowercase
    uppercase_chars = string.ascii_uppercase
    digits_chars = string.digits
    special_chars = string.punctuation

    # Generate a random password with a mix of characters
    suggested_password = (
        random.choice(lowercase_chars) +
        random.choice(uppercase_chars) +
        random.choice(digits_chars) +
        random.choice(special_chars) +
        ''.join(random.choice(string.ascii_letters + string.digits + string.punctuation) for _ in range(8))
    )

    return suggested_password

def calculate_entropy(password):
    # Calculate entropy based on the number of possible characters and the length of the password
    possible_characters = 0
    for char_set in [string.ascii_lowercase, string.ascii_uppercase, string.digits, string.punctuation]:
        possible_characters += len(set(password) & set(char_set))
    entropy = math.log2(possible_characters) * len(password)
    return entropy

def calculate_crack_time(entropy):
    # Calculate an estimate of the time to crack based on the password entropy
    # This is a rough estimation and can vary based on attacker's methods and resources
    seconds_to_crack = 2 ** entropy
    days_to_crack = seconds_to_crack / (24 * 3600)
    hours_to_crack = (seconds_to_crack % (24 * 3600)) / 3600
    minutes_to_crack = (seconds_to_crack % 3600) / 60
    seconds_remainder = seconds_to_crack % 60

    return (
        f"{int(days_to_crack)} days, "
        f"{int(hours_to_crack)} hours, "
        f"{int(minutes_to_crack)} minutes, "
        f"{int(seconds_remainder)} seconds"
    )

def check_pwd():
    password = entry_password.get()
    strength = 0
    remarks = ''
    lower_count = upper_count = num_count = wspace_count = special_count = 0

    for char in list(password):
        if char in string.ascii_lowercase:
            lower_count += 1
        elif char in string.ascii_uppercase:
            upper_count += 1
        elif char in string.digits:
            num_count += 1
        elif char == ' ':
            wspace_count += 1
        else:
            special_count += 1
    if lower_count >= 1:
        strength += 1
    if upper_count >= 1:
        strength += 1
    if num_count >= 1:
        strength += 1
    if special_count >= 1:
        strength += 1
    
    if strength == 1:
        remarks = "Very Bad Password !! Change ASAP"
    elif strength == 2:
        remarks = "Not A Good Password !! Change ASAP"
    elif strength == 3:
        remarks = "It's A Weak Password !! Change ASAP"
    elif strength == 4:
        remarks = "It's A Hard Password, but can be better"
    elif strength == 5:
        remarks = "Very Strong Password"

    result_text.set(f"Password strength: {remarks}\nHint: {remarks}")

    # Display password statistics
    result_text.set(result_text.get() +
                   f"\nYour password has:\n"
                   f"{lower_count} Lowercase characters\n"
                   f"{upper_count} Uppercase characters\n"
                   f"{num_count} Numeric characters\n"
                   f"{wspace_count} Whitespace characters\n"
                   f"{special_count} Special characters")

    # Calculate and display estimated time to crack
    entropy = calculate_entropy(password)
    crack_time = calculate_crack_time(entropy)
    result_text.set(result_text.get() +
                   f"\nPassword entropy: {entropy:.2f}\n"
                   f"Estimated time to crack: {crack_time}")

    # Show or hide the "Generate Suggested Password" button based on password strength
    suggested_button.grid(row=2, column=0, columnspan=3, sticky=tk.W)
    if strength >= 4:
        suggested_button.grid_forget()

def on_suggested_button():
    suggested_password = generate_suggested_password()
    result_text.set(result_text.get() + f"\nSuggested password: {suggested_password}")

def on_submit():
    check_pwd()

# GUI setup
root = tk.Tk()
root.title("Password Strength Checker")
root.geometry("500x300")  # Set the initial window size

frame = ttk.Frame(root, padding="10")
frame.grid(column=0, row=0, sticky=(tk.W, tk.E, tk.N, tk.S))

label_password = ttk.Label(frame, text="Enter Password:")
label_password.grid(column=0, row=0, sticky=tk.W)

entry_password = ttk.Entry(frame, show="*")
entry_password.grid(column=1, row=0, sticky=(tk.W, tk.E))

button_submit = ttk.Button(frame, text="Check Password", command=on_submit)
button_submit.grid(column=2, row=0, sticky=tk.W)

result_text = tk.StringVar()
label_result = ttk.Label(frame, textvariable=result_text, wraplength=400, justify=tk.LEFT)
label_result.grid(column=0, row=1, columnspan=3, sticky=(tk.W, tk.E))

suggested_button = ttk.Button(frame, text="Generate Suggested Password", command=on_suggested_button)

root.mainloop()
