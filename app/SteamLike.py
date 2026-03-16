import os

from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import QColor
from PyQt6.QtGui import QIcon
import sys

import keyring
from components.Navbar import Navbar
from components.card import GameCard
import json
from Itypes.IGame import Game
from scripts.utilpath import get_data_path
from scripts.run import main as run_main


json_path = get_data_path("ranked.json")
if os.path.exists(json_path):
    with open(json_path) as f:
        games_json = json.load(f)
    games = [Game.from_dict(g) for g in games_json]
else:
    games = []

GAMES_PER_PAGE = 12

if getattr(sys, 'frozen', False):
    icon_path = os.path.join(sys._MEIPASS, "SteamLike.ico")
else:
    icon_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "SteamLike.ico")

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowIcon(QIcon(icon_path))
        STEAM_API_KEY = keyring.get_password("steamlike", "STEAM_API_KEY")
        STEAM_ID = keyring.get_password("steamlike", "STEAM_ID")
        if not STEAM_API_KEY:
            key, ok = QInputDialog.getText(self, "Setup", "Enter your Steam API key:")
            if ok and key:
                keyring.set_password("steamlike", "STEAM_API_KEY", key)
        if not STEAM_ID:
            key, ok = QInputDialog.getText(self, "Setup", "Enter your Steam User ID:")
            if ok and key:
                keyring.set_password("steamlike", "STEAM_ID", key)
        
       
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)
        self.showFullScreen()
        self.setWindowTitle("SteamLike")
        self.setMinimumSize(1100, 750)
        self.setStyleSheet("background: #08080f;")
        self.page = 0

        container = QWidget()
        main_layout = QVBoxLayout(container)
        main_layout.setContentsMargins(24, 24, 24, 24)
        main_layout.setSpacing(16)
        self.navbar = Navbar()
        if not games: self.navbar.terminal.setText("[ PRESS ANALYSE TO BEGIN ]")
        self.grid_widget = QWidget()
        self.grid_layout = QGridLayout(self.grid_widget)
        self.grid_layout.setSpacing(16)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setWidget(self.grid_widget)
        scroll.setStyleSheet("""
            QScrollArea {
                border: none;
                background: transparent;
            }
            QScrollBar:vertical {
                background: #0a0a18;
                width: 6px;
                border-radius: 3px;
                margin: 0;
            }
            QScrollBar::handle:vertical {
                background: #00ffff;
                border-radius: 3px;
                min-height: 20px;
            }
            QScrollBar::handle:vertical:hover {
                background: #ffffff;
            }
            QScrollBar::add-line:vertical,
            QScrollBar::sub-line:vertical {
                height: 0px;
            }
            QScrollBar::add-page:vertical,
            QScrollBar::sub-page:vertical {
                background: none;
            }
        """)

        # pagination buttons
        btn_style = """
            QPushButton {
                background: transparent;
                color: #00ffff;
                border: none;
                font-family: 'Courier New';
                font-size: 14px;
                letter-spacing: 2px;
                padding: 6px 16px;
            }
            QPushButton:hover { color: #ffffff; }
            QPushButton:disabled { color: #333355; }
        """
        
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(12)
        shadow.setOffset(2, 2)
        shadow.setColor(QColor("#00ff88"))

        self.prev_btn = QPushButton("← Prev")
        self.next_btn = QPushButton("Next →")
        self.page_label = QLabel()
        self.prev_btn.setStyleSheet(btn_style)
        self.prev_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.next_btn.setStyleSheet(btn_style)
        self.next_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.page_label.setStyleSheet("color: #555577; font-size: 12px;")
        self.prev_btn.setGraphicsEffect(shadow)
        self.next_btn.setGraphicsEffect(shadow)

        self.placeholder = QLabel("PRESS [ ANALYSE ] TO LOAD GAMES")
        self.placeholder.setStyleSheet("""
            color: #1a1a3a;
            font-family: 'Courier New';
            font-size: 18px;
            letter-spacing: 6px;
            background: transparent;
        """)
        self.placeholder.setAlignment(Qt.AlignmentFlag.AlignCenter)

        pagination = QWidget()
        pagination_layout = QHBoxLayout(pagination)
        pagination_layout.addStretch()
        pagination_layout.addWidget(self.prev_btn)
        pagination_layout.addWidget(self.page_label)
        pagination_layout.addWidget(self.next_btn)
        pagination_layout.addStretch()

        main_layout.addWidget(self.navbar)
        main_layout.addWidget(scroll)
        main_layout.addWidget(pagination)
        self.main_layout = main_layout
        self.prev_btn.clicked.connect(self.prev_page)
        self.next_btn.clicked.connect(self.next_page)
        self.navbar.exit_btn.clicked.connect(self.close)
        self.navbar.analyse_btn.clicked.connect(self.on_analyse)
        self.setCentralWidget(container)
        self.render_page()

    def render_page(self):
        for i in reversed(range(self.grid_layout.count())):
            self.grid_layout.itemAt(i).widget().setParent(None)

        start = self.page * GAMES_PER_PAGE
        page_games = games[start:start + GAMES_PER_PAGE]
       
        for i, game in enumerate(page_games):
            card = GameCard(game)
            self.grid_layout.addWidget(card, i // 3, i % 3)

        total_pages = (len(games) - 1) // GAMES_PER_PAGE + 1
        self.page_label.setText(f"  {self.page + 1} / {total_pages}  ")
        self.prev_btn.setEnabled(self.page > 0)
        self.next_btn.setEnabled(self.page < total_pages - 1)
    def prev_page(self):
        self.page -= 1
        self.render_page()

    def next_page(self):
        self.page += 1
        self.render_page()

    def on_analyse(self):
        self.navbar.analyse_btn.setEnabled(False)

        self.dot_count = 0
        self.dot_timer = QTimer(self)
        self.dot_timer.timeout.connect(self.animate_dots)
        self.dot_timer.start(500)

        self.navbar.terminal.setText("[ INITIALIZING... ]")

        self.thread = AnalyseThread()
        self.thread.finished.connect(self.on_analyse_done)
        self.thread.output.connect(lambda text: self.navbar.terminal.setText(f"[ {text[:50].upper()} ]"))
        self.thread.start()


    def animate_dots(self):
        dots = "." * self.dot_count
        self.navbar.analyse_btn.setText(f"ANALYSING{dots}")
        self.dot_count = (self.dot_count + 1) % 4

    def on_process_output(self):
        output = self.process.readAllStandardOutput().data().decode().strip()
        if output:
            last_line = output.split("\n")[-1][:60]
            self.navbar.terminal.setText(f"[ {last_line.upper()} ]")

    def on_process_error(self):
        error = self.process.readAllStandardError().data().decode().strip()
        if error:
            last_line = error.split("\n")[-1][:60]
            self.navbar.terminal.setStyleSheet("""
                color: #ff4466;
                font-family: 'Courier New';
                font-size: 11px;
                letter-spacing: 1px;
                padding: 0 16px;
            """)
            self.navbar.terminal.setText(f"[ {last_line.upper()} ]")

    def on_analyse_done(self):
        self.dot_timer.stop()
        self.navbar.analyse_btn.setEnabled(True)
        self.navbar.analyse_btn.setText("[ ANALYSE ]")
        self.navbar.analyse_btn.setEnabled(True)
        self.navbar.terminal.setStyleSheet("""
            color: #00ff88;
            font-family: 'Courier New';
            font-size: 11px;
            letter-spacing: 1px;
            padding: 0 16px;
        """)
        self.navbar.terminal.setText("[ COMPLETE ]")

        with open(json_path) as f:
            raw = json.load(f)
        global games
        games = [Game.from_dict(g) for g in raw]
        self.page = 0
        self.render_page()

class AnalyseThread(QThread):
    finished = pyqtSignal()
    output = pyqtSignal(str)

    def run(self):
        import builtins
        original_print = builtins.print

        def custom_print(*args, **kwargs):
            text = " ".join(str(a) for a in args)
            self.output.emit(text)
            original_print(*args, **kwargs)

        builtins.print = custom_print
        try:
            run_main()
            self.finished.emit()
        except Exception as e:
            self.output.emit(f"ERROR: {e}")
        finally:
            builtins.print = original_print


app = QApplication(sys.argv)

window = MainWindow()
window.show()

app.exec()