INSTALLATION:

$pip install passfactory

USAGE:

import src.passfactory as pf

root = pf.Password(2, "") # Security level: 2, Forbidden characters: no forbidden characters
root2 = pf.Password(1, "#45f") # Security level: 1, Forbidden characters: "#", "4", "5" and "f"

password = root.generate()
password2 = root2.generate()

root.copy() # Copies the current password to paperclip

root.save("mypasswords.txt") # Save the current password in a file

chars, nums, special_chars = root.stats() # Get the number of characters, numbers and special characters present
                                          # in the current password

def getSavestPass(): # Get the savest password (one which fulfills some given parameters for security such as length, variety of data types etc.)
    global root
    while not root.test():
        new_pass = root.generate()
    return new_pass

remainant = root - root2 # Get the characters 2 or more passwords don't have in common