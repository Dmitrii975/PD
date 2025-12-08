import matplotlib.pyplot as plt
import pandas as pd
from vars import get_calculated_vars
import numpy as np


def calculate_metrics(pth, hsh) -> dict: #Возвращем метрики для анализа
    vrs = get_calculated_vars(hsh)

    metrics = dict()
    df = pd.read_csv(pth)
    df = df.iloc[-30:]
    metrics['avg_fullness'] = round(df['inventory'].mean() / df['max_space'].iloc[0] * 100, 2)
    metrics['status'] = df['inventory'].iloc[-1] >= vrs['ACTION_ON']
    metrics['cur_fullness'] = round(df['inventory'].iloc[-1] / df['max_space'].iloc[0] * 100, 2)
    metrics['avg_salles'] = df['demand'].mean().__round__(2)
    metrics['days_with_over'] = round(sum(df['inventory'] > vrs['TARGET_INVENTORY']) / len(df) * 100, 2)
    metrics['volaty'] = df['demand'].std().__round__(2)
    metrics['arrived_count'] = sum(df['travel'])

    return metrics


def make_plot(pth, figure, canvas): # Под главный график заготовка
    """Создает график синусоиды"""
    df = pd.read_csv(pth)
    df = df.iloc[-60:]
    figure.clear()
    ax = figure.add_subplot(111)
    
    # Увеличиваем нижний отступ еще больше для легенды
    figure.subplots_adjust(left=0.08, right=0.95, top=0.92, bottom=0.30)
    
    # Генерация данных
    x = df['date']
    prod = df['production']
    dem = df['demand']
    inv = df['inventory']
    
    # Настройка графика
    line_prod = ax.plot(x, prod, '-', color="#224de6", linewidth=2, label='Производство')
    line_dem = ax.plot(x, dem, '-', color="#d24336", linewidth=2, label='Спрос')
    line_inv = ax.plot(x, inv, '--', color="#00ab33", linewidth=2, label='Инвентарь')

    ax.set_xlabel('Время', fontsize=12, color='#5a3921')
    ax.set_ylabel('Единицы', fontsize=12, color='#5a3921')
    ax.grid(False)
    
    # Полностью персиковый фон графика
    ax.set_facecolor('#ffd2a6')
    figure.patch.set_facecolor('#ffd2a6')
    
    # Настройка делений на оси Y
    y_max = max(prod.max(), dem.max(), inv.max())
    y_ticks = np.linspace(0, y_max, 6)
    ax.set_yticks(y_ticks)
    ax.set_yticklabels([f"{int(tick)}" for tick in y_ticks], color='#5a3921')
    
    # Настройка делений на оси X
    n = len(x)
    if n > 10:
        step = max(2, n // 8)
        indices = list(range(0, n, step))
        if n-1 not in indices:
            indices.append(n-1)
    else:
        indices = list(range(n))
    
    ax.set_xticks(indices)
    
    # Укорачиваем даты до формата "день-месяц"
    x_labels = []
    for i in indices:
        if i < len(x):
            date_str = str(x.iloc[i])
            # Пытаемся разобрать дату в разных форматах
            try:
                # Если дата в формате "YYYY-MM-DD"
                if '-' in date_str:
                    parts = date_str.split('-')
                    if len(parts) >= 2:
                        x_labels.append(f"{parts[2]}-{parts[1]}")  # день-месяц
                    else:
                        x_labels.append(date_str)
                # Если дата в формате "DD.MM.YYYY"
                elif '.' in date_str:
                    parts = date_str.split('.')
                    if len(parts) >= 2:
                        x_labels.append(f"{parts[0]}-{parts[1]}")  # день-месяц
                    else:
                        x_labels.append(date_str)
                else:
                    x_labels.append(date_str)
            except:
                x_labels.append(date_str)
        else:
            x_labels.append('')
    
    ax.set_xticklabels(x_labels, rotation=45, ha='right', color='#5a3921', fontsize=9)
    
    # Стилизация осей
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_color('#e67e22')
    ax.spines['bottom'].set_color('#e67e22')
    
    # КОМПАКТНАЯ легенда в одну строку ПОД осью X
    legend = ax.legend(
        loc='lower left',  # По центру сверху
        frameon=True,
        framealpha=0.9,
        facecolor='#ffe6cc',
        edgecolor='#e67e22',
        fontsize=9,
        ncol=3,  # Все элементы в одну строку
        borderaxespad=0.5,
        handlelength=1.2,  # Очень короткие линии
        handletextpad=0.3,  # Минимальный отступ
        columnspacing=1.0,  # Расстояние между колонками
        borderpad=0.3,  # Минимальные внутренние отступы
        labelspacing=0.2  # Минимальное расстояние между строками
    )
    
    # Устанавливаем цвет текста легенды
    for text in legend.get_texts():
        text.set_color('#5a3921')
    
    # Делаем рамку легенды тоньше
    legend.get_frame().set_linewidth(0.5)
    
    # Обновляем холст
    canvas.draw()

