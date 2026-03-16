from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from Itypes.IGame import Game
from components.imageLoad import ImageLoader
from PyQt6.QtGui import QColor, QDesktopServices, QPainter, QPainterPath, QPixmap
from PyQt6.QtCore import QUrl

class GameCard(QFrame):
    def __init__(self, game: Game):
        super().__init__()
        self.game = game
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setStyleSheet("""
            QFrame#GameCard {
                background: #0d0d1a;
                border: 1px solid #1a1a3a;
                border-radius: 12px;
            }
            QFrame#GameCard:hover {
                border: 1px solid #00ffff;
            }
            QLabel {
                border: none;
                background: transparent;
            }
        """)
        self.setObjectName("GameCard")

        self.img_label = QLabel()
        self.setMaximumSize(400,215)
        self.img_label.setScaledContents(True)
        self.img_label.setStyleSheet("""
            border-top-left-radius: 10px;
            border-top-right-radius: 10px;
            border-bottom-left-radius: 0px;
            border-bottom-right-radius: 0px;
        """)
        self.img_label.setFixedHeight(140)
        self.setFixedHeight(240)
        title = QLabel(game.name)
        title.setStyleSheet("color: #e8f4f8; font-size: 14px; font-weight: bold; padding: 6px 10px 2px 10px;")
        title.setWordWrap(True)
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)

        bottom = QWidget()
        bottom.setStyleSheet("background: transparent;")
        bottom_layout = QHBoxLayout(bottom)
        bottom_layout.setContentsMargins(10, 0, 10, 6)

        genres = QLabel("  ".join(game.genres[:3]))
        genres.setStyleSheet("color: #555577; font-size: 10px;")

        score = QLabel(f"★ {game.similarity_score:.2f}")
        score.setStyleSheet("color: #00ffff; font-size: 12px; font-weight: bold;")
        
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(12)
        shadow.setOffset(2, 2)
        shadow.setColor(QColor("#00ff88"))
        score.setGraphicsEffect(shadow)
        shadow.setColor(QColor("#005566"))
        title.setGraphicsEffect(shadow)

        bottom_layout.addWidget(genres)
        bottom_layout.addStretch()    
        bottom_layout.addWidget(score)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(4)
        layout.addWidget(self.img_label)
        layout.addWidget(title)
        layout.addWidget(bottom)
        layout.setContentsMargins(0, 0, 0, 0)

        self.loader = ImageLoader(game.img_icon_url)
        self.loader.image_loaded.connect(self.set_image)
        self.loader.start()

    def set_image(self, pixmap):
        w = self.img_label.width()
        h = self.img_label.height()
        scaled = pixmap.scaled(w, h,
            Qt.AspectRatioMode.IgnoreAspectRatio,
            Qt.TransformationMode.SmoothTransformation)
        #This is to clip the image to make it look pretty because qt pixmap is stupid
        rounded = QPixmap(scaled.size())
        rounded.fill(Qt.GlobalColor.transparent)

        painter = QPainter(rounded)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        path = QPainterPath()
        r = 10 
        #This is to clip the top 2 corners only 
        path.moveTo(r, 0)                          
        path.lineTo(w - r, 0)                      
        path.arcTo(w - r*2, 0, r*2, r*2, 90, -90) 
        path.lineTo(w, h)                          
        path.lineTo(0, h)                         
        path.arcTo(0, 0, r*2, r*2, 180, -90)
        path.closeSubpath()
        painter.setClipPath(path)
        painter.drawPixmap(0, 0, scaled)
        painter.end()

        self.img_label.setPixmap(rounded)

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            QDesktopServices.openUrl(QUrl(f"steam://store/{self.game.appid}"))