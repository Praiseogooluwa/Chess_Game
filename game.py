import chess
import chess.engine

class AdvancedChessAI:
    def __init__(self, depth=3, engine_path=r'C:\Users\USER\Desktop\OG\env\CHESS\stockfish\stockfish-windows-x86-64.exe'):
        self.depth = depth
        self.engine = chess.engine.SimpleEngine.popen_uci(engine_path)

    def evaluate_board(self, board):
        # You can replace this with a more sophisticated evaluation function
        return sum([self.get_piece_value(piece) for piece in board.piece_map().values()])

    def get_piece_value(self, piece):
        values = {chess.PAWN: 100, chess.KNIGHT: 320, chess.BISHOP: 330, chess.ROOK: 500, chess.QUEEN: 900, chess.KING: 20000}
        return values[piece.piece_type] if piece.color == chess.WHITE else -values[piece.piece_type]

    def minimax(self, board, depth, alpha, beta, maximizing_player):
        if depth == 0 or board.is_game_over():
            return self.evaluate_board(board)
        
        if maximizing_player:
            max_eval = float('-inf')
            for move in board.legal_moves:
                board.push(move)
                eval = self.minimax(board, depth - 1, alpha, beta, False)
                board.pop()
                max_eval = max(max_eval, eval)
                alpha = max(alpha, eval)
                if beta <= alpha:
                    break
            return max_eval
        else:
            min_eval = float('inf')
            for move in board.legal_moves:
                board.push(move)
                eval = self.minimax(board, depth - 1, alpha, beta, True)
                board.pop()
                min_eval = min(min_eval, eval)
                beta = min(beta, eval)
                if beta <= alpha:
                    break
            return min_eval

    def get_best_move(self, board):
        best_move = None
        max_eval = float('-inf')
        for move in board.legal_moves:
            board.push(move)
            eval = self.minimax(board, self.depth, float('-inf'), float('inf'), False)
            board.pop()
            if eval > max_eval:
                max_eval = eval
                best_move = move
        return best_move

    def get_stockfish_best_move(self, board, time_limit=0.1):
        with self.engine.analysis(board, chess.engine.Limit(time=time_limit)) as analysis:
            result = analysis.get()
            if isinstance(result, dict):  # Handle the case where it returns a dictionary
                try:
                    best_move = result.get('pv', [])[0]
                except IndexError:
                    # Return a default move if no best move is found
                    best_move = list(board.legal_moves)[0]
            else:  # Handle the case where it returns a ChessEngineAnalysisResult object
                best_move = result.pv[0]
            return best_move

    def play(self, board, use_stockfish=False):
        if use_stockfish:
            return self.get_stockfish_best_move(board)
        else:
            return self.get_best_move(board)

    def close(self):
        self.engine.quit()

# Example usage
if __name__ == "__main__":
    ai = AdvancedChessAI(depth=4, engine_path=r'C:\Users\USER\Desktop\OG\env\CHESS\stockfish\stockfish-windows-x86-64.exe')
    board = chess.Board()
    
    while not board.is_game_over():
        if board.turn == chess.WHITE:
            move = ai.play(board, use_stockfish=False)  # Set to True to use Stockfish
        else:
            move = ai.play(board, use_stockfish=True)

        if move:
            board.push(move)
            print(board)
        else:
            print("No move available")

    ai.close()