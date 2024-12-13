txt = input("enter string: ")

contains_digits = any([char.isdigit() for  char in txt])

print(f"is this string contain any digits? ``{contains_digits}``")