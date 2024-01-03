print("Calculator")

num1 = int(input("Enter the first number: "))
num2 = int(input("Enter the second number: "))
operation = input("Enter the operation you want to perform: ")
if operation == "add":
    result = num1+num2
    print(result)
elif operation == "difference":
    result = num1 - num2
    print(result)
elif operation == "division":
    result =  num1/num2
    print("result")
elif operation == "multiply":
    result = num1*num2
    print("result")
else:
    print("invalid operation")