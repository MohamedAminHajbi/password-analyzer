import string
import getpass
import requests
import random
import math
import tkinter as tk
import hashlib
from tkinter import ttk

def check_pwned_api(password):
    # Hash the password using SHA-1
    hashed_password = hashlib.sha1(password.encode()).hexdigest().upper()
    hash_prefix, hash_suffix = hashed_password[:5], hashed_password[5:]

    # Make a request to the HIBP API
    response = requests.get(f"https://api.pwnedpasswords.com/range/{hash_prefix}")

    if response.status_code == 200:
        # Check if the password hash suffix is present in the response
        pwned_hashes = [line.split(':')[0] for line in response.text.splitlines()]
        return hash_suffix in pwned_hashes

    return False


def generate_suggested_password():
    lowercase_chars = string.ascii_lowercase
    uppercase_chars = string.ascii_uppercase
    digits_chars = string.digits
    special_chars = string.punctuation

    suggested_password = (
        random.choice(lowercase_chars) +
        random.choice(uppercase_chars) +
        random.choice(digits_chars) +
        random.choice(special_chars) +
        ''.join(random.choice(string.ascii_letters + string.digits + string.punctuation) for _ in range(8))
    )

    return suggested_password

def calculate_entropy(password):
    possible_characters = 0
    for char_set in [string.ascii_lowercase, string.ascii_uppercase, string.digits, string.punctuation]:
        possible_characters += len(set(password) & set(char_set))
    entropy = math.log2(possible_characters) * len(password)
    return entropy

def calculate_crack_time(entropy):
    seconds_to_crack = 2 ** entropy
    minutes_to_crack = seconds_to_crack / 60
    hours_to_crack = minutes_to_crack / 60
    days_to_crack = hours_to_crack / 24
    years_to_crack = days_to_crack / 365

    remaining_seconds = seconds_to_crack % 60
    remaining_minutes = minutes_to_crack % 60
    remaining_hours = hours_to_crack % 24

    return (
        f"{int(years_to_crack)} years, "
        f"{int(days_to_crack % 365)} days, "
        f"{int(remaining_hours)} hours, "
        f"{int(remaining_minutes)} minutes, "
        f"{int(remaining_seconds)} seconds"
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
    
    if check_pwned_api(password):
        result_label.config(text=f"Warning: Password '{password}' has been exposed in previous data breaches!", fg="red")
    else:
        result_label.config(text="Success: The password is secure.", fg="green")
    result_text.set(f"Password strength: {remarks}\nHint: {remarks}")

    result_text.set(result_text.get() +
                   f"\nYour password has:\n"
                   f"{lower_count} Lowercase characters\n"
                   f"{upper_count} Uppercase characters\n"
                   f"{num_count} Numeric characters\n"
                   f"{wspace_count} Whitespace characters\n"
                   f"{special_count} Special characters")

    entropy = calculate_entropy(password)
    crack_time = calculate_crack_time(entropy)
    result_text.set(result_text.get() +
                   f"\nPassword entropy: {entropy:.2f}\n"
                   f"Estimated time to crack: {crack_time}")

    suggested_button.grid(row=2, column=0, columnspan=3, sticky=tk.W)
    if strength >= 4:
        suggested_button.grid_forget()

def on_suggested_button():
    suggested_password = generate_suggested_password()
    result_text.set(result_text.get() + f"\nSuggested password: {suggested_password}")

def on_submit():
    check_pwd()

root = tk.Tk()
root.title("Password Strength Checker")
root.geometry("750x500")

style = ttk.Style()

frame = ttk.Frame(root, padding="10")  # Increase the padding for the frame
frame.grid(column=0, row=0, sticky=(tk.W, tk.E, tk.N, tk.S))

label_password = ttk.Label(frame, text="Enter Password:", font=("Roboto", 20, "bold"))
label_password.grid(column=0, row=0, sticky=tk.W, padx=20)

entry_password = ttk.Entry(frame, show="*")
entry_password.grid(column=1, row=0, sticky=(tk.W, tk.E))

style.configure("Custom.TButton", font=("Helvetica", 12, "bold"), foreground="white", background="#45b592", padding=10)

button_submit = ttk.Button(frame, text="Check Password", command=on_submit, style="Custom.TButton")  # Use the default style
button_submit.grid(column=2, row=0, sticky=tk.W, padx=20)


result_text = tk.StringVar()
label_result = ttk.Label(frame, textvariable=result_text, wraplength=400, justify=tk.LEFT)
label_result.grid(column=0, row=1, columnspan=3, sticky=(tk.W, tk.E))

result_label = tk.Label(root, text="")
result_label.grid(row=3, column=0, columnspan=3, sticky=tk.W, pady=10)

suggested_button = ttk.Button(frame, text="Generate Suggested Password", command=on_suggested_button)

root.mainloop()
