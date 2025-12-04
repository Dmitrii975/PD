# -*- coding: utf-8 -*-
import sys
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                           QHBoxLayout, QPushButton, QStackedWidget, QFrame, QLabel)
from PyQt6.QtCore import Qt, QPropertyAnimation, QEasingCurve
from PyQt6.QtGui import QColor, QFont

class HomeScreen(QWidget):
    def __init__(self):
        super().__init__()
        self.setStyleSheet("background-color: #fffaf0; border-radius: 15px;")
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        label = QLabel("🏠 Добро пожаловать на главную страницу!")
        label.setStyleSheet("font-size: 18px; color: #5a3921; font-weight: bold;")
        layout.addWidget(label)
        self.setLayout(layout)

class AnalysisScreen(QWidget):
    def __init__(self):
        super().__init__()
        self.setStyleSheet("background-color: #fffaf0; border-radius: 15px;")
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        label = QLabel("📊 Страница анализа данных")
        label.setStyleSheet("font-size: 18px; color: #5a3921; font-weight: bold;")
        layout.addWidget(label)
        self.setLayout(layout)

class ForecastScreen(QWidget):
    def __init__(self):
        super().__init__()
        self.setStyleSheet("background-color: #fffaf0; border-radius: 15px;")
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        label = QLabel("📈 Страница прогнозирования")
        label.setStyleSheet("font-size: 18px; color: #5a3921; font-weight: bold;")
        layout.addWidget(label)
        self.setLayout(layout)

class SettingsScreen(QWidget):
    def __init__(self):
        super().__init__()
        self.setStyleSheet("background-color: #fffaf0; border-radius: 15px;")
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        label = QLabel("⚙️ Настройки приложения")
        label.setStyleSheet("font-size: 18px; color: #5a3921; font-weight: bold;")
        layout.addWidget(label)
        self.setLayout(layout)

class AccountScreen(QWidget):
    def __init__(self):
        super().__init__()
        self.setStyleSheet("background-color: #fffaf0; border-radius: 15px;")
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        label = QLabel("👤 Управление аккаунтом")
        label.setStyleSheet("font-size: 18px; color: #5a3921; font-weight: bold;")
        layout.addWidget(label)
        self.setLayout(layout)

class MenuButton(QPushButton):
    """Кастомная кнопка меню с анимацией и иконками"""
    def __init__(self, icon_text, text, parent=None):
        super().__init__(parent)
        self.setFixedHeight(50)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        
        # Основной контент кнопки
        layout = QHBoxLayout()
        layout.setContentsMargins(25, 0, 25, 0)
        layout.setSpacing(15)
        
        # Иконка (используем текст-эмоджи как иконку)
        icon_label = QLabel(icon_text)
        icon_label.setStyleSheet("font-size: 20px; color: #5a3921; background: transparent;")
        
        # Текст кнопки
        text_label = QLabel(text)
        text_label.setStyleSheet("font-size: 14px; font-weight: 500; color: #5a3921; background: transparent;")
        
        layout.addWidget(icon_label)
        layout.addWidget(text_label)
        layout.addStretch()
        
        self.setLayout(layout)
        
        # Начальный стиль кнопки
        self.setStyleSheet("""
            QPushButton {
                text-align: left;
                border: none;
                border-radius: 10px;
                background-color: transparent;
                padding: 5px 10px;
            }
            QPushButton:hover {
                background-color: rgba(255, 255, 255, 0.2);
            }
            QPushButton:pressed {
                background-color: rgba(255, 255, 255, 0.3);
            }
        """)

class MainApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Аналитическое приложение")
        self.setGeometry(100, 100, 1100, 750)
        
        # Центральный виджет
        central_widget = QWidget()
        central_widget.setStyleSheet("background-color: #f8f4e9;")  # Теплый бежевый фон
        self.setCentralWidget(central_widget)
        
        # Основной горизонтальный layout
        main_layout = QHBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # ====== Боковое меню ======
        sidebar = QFrame()
        sidebar.setStyleSheet("background-color: #ffbd8c;")  # Персиковый фон как в ТЗ
        sidebar.setFixedWidth(250)
        
        sidebar_layout = QVBoxLayout(sidebar)
        sidebar_layout.setContentsMargins(0, 20, 0, 20)
        sidebar_layout.setSpacing(5)
        
        # # Заголовок меню
        # header_layout = QHBoxLayout()
        # header_layout.setContentsMargins(25, 0, 25, 25)
        # header_layout.setSpacing(10)
        
        # app_icon = QLabel("📊")
        # app_icon.setStyleSheet("font-size: 28px; color: #5a3921;")
        
        # app_title = QLabel("")
        # app_title.setStyleSheet("""
        #     font-size: 20px; 
        #     font-weight: bold; 
        #     color: #5a3921;
        #     line-height: 1.2;
        # """)
        
        # header_layout.addWidget(app_icon)
        # header_layout.addWidget(app_title)
        # header_layout.addStretch()
        
        # Добавляем заголовок в layout
        # sidebar_layout.addLayout(header_layout)
        
        # Кнопки меню с иконками
        menu_items = [
            ("🏠", "Главная", self.show_home),
            ("🔍", "Анализ", self.show_analysis),
            ("📈", "Прогноз", self.show_forecast),
            ("⚙️", "Настройки", self.show_settings),
            ("👤", "Аккаунт", self.show_account)
        ]
        
        self.menu_buttons = []
        for icon, text, handler in menu_items:
            btn = MenuButton(icon, text)
            btn.clicked.connect(handler)
            sidebar_layout.addWidget(btn)
            self.menu_buttons.append(btn)
        
        sidebar_layout.addStretch()
        
        # ====== Контентная область ======
        content_area = QFrame()
        content_area.setStyleSheet("""
            QFrame {
                background-color: #f8f4e9;  /* Теплый бежевый фон */
                border-radius: 15px;
                margin: 15px;
            }
        """)
        
        content_layout = QVBoxLayout(content_area)
        content_layout.setContentsMargins(15, 15, 15, 15)
        
        self.stacked_widget = QStackedWidget()
        self.stacked_widget.setStyleSheet("background: transparent;")
        
        # Добавление экранов
        self.screens = [
            HomeScreen(),
            AnalysisScreen(),
            ForecastScreen(),
            SettingsScreen(),
            AccountScreen()
        ]
        
        for screen in self.screens:
            self.stacked_widget.addWidget(screen)
        
        content_layout.addWidget(self.stacked_widget)
        
        # ====== Сборка интерфейса ======
        main_layout.addWidget(sidebar)
        main_layout.addWidget(content_area, 1)
        
        # Установка начального экрана
        self.show_home()
        self.highlight_button(0)
    
    def highlight_button(self, index):
        """Визуальное выделение активной кнопки меню"""
        for i, btn in enumerate(self.menu_buttons):
            if i == index:
                # Активное состояние с мягкой подсветкой
                btn.setStyleSheet("""
                    QPushButton {
                        background-color: rgba(255, 255, 255, 0.3);
                        border-left: 4px solid #e67e22;
                        border-radius: 10px;
                        text-align: left;
                        border: none;
                        padding: 5px 10px;
                    }
                    QLabel {
                        color: #2c1810;
                        font-weight: bold;
                    }
                """)
            else:
                # Неактивное состояние
                btn.setStyleSheet("""
                    QPushButton {
                        text-align: left;
                        border: none;
                        border-radius: 10px;
                        background-color: transparent;
                        padding: 5px 10px;
                    }
                    QPushButton:hover {
                        background-color: rgba(255, 255, 255, 0.2);
                    }
                    QPushButton:pressed {
                        background-color: rgba(255, 255, 255, 0.3);
                    }
                    QLabel {
                        color: #5a3921;
                        font-weight: 500;
                    }
                """)
    
    # Методы переключения экранов
    def show_home(self):
        self.stacked_widget.setCurrentIndex(0)
        self.highlight_button(0)
    
    def show_analysis(self):
        self.stacked_widget.setCurrentIndex(1)
        self.highlight_button(1)
    
    def show_forecast(self):
        self.stacked_widget.setCurrentIndex(2)
        self.highlight_button(2)
    
    def show_settings(self):
        self.stacked_widget.setCurrentIndex(3)
        self.highlight_button(3)
    
    def show_account(self):
        self.stacked_widget.setCurrentIndex(4)
        self.highlight_button(4)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    # Установка глобального шрифта
    font = QFont("Segoe UI", 11)
    app.setFont(font)
    
    window = MainApp()
    window.show()
    sys.exit(app.exec())