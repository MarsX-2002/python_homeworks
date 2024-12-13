num = int(input("enter a number: "))

check3 = num % 3
check5 = num % 5

print(f"{num} is divisible by {'3' if not check3 else ''} {'and' if not check3 and not check5 else ''} {'5' if not check5 else ''}")