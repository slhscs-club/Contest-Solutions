def create_file(name):
    with open(f"{name}.py", "w") as f:
        pass

def format_num(num):
    if num < 10: return "0" + str(num)
    else: return str(num)

def create_name(num):
    return "problem" + str(num)

if __name__ == "__main__":
    for i in range(32):
        create_file(create_name(format_num(i)))