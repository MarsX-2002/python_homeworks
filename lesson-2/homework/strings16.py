txt = input("enter a string: ")
character = input("enter a character: ")

check = txt.replace(character, '')

print(f"removed `{character}`: {check}")
