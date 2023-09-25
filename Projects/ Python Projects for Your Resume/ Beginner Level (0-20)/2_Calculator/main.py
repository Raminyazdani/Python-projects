
# Function to perform if the input is a number
def is_number(func):
    def wrapper(*args,**kwargs):
        temp = []
        for arg in args:
            try:
                temp.append(int(arg))
            except:
                raise ValueError("Input is not a number")
        if len(temp)<len(func.__code__.co_varnames):
            raise ValueError("Not enough inputs")
        return func(*temp)
    return wrapper


# Function to perform addition
@is_number
def add(x, y):
    return x + y

# Function to perform subtraction
@is_number
def subtract(x, y):
    return x - y

# Function to perform multiplication
@is_number
def multiply(x, y):
    return x * y

# Function to perform division
@is_number
def divide(x, y):
    if y == 0:
        raise ValueError("Cannot divide by zero")
    return x / y

def get_menu():
    menu = {}
    items = ["add","subtract","multiply","divide","exit"]
    for i in range(len(items)):
        menu[i+1] = (items[i],eval(items[i]))

    return menu

if __name__ == '__main__':
    menu = get_menu()
    while True:
        [print(f"{key}. {value[0]}") for key,value in menu.items()]
        choice = input("Enter your choice: ")
        try:
            int(choice)
        except:
            print("Invalid choice")
            continue
        if int(choice) == len(menu):
            break
        elif int(choice) in menu.keys():
            x = input("Enter first number: ")
            y = input("Enter second number: ")
            try:
                print(menu[int(choice)][1](x,y))
            except ValueError as e:
                print(e)
        else:
            print("Invalid choice")
            continue
    print("Thank you for using the calculator")


