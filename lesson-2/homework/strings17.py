txt = input("enter a string: ")

vowels = ['a', 'e', 'i', 'o', 'u']

check = ''.join(['*' if char in vowels else char for char in txt])

print(f"vowels replaced with `*`: {check}")