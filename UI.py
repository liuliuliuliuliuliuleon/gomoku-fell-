import pygame

class GomokuUI:
    def __init__(self, screen, board_size, cell_size):
        self.screen = screen
        self.board_size = board_size
        self.cell_size = cell_size
        self.colors = {
            "background": (240, 217, 181),  # 浅棕色背景
            "line": (0, 0, 0),  # 黑色棋盘线
            "black_piece": (0, 0, 0),  # 黑棋
            "white_piece": (255, 255, 255)  # 白棋
        }

    def draw_board(self):
        """绘制棋盘"""
        self.screen.fill(self.colors["background"])  # 填充背景颜色
        for i in range(self.board_size):
            # 画横线
            pygame.draw.line(
                self.screen, self.colors["line"],
                (self.cell_size, self.cell_size * (i + 1)),
                (self.cell_size * self.board_size, self.cell_size * (i + 1)), 1
            )
            # 画竖线
            pygame.draw.line(
                self.screen, self.colors["line"],
                (self.cell_size * (i + 1), self.cell_size),
                (self.cell_size * (i + 1), self.cell_size * self.board_size), 1
            )

    def update(self, board):
        """更新界面，绘制棋子"""
        self.draw_board()
        for x in range(self.board_size):
            for y in range(self.board_size):
                if board[x][y] == 1:  # 黑棋
                    pygame.draw.circle(
                        self.screen, self.colors["black_piece"],
                        (self.cell_size * (y + 1), self.cell_size * (x + 1)),
                        self.cell_size // 3
                    )
                elif board[x][y] == -1:  # 白棋
                    pygame.draw.circle(
                        self.screen, self.colors["white_piece"],
                        (self.cell_size * (y + 1), self.cell_size * (x + 1)),
                        self.cell_size // 3
                    )

    def get_click_position(self, pos):
        """将鼠标点击的位置转换为棋盘坐标"""
        x, y = pos
        grid_x = (y - self.cell_size // 2) // self.cell_size
        grid_y = (x - self.cell_size // 2) // self.cell_size

        if 0 <= grid_x < self.board_size and 0 <= grid_y < self.board_size:
            return grid_x, grid_y
        return None


