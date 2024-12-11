km = float(input("enter km: "))
meters = int(km * 1000)
centimeters = int((km * 1000 - meters) * 100)  
print(f"{km} = {meters} meters and {centimeters} centimeters")