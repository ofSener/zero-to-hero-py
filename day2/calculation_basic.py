#this project is about calculation of two numbers.
#first i need a loop to ask user to enter two numbers.
#then ineed to ask user to enter the operation.
#then i need to calculate the result of the operation.
#then i need to print the result.
#then i need to ask user if they want to continue.


print("Welcome to the calculation program!")

token =''

while token != 'q':
    number1 = int(input("Enter the first number: "))
    number2 = int(input("Enter the second number: "))
    operation = input("Enter the operation: ")
    if operation == '+':
        print(number1 + number2)
    elif operation == '-':
        print(number1 - number2)
    elif operation == '*':
        print(number1 * number2)
    elif operation == '/':
        print(number1 / number2)
    else:
        print("Invalid operation")
    token = input("press q to quit or press any key to continue")
