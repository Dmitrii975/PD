# -*- coding: utf-8 -*-
import sys
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                           QHBoxLayout, QPushButton, QStackedWidget, QFrame, QLabel,
                           QLineEdit, QSpacerItem, QSizePolicy, QScrollArea, QInputDialog, 
                           QDialog, QFormLayout, QFileDialog, QGridLayout, QComboBox, QDoubleSpinBox,
                           QAbstractSpinBox)
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QFont, QPalette, QColor
from server import *
from vars import *
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import numpy as np



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
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(20, 20, 20, 20)
        
        # Хедер с заголовком и кнопкой
        header_layout = QHBoxLayout()
        title = QLabel("Главная")
        title.setStyleSheet("font-size: 24px; color: #5a3921; font-weight: bold;")
        header_layout.addWidget(title)
        header_layout.addStretch()
        
        add_btn = QPushButton("Добавить")
        add_btn.setFixedHeight(35)
        add_btn.setStyleSheet("""
            QPushButton {
                background-color: #ffbd8c;
                color: #5a3921;
                border: none;
                border-radius: 8px;
                font-size: 14px;
                font-weight: bold;
                padding: 0 15px;
            }
            QPushButton:hover {
                background-color: #ffa56a;
            }
        """)
        add_btn.clicked.connect(self.get_data_for_item)
        header_layout.addWidget(add_btn)
        
        main_layout.addLayout(header_layout)
        
        # Список складов в QScrollArea
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setStyleSheet("background: transparent; border: none;")
        
        self.scroll_content = QWidget()
        self.scroll_layout = QVBoxLayout(self.scroll_content)
        self.scroll_layout.setContentsMargins(10, 10, 10, 10)
        self.scroll_layout.setSpacing(10)
        self.scroll_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        
        self.scroll_area.setWidget(self.scroll_content)
        main_layout.addWidget(self.scroll_area)
        
        # Изначально список пустой
        self.warehouses = []

    def add_warehouse(self):
        """Открывает диалог для добавления нового склада"""
        dialog = QDialog(self)
        dialog.setWindowTitle("Добавить склад")
        dialog.setFixedSize(350, 200)
        
        main_layout = QVBoxLayout(dialog)
        main_layout.setContentsMargins(15, 15, 15, 15)
        
        # Используем QGridLayout вместо QFormLayout для лучшего контроля
        grid = QGridLayout()
        grid.setSpacing(10)
        
        # Имя склада
        name_label = QLabel("Имя склада:")
        name_label.setStyleSheet("font-weight: normal;")
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Введите имя склада")
        grid.addWidget(name_label, 0, 0)
        grid.addWidget(self.name_input, 0, 1, 1, 2)  # Занимает 2 колонки
        
        # Файл данных
        file_label = QLabel("Файл данных:")
        file_label.setStyleSheet("font-weight: normal;")
        self.file_path = QLineEdit()
        self.file_path.setPlaceholderText("Выберите файл")
        self.file_path.setReadOnly(True)
        
        browse_btn = QPushButton("Обзор...")
        browse_btn.setFixedWidth(80)
        browse_btn.clicked.connect(self.browse_file)
        
        grid.addWidget(file_label, 1, 0)
        grid.addWidget(self.file_path, 1, 1)
        grid.addWidget(browse_btn, 1, 2)
        
        main_layout.addLayout(grid)
        
        # Кнопки
        button_layout = QHBoxLayout()
        cancel_btn = QPushButton("Отмена")
        cancel_btn.setStyleSheet("""
            QPushButton {
                background-color: #e0e0e0;
                border: none;
                border-radius: 5px;
                padding: 5px 15px;
            }
            QPushButton:hover {
                background-color: #d0d0d0;
            }
        """)
        cancel_btn.clicked.connect(dialog.reject)
        
        add_btn = QPushButton("Добавить")
        add_btn.setStyleSheet("""
            QPushButton {
                background-color: #27ae60;
                color: white;
                border: none;
                border-radius: 5px;
                padding: 5px 15px;
            }
            QPushButton:hover {
                background-color: #219955;
            }
        """)
        add_btn.clicked.connect(lambda: self.add_item_with_data(
            self.name_input.text().strip(),
            self.file_path.text().strip()
        ))
        add_btn.clicked.connect(dialog.accept)
        
        button_layout.addStretch()
        button_layout.addWidget(cancel_btn)
        button_layout.addWidget(add_btn)
        
        main_layout.addLayout(button_layout)
        
        dialog.exec()

    def browse_file(self):
        """Открывает проводник для выбора файла"""
        file_path, _ = QFileDialog.getOpenFileName(
            self, 
            "Выберите файл", 
            "", 
            "CSV Files (*.csv);;Excel Files (*.xlsx);;All Files (*)"
        )
        if file_path:
            self.file_path.setText(file_path)

    def add_item_with_data(self, name, file_path, load_percentage=None, is_active=False, status_text=""):
        """
        Добавляет элемент в список складов с переданными данными
        
        Параметры:
        - name: имя склада
        - file_path: путь к файлу
        - load_percentage: загруженность в процентах (опционально)
        - is_active: активен ли склад (опционально)
        - status_text: текст статуса (опционально)
        """
        if not name:
            return
            
        # Создаем элемент списка
        item = QWidget()
        item.setStyleSheet("""
            QWidget {
                background-color: #ffbd8c;
                border-radius: 8px;
                border: 1px solid #e67e22;
            }
        """)
        item.setFixedHeight(55)
        
        layout = QHBoxLayout(item)
        layout.setContentsMargins(15, 0, 15, 0)
        layout.setSpacing(15)
        
        # Имя склада
        name_label = QLabel(name)
        name_label.setStyleSheet("""
            font-weight: bold; 
            color: #5a3921; 
            font-size: 14px; 
            background: transparent;
            border: none;
            outline: none;
        """)
        layout.addWidget(name_label)
        
        # Вертикальная разделительная линия
        separator = QFrame()
        separator.setFrameShape(QFrame.Shape.VLine)
        separator.setFrameShadow(QFrame.Shadow.Sunken)
        separator.setStyleSheet("color: #e67e22;")
        separator.setFixedWidth(1)
        layout.addWidget(separator)
        
        # Загруженность
        load_text = f"Загруженность: {load_percentage}%" if load_percentage is not None else "Загруженность: --"
        load_label = QLabel(load_text)
        load_label.setStyleSheet("""
            color: #5a3921; 
            font-size: 14px;
            background: transparent;
            border: none;
            outline: none;
        """)
        layout.addWidget(load_label)
        
        # Растягиваемое пространство для прижатия статуса вправо
        layout.addStretch()
        
        # Статус (справа)
        if status_text:
            status_label = QLabel(status_text)
            status_label.setStyleSheet("""
                color: #e74c3c; 
                font-weight: bold; 
                font-size: 14px;
                background: transparent;
                border: none;
                outline: none;
            """)
            layout.addWidget(status_label)
        
        self.scroll_layout.addWidget(item)
        
        # Сохраняем данные склада
        warehouse = {
            "name": name,
            "file_path": file_path,
            "item": item,
            "status_label": status_label if status_text else None,
            "load_label": load_label,
            "is_active": is_active
        }
        self.warehouses.append(warehouse)
        return warehouse

    def get_data_for_item(self):
        """Заглушка для получения данных (будет заменена на реальную логику)"""
        import random
        # Генерируем рандомные данные для тестирования
        name = f"Склад-{random.randint(1, 100)}"
        load = random.randint(0, 100)
        is_active = random.choice([True, False])
        status = "Требуется действие!" if is_active else ""
        
        # Добавляем новый элемент с рандомными данными
        self.add_item_with_data(
            name=name,
            file_path="",
            load_percentage=load,
            is_active=is_active,
            status_text=status
        )

class AnalysisScreen(QWidget):
    def __init__(self):
        super().__init__()
        self.setStyleSheet("background-color: #fffaf0; border-radius: 15px;")
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(15, 15, 15, 15)
        main_layout.setSpacing(10)
        
        # Заголовок
        title = QLabel("Анализ & Прогноз")
        title.setStyleSheet("font-size: 24px; color: #5a3921; font-weight: bold;")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(title)
        
        # Выбор склада
        self.warehouse_combo = QComboBox()
        self.warehouse_combo.setStyleSheet("""
            QComboBox {
                background-color: white;
                border: 1px solid #e67e22;
                border-radius: 8px;
                padding: 8px 15px;
                font-size: 14px;
                color: #5a3921;
            }
            QComboBox::drop-down {
                width: 30px;
                border-left: 1px solid #e67e22;
            }
            QComboBox QAbstractItemView {
                background-color: white;
                border: 1px solid #e67e22;
                selection-background-color: #ffbd8c;
            }
        """)
        self.warehouse_items = [f"Склад {i}" for i in range(1, 6)]  # можно заменить на реальные данные
        
        # Добавляем "Выберите склад" только если есть склады
        if self.warehouse_items:
            self.warehouse_combo.addItems(["Выберите склад"] + self.warehouse_items)
        else:
            self.warehouse_combo.addItem("Нет складов")
            self.warehouse_combo.setEnabled(False)

        self.warehouse_combo.currentIndexChanged.connect(self.update_data)
        main_layout.addWidget(self.warehouse_combo)
        
        # Контейнер для графика
        self.graph_container = QFrame()
        self.graph_container.setStyleSheet("""
            QFrame {
                background-color: #ffbd8c;
                border-radius: 10px;
                margin: 10px;
                padding: 10px;
            }
        """)
        self.graph_container.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        graph_layout = QVBoxLayout(self.graph_container)
        
        # График
        self.figure = Figure(figsize=(5, 4), dpi=100)
        self.canvas = FigureCanvas(self.figure)
        self.canvas.setStyleSheet("background-color: #ffbd8c; border-radius: 8px;")
        self.canvas.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        graph_layout.addWidget(self.canvas)
        
        # Статистика
        self.stats_container = QFrame()
        self.stats_container.setStyleSheet("""
            QFrame {
                background-color: #ffbd8c;
                border-radius: 10px;
                margin: 10px;
                padding: 8px;
            }
        """)
        self.stats_container.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)
        stats_layout = QGridLayout(self.stats_container)
        stats_layout.setSpacing(5)
        stats_layout.setContentsMargins(5, 5, 5, 5)
        
        self.stats_blocks = []
        stats_items = [
            ("Загруженность", ""),
            ("Товары на складе", ""),
            ("Свободное место", ""),
            ("Последняя проверка", "")
        ]
        
        for i, (label, _) in enumerate(stats_items):
            row = i // 2
            col = i % 2
            
            block = QFrame()
            block.setStyleSheet("""
                QFrame {
                    background-color: #ffe0c0;
                    border: 1px solid #e67e22;
                    border-radius: 5px;
                    padding: 2px 5px;
                }
            """)
            block_layout = QHBoxLayout(block)
            block_layout.setContentsMargins(0, 0, 0, 0)
            block_layout.setSpacing(8)
            
            label_widget = QLabel(label)
            label_widget.setStyleSheet("font-weight: bold; color: #5a3921; font-size: 11px;")
            block_layout.addWidget(label_widget)
            block_layout.addStretch()
            
            value_widget = QLabel("--")
            value_widget.setStyleSheet("color: #5a3921; font-size: 11px; font-weight: bold;")
            block_layout.addWidget(value_widget)
            
            stats_layout.addWidget(block, row, col)
            self.stats_blocks.append((block, label_widget, value_widget))
        
        stats_layout.addWidget(QLabel(), 2, 0, 1, 2)
        
        # Добавляем виджеты в макет только если есть склады
        if self.warehouse_items:
            main_layout.addWidget(self.graph_container, 4)
            main_layout.addWidget(self.stats_container, 1)
            # Выбираем первый склад по умолчанию (индекс 1, т.к. "Выберите склад" на 0)
            self.warehouse_combo.setCurrentIndex(1)
            self.update_data()
        else:
            # Если складов нет — не добавляем график и статистику
            pass

    def plot_sine_wave(self):
        """Создает график синусоиды"""
        self.figure.clear()
        ax = self.figure.add_subplot(111)
        
        # Настройка отступов графика
        self.figure.subplots_adjust(left=0.08, right=0.95, top=0.85, bottom=0.15)
        
        # Генерация данных
        x = np.linspace(0, 2 * np.pi, 100)
        y = np.sin(x) * 500 + 500  # Нормализуем для диапазона 0-1000
        
        # Настройка графика
        ax.plot(x, y, 'o-', color='#e67e22', linewidth=2, markersize=6)
        ax.set_xlabel('Время', fontsize=12, color='#5a3921')
        ax.set_ylabel('Единицы', fontsize=12, color='#5a3921')
        ax.grid(False)
        
        # Полностью персиковый фон графика
        ax.set_facecolor('#ffbd8c')
        self.figure.patch.set_facecolor('#ffbd8c')
        
        ax.set_yticks([0, 250, 500, 750, 1000])
        ax.set_xticks(np.linspace(0, 2 * np.pi, 10))
        ax.set_xticklabels([f"{i:.1f}" for i in np.linspace(0, 2 * np.pi, 10)])
        
        # Стилизация осей
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['left'].set_color('#e67e22')
        ax.spines['bottom'].set_color('#e67e22')
        
        # Обновляем холст
        self.canvas.draw()

    def update_data(self):
        index = self.warehouse_combo.currentIndex()
        
        # Если выбрана "заглушка" или список пуст — скрываем данные
        if index == 0 or not self.warehouse_items:
            for _, _, value_widget in self.stats_blocks:
                value_widget.setText("--")
            # Опционально: очистить график
            self.figure.clear()
            self.canvas.draw()
            return
        
        # Реальные данные для склада
        warehouse_index = index - 1  # индекс в warehouse_items
        stats_data = {
            "Загруженность": f"{70 + warehouse_index * 5}%",
            "Товары на складе": f"{1000 + warehouse_index * 100} шт.",
            "Свободное место": f"{30 - warehouse_index * 5}%",
            "Последняя проверка": "15.12.2025"
        }
        
        for block, label_widget, value_widget in self.stats_blocks:
            key = label_widget.text()
            if key in stats_data:
                value_widget.setText(stats_data[key])
        
        self.plot_sine_wave()

class Wall(QWidget):
    def __init__(self):
        super().__init__()
        self.setStyleSheet("background-color: #fffaf0;")
        
        # Основной layout
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(10)
        
        # Заголовок
        title = QLabel("Объявления")
        title.setStyleSheet("font-size: 24px; font-weight: bold; color: #5a3921;")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(title)
        
        # Создаем прокручиваемую область
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setStyleSheet("background: transparent; border: none;")
        main_layout.addWidget(scroll_area)
        
        # Контейнер для объявлений
        container = QWidget()
        container_layout = QVBoxLayout(container)
        container_layout.setContentsMargins(0, 0, 0, 0)
        container_layout.setSpacing(10)
        
        # Данные объявлений
        announcements = [
            ["Компания 1", "50", "3 дня"],
            ["Компания 2", "200", "5 дней"],
            ["Склад-партнер", "150", "2 дня"],
            ["Логистик-Хаб", "300", "7 дней"],
            ["Доп. Компания", "75", "1 день"],
            ["Еще одна", "250", "4 дня"],
            ["Тестовая", "100", "6 дней"],
            ["Пример", "400", "2 дня"]
        ]
        
        # Создание блоков объявлений
        for announcement in announcements:
            block = QWidget()
            block.setStyleSheet("""
                QWidget {
                    background-color: #ffbd8c;
                    border-radius: 8px;
                    margin: 5px;
                }
            """)
            block.setFixedHeight(55)  # Фиксированная высота для каждого блока
            
            block_layout = QHBoxLayout(block)
            block_layout.setContentsMargins(15, 5, 15, 5)
            block_layout.setSpacing(15)
            
            # Название компании
            company_label = QLabel(announcement[0])
            company_label.setStyleSheet("font-size: 16px; font-weight: bold; color: #5a3921;")
            company_label.setFixedWidth(150)
            
            # Информация в одной строке
            info_layout = QHBoxLayout()
            info_layout.setSpacing(15)
            info_layout.setContentsMargins(0, 0, 0, 0)
            
            # Количество излишков
            quantity_label = QLabel(f"Кол-во: {announcement[1]} е.т")
            quantity_label.setStyleSheet("font-size: 14px; font-weight: bold; color: #5a3921;")
            
            # Вертикальная разделительная линия
            separator = QFrame()
            separator.setFrameShape(QFrame.Shape.VLine)
            separator.setFrameShadow(QFrame.Shadow.Sunken)
            separator.setStyleSheet("color: #e67e22;")
            separator.setFixedWidth(1)
            
            # Срок доставки
            delivery_label = QLabel(f"Срок: {announcement[2]} дн.")
            delivery_label.setStyleSheet("font-size: 14px; font-weight: bold; color: #5a3921;")
            
            info_layout.addWidget(quantity_label)
            info_layout.addWidget(separator)
            info_layout.addWidget(delivery_label)
            
            # Кнопка оформления
            order_btn = QPushButton("Оформить")
            order_btn.setStyleSheet("""
                QPushButton {
                    background-color: #2c3e50; 
                    color: white; 
                    border-radius: 5px; 
                    padding: 8px 15px;
                    font-weight: bold;
                    min-width: 100px;
                }
                QPushButton:hover {
                    background-color: #34495e;
                }
            """)
            
            block_layout.addWidget(company_label)
            block_layout.addStretch()
            block_layout.addLayout(info_layout)
            block_layout.addWidget(order_btn)
            
            container_layout.addWidget(block)
        
        # Добавляем растягивающийся элемент в конец
        container_layout.addStretch()
        
        scroll_area.setWidget(container)

class SettingsScreen(QWidget):
    def __init__(self):
        super().__init__()
        self.setStyleSheet("background-color: #fffaf0; border-radius: 15px;")
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(10)
        
        # Заголовок
        title = QLabel("⚙️ Настройки приложения")
        title.setStyleSheet("font-size: 24px; color: #5a3921; font-weight: bold;")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(title)
        
        # Данные настроек
        settings_list = [
            ["Максимальная загрузка склада", 85.5],
            ["Порог уведомления", 90.0],
            ["Частота обновления данных (мин)", 5.0],
            ["Минимальное свободное место", 10.0],
            ["Срок хранения данных (дней)", 30.0]
        ]
        
        # Создание блоков настроек
        for name, value in settings_list:
            setting_container = QFrame()
            setting_container.setStyleSheet("""
                QFrame {
                    background-color: #ffbd8c;
                    border-radius: 8px;
                    margin: 3px;
                    padding: 8px;
                }
            """)
            setting_layout = QHBoxLayout(setting_container)
            setting_layout.setContentsMargins(5, 5, 5, 5)
            setting_layout.setSpacing(10)
            
            # Название настройки
            label = QLabel(name)
            label.setStyleSheet("font-size: 13px; color: #5a3921;")
            label.setFixedWidth(220)
            
            # Поле ввода числа (без кнопок-спиннеров)
            spinbox = QDoubleSpinBox()
            spinbox.setButtonSymbols(QAbstractSpinBox.ButtonSymbols.NoButtons)
            spinbox.setValue(value)
            spinbox.setRange(0, 1000)
            spinbox.setSingleStep(0.5)
            spinbox.setStyleSheet("""
                QDoubleSpinBox {
                    background-color: white;
                    border: 1px solid #e67e22;
                    border-radius: 5px;
                    padding: 4px 10px;
                    font-size: 13px;
                    color: #5a3921;
                }
                QDoubleSpinBox:focus {
                    border-color: #d35400;
                }
            """)
            spinbox.editingFinished.connect(lambda n=name, sb=spinbox: self.setting_changed(n, sb.value()))
            
            setting_layout.addWidget(label)
            setting_layout.addWidget(spinbox)
            setting_layout.addStretch()
            
            main_layout.addWidget(setting_container)
        
        # Добавляем растягивающийся элемент перед кнопкой
        main_layout.addStretch()
        
        # Кнопка "Добавить день" внизу слева
        add_day_btn = QPushButton("Добавить день")
        add_day_btn.setStyleSheet("""
            QPushButton {
                background-color: #e0e0e0;
                color: #5a3921;
                border: 1px solid #c0c0c0;
                border-radius: 5px;
                padding: 8px 15px;
                font-weight: bold;
                min-width: 120px;
            }
            QPushButton:hover {
                background-color: #d0d0d0;
            }
        """)
        add_day_btn.clicked.connect(self.add_day)
        
        btn_layout = QHBoxLayout()
        btn_layout.addWidget(add_day_btn)
        btn_layout.addStretch()
        
        main_layout.addLayout(btn_layout)

    def setting_changed(self, name, value):
        """Обработчик изменения настройки (срабатывает после завершения редактирования)"""
        print(f"Изменение сохранено: {name} = {value}")
    
    def add_day(self):
        """Заглушка для кнопки 'Добавить день'"""
        print("Добавлен новый день")

class AccountScreen(QWidget):
    def __init__(self):
        super().__init__()
        self.setStyleSheet("background-color: #fffaf0; border-radius: 15px;")
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(15)
        
        # Заголовок
        title = QLabel("Информация о пользователе")
        title.setStyleSheet("font-size: 24px; color: #5a3921; font-weight: bold;")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(title)
        
        # Контейнер для полей
        form_container = QFrame()
        form_container.setStyleSheet("""
            QFrame {
                background-color: #ffbd8c;
                border-radius: 10px;
                margin: 15px;
                padding: 20px;
            }
        """)
        form_layout = QVBoxLayout(form_container)
        form_layout.setContentsMargins(10, 10, 10, 10)
        form_layout.setSpacing(25)
        
        # Наименование компании
        company_layout = QHBoxLayout()
        company_layout.setSpacing(15)
        
        company_label = QLabel("Наименование компании:")
        company_label.setStyleSheet("color: #5a3921; font-size: 18px; font-weight: bold; padding-left: 5px;")
        company_label.setFixedWidth(350)  # Увеличена ширина метки
        
        self.company_input = QLineEdit("ООО 'Склад-Партнер'")
        self.company_input.setReadOnly(True)
        self.company_input.setStyleSheet("""
            QLineEdit {
                background-color: white;
                border: 1px solid #e67e22;
                border-radius: 5px;
                padding: 10px 15px;
                font-size: 16px;
                color: #5a3921;
            }
        """)
        self.company_input.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        self.company_input.setFixedHeight(40)
        
        company_layout.addWidget(company_label)
        company_layout.addWidget(self.company_input)
        
        # Электронная почта
        email_layout = QHBoxLayout()
        email_layout.setSpacing(15)
        
        email_label = QLabel("Электронная почта:")
        email_label.setStyleSheet("color: #5a3921; font-size: 18px; font-weight: bold; padding-left: 5px;")
        email_label.setFixedWidth(350)  # Увеличена ширина метки
        
        self.email_input = QLineEdit("user@example.com")
        self.email_input.setReadOnly(True)
        self.email_input.setStyleSheet("""
            QLineEdit {
                background-color: white;
                border: 1px solid #e67e22;
                border-radius: 5px;
                padding: 10px 15px;
                font-size: 16px;
                color: #5a3921;
            }
        """)
        self.email_input.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        self.email_input.setFixedHeight(40)
        
        email_layout.addWidget(email_label)
        email_layout.addWidget(self.email_input)
        
        form_layout.addLayout(company_layout)
        form_layout.addLayout(email_layout)
        
        # Добавляем растягивающийся элемент перед кнопками
        form_layout.addStretch()
        
        # Кнопки управления
        button_layout = QHBoxLayout()
        button_layout.setSpacing(10)
        button_layout.setContentsMargins(10, 10, 10, 10)
        
        # Добавляем растягивающийся элемент для прижатия кнопок к правому краю
        button_layout.addStretch()
        
        # Кнопки в нужном порядке
        delete_account_btn = QPushButton("Удалить аккаунт")
        delete_account_btn.setStyleSheet("""
            QPushButton {
                background-color: #f0f0f0;
                color: #e74c3c;
                border: 1px solid #e0e0e0;
                border-radius: 5px;
                padding: 12px 20px;
                font-weight: bold;
                font-size: 14px;
                min-width: 140px;
            }
            QPushButton:hover {
                background-color: #e0e0e0;
                color: #c0392b;
            }
        """)
        
        logout_btn = QPushButton("Выйти из аккаунта")
        logout_btn.setStyleSheet("""
            QPushButton {
                background-color: #e0e0e0;
                color: #5a3921;
                border: 1px solid #c0c0c0;
                border-radius: 5px;
                padding: 12px 20px;
                font-weight: bold;
                font-size: 14px;
                min-width: 140px;
            }
            QPushButton:hover {
                background-color: #d0d0d0;
            }
        """)
        
        clear_data_btn = QPushButton("Очистить данные")
        clear_data_btn.setStyleSheet("""
            QPushButton {
                background-color: #f0f0f0;
                color: #e67e22;
                border: 1px solid #e0e0e0;
                border-radius: 5px;
                padding: 12px 20px;
                font-weight: bold;
                font-size: 14px;
                min-width: 140px;
            }
            QPushButton:hover {
                background-color: #e0e0e0;
                color: #d35400;
            }
        """)
        
        change_pass_btn = QPushButton("Сменить пароль")
        change_pass_btn.setStyleSheet("""
            QPushButton {
                background-color: #e0e0e0;
                color: #5a3921;
                border: 1px solid #c0c0c0;
                border-radius: 5px;
                padding: 12px 20px;
                font-weight: bold;
                font-size: 14px;
                min-width: 140px;
            }
            QPushButton:hover {
                background-color: #d0d0d0;
            }
        """)
        
        # Добавляем кнопки в нужном порядке
        
        button_layout.addWidget(change_pass_btn)
        button_layout.addWidget(clear_data_btn)
        button_layout.addWidget(logout_btn)
        button_layout.addWidget(delete_account_btn)

        form_layout.addLayout(button_layout)
        
        main_layout.addWidget(form_container)

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
        
        # Кнопки меню с иконками (изменены на соответствие фото)
        menu_items = [
            ("🏠", "Главная", self.show_home),
            ("🔍📈", "Анализ & Прогноз", self.show_analysis),
            ("📢", "Объявление", self.show_forecast),
            ("👤", "Аккаунт", self.show_account),
            ("⚙️", "Настройки", self.show_settings)
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
            Wall(),
            AccountScreen(),
            SettingsScreen()
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
    
    def show_account(self):
        self.stacked_widget.setCurrentIndex(3)
        self.highlight_button(3)

    def show_settings(self):
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

    get_warehouses_list()
    check_data_loaded()
    get_ob()

    app = QApplication(sys.argv)
    
    # Установка глобального шрифта
    font = QFont("Segoe UI", 11)
    app.setFont(font)
    
    window = MainApp()
    window.show()
    sys.exit(app.exec())