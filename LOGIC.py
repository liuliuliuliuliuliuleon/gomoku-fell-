class GomokuGame:
    def __init__(self, board_size=15):
        self.board_size = board_size
        self.board = [[0 for _ in range(board_size)] for _ in range(board_size)]
        self.winner = None

    def place_piece(self, x, y, player):
        """放置棋子"""
        if self.board[x][y] == 0:
            self.board[x][y] = player
            return True
        return False

    def is_win(self, x, y, player):
        """检查是否胜利"""
        directions = [(1, 0), (0, 1), (1, 1), (1, -1)]  # 四个方向
        for d_x, d_y in directions:
            count = 1

            # 检查正方向
            n_x, n_y = x + d_x, y + d_y
            while 0 <= n_x < self.board_size and 0 <= n_y < self.board_size and self.board[n_x][n_y] == player:
                count += 1
                n_x += d_x
                n_y += d_y

            # 检查反方向
            n_x, n_y = x - d_x, y - d_y
            while 0 <= n_x < self.board_size and 0 <= n_y < self.board_size and self.board[n_x][n_y] == player:
                count += 1
                n_x -= d_x
                n_y -= d_y

            # 判断是否连成五子
            if count >= 5:
                self.winner = player
                return True
        return False

    def is_draw(self):
        """检查是否平局"""
        for row in self.board:
            if 0 in row:  # 棋盘上有空位
                return False
        return self.winner is None  # 没有赢家则为平局

    def print_board(self):
        """打印棋盘"""
        for row in self.board:
            print(' '.join(['.' if x == 0 else ('X' if x == 1 else 'O') for x in row]))
        print()


if __name__ == "__main__":
    game = GomokuGame()
    moves = [
        (7, 7, 1),  # 黑棋
        (7, 8, -1),  # 白棋
        (6, 6, 1),  # 黑棋
        (7, 9, -1),  # 白棋
        (5, 5, 1),  # 黑棋
        (7, 10, -1),  # 白棋
        (4, 4, 1),  # 黑棋
        (7, 11, -1),  # 白棋
        (3, 3, 1),  # 黑棋获胜
    ]

    for x, y, player in moves:
        if game.place_piece(x, y, player):
            print(f"玩家 {'黑' if player == 1 else '白'} 在 ({x}, {y}) 处落子。")
            if game.is_win(x, y, player):
                game.print_board()
                print(f"玩家 {'黑' if player == 1 else '白'} 胜利！")
                break 
            elif game.is_draw():
                game.print_board()
                print("平局！")
                break
        else:
            print(f"位置 ({x}, {y}) 已被占用！")



