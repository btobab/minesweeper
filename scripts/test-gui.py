from PyQt5 import QtCore
from PyQt5.QtWidgets import QWidget, QApplication, QGridLayout
from minesweeper.msgame import MSGame
from minesweeper import gui
import time


def main(board_width, board_height, num_mines, port, ip_add):
    ms_game = MSGame(board_width, board_height, num_mines,
                     port=port, ip_add=ip_add)

    ms_app = QApplication([])

    ms_window = QWidget()
    ms_window.setAutoFillBackground(True)
    ms_window.setWindowTitle("Mine Sweeper")
    ms_layout = QGridLayout()
    ms_window.setLayout(ms_layout)

    fun_wg = gui.ControlWidget()
    grid_wg = gui.GameWidget(ms_game, fun_wg)
    remote_thread = gui.RemoteControlThread()

    def update_grid_remote(move_msg):
        """Update grid from remote control."""
        if grid_wg.ms_game.game_status == 2:
            grid_wg.ms_game.play_move_msg(str(move_msg))
            grid_wg.update_grid()

    remote_thread.transfer.connect(update_grid_remote)

    def reset_button_state():
        """Reset button state."""
        grid_wg.reset_game()

    fun_wg.reset_button.clicked.connect(reset_button_state)

    ms_layout.addWidget(fun_wg, 0, 0)
    ms_layout.addWidget(grid_wg, 1, 0)

    remote_thread.control_start(grid_wg.ms_game)

    for i in range(10):
        print(ms_game.game_status)
        grid_wg.ms_game.play_move("flag", i, i)
        grid_wg.update_grid()
        # time.sleep(0.1)

    print(grid_wg.ms_game.board.info_map)

    ms_window.show()
    ms_app.exec_()


if __name__ == "__main__":
    main(20, 20, 40, 5678, "127.0.0.1")
