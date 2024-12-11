def default_input(prompt, default="Hello World!"):
    user_input = input(f"{prompt} (default: {default})")
    return user_input if user_input.strip() else default


txt = default_input("enter some string:")

print(f"txt_length: {len(txt)} \ntxt_lower: {txt.lower()} \ntxt_upper: {txt.upper()}")
