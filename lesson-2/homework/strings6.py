txt1 = input("enter 1st string: ").strip()
txt2 = input("enter 2ns string: ").strip()

check = txt1 in txt2 or txt2 in txt1
print(f"string {'' if check else "NOT "}contains another")