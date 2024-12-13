txt = input("enter a word for palindrom check: ")
txt_len = len(txt)
mid = txt_len // 2

if txt_len % 2 == 0:
    print(txt[:mid] == txt[mid:][::-1])
else:
    print(txt[:mid] == txt[mid + 1:][::-1])    
