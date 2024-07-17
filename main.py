import string
import zipfile
import sys
import time
import os

from threading import Thread

from getpass import getpass

class ThreadWithReturnValue(Thread):

    def __init__(self, group=None, target=None, name=None,
                 args=(), kwargs={}, Verbose=None):
        Thread.__init__(self, group, target, name, args, kwargs)
        self._return = None

    def run(self):
        if self._target is not None:
            self._return = self._target(*self._args,
                                                **self._kwargs)
    def join(self, *args):
        Thread.join(self, *args)
        return self._return

def animated_loading():
    chars = r'/—\|'
    for char in chars:
        sys.stdout.write('\r'+'searching...'+char)
        time.sleep(.1)
        sys.stdout.flush()

def get_folder_name(character):
    if character.isdigit():
        return character
    elif character in string.ascii_letters:
        return character.lower()
    elif character == '$':
        return 'DollarSymbol'
    elif character.isalnum():
        return 'Symbol'
    else:
        return 'Others'

def check_string_in_zip(zip_path, search_string):
    if not search_string:
        print("Search string is empty.")
        return False

    folder_to_check = get_folder_name(search_string[0])

    try:
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            for file_name in zip_ref.namelist():
                # Check if the file is in the correct folder
                if file_name.lower().startswith(folder_to_check):
                    # Extract just the filename from the full path
                    filename = os.path.basename(file_name)

                    # Check if the file is a text file
                    if filename.lower().endswith('.txt'):
                        with zip_ref.open(file_name) as file:
                            try:
                                content = file.read().decode('utf-8')
                                # Check if the search string is in the content
                                if search_string in content:
                                    # print(f"The string '{search_string}' was found in the file '{filename}' in folder '{folder_to_check}'.")
                                    return True
                            except UnicodeDecodeError:
                                # Skip files that cannot be decoded as text
                                continue
        return False
    except Exception as e:
        print(f"An error occurred while processing {zip_path}: {e}")
        return False


def main():
    print("Password checker!")
    print("Please Provide your password it will be checked against RockMe2024! (dont worry localy)")
    search_string = getpass()
    large_zip_path = 'data/archive.zip'

    the_process = ThreadWithReturnValue(name='password_search',target=check_string_in_zip, args=(large_zip_path, search_string))

    the_process.start()
    while the_process.is_alive():
        animated_loading()

    if the_process.join():
        print('\r'+"The password was found in the zip files.")
        print("OH NO :( your password was in the leak! PLEASE CHANGE IT ASAP!!!")
    else:
        print('\r'+"The password was not found in the zip files.")
        print("All fine! :)")


if __name__ == "__main__":
    main()