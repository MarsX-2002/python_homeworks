num1 = int(input("enter 1st number: "))
num2 = int(input("enter 2nd number: "))
num3 = int(input("enter 3rd number: "))

check = num1 != num2 and num1 != num3 and num2 != num3

print(f"{'all numbers different' if check else 'some numbers similar'}")
