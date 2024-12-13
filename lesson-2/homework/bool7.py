num1 = int(input("enter 1st number: "))
num2 = int(input("enter 2nd number: "))

check = (num1 + num2) > 50

print(f"{num1} + {num2} {'> ' if check else '< '}50")
