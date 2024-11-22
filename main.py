def display_board(board):
    print("\n")
    print(f" {board[0]} | {board[1]} | {board[2]} ")
    print("---|---|---")
    print(f" {board[3]} | {board[4]} | {board[5]} ")
    print("---|---|---")
    print(f" {board[6]} | {board[7]} | {board[8]} ")
    print("\n")

def get_win_combinations():
    win_combinations = [
        [0, 1, 2], [3, 4, 5], [6, 7, 8],
        [0, 3, 6], [1, 4, 7], [2, 5, 8],
        [0, 4, 8], [2, 4, 6]
    ]
    return win_combinations

def check_winner(board, player):
    for combo in get_win_combinations():
        if board[combo[0]] == board[combo[1]] == board[combo[2]] == player:
            return True
    return False

def check_draw(board):
    return all(cell != " " for cell in board)

def just_block_or_win(board):
    for i in range(len(board)):
        temp_board = board[:]
        if temp_board[i] == " ":
            temp_board[i] = "O"
            if check_winner(temp_board, "O"):
                return i

    for i in range(len(board)):
        temp_board = board[:]
        if temp_board[i] == " ":
            temp_board[i] = "X"
            if check_winner(temp_board, "X"):
                return i

def bot_move(board, last_player_move):
    corners = [0, 2, 6, 8]
    sides = [1, 3, 5, 7]
    center = 4
    total_moves = sum(1 for cell in board if cell != " ")

    if total_moves == 1:
        if last_player_move == center:
            for corner in corners:
                if board[corner] == " ":
                    return corner
        elif last_player_move in corners or last_player_move in sides:
            return center

    if total_moves == 3:
        move = just_block_or_win(board)
        if move is not None:
            return move

        if board[center] == "X":
            for side in sides:
                if board[side] == "X":
                    for corner in corners:
                        if board[corner] == " ":
                            return corner

        side_to_corner_intersection = {
            1: (8, 2),
            3: (2, 0),
            5: (6, 8),
            7: (0, 6)
        }
        for side, (corner1, corner2) in side_to_corner_intersection.items():
            if board[side] == "X" and board[corner1] == "X" and board[corner2] == " ":
                return corner2
            elif board[side] == "X" and board[corner2] == "X" and board[corner1] == " ":
                return corner1

        if board[center] == "X":
            for corner in corners:
                if board[corner] == "X":
                    for other_corner in corners:
                        if board[other_corner] == " ":
                            return other_corner

    move = just_block_or_win(board)
    if move is not None:
        return move

    for i in range(len(board)):
        if board[i] == " ":
            return i

def main():
    board = [" "] * 9
    human = "X"
    bot = "O"
    last_player_move = None

    print("Welcome to the game 'Tic-Tac-Toe'!")
    display_board(board)

    while True:
        while True:
            try:
                move = int(input("Choose a cell (1-9): ")) - 1
                if move not in range(0, 10):
                    raise ValueError("Invalid move! Please choose a number from 1 to 9.")
                if board[move] == " ":
                    board[move] = human
                    last_player_move = move
                    break
                else:
                    print("This cell is already occupied!")
            except (ValueError, IndexError) as e:
                print(e if isinstance(e, ValueError) else "Enter a number from 1 to 9!")

        display_board(board)

        if check_winner(board, human):
            print("Impossible! You won!")
            break

        if check_draw(board):
            print("It's a draw!")
            break

        print("Bot's turn...")
        move = bot_move(board, last_player_move)
        board[move] = bot
        display_board(board)

        if check_winner(board, bot):
            print("The bot won!")
            break

        if check_draw(board):
            print("It's a draw!")
            break

if __name__ == "__main__":
    main()
