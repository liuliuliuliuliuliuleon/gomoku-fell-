difficulty_levels = {
    "easy": {"depth": 1},     # 简单：搜索 1 层
    "medium": {"depth": 2},   # 中等：搜索 2 层
    "hard": {"depth": 3},     # 困难：搜索 3 层
    "expert": {"depth": 4},   # 专家：搜索 4 层
}

#设置评估函数（评分规则，通过模式匹配和权重分配来实现）
def evaluate_line(line, player):
    score = 0
    opponent = -player
    if "11111" in line: #win
        return 10000 
    if "011110" in line: #活四
        score += 1000
    if "011100" in line or "001110" in line: #冲四、活三
        score += 100
    if "0110" in line or "01010" in line: #冲三
        score += 10
    if "11112" in line or "21111" in line: #冲三
        score -= 50  # 对手威胁
    return score

#simple模式下的评估函数
def evaluate_line_simple(line, player):
    score = 0
    if f"{player * 3}" in line:  # 连三
        score += 10
    if f"{player * 4}" in line:  # 连四
        score += 100
    return score

def evaluate(board, player, difficulty="medium"):
    score = 0
    evaluate_function = evaluate_line if difficulty in ["hard", "expert"] else evaluate_line_simple

    board_size = len(board)
    for i in range(board_size):
        # 评估每一行
        row = ''.join(str(board[i][j]) for j in range(board_size))
        score += evaluate_function(row, player)
        # 评估每一列
        col = ''.join(str(board[j][i]) for j in range(board_size))
        score += evaluate_function(col, player)
    # 评估对角线
    for d in range(-board_size + 1, board_size):
        diag1 = ''.join(str(board[i][i - d]) for i in range(max(0, d), min(board_size, board_size + d)))
        diag2 = ''.join(str(board[i][board_size - i - 1 + d]) for i in range(max(0, d), min(board_size, board_size + d)))
        score += evaluate_function(diag1, player)
        score += evaluate_function(diag2, player)
    return score


#α-β剪枝
def alpha_beta(board, depth, alpha, beta, maximizing_player, player):
    if depth == 0:
        return evaluate(board, player)

    best_score = float('-inf') if maximizing_player else float('inf')
    opponent = -player

    for x in range(len(board)):
        for y in range(len(board)):
            if board[x][y] == 0:  # 找空位
                board[x][y] = player if maximizing_player else opponent
                score = alpha_beta(board, depth - 1, alpha, beta, not maximizing_player, player)
                board[x][y] = 0  # 恢复原状
                if maximizing_player:
                    best_score = max(best_score, score)
                    alpha = max(alpha, score)
                else:
                    best_score = min(best_score, score)
                    beta = min(beta, score)
                if beta <= alpha:
                    return best_score  # 剪枝
    return best_score

def get_best_move(board, player, difficulty="medium"):
    depth = difficulty_levels[difficulty]["depth"]
    best_move = None
    best_score = float('-inf')

    for x in range(len(board)):
        for y in range(len(board)):
            if board[x][y] == 0:  # 找空位
                board[x][y] = player
                score = alpha_beta(board, depth - 1, float('-inf'), float('inf'), False, player)
                board[x][y] = 0  # 恢复原状
                if score > best_score:
                    best_score = score
                    best_move = (x, y)

    return best_move

if __name__ == "__main__":
    from LOGIC import GomokuGame
    from AI import get_best_move

    game = GomokuGame()
    print("选择难度：easy, medium, hard, expert")
    difficulty = input("输入难度 (默认: medium): ").strip() or "medium"

    game.place_piece(7, 7, 1)  # 黑棋
    game.place_piece(7, 8, -1)  # 白棋

    # AI 根据难度计算最佳位置
    best_move = get_best_move(game.board, 1, difficulty)
    print(f"AI 在 {difficulty} 难度下建议落子位置:", best_move)
