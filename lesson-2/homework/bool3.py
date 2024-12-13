num = int(input("enter a number: "))

check_even = num % 2 == 0
check_positive = num > 0

print(f"{num} is {'positive' if check_positive else 'negative'} and {'even' if check_even else 'odd'}")