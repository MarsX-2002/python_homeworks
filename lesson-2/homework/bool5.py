txt1 = input("enter 1st string: ")
txt2 = input("enter 2nd string: ")

check = len(txt1) == len(txt2)

print(f"Strings have {'' if check else 'NOT'}same length")