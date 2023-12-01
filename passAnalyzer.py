import string
import getpass
import random

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

def check_pwd():
    password = getpass.getpass("Enter Password: ")
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

    print('Your password has: ')
    print(f"{lower_count} Lowercase characters")
    print(f"{upper_count} Uppercase characters")
    print(f"{num_count} Numeric characters")
    print(f"{wspace_count} Whitespace characters")
    print(f"{special_count} Special characters")

    print(f"Password strength: {strength}")
    print(f"Hint: {remarks}")

    # Suggest a password if the entered password is not strong
    if strength < 4:
        suggested_password = generate_suggested_password()
        print(f"Suggested password: {suggested_password}")

def ask_pwd(another_pwd=False):
    valid = False
    if another_pwd:
        choice = input('Do you want to enter another pwd (y/n): ')
    else:
        choice = input('Do you want to check pwd strength (y/n): ')

    while not valid:
        if choice.lower() == 'y':
            return True
        elif choice.lower() == 'n':
            return False
        else:
            print('Invalid, Try Again')

if __name__ == '__main__':
    print("+++ welcome to PWD checker +++")
    ask_pw = ask_pwd()
    while ask_pw:
        check_pwd()
        ask_pw = ask_pwd(True)
