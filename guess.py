import random

def guess(x):
    random_number = random.randint(1,x)
    guess = 0
    while guess!= random_number:
        guess = int(input(f"Guess the number between 1 and {x}: "))
        if guess < random_number:
            print("Too low. Try again")
        elif guess > random_number:
            print("Too high. Try again")
    
    print("Congratulations you've guessed it right")
guess(20)
