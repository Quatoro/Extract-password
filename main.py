import re
import os
import tkinter as tk
from tkinter import filedialog

def extract_credentials(file_path) -> list:
    with open(file_path, 'r') as file:
        lines = file.readlines()
    
    credentials = []
    
    for line in lines:
        if 'PublicKeyToken=null' in line:
            # Extract password and username within the same line
            password_match = re.search(r'\.+(\w+)\.+', line)  # The password will be surrounded by periods (.)
            if password_match:
                password = password_match.group(1)
                
                # The password will be found on the same line but after the password minus 1 to get at least one period for the regex to find the user.
                post_password_content = line[password_match.end()-1:]
                
                username_match = re.search(r'\.+(\w+)\.+', post_password_content)  # The username will be surrounded by periods (.)
                if username_match:
                    username = username_match.group(1)
                    credentials.append((password, username))
    
    return credentials

def search_multiple_files(directory):
    credentials_with_files = []
    
    # Walk in all folders starting from root selected by user.
    for root, _, files in os.walk(directory):
        for filename in files:
            if filename.endswith(".data"):  # Password and user will be found in a file with the '.data' extension.
                file_path = os.path.join(root, filename)
                credentials = extract_credentials(file_path)
                for credential in credentials:
                    credentials_with_files.append((credential, file_path))  # Associate each credential with its file path
    
    return credentials_with_files

def choose_directory():
    root = tk.Tk()
    root.withdraw()  # Hide the main window
    return filedialog.askdirectory()  # Open the directory chooser dialog

# Choose directory containing the text files
directory = choose_directory()

if directory:
    # Search for credentials in all text files in the directory and subdirectories
    credentials_with_files = search_multiple_files(directory)
    with open('result.txt', 'w') as f:
        if credentials_with_files:
            # Print the extracted credentials along with their file paths
            for (password, username), file_path in credentials_with_files:
                f.write(f'\n##   Password: {password}\tUsername: {username}\tFound in file: {file_path}')
                print(f'\n##   Password: {password}\tUsername: {username}\tFound in file: {file_path}')
        else: 
            f.write(f'\n##   No credentials found in the selected directory. \n'
                f'##   Please select a directory containing text files with the .data extension.\n')
            print(f'\n##   No credentials found in the selected directory. \n'
                f'##   Please select a directory containing text files with the .data extension.\n')
else:
    print("No directory selected.")
