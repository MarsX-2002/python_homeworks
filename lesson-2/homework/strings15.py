txt = input("enter a sentence: (World Health Organization)").split()

acronym = ''.join([word[0] for word in txt])

print(f"acronym: {acronym}")
