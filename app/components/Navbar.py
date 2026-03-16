from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import QColor
import random

class Navbar(QWidget):
    def __init__(self):
        super().__init__()
        self.setFixedHeight(56)
        self.setStyleSheet("""
            QWidget#Navbar {
                background: #0a0a18;
                border-bottom: 1px solid #00ffff33;
            }
        """)
        self.setObjectName("Navbar")

        self.title = QLabel("SteamLike")
        self.title.setStyleSheet("""
            color: #00ffff;
            font-size: 22px;
            font-weight: bold;
            font-family: 'Orbitron';
            letter-spacing: 5px;
            padding-left: 24px;
            background: transparent;
        """)

        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(12)
        shadow.setOffset(2, 2)
        shadow.setColor(QColor("#00ff88"))
        self.title.setGraphicsEffect(shadow)

        self.analyse_btn = QPushButton("[ ANALYSE ]")
        self.analyse_btn.setFixedSize(130, 34)
        self.analyse_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.analyse_btn.setStyleSheet("""
            QPushButton {
                background: transparent;
                color: #00ffff;
                border: 1px solid #00ffff;
                border-radius: 4px;
                font-family: 'Courier New';
                font-size: 12px;
                letter-spacing: 2px;
            }
            QPushButton:hover {
                background: #00ffff;
                color: #0a0a18;
            }
            QPushButton:pressed {
                background: #00cccc;
            }
        """)

        self.exit_btn = QPushButton("X")
        self.exit_btn.setFixedSize(50, 50)
        self.exit_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.exit_btn.setStyleSheet("""
             QPushButton {
                background: transparent;
                color: #00ffff;
                border: none;
                font-family: 'Courier New';
                font-size: 14px;
                letter-spacing: 2px;
                padding: 0px 0px;
            }
            QPushButton:hover { color: #ffffff; }
            QPushButton:disabled { color: #333355; }
        """)
        self.exit_btn.clicked.connect(self.close)

        self.terminal = QLabel("[ READY ]")
        self.terminal.setStyleSheet("""
            color: #00ff88;
            font-family: 'Courier New';
            font-size: 11px;
            letter-spacing: 1px;
            padding: 0 16px;
        """)
        self.terminal.setCursor(Qt.CursorShape.IBeamCursor)
        self.terminal.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 24, 0)
        layout.addWidget(self.title)
        layout.addStretch()
        layout.addWidget(self.terminal)
        layout.addStretch()
        layout.addWidget(self.analyse_btn)
        layout.addWidget(self.exit_btn)

        self._original = "SteamLike"
        self._glitch_chars = "!@#$%^&*<>?/\\|"
        self._glitching = False
        timer = QTimer(self)
        timer.timeout.connect(self._trigger_glitch)
        timer.start(3000)

    def _trigger_glitch(self):
        if self._glitching:
            return
        self._glitching = True
        self._glitch_steps = 0
        glitch_timer = QTimer(self)
        glitch_timer.timeout.connect(lambda: self._glitch_step(glitch_timer))
        glitch_timer.start(60)

    def _glitch_step(self, timer):
        self._glitch_steps += 1
        if self._glitch_steps > 6:
            self.title.setText(self._original)
            self._glitching = False
            timer.stop()
            return
        glitched = ""
        for ch in self._original:
            if random.random() < 0.35:
                glitched += random.choice(self._glitch_chars)
            else:
                glitched += ch
        self.title.setText(glitched)