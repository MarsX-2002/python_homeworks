txt = input("enter string: ").strip().lower().replace(' ', '')
vowels = ['a', 'e', 'i', 'o', 'u']

count_vowels = len([char for char in txt if char in vowels])
count_consonants = len([char for char in txt if char not in vowels])

print(f"vowels: {count_vowels}\nconsonants: {count_consonants}")