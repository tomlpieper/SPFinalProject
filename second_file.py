print("Welcome to the second new created python file")
print("I will be your host today")



def addOrMultiply(bool, x, y):
    if bool:
        print("Multiplied:")
        print(x*y)
    else:
        print("Added")
        print(x+y)



addOrMultiply(True, 10, 10)
addOrMultiply(False, 10, 10)
