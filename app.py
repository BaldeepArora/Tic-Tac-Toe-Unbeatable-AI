from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# Function to check if a player has won
def check_win(board, player):
    win_conditions = [
        [0, 1, 2], [3, 4, 5], [6, 7, 8],        # Rows
        [0, 3, 6], [1, 4, 7], [2, 5, 8],        # Columns
        [0, 4, 8], [2, 4, 6]                    # Diagonals
    ]
    for condition in win_conditions:
        if all(board[i] == player for i in condition):
            return True
    return False

# Function to check if the board is full
def board_full(board):
    return all(cell != '' for cell in board)

# Minimax algorithm implementation
def minimax(board, depth, is_maximizing):
    if check_win(board, 'O'):
        return 10 - depth
    if check_win(board, 'X'):
        return depth - 10
    if board_full(board):
        return 0

    if is_maximizing:
        best_score = -float('inf')
        for i in range(9):
            if board[i] == '':
                board[i] = 'O'
                score = minimax(board, depth + 1, False)
                board[i] = ''
                best_score = max(score, best_score)
        return best_score
    else:
        best_score = float('inf')
        for i in range(9):
            if board[i] == '':
                board[i] = 'X'
                score = minimax(board, depth + 1, True)
                board[i] = ''
                best_score = min(score, best_score)
        return best_score

# Function to determine the best move for the computer
def best_move(board):
    best_score = -float('inf')
    move = None
    for i in range(9):
        if board[i] == '':
            board[i] = 'O'
            score = minimax(board, 0, False)
            board[i] = ''
            if score > best_score:
                best_score = score
                move = i
    return move

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/start', methods=['POST'])
def start():
    board = [''] * 9
    return jsonify({'board': board})

@app.route('/cpu_move', methods=['POST'])
def cpu_move():
    data = request.get_json()
    board = data['board']

    # Computer makes its move
    comp_move = best_move(board)
    if comp_move is not None:
        board[comp_move] = 'O'
    else:
        return jsonify({'status': 'draw', 'board': board})

    if check_win(board, 'O'):
        return jsonify({'status': 'lose', 'board': board})
    if board_full(board):
        return jsonify({'status': 'draw', 'board': board})

    return jsonify({'status': 'continue', 'board': board})

@app.route('/move', methods=['POST'])
def move():
    data = request.get_json()
    board = data['board']
    user_move = data['move']

    if board[user_move] == '':
        board[user_move] = 'X'
    else:
        return jsonify({'status': 'invalid', 'board': board})

    if check_win(board, 'X'):
        return jsonify({'status': 'win', 'board': board})
    if board_full(board):
        return jsonify({'status': 'draw', 'board': board})

    return jsonify({'status': 'continue', 'board': board})

if __name__ == '__main__':
    app.run(debug=True)
