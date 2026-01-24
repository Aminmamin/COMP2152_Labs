# List of game choices
choices = ["Rock", "Paper", "Scissors"]

# Ask the player for their choice
player_choice = int(input("Enter your choice (1=Rock, 2=Paper, 3=Scissors): "))

# Make sure the player's choice is valid
if player_choice < 1 or player_choice > 3:
    print("Error: Choice must be between 1 and 3.")
else:
    # Ask for the computer's choice (simulated)
    computer_choice = int(input("Enter computer's choice (1-3): "))

    # Validate computer's choice
    if computer_choice < 1 or computer_choice > 3:
        print("Error: Choice must be between 1 and 3.")
    else:
        # Convert choices to list indexes
        player_index = player_choice - 1
        computer_index = computer_choice - 1

        # Show what each side picked
        print("You chose:", choices[player_index])
        print("Computer chose:", choices[computer_index])

        # Decide who wins
        if player_choice == computer_choice:
            print("It's a tie!")
        elif player_choice == 1 and computer_choice == 3:
            print("Rock beats Scissors - You win!")
        elif player_choice == 2 and computer_choice == 1:
            print("Paper beats Rock - You win!")
        elif player_choice == 3 and computer_choice == 2:
            print("Scissors beats Paper - You win!")
        else:
            print("You lose!")

        # Extra message if player didn't choose Rock
        if choices[player_index] != "Rock":
            print("You didn't pick the classic Rock...") 
