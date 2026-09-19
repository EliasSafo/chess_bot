from pathlib import Path

import chess

from PySide6.QtCore import Qt, QSize, QUrl, QTimer
from PySide6.QtGui import QIcon
from PySide6.QtMultimedia import QSoundEffect
from PySide6.QtWidgets import (
    QWidget,
    QGridLayout,
    QPushButton,
    QVBoxLayout,
    QLabel,
)


BASE_DIR = Path(__file__).resolve().parent.parent


PIECE_IMAGES = {
    (chess.PAWN, chess.WHITE): BASE_DIR / "assets/pieces/white_pawn.svg",
    (chess.KNIGHT, chess.WHITE): BASE_DIR / "assets/pieces/white_knight.svg",
    (chess.BISHOP, chess.WHITE): BASE_DIR / "assets/pieces/white_bishop.svg",
    (chess.ROOK, chess.WHITE): BASE_DIR / "assets/pieces/white_rook.svg",
    (chess.QUEEN, chess.WHITE): BASE_DIR / "assets/pieces/white_queen.svg",
    (chess.KING, chess.WHITE): BASE_DIR / "assets/pieces/white_king.svg",

    (chess.PAWN, chess.BLACK): BASE_DIR / "assets/pieces/black_pawn.svg",
    (chess.KNIGHT, chess.BLACK): BASE_DIR / "assets/pieces/black_knight.svg",
    (chess.BISHOP, chess.BLACK): BASE_DIR / "assets/pieces/black_bishop.svg",
    (chess.ROOK, chess.BLACK): BASE_DIR / "assets/pieces/black_rook.svg",
    (chess.QUEEN, chess.BLACK): BASE_DIR / "assets/pieces/black_queen.svg",
    (chess.KING, chess.BLACK): BASE_DIR / "assets/pieces/black_king.svg",
}


class ChessWindow(QWidget):

    def __init__(
            self,
            controller,
            interactive=True,
            sound_enabled=True,
    ):
        super().__init__()

        self.controller = controller
        self.interactive = interactive
        self.sound_enabled = sound_enabled

        # Set this BEFORE create_board()
        self.orientation = getattr(
            controller,
            "human_color",
            chess.WHITE,
        )

        self.selected_square = None
        self.last_move = None
        self.square_buttons = {}

        self.setWindowTitle("Chess Brain")

        if self.sound_enabled:
            self.setup_sound()

        self.board_grid = QGridLayout()
        self.board_grid.setSpacing(0)

        self.status_label = QLabel()
        self.status_label.setAlignment(Qt.AlignCenter)

        layout = QVBoxLayout()
        layout.addLayout(self.board_grid)
        layout.addWidget(self.status_label)

        self.setLayout(layout)

        self.create_board()
        self.update_board()


    @property
    def board(self):
        return self.controller.game.board

    def setup_sound(self):
        self.move_sound = QSoundEffect()

        sound_path = BASE_DIR / "assets/sounds/move.wav"

        self.move_sound.setSource(
            QUrl.fromLocalFile(str(sound_path))
        )

        self.move_sound.setVolume(0.5)

    def register_move(self, move: chess.Move):
        self.last_move = move

        if self.sound_enabled:
            self.move_sound.play()

    def create_board(self):
        for row in range(8):
            for col in range(8):

                button = QPushButton()

                button.setFixedSize(90, 90)

                button.clicked.connect(
                    lambda checked=False, r=row, c=col:
                    self.handle_square_click(r, c)
                )

                self.board_grid.addWidget(
                    button,
                    row,
                    col,
                )

                square = self.coordinates_to_square(
                    row,
                    col,
                )

                self.square_buttons[square] = button

    def coordinates_to_square(
            self,
            row: int,
            col: int,
    ) -> chess.Square:

        if self.orientation == chess.WHITE:
            file_index = col
            rank_index = 7 - row

        else:
            file_index = 7 - col
            rank_index = row

        return chess.square(
            file_index,
            rank_index,
        )

    def handle_square_click(
        self,
        row: int,
        col: int,
    ):
        if not self.interactive:
            return

        clicked_square = self.coordinates_to_square(
            row,
            col,
        )

        if self.selected_square is None:
            self.select_square(clicked_square)
            return

        if clicked_square == self.selected_square:
            self.selected_square = None
            self.update_board()
            return

        human_move = self.controller.make_human_move(
            self.selected_square,
            clicked_square,
        )

        if human_move is not None:
            self.register_move(human_move)

            self.selected_square = None

            self.update_board()

            QTimer.singleShot(
                200,
                self.make_delayed_bot_move,
            )

            return

        piece = self.board.piece_at(
            clicked_square
        )

        if (
            piece is not None
            and piece.color == self.board.turn
        ):
            self.selected_square = clicked_square

        else:
            self.selected_square = None

        self.update_board()

    def make_delayed_bot_move(self):
        bot_move = self.controller.make_bot_move()

        if bot_move is not None:
            self.register_move(bot_move)

        self.update_board()

    def select_square(
        self,
        square: chess.Square,
    ):
        piece = self.board.piece_at(square)

        if piece is None:
            return

        if piece.color != self.board.turn:
            return

        if hasattr(self.controller, "human_color"):
            if piece.color != self.controller.human_color:
                return

        self.selected_square = square

        self.update_board()

    def update_board(self):

        legal_destination_squares = set()

        if self.selected_square is not None:
            legal_destination_squares = {
                move.to_square
                for move in self.board.legal_moves
                if move.from_square == self.selected_square
            }

        for square, button in self.square_buttons.items():

            piece = self.board.piece_at(square)

            if piece is None:
                button.setIcon(QIcon())

            else:
                image_path = PIECE_IMAGES[
                    (piece.piece_type, piece.color)
                ]

                button.setIcon(
                    QIcon(str(image_path))
                )

                button.setIconSize(
                    QSize(72, 72)
                )

            button.setStyleSheet(
                self.get_square_style(
                    square,
                    legal_destination_squares,
                )
            )

        self.update_status()

    def get_square_style(
        self,
        square: chess.Square,
        legal_destination_squares: set[chess.Square],
    ) -> str:

        file_index = chess.square_file(square)
        rank_index = chess.square_rank(square)

        is_light = (
            file_index + rank_index
        ) % 2 == 1

        if is_light:
            background = "#F0D9B5"
        else:
            background = "#B58863"

        # Last move
        if (
            self.last_move is not None
            and square in (
                self.last_move.from_square,
                self.last_move.to_square,
            )
        ):
            background = "#F6E05E"

        # Legal destination
        if square in legal_destination_squares:
            background = "#A9D18E"

        # Currently selected piece gets highest priority
        if square == self.selected_square:
            background = "#FFF176"

        return f"""
            QPushButton {{
                background-color: {background};
                border: none;
            }}

            QPushButton:hover {{
                border: 2px solid #333333;
            }}
        """

    def update_status(self):

        if self.board.is_checkmate():

            winner = (
                "Black"
                if self.board.turn == chess.WHITE
                else "White"
            )

            self.status_label.setText(
                f"Checkmate — {winner} wins"
            )

            return

        if self.board.is_stalemate():
            self.status_label.setText(
                "Stalemate"
            )
            return

        if self.board.turn == chess.WHITE:
            turn = "White"
        else:
            turn = "Black"

        if self.board.is_check():
            self.status_label.setText(
                f"{turn} to move — CHECK"
            )
        else:
            self.status_label.setText(
                f"{turn} to move"
            )