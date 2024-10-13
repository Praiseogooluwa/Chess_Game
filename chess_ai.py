from flask import Flask, render_template, request, jsonify
import chess
from game import AdvancedChessAI  # Assuming your AI logic is in this file

app = Flask(__name__)
ai = AdvancedChessAI(depth=4, engine_path=r'C:\Users\USER\Desktop\OG\env\CHESS\stockfish\stockfish-windows-x86-64.exe')
board = chess.Board()

@app.route('/')
def index():
    return render_template('index.html', board=board.fen())

@app.route('/move', methods=['POST'])
def make_move():
    global board
    move_uci = request.json['move']
    try:
        board.push_uci(move_uci)
    except ValueError:
        return jsonify({'error': 'Invalid move'}), 400  # Handle invalid moves

    ai_move = ai.play(board, use_stockfish=False)  # Your AI logic
    board.push(ai_move)
    return jsonify({'board': board.fen(), 'move': ai_move.uci()})

@app.route('/reset', methods=['POST'])
def reset_board():
    global board
    board = chess.Board()
    return jsonify({'board': board.fen()})

@app.route('/undo', methods=['POST'])
def undo_move():
    global board
    if board.move_stack:  # Check if there are moves to undo
        board.pop()
        return jsonify({'board': board.fen()})
    else:
        return jsonify({'error': 'No moves to undo'}), 400

@app.route('/redo', methods=['POST'])
def redo_move():
    # Implement redo logic (likely not as straightforward as undo)
    return jsonify({'error': 'Redo is not yet implemented'}), 400

if __name__ == '__main__':
    app.run(debug=True)