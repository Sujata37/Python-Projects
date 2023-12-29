import random

possible_actions = ["Rock", "Paper", "Scissor"]
user_actions = input("Enter you choice (Rock,Paper or Scissor): ")
computer_actions = random.choice (possible_actions)

if user_actions == computer_actions:
    print("Both of you chose {user_actions}. It's a tie.")
elif user_actions== "Rock":
    if computer_actions == "Paper":
        print("You chose Rock, Computer chose Paper.\n Computer Won")
    else:
        print("Your Rock smacked Scissor. you won.")
elif user_actions == "Paper":
    if computer_actions == "Scissor":
        print("You chose Paper, Computer chose Scissor. Computer won.")
    else:
        print("Your Paper covers the rock. You won.")
elif user_actions == "Scissor":
    if computer_actions == "Rock":
        print("Rock smashed your scissor. Computer won.")
    else:
        print("Your scissor cut the paper. You won")
else:
    print("Invalid Command")
