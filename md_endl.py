path = input("> ")
with open(path, "r") as f:
    content = f.read().splitlines()
with open(path, "w") as f:
    f.write("   \n".join(content))