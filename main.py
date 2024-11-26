import pygame
from UI import GomokuUI
from LOGIC import GomokuGame
from AI import get_best_move
import threading

# 游戏参数
BOARD_SIZE = 15
CELL_SIZE = 40
WINDOW_SIZE = BOARD_SIZE * CELL_SIZE

def main():
    pygame.init()
    screen = pygame.display.set_mode((WINDOW_SIZE, WINDOW_SIZE))
    pygame.display.set_caption("Gomoku 五子棋")
    clock = pygame.time.Clock()

    # 初始化游戏逻辑和 UI
    game = GomokuGame(board_size=BOARD_SIZE)
    ui = GomokuUI(screen, BOARD_SIZE, CELL_SIZE)

    ui.draw_board()  # 初始化棋盘网格
    pygame.display.flip()  # 刷新屏幕显示初始状态

    # 玩家选择模式
    mode = int(input("选择模式：1. 玩家对玩家  2. 玩家对AI (默认: 2): ") or 2)
    ai_player = -1 if mode == 2 else None  # 默认 AI 使用白棋
    difficulty = input("选择 AI 难度：easy, medium, hard, expert (默认: medium): ").strip() or "medium"
    current_player = 1  # 黑棋先手
    running = True
    game_over = False

    # AI 落子函数
    def ai_move():
        nonlocal x, y
        x, y = get_best_move(game.board, ai_player, difficulty)
        game.place_piece(x, y, ai_player)
        ui.update(game.board)

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            # 玩家落子逻辑
            elif event.type == pygame.MOUSEBUTTONDOWN and (mode == 1 or current_player != ai_player):
                pos = event.pos
                grid_pos = ui.get_click_position(pos)
                if grid_pos:
                    x, y = grid_pos
                    if game.place_piece(x, y, current_player):
                        ui.update(game.board)
                        pygame.display.flip()
                        if game.is_win(x, y, current_player):
                            print(f"玩家 {'黑' if current_player == 1 else '白'} 胜利！")
                            game_over = True
                        elif game.is_draw():
                            print("平局！")
                            game_over = True
                        current_player *= -1  # 切换玩家

        # AI 落子逻辑
        if mode == 2 and current_player == ai_player and not game_over:
            ai_thread = threading.Thread(target=ai_move)
            ai_thread.start()
            ai_thread.join()  # 等待 AI 思考完成
            if game.is_win(x, y, ai_player):
                print(f"AI（{'黑' if ai_player == 1 else '白'}）胜利！")
                game_over = True
            elif game.is_draw():
                print("平局！")
                game_over = True
            current_player *= -1

        clock.tick(30)  # 限制帧率，防止过高帧率消耗资源
        pygame.display.flip()  # 刷新屏幕

    print("游戏结束！")
    pygame.quit()

if __name__ == "__main__":
    main()



