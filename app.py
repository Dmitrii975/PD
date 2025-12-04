# -*- coding: utf-8 -*-
import sys
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                           QHBoxLayout, QPushButton, QStackedWidget, QFrame, QLabel,
                           QLineEdit, QSpacerItem, QSizePolicy)
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QFont, QPalette, QColor

class LoginScreen(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setStyleSheet("background-color: #f8f4e9;")
        
        # Главный layout для центрирования
        main_layout = QVBoxLayout()
        main_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.setContentsMargins(0, 0, 0, 0)
        
        # Контейнер для формы
        form_container = QFrame()
        form_container.setStyleSheet("""
            QFrame {
                background-color: #fffaf0;
                border-radius: 15px;
                padding: 30px;
            }
        """)
        form_container.setFixedWidth(400)  # Фиксированная ширина для оптимального размера
        
        form_layout = QVBoxLayout(form_container)
        form_layout.setSpacing(20)
        form_layout.setContentsMargins(20, 20, 20, 20)
        
        # Заголовок
        title = QLabel("Вход в аккаунт")
        title.setStyleSheet("font-size: 24px; font-weight: bold; color: #5a3921;")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        # Поля ввода с placeholder вместо лейблов
        self.email_input = QLineEdit()
        self.email_input.setFixedHeight(45)
        self.email_input.setPlaceholderText("Электронная почта")
        self.email_input.setStyleSheet("""
            QLineEdit {
                padding: 8px 15px;
                border: 2px solid #ffbd8c;
                border-radius: 8px;
                font-size: 14px;
                background-color: white;
                color: #5a3921;
            }
            QLineEdit:focus {
                border-color: #e67e22;
                background-color: #fffdfa;
            }
            QLineEdit::placeholder {
                color: #b09c85;
                font-style: italic;
            }
        """)
        
        self.password_input = QLineEdit()
        self.password_input.setFixedHeight(45)
        self.password_input.setPlaceholderText("Пароль")
        self.password_input.setStyleSheet("""
            QLineEdit {
                padding: 8px 15px;
                border: 2px solid #ffbd8c;
                border-radius: 8px;
                font-size: 14px;
                background-color: white;
                color: #5a3921;
            }
            QLineEdit:focus {
                border-color: #e67e22;
                background-color: #fffdfa;
            }
            QLineEdit::placeholder {
                color: #b09c85;
                font-style: italic;
            }
        """)
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        
        # Забыли пароль?
        forgot_password = QPushButton("Забыли пароль?")
        forgot_password.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                color: #7f8c8d;
                border: none;
                font-size: 13px;
                text-align: right;
                padding: 0;
            }
            QPushButton:hover {
                color: #e74c3c;
                text-decoration: underline;
            }
        """)
        forgot_password.setCursor(Qt.CursorShape.PointingHandCursor)
        
        # Кнопка входа
        login_btn = QPushButton("Войти")
        login_btn.setFixedHeight(48)
        login_btn.setStyleSheet("""
            QPushButton {
                background-color: #e67e22;
                color: white;
                border: none;
                border-radius: 8px;
                font-size: 16px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #d35400;
            }
            QPushButton:pressed {
                background-color: #c0392b;
            }
        """)
        login_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        
        # Кнопки переключения
        button_container = QHBoxLayout()
        button_container.setContentsMargins(0, 0, 0, 0)
        
        register_btn = QPushButton("Регистрация")
        register_btn.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                color: #5a3921;
                border: none;
                font-size: 14px;
                text-decoration: underline;
            }
            QPushButton:hover {
                color: #e67e22;
            }
        """)
        register_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        
        separator = QLabel("•")
        separator.setStyleSheet("color: #bdc3c7; font-size: 16px;")
        
        skip_btn = QPushButton("Пропустить")
        skip_btn.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                color: #7f8c8d;
                border: none;
                font-size: 14px;
                text-decoration: underline;
            }
            QPushButton:hover {
                color: #e74c3c;
            }
        """)
        skip_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        
        button_container.addWidget(register_btn)
        button_container.addWidget(separator)
        button_container.addWidget(skip_btn)
        button_container.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        # Сборка интерфейса
        form_layout.addWidget(title)
        form_layout.addWidget(self.email_input)
        form_layout.addWidget(self.password_input)
        form_layout.addWidget(forgot_password, alignment=Qt.AlignmentFlag.AlignRight)
        form_layout.addWidget(login_btn)
        form_layout.addLayout(button_container)
        
        main_layout.addWidget(form_container, alignment=Qt.AlignmentFlag.AlignCenter)
        self.setLayout(main_layout)
        
        # Сигналы
        login_btn.clicked.connect(parent.show_main_interface if parent else None)
        register_btn.clicked.connect(parent.show_register_screen if parent else None)
        skip_btn.clicked.connect(parent.show_main_interface if parent else None)
        forgot_password.clicked.connect(self.show_forgot_password)

    def show_forgot_password(self):
        """Заглушка для функции восстановления пароля"""
        print("Восстановление пароля")

class RegisterScreen(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setStyleSheet("background-color: #f8f4e9;")
        
        # Главный layout для центрирования
        main_layout = QVBoxLayout()
        main_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.setContentsMargins(0, 0, 0, 0)
        
        # Контейнер для формы
        form_container = QFrame()
        form_container.setStyleSheet("""
            QFrame {
                background-color: #fffaf0;
                border-radius: 15px;
                padding: 30px;
            }
        """)
        form_container.setFixedWidth(400)  # Фиксированная ширина для оптимального размера
        
        form_layout = QVBoxLayout(form_container)
        form_layout.setSpacing(20)
        form_layout.setContentsMargins(20, 20, 20, 20)
        
        # Заголовок
        title = QLabel("Регистрация")
        title.setStyleSheet("font-size: 24px; font-weight: bold; color: #5a3921;")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        # Поля ввода с placeholder вместо лейблов
        self.email_input = QLineEdit()
        self.email_input.setFixedHeight(45)
        self.email_input.setPlaceholderText("Электронная почта")
        self.email_input.setStyleSheet("""
            QLineEdit {
                padding: 8px 15px;
                border: 2px solid #ffbd8c;
                border-radius: 8px;
                font-size: 14px;
                background-color: white;
                color: #5a3921;
            }
            QLineEdit:focus {
                border-color: #e67e22;
                background-color: #fffdfa;
            }
            QLineEdit::placeholder {
                color: #b09c85;
                font-style: italic;
            }
        """)
        
        self.password_input = QLineEdit()
        self.password_input.setFixedHeight(45)
        self.password_input.setPlaceholderText("Пароль (минимум 8 символов)")
        self.password_input.setStyleSheet("""
            QLineEdit {
                padding: 8px 15px;
                border: 2px solid #ffbd8c;
                border-radius: 8px;
                font-size: 14px;
                background-color: white;
                color: #5a3921;
            }
            QLineEdit:focus {
                border-color: #e67e22;
                background-color: #fffdfa;
            }
            QLineEdit::placeholder {
                color: #b09c85;
                font-style: italic;
            }
        """)
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        
        self.confirm_input = QLineEdit()
        self.confirm_input.setFixedHeight(45)
        self.confirm_input.setPlaceholderText("Подтвердите пароль")
        self.confirm_input.setStyleSheet("""
            QLineEdit {
                padding: 8px 15px;
                border: 2px solid #ffbd8c;
                border-radius: 8px;
                font-size: 14px;
                background-color: white;
                color: #5a3921;
            }
            QLineEdit:focus {
                border-color: #e67e22;
                background-color: #fffdfa;
            }
            QLineEdit::placeholder {
                color: #b09c85;
                font-style: italic;
            }
        """)
        self.confirm_input.setEchoMode(QLineEdit.EchoMode.Password)
        
        # Кнопка регистрации
        register_btn = QPushButton("Зарегистрироваться")
        register_btn.setFixedHeight(48)
        register_btn.setStyleSheet("""
            QPushButton {
                background-color: #27ae60;
                color: white;
                border: none;
                border-radius: 8px;
                font-size: 16px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #219955;
            }
            QPushButton:pressed {
                background-color: #1e8449;
            }
        """)
        register_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        
        # Кнопки переключения
        button_container = QHBoxLayout()
        button_container.setContentsMargins(0, 0, 0, 0)
        
        login_btn = QPushButton("Вход")
        login_btn.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                color: #5a3921;
                border: none;
                font-size: 14px;
                text-decoration: underline;
            }
            QPushButton:hover {
                color: #e67e22;
            }
        """)
        login_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        
        separator = QLabel("•")
        separator.setStyleSheet("color: #bdc3c7; font-size: 16px;")
        
        skip_btn = QPushButton("Пропустить")
        skip_btn.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                color: #7f8c8d;
                border: none;
                font-size: 14px;
                text-decoration: underline;
            }
            QPushButton:hover {
                color: #e74c3c;
            }
        """)
        skip_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        
        button_container.addWidget(login_btn)
        button_container.addWidget(separator)
        button_container.addWidget(skip_btn)
        button_container.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        # Сборка интерфейса
        form_layout.addWidget(title)
        form_layout.addWidget(self.email_input)
        form_layout.addWidget(self.password_input)
        form_layout.addWidget(self.confirm_input)
        form_layout.addWidget(register_btn)
        form_layout.addLayout(button_container)
        
        main_layout.addWidget(form_container, alignment=Qt.AlignmentFlag.AlignCenter)
        self.setLayout(main_layout)
        
        # Сигналы
        register_btn.clicked.connect(parent.show_main_interface if parent else None)
        login_btn.clicked.connect(parent.show_login_screen if parent else None)
        skip_btn.clicked.connect(parent.show_main_interface if parent else None)

class HomeScreen(QWidget):
    def __init__(self):
        super().__init__()
        self.setStyleSheet("background-color: #fffaf0; border-radius: 15px;")
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.setContentsMargins(50, 50, 50, 50)
        
        label = QLabel("🏠 Добро пожаловать на главную страницу!")
        label.setStyleSheet("font-size: 24px; color: #5a3921; font-weight: bold;")
        layout.addWidget(label)
        
        self.setLayout(layout)

class AnalysisScreen(QWidget):
    def __init__(self):
        super().__init__()
        self.setStyleSheet("background-color: #fffaf0; border-radius: 15px;")
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.setContentsMargins(50, 50, 50, 50)
        
        label = QLabel("📊 Страница анализа данных")
        label.setStyleSheet("font-size: 24px; color: #5a3921; font-weight: bold;")
        layout.addWidget(label)
        
        self.setLayout(layout)

class ForecastScreen(QWidget):
    def __init__(self):
        super().__init__()
        self.setStyleSheet("background-color: #fffaf0; border-radius: 15px;")
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.setContentsMargins(50, 50, 50, 50)
        
        label = QLabel("📈 Страница прогнозирования")
        label.setStyleSheet("font-size: 24px; color: #5a3921; font-weight: bold;")
        layout.addWidget(label)
        
        self.setLayout(layout)

class SettingsScreen(QWidget):
    def __init__(self):
        super().__init__()
        self.setStyleSheet("background-color: #fffaf0; border-radius: 15px;")
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.setContentsMargins(50, 50, 50, 50)
        
        label = QLabel("⚙️ Настройки приложения")
        label.setStyleSheet("font-size: 24px; color: #5a3921; font-weight: bold;")
        layout.addWidget(label)
        
        self.setLayout(layout)

class AccountScreen(QWidget):
    def __init__(self):
        super().__init__()
        self.setStyleSheet("background-color: #fffaf0; border-radius: 15px;")
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.setContentsMargins(50, 50, 50, 50)
        
        label = QLabel("👤 Управление аккаунтом")
        label.setStyleSheet("font-size: 24px; color: #5a3921; font-weight: bold;")
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

class MainInterface(QWidget):
    """Основной интерфейс приложения с боковым меню"""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setStyleSheet("background-color: #f8f4e9;")  # Фон основного интерфейса
        
        # Основной горизонтальный layout
        main_layout = QHBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # ====== Боковое меню ======
        sidebar = QFrame()
        sidebar.setStyleSheet("background-color: #ffbd8c;")  # Персиковый фон как в ТЗ
        sidebar.setFixedWidth(250)
        
        sidebar_layout = QVBoxLayout(sidebar)
        sidebar_layout.setContentsMargins(0, 30, 0, 30)
        sidebar_layout.setSpacing(5)
        sidebar_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        
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
                border-radius: 0px;
                margin: 20px;
            }
        """)
        
        content_layout = QVBoxLayout(content_area)
        content_layout.setContentsMargins(1, 15, 1, 15)
        
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

class MainApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Аналитическое приложение")
        self.setGeometry(100, 100, 1100, 750)
        
        # Настройка светлой темы для всего приложения
        self.setup_light_theme()
        
        # Центральный виджет - стек для переключения между экранами входа и основным интерфейсом
        self.central_widget = QStackedWidget()
        self.setCentralWidget(self.central_widget)
        
        # Создание экранов
        self.login_screen = LoginScreen(self)
        self.register_screen = RegisterScreen(self)
        self.main_interface = MainInterface(self)
        
        # Добавление экранов в стек
        self.central_widget.addWidget(self.login_screen)    # index 0
        self.central_widget.addWidget(self.register_screen) # index 1
        self.central_widget.addWidget(self.main_interface)  # index 2
        
        # По умолчанию показываем экран входа
        self.show_login_screen()
    
    def setup_light_theme(self):
        """Настройка светлой темы для всего приложения"""
        palette = QPalette()
        palette.setColor(QPalette.ColorRole.Window, QColor(248, 244, 233))  # #f8f4e9
        palette.setColor(QPalette.ColorRole.WindowText, QColor(89, 57, 33))  # #593921
        palette.setColor(QPalette.ColorRole.Base, QColor(255, 250, 240))  # #fffaf0
        palette.setColor(QPalette.ColorRole.AlternateBase, QColor(245, 240, 227))
        palette.setColor(QPalette.ColorRole.ToolTipBase, QColor(255, 255, 255))
        palette.setColor(QPalette.ColorRole.ToolTipText, QColor(89, 57, 33))
        palette.setColor(QPalette.ColorRole.Text, QColor(89, 57, 33))
        palette.setColor(QPalette.ColorRole.Button, QColor(255, 255, 255))
        palette.setColor(QPalette.ColorRole.ButtonText, QColor(89, 57, 33))
        palette.setColor(QPalette.ColorRole.BrightText, QColor(255, 0, 0))
        palette.setColor(QPalette.ColorRole.Highlight, QColor(230, 126, 34))  # #e67e22
        palette.setColor(QPalette.ColorRole.HighlightedText, QColor(255, 255, 255))
        
        # Установка палитры для всего приложения
        QApplication.setPalette(palette)
        
        # Установка стиля виджетов
        QApplication.setStyle("Fusion")
    
    def show_login_screen(self):
        self.central_widget.setCurrentIndex(0)
    
    def show_register_screen(self):
        self.central_widget.setCurrentIndex(1)
    
    def show_main_interface(self):
        self.central_widget.setCurrentIndex(2)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    # Установка глобального шрифта
    font = QFont("Segoe UI", 11)
    app.setFont(font)
    
    window = MainApp()
    window.show()
    sys.exit(app.exec())