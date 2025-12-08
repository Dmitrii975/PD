# -*- coding: utf-8 -*-
import sys
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                           QHBoxLayout, QPushButton, QStackedWidget, QFrame, QLabel,
                           QLineEdit, QSpacerItem, QSizePolicy, QScrollArea, QInputDialog, 
                           QDialog, QFormLayout, QFileDialog, QGridLayout, QComboBox, QDoubleSpinBox,
                           QAbstractSpinBox, QMessageBox)
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QFont, QPalette, QColor, QPixmap
from server import *
from vars import *
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import numpy as np
import pandas as pd
from analys import calculate_metrics, make_plot
import pickle
import os
import hashlib


WAREHOUSES = []

USER_ID = None
UH = None

def set_user_id(uid):
    global USER_ID, UH

    USER_ID = uid
    UH = hashlib.md5(str(uid).encode('utf-8')).hexdigest()

def get_user_id():
    return USER_ID

def get_hash():
    return UH

def add_warehouse(data):
    """Добавляет склад в глобальный список"""
    # Проверяем, нет ли уже склада с таким именем
    for i, existing in enumerate(WAREHOUSES):
        if existing.get('name') == data.get('name'):
            # Обновляем существующий
            WAREHOUSES[i] = data
            return
    
    # Добавляем новый
    WAREHOUSES.append(data)

def get_warehouses():
    """Возвращает копию списка складов"""
    return WAREHOUSES.copy()

def read_warehouses():
    if os.path.exists(f'.cache/{get_hash()}/warehouses.pickle'):
        with open(f'.cache/{get_hash()}/warehouses.pickle', 'rb') as f:
            data = pickle.load(f)
        for i in data:
            add_warehouse(i)

def write_warehouses():
    wh = get_warehouses()
    with open(f'.cache/{get_hash()}/warehouses.pickle', 'wb') as f:
        pickle.dump(wh, f)

class LoginScreen(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.main_app = parent  # Сохраняем ссылку на MainApp
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
                border: 2px solid #ffd2a6;
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
                border: 2px solid #ffd2a6;
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
        # Кнопка переключения на регистрацию
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
        button_container.addWidget(register_btn)
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
        # Сигналы - используем сохраненную ссылку на main_app
        login_btn.clicked.connect(self.handle_login)
        register_btn.clicked.connect(self.main_app.show_register_screen if self.main_app else None)
        forgot_password.clicked.connect(self.show_forgot_password)
    
    # Новый метод обработки входа
    def handle_login(self):
        """Обработчик нажатия кнопки входа с валидацией"""
        if self.validate_input():
            # Все данные корректны — переходим в основной интерфейс
            if self.main_app:
                self.main_app.show_main_interface()
    
    def validate_input(self) -> bool:
        """Проверка корректности введенных данных"""
        email = self.email_input.text().strip()
        password = self.password_input.text()
        
        # Специальное исключение для отладки: если во все поля введена "1"
        if email == "1" and password == "1":
            return True
            
        # Проверка email
        if not email:
            self.show_error("Поле email обязательно для заполнения")
            return False
        if '@' not in email or '.' not in email.split('@')[-1]:
            self.show_error("Некорректный формат email адреса")
            return False
            
        # Проверка пароля
        if len(password) < 8:
            self.show_error("Пароль должен содержать минимум 8 символов")
            return False
            
        return True

    def show_error(self, message: str):
        """Унифицированное отображение ошибок"""
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Icon.Warning)
        msg.setWindowTitle("Ошибка входа")
        msg.setText(message)
        msg.setStyleSheet("""
            QMessageBox {
                background-color: #fffaf0;
                font-family: Arial;
            }
            QLabel {
                color: #5a3921;
                font-size: 14px;
            }
            QPushButton {
                background-color: #e67e22;
                color: white;
                border-radius: 4px;
                padding: 5px 15px;
            }
        """)
        msg.exec()
    
    def show_forgot_password(self):
        """Заглушка для функции восстановления пароля"""
        print("Восстановление пароля")

class RegisterScreen(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.main_app = parent  # Сохраняем ссылку на MainApp
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
                border: 2px solid #ffd2a6;
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
                border: 2px solid #ffd2a6;
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
        # Поле для имени компании (вместо подтверждения пароля)
        self.company_input = QLineEdit()
        self.company_input.setFixedHeight(45)
        self.company_input.setPlaceholderText("Название компании")
        self.company_input.setStyleSheet("""
            QLineEdit {
                padding: 8px 15px;
                border: 2px solid #ffd2a6;
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
        # Кнопка переключения на вход
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
        button_container.addWidget(login_btn)
        button_container.setAlignment(Qt.AlignmentFlag.AlignCenter)
        # Сборка интерфейса
        form_layout.addWidget(title)
        form_layout.addWidget(self.email_input)
        form_layout.addWidget(self.password_input)
        form_layout.addWidget(self.company_input)  # Поле для названия компании
        form_layout.addWidget(register_btn)
        form_layout.addLayout(button_container)
        main_layout.addWidget(form_container, alignment=Qt.AlignmentFlag.AlignCenter)
        self.setLayout(main_layout)
        # Сигналы - используем сохраненную ссылку на main_app
        register_btn.clicked.connect(self.handle_registration)
        login_btn.clicked.connect(self.main_app.show_login_screen if self.main_app else None)
    
    def handle_registration(self):
        """Обработчик нажатия кнопки регистрации с валидацией"""
        if self.validate_input():
            # Все данные корректны — переходим в основной интерфейс
            if self.main_app:
                self.main_app.show_main_interface()
    
    def validate_input(self) -> bool:
        """Проверка корректности введенных данных"""
        email = self.email_input.text().strip()
        password = self.password_input.text()
        company_name = self.company_input.text().strip()
        
        # Специальное исключение для отладки: если во все поля введена "1"
        if email == "1" and password == "1" and company_name == "1":
            return True
        
        # Проверка email
        if not email:
            self.show_error("Поле email обязательно для заполнения")
            return False
        if '@' not in email or '.' not in email.split('@')[-1]:
            self.show_error("Некорректный формат email адреса")
            return False
            
        # Проверка пароля
        if len(password) < 8:
            self.show_error("Пароль должен содержать минимум 8 символов")
            return False
            
        # Проверка названия компании
        if not company_name:
            self.show_error("Название компании обязательно для заполнения")
            return False
        
        return True

    def show_error(self, message: str):
        """Унифицированное отображение ошибок"""
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Icon.Warning)
        msg.setWindowTitle("Ошибка регистрации")
        msg.setText(message)
        msg.setStyleSheet("""
            QMessageBox {
                background-color: #fffaf0;
                font-family: Arial;
            }
            QLabel {
                color: #5a3921;
                font-size: 14px;
            }
            QPushButton {
                background-color: #e67e22;
                color: white;
                border-radius: 4px;
                padding: 5px 15px;
            }
        """)
        msg.exec()
        

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
                background-color: #ffd2a6;
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
        add_btn.clicked.connect(self.add_warehouse)
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
        
        # Локальное хранилище виджетов
        self.warehouse_widgets = {}  # {name: widget}

    def showEvent(self, event):
        """Вызывается при каждом показе экрана"""
        super().showEvent(event)
        self.refresh_warehouses()

    def refresh_warehouses(self):
        """Обновляет список складов из глобальных данных"""
        # Очищаем текущие виджеты
        self.clear_warehouse_widgets()
        
        # Загружаем склады из глобального списка
        warehouses_data = get_warehouses()
        
        # Создаем виджеты для каждого склада
        for warehouse_data in warehouses_data:
            self.create_warehouse_widget(warehouse_data)
        
        print(f"Загружено {len(warehouses_data)} складов")

    def clear_warehouse_widgets(self):
        """Очищает все виджеты складов"""
        # Удаляем все виджеты из layout
        while self.scroll_layout.count():
            item = self.scroll_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
        
        # Очищаем локальный словарь
        self.warehouse_widgets.clear()

    def create_warehouse_widget(self, warehouse_data):
        """Создает виджет для склада на основе данных"""
        name = warehouse_data.get('name', 'Без названия')
        file_path = warehouse_data.get('file_path', '')
        
        # ВЫЧИСЛЯЕМ СТАТУС ДИНАМИЧЕСКИ на основе текущих метрик
        metrics = calculate_metrics(file_path, get_hash())
        load_percentage = metrics.get('cur_fullness')
        status = metrics.get('status', False)  # Динамически вычисляем!
        
        # Определяем статус текст и цвет
        if status:  # True = требуется действие
            status_text = "Требуется действие!"
            status_color = "#e74c3c"  # Красный
        else:  # False = все ОК
            status_text = "ОК"
            status_color = "#27ae60"  # Зеленый
        
        # Создаем элемент списка
        item = QWidget()
        item.setStyleSheet("""
            QWidget {
                background-color: #ffd2a6;
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
        
        # Растягиваемое пространство
        layout.addStretch()
        
        # Статус (справа)
        status_label = QLabel(status_text)
        status_label.setStyleSheet(f"""
            color: {status_color}; 
            font-weight: bold; 
            font-size: 14px;
            background: transparent;
            border: none;
            outline: none;
        """)
        layout.addWidget(status_label)
        
        self.scroll_layout.addWidget(item)
        
        # Сохраняем связь между данными и виджетом
        item.warehouse_data = warehouse_data
        
        # Сохраняем в локальный словарь
        self.warehouse_widgets[name] = item
        
        return item

    def add_warehouse(self):
        """Открывает диалог для добавления нового склада"""
        dialog = QDialog(self)
        dialog.setWindowTitle("Добавить склад")
        dialog.setFixedSize(350, 200)
        
        main_layout = QVBoxLayout(dialog)
        main_layout.setContentsMargins(15, 15, 15, 15)
        
        grid = QGridLayout()
        grid.setSpacing(10)
        
        # Имя склада
        name_label = QLabel("Имя склада:")
        name_label.setStyleSheet("font-weight: normal;")
        name_input = QLineEdit()
        name_input.setPlaceholderText("Введите имя склада")
        grid.addWidget(name_label, 0, 0)
        grid.addWidget(name_input, 0, 1, 1, 2)
        
        # Файл данных
        file_label = QLabel("Файл данных:")
        file_label.setStyleSheet("font-weight: normal;")
        file_path_input = QLineEdit()
        file_path_input.setPlaceholderText("Выберите файл")
        file_path_input.setReadOnly(True)
        
        browse_btn = QPushButton("Обзор...")
        browse_btn.setFixedWidth(80)
        
        def browse_file():
            file_path, _ = QFileDialog.getOpenFileName(
                self, 
                "Выберите файл", 
                "", 
                "CSV Files (*.csv)"
            )
            if file_path:
                file_path_input.setText(file_path)
        
        browse_btn.clicked.connect(browse_file)
        
        grid.addWidget(file_label, 1, 0)
        grid.addWidget(file_path_input, 1, 1)
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
        
        def add_and_close():
            name = name_input.text().strip()
            pth = file_path_input.text().strip()
            
            if not name:
                QMessageBox.warning(self, "Ошибка", "Введите имя склада")
                return
                
            if not pth:
                QMessageBox.warning(self, "Ошибка", "Выберите файл")
                return
            
            # Проверяем, нет ли уже склада с таким именем
            existing_warehouses = get_warehouses()
            for existing in existing_warehouses:
                if existing.get('name') == name:
                    QMessageBox.warning(self, "Ошибка", f"Склад с именем '{name}' уже существует")
                    return
            
            try:
                # Формируем данные склада (ТОЛЬКО ОСНОВНЫЕ ДАННЫЕ!)
                warehouse_data = {
                    "name": name,
                    "file_path": pth
                    # НЕ сохраняем статус, он вычисляется динамически!
                    # НЕ сохраняем метрики, они вычисляются при каждом обновлении!
                }
                
                print(f"Добавлен склад '{name}'")
                
                # Добавляем в глобальный список
                add_warehouse(warehouse_data)
                
                # Создаем виджет (он сам вычислит статус)
                self.create_warehouse_widget(warehouse_data)
                
                dialog.accept()
                
            except Exception as e:
                QMessageBox.critical(self, "Ошибка", f"Не удалось обработать файл:\n{str(e)}")
                import traceback
                traceback.print_exc()
        
        add_btn.clicked.connect(add_and_close)
        
        button_layout.addStretch()
        button_layout.addWidget(cancel_btn)
        button_layout.addWidget(add_btn)
        
        main_layout.addLayout(button_layout)
        
        dialog.exec()

    def update_all_warehouses_status(self):
        """Обновляет статусы всех складов (например, при изменении настроек)"""
        for name, widget in self.warehouse_widgets.items():
            warehouse_data = widget.warehouse_data
            file_path = warehouse_data.get('file_path')
            
            if file_path:
                # Пересчитываем метрики
                metrics = calculate_metrics(file_path, get_hash())
                status = metrics.get('status', False)
                
                # Находим статус лейбл
                for child in widget.findChildren(QLabel):
                    if child.text() in ["Требуется действие!", "ОК"]:
                        # Обновляем текст и цвет
                        if status:
                            child.setText("Требуется действие!")
                            child.setStyleSheet("""
                                color: #e74c3c; 
                                font-weight: bold; 
                                font-size: 14px;
                                background: transparent;
                                border: none;
                                outline: none;
                            """)
                        else:
                            child.setText("ОК")
                            child.setStyleSheet("""
                                color: #27ae60; 
                                font-weight: bold; 
                                font-size: 14px;
                                background: transparent;
                                border: none;
                                outline: none;
                            """)
                        break


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
                selection-background-color: #ffd2a6;
            }
        """)
        
        # ИНИЦИАЛИЗИРУЕМ ПУСТЫЕ ДАННЫЕ
        self.warehouse_items = []
        self.warehouse_data = []
        
        # ДОБАВЛЯЕМ ПУСТОЙ КОМБОБОКС С ЗАГЛУШКОЙ
        self.warehouse_combo.addItem("Загрузка складов...")
        self.warehouse_combo.setEnabled(False)

        self.warehouse_combo.currentIndexChanged.connect(self.update_data)
        main_layout.addWidget(self.warehouse_combo)
        
        # Контейнер для графика (СОЗДАЕМ ВСЕГДА)
        self.graph_container = QFrame()
        self.graph_container.setStyleSheet("""
            QFrame {
                background-color: #ffd2a6;
                border-radius: 10px;
                margin: 10px;
                padding: 10px;
            }
        """)
        self.graph_container.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        graph_layout = QVBoxLayout(self.graph_container)
        
        # График (СОЗДАЕМ ВСЕГДА)
        self.figure = Figure(figsize=(5, 4), dpi=100)
        self.canvas = FigureCanvas(self.figure)
        self.canvas.setStyleSheet("background-color: #ffd2a6; border-radius: 8px;")
        self.canvas.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        graph_layout.addWidget(self.canvas)
        
        # Статистика (СОЗДАЕМ ВСЕГДА)
        self.stats_container = QFrame()
        self.stats_container.setStyleSheet("""
            QFrame {
                background-color: #ffd2a6;
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
            ("Средняя загруженность", ""),
            ("Средние продажи", ""),
            ("Дней с излишками", ""),
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
        
        # ВАЖНО: ДОБАВЛЯЕМ ВСЕ ВИДЖЕТЫ В МАКЕТ СРАЗУ
        # (они будут скрыты/показаны позже)
        main_layout.addWidget(self.graph_container, 4)
        main_layout.addWidget(self.stats_container, 1)
        
        # ИНИЦИАЛИЗИРУЕМ ПУСТОЙ ГРАФИК
        self.initialize_empty_graph()
        
        # НЕ вызываем update_data() здесь - будет вызван в showEvent()
        # self.update_data()  # <-- УБРАТЬ
        
        # Изначально скрываем график и статистику
        self.graph_container.hide()
        self.stats_container.hide()

    def showEvent(self, event):
        """Вызывается при каждом показе виджета"""
        super().showEvent(event)
        self.refresh_warehouses()  # Теперь здесь будет и обновление данных
        
    def refresh_warehouses(self):
        """Обновляет список складов"""
        # Получаем актуальный список складов
        raw_data = get_warehouses()
        
        # Сохраняем оригинальные данные
        self.warehouse_data = raw_data
        
        # Извлекаем названия складов
        self.warehouse_items = []
        for item in raw_data:
            if isinstance(item, dict):
                name = item.get('name', item.get('warehouse_name', 
                          item.get('title', 'Без названия')))
                self.warehouse_items.append(name)
            elif isinstance(item, str):
                self.warehouse_items.append(item)
            else:
                self.warehouse_items.append(str(item))
        
        # Сохраняем текущий выбранный склад (если был)
        current_text = self.warehouse_combo.currentText()
        
        # Блокируем сигналы чтобы не вызывать update_data при очистке
        self.warehouse_combo.blockSignals(True)
        
        # Очищаем комбобокс
        self.warehouse_combo.clear()
        
        # Добавляем новые элементы
        if self.warehouse_items:
            self.warehouse_combo.addItems(["Выберите склад"] + self.warehouse_items)
            self.warehouse_combo.setEnabled(True)
            
            # Разблокируем сигналы
            self.warehouse_combo.blockSignals(False)
            
            # Восстанавливаем предыдущий выбор
            if current_text in self.warehouse_items and current_text != "Загрузка складов...":
                index = self.warehouse_combo.findText(current_text)
                self.warehouse_combo.setCurrentIndex(index)
            else:
                # Иначе выбираем первый склад
                self.warehouse_combo.setCurrentIndex(1)
                
            # ПОКАЗЫВАЕМ график и статистику
            self.graph_container.show()
            self.stats_container.show()
            
            # ОБНОВЛЯЕМ ДАННЫЕ ДЛЯ ВЫБРАННОГО СКЛАДА
            self.update_data()
        else:
            self.warehouse_combo.addItem("Нет складов")
            self.warehouse_combo.setEnabled(False)
            
            # Разблокируем сигналы
            self.warehouse_combo.blockSignals(False)
            
            # Скрываем график и статистику
            self.graph_container.hide()
            self.stats_container.hide()
            
            # Очищаем данные
            self.clear_data_display()
    
    def initialize_empty_graph(self):
        """Инициализирует пустой график"""
        self.figure.clear()
        ax = self.figure.add_subplot(111)
        ax.text(0.5, 0.5, 'Выберите склад для отображения данных', 
                horizontalalignment='center', verticalalignment='center',
                transform=ax.transAxes, fontsize=12, color='#5a3921')
        ax.set_facecolor('#ffd2a6')
        self.figure.patch.set_facecolor('#ffd2a6')
        ax.set_xticks([])
        ax.set_yticks([])
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['left'].set_visible(False)
        ax.spines['bottom'].set_visible(False)
        self.canvas.draw()
    
    def clear_data_display(self):
        """Очищает отображение данных"""
        for _, _, value_widget in self.stats_blocks:
            value_widget.setText("--")
        self.initialize_empty_graph()

    def update_data(self):
        """Обновляет график и статистику для выбранного склада"""
        index = self.warehouse_combo.currentIndex()
        
        # Если выбрана "заглушка" или список пуст — очищаем данные
        if index == 0 or not self.warehouse_items:
            self.clear_data_display()
            return
        
        # Получаем данные выбранного склада
        warehouse_index = index - 1  # индекс в warehouse_items
        
        # Заполняем статистику
        warehouse_info = self.warehouse_data[warehouse_index]
        # Используйте реальные данные из warehouse_info
        metrics = calculate_metrics(warehouse_info['file_path'], get_hash())
        stats_data = {
            "Загруженность": f"{metrics['cur_fullness']}%",
            "Средняя загруженность": f"{metrics['avg_fullness']}%.",
            "Средние продажи": f"{metrics['avg_salles']} е.т.",
            "Дней с излишками": f"{metrics['days_with_over']}%",
        }
        
        for block, label_widget, value_widget in self.stats_blocks:
            key = label_widget.text()
            if key in stats_data:
                value_widget.setText(stats_data[key])
        
        # Отрисовываем график
        make_plot(warehouse_info['file_path'], self.figure, self.canvas)

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
        ax.set_facecolor('#ffd2a6')
        self.figure.patch.set_facecolor('#ffd2a6')
        
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
        ax.set_facecolor('#ffd2a6')
        self.figure.patch.set_facecolor('#ffd2a6')
        
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
            ["Компания 1", "50", "3"],
            ["Компания 2", "200", "5"],
            ["Склад-партнер", "150", "2"],
            ["Логистик-Хаб", "300", "7"],
            ["Доп. Компания", "75", "1"],
            ["Еще одна", "250", "4"],
            ["Тестовая", "100", "6"],
            ["Пример", "400", "2"]
        ]
        
        # Создание блоков объявлений
        for announcement in announcements:
            block = QWidget()
            block.setStyleSheet("""
                QWidget {
                    background-color: #ffd2a6;
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
                    background-color: #ffd2a6;
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
                background-color: #ffd2a6;
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
    def __init__(self, icon_path, text, parent=None):
        super().__init__(parent)
        self.setFixedHeight(50)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        
        # Контейнер для содержимого (обычный виджет, а не сама кнопка)
        container = QWidget()
        container.setStyleSheet("background: transparent;")
        
        # Основной горизонтальный layout
        layout = QHBoxLayout(container)
        layout.setContentsMargins(15, 0, 15, 0)
        layout.setSpacing(12)
        
        # Иконка как отдельный элемент слева (PNG картинка)
        icon_label = QLabel()
        icon_label.setStyleSheet("""
            QLabel {
                background: transparent;
                min-width: 30px;
                text-align: center;
            }
        """)
        icon_label.setFixedWidth(30)
        icon_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        # Загружаем изображение
        if icon_path:
            pixmap = QPixmap(icon_path)
            # Масштабируем до 24x24 пикселей
            pixmap = pixmap.scaledToHeight(24, Qt.TransformationMode.SmoothTransformation)
            icon_label.setPixmap(pixmap)
        
        # Текст кнопки
        text_label = QLabel(text)
        text_label.setStyleSheet("""
            QLabel {
                font-size: 14px;
                font-weight: 500;
                color: #5a3921;
                background: transparent;
            }
        """)
        
        layout.addWidget(icon_label)
        layout.addWidget(text_label)
        layout.addStretch()
        
        self.setLayout(layout)
        
        # Начальный стиль кнопки
        self.setStyleSheet("""
            QPushButton {
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
        sidebar.setStyleSheet("background-color: #ffd2a6;")  # Персиковый фон как в ТЗ
        sidebar.setFixedWidth(250)
        
        sidebar_layout = QVBoxLayout(sidebar)
        sidebar_layout.setContentsMargins(0, 30, 0, 30)
        sidebar_layout.setSpacing(5)
        sidebar_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        
        # ====== Логотип и название компании ======
        header_container = QFrame()
        header_container.setStyleSheet("""
            QFrame {
                background-color: transparent;
                padding: 0 10px 10px 10px;
                margin: 0;
            }
        """)
        header_layout = QHBoxLayout(header_container)
        header_layout.setContentsMargins(15, 0, 15, 0)
        header_layout.setSpacing(6)
        
        # Логотип
        logo_label = QLabel()
        logo_label.setStyleSheet("""
            QLabel {
                background: transparent;
                min-width: 60px;
                text-align: center;
            }
        """)
        logo_label.setFixedWidth(60)
        logo_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        logo_pixmap = QPixmap("icons/logo.png")
        if not logo_pixmap.isNull():
            logo_pixmap = logo_pixmap.scaledToHeight(48, Qt.TransformationMode.SmoothTransformation)
            logo_label.setPixmap(logo_pixmap)
        
        # Название компании
        company_name_label = QLabel("Излишков.net")
        company_name_label.setStyleSheet("""
            QLabel {
                font-size: 14px;
                font-weight: 500;
                color: #5a3921;
                background: transparent;
            }
        """)
        company_name_label.setAlignment(Qt.AlignmentFlag.AlignVCenter)
        
        header_layout.addWidget(logo_label)
        header_layout.addWidget(company_name_label)
        header_layout.addStretch()
        
        sidebar_layout.addWidget(header_container)
        
        # ====== Кнопки меню ======
        menu_items = [
            ("icons/home.png", "Главная", self.show_home),
            ("icons/analysis.png", "Анализ & Прогноз", self.show_analysis),
            ("icons/announcement.png", "Объявление", self.show_forecast),
            ("icons/account.png", "Аккаунт", self.show_account),
            ("icons/settings.png", "Настройки", self.show_settings)
        ]
        
        self.menu_buttons = []
        for icon, text, handler in menu_items:
            btn = MenuButton(icon, text)
            btn.clicked.connect(handler)
            sidebar_layout.addWidget(btn)
            self.menu_buttons.append(btn)
        
        sidebar_layout.addStretch()
        
        # ====== Плашка с датой внизу ======
        date_container = QFrame()
        date_container.setStyleSheet("""
            QFrame {
                background-color: rgba(230, 126, 34, 0.2);
                border-radius: 8px;
                padding: 10px;
                margin: 0 10px;
            }
        """)
        date_layout = QVBoxLayout(date_container)
        date_layout.setContentsMargins(10, 8, 10, 8)
        date_layout.setSpacing(0)
        
        # Получаем дату из переменных
        try:
            vrs = get_calculated_vars(get_hash())
            current_date = vrs.get('DATA')
            date_text = current_date.strftime("%d.%m.%Y") if current_date else "--"
        except:
            date_text = "--"
        
        date_label = QLabel(date_text)
        date_label.setStyleSheet("""
            QLabel {
                font-size: 16px;
                font-weight: bold;
                color: #5a3921;
                background: transparent;
            }
        """)
        date_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        date_title = QLabel("Текущая дата")
        date_title.setStyleSheet("""
            QLabel {
                font-size: 11px;
                color: #8B6F47;
                background: transparent;
            }
        """)
        date_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        date_layout.addWidget(date_title)
        date_layout.addWidget(date_label)
        
        sidebar_layout.addWidget(date_container)
        
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
        self.setup_light_theme()

        self.central_widget = QStackedWidget()
        self.setCentralWidget(self.central_widget)

        self.login_screen = LoginScreen(self)
        self.register_screen = RegisterScreen(self)
        # НЕ создаём self.main_interface здесь!

        self.central_widget.addWidget(self.login_screen)    # index 0
        self.central_widget.addWidget(self.register_screen) # index 1

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
        # Устанавливаем USER_ID (заглушка)
        set_user_id(-1)
        print(get_hash())
        # Инициализируем склады из кэша (если есть)
        read_warehouses()

        # Создаём MainInterface только при первом вызове
        if not hasattr(self, 'main_interface'):
            self.main_interface = MainInterface(self)
            self.central_widget.addWidget(self.main_interface)

        self.central_widget.setCurrentWidget(self.main_interface)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    font = QFont("Segoe UI", 11)
    app.setFont(font)

    window = MainApp()
    window.show()

    # Сохранение складов при выходе
    app.aboutToQuit.connect(write_warehouses)

    sys.exit(app.exec())
