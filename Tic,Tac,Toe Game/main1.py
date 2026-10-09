board = [" " for i in range(9)]

def display():
    print()
    for i in range(0, 9, 3):
        print(" " + " | ".join(board[i:i+3]))
        if i < 6:
            print("---+---+---")
    print()

def check_winner():
    wins = [
        (0, 1, 2), (3, 4, 5), (6, 7, 8),
        (0, 3, 6), (1, 4, 7), (2, 5, 8),
        (0, 4, 8), (2, 4, 6)
    ]

    for a, b, c in wins:
        if board[a] == board[b] == board[c] != " ":
            return True
    return False

player = "X"

while True:
    display()
    print("Player", player)

    try:
        move = int(input("Enter position (1-9): ")) - 1
    except ValueError:
        print("Please enter a number!")
        continue

    if move < 0 or move > 8 or board[move] != " ":
        print("Invalid move! Try again.")
        continue

    board[move] = player

    if check_winner():
        display()
        print("Player", player, "wins! 🎉")
        break

    if " " not in board:
        display()
        print("It's a draw!")
        break

    player = "O" if player == "X" else "X"