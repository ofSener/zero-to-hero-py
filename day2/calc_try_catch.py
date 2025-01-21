def calc_try_catch(number1, number2, operation):
    if operation == '+':
        return number1 + number2
    elif operation == '-':
        return number1 - number2
    elif operation == '*':
        return number1 * number2
    elif operation == '/':
        return number1 / number2
    else:
        return "Invalid operation"

while True:
    user_input = input("Enter your operation (e.g., '5 + 3') or 'q' to quit: ")
    
    if user_input.lower() == 'q':
        break
    
    try:
        # Split the user input by spaces and parse the components
        parts = user_input.split()
        number1 = float(parts[0])  # First number
        operation = parts[1]       # Operation
        number2 = float(parts[2])  # Second number
        
        # Perform the calculation and print the result
        result = calc_try_catch(number1, number2, operation)
        print(result)
        
    except ValueError:
        print("Invalid input. Please make sure you enter two numbers and an operator.")
    except IndexError:
        print("Incomplete input. Please make sure you enter both numbers and an operator.")
    except ZeroDivisionError:
        print("Error: Division by zero is not allowed.")
