# Импорт библиотек для создания графического интерфейса
import tkinter as tk  # Основная библиотека для GUI
from tkinter import ttk, filedialog, messagebox, colorchooser  # Дополнительные модули tkinter

# Импорт математических функций
import math  # Для тригонометрических расчетов (cos, sin, pi)
import random  # Для генерации случайных чисел (позиции звезд, углы планет)

# Импорт для работы со временем
import time  # Для замера FPS и временных интервалов
from datetime import datetime, timedelta  # Для работы с датами (имена файлов)

# Импорт для работы с данными
import json  # Для сохранения/загрузки симуляции в формате JSON
import os  # Для работы с файловой системой (создание папок, проверка файлов)
import sys  # Для системных функций (завершение программы)
import threading  # Для многопоточности (фоновый подсчет FPS)
from collections import deque  # Двусторонняя очередь для хранения траекторий

# Импорт для цветовых преобразований
import colorsys  # Для конвертации цветов RGB в HSV и обратно
import hashlib  # Для хеширования (не используется, но импортирован)
import io  # Для работы с потоками ввода-вывода
import webbrowser  # Для открытия ссылок в браузере

# Попытка импорта библиотеки Pillow для работы с изображениями
try:
    from PIL import Image, ImageTk, ImageDraw, ImageFilter, ImageEnhance, ImageFont
    HAS_PIL = True  # Флаг, что Pillow установлен
except ImportError:
    HAS_PIL = False  # Флаг, что Pillow не установлен
    print("Для максимальной визуализации установите Pillow: pip install Pillow")


class MegaSolarSystem:
    """Главный класс симуляции солнечной системы"""
    
    def __init__(self, root):
        """Конструктор класса, инициализирует все компоненты симуляции"""
        
        # Сохраняем ссылку на главное окно
        self.root = root
        
        # Устанавливаем заголовок окна
        self.root.title("🚀 МЕГА-СИМУЛЯЦИЯ СОЛНЕЧНОЙ СИСТЕМЫ 3000 - КОСМИЧЕСКИЙ ЭПОС 🌌")
        
        # Устанавливаем размер окна (ширина 1900, высота 1000 пикселей)
        self.root.geometry("1900x1000")
        
        # Устанавливаем черный фон окна
        self.root.configure(bg='#000000')
        
        # Разрешаем изменение размера окна пользователем
        self.root.resizable(True, True)
        
        # ==================== КОНСТАНТЫ И ПАРАМЕТРЫ ====================
        
        # Астрономическая единица в пикселях (сколько пикселей соответствует 1 АЕ)
        self.AU = 150
        
        # Базовая скорость анимации (чем меньше, тем медленнее движение)
        self.BASE_SPEED = 0.0002
        
        # Множитель скорости (пользователь может ускорять/замедлять время)
        self.time_multiplier = 1.0
        
        # Коэффициент масштабирования (зум)
        self.zoom_factor = 1.0
        
        # Смещение камеры по X и Y (для панорамирования)
        self.pan_x = 0
        self.pan_y = 0
        
        # Флаг, указывающий, что пользователь перетаскивает вид
        self.dragging = False
        
        # Начальные координаты перетаскивания
        self.drag_start_x = 0
        self.drag_start_y = 0
        
        # Последние координаты мыши
        self.last_mouse_x = 0
        self.last_mouse_y = 0
        
        # Планета, над которой находится курсор мыши
        self.mouse_over_planet = None
        
        # Флаги отображения панелей
        self.show_controls = True
        self.control_panel_visible = True
        
        # Флаг полноэкранного режима
        self.fullscreen = False
        
        # ==================== РЕЖИМЫ И СОСТОЯНИЯ ====================
        
        # Выбранная планета (для отображения информации)
        self.selected_planet = None
        
        # Флаг паузы
        self.paused = False
        
        # Флаги отображения различных элементов
        self.show_orbits = True          # Показывать орбиты
        self.show_labels = True           # Показывать названия
        self.show_effects = True          # Показывать спецэффекты
        self.show_grid = False             # Показывать сетку
        self.show_asteroids = True        # Показывать астероиды
        self.show_nebula = True            # Показывать туманности
        self.show_constellations = False  # Показывать созвездия
        self.night_mode = False            # Ночной режим
        self.hdr_mode = True                # HDR режим
        self.motion_blur = False           # Размытие движения
        self.rainbow_mode = False          # Радужный режим
        self.trails_enabled = False        # Включить траектории
        self.trails = deque(maxlen=100)    # Очередь для хранения траекторий (макс 100 точек)
        self.show_stats = True              # Показывать статистику
        self.show_minimap = True            # Показывать миникарту
        self.show_legend = True             # Показывать легенду
        self.auto_rotate = False            # Автоматическое вращение
        self.smooth_zoom = True             # Плавный зум
        self.zoom_speed = 0.1                # Скорость зума
        self.target_zoom = 1.0               # Целевой зум
        self.follow_selected = False         # Следовать за выбранной планетой
        
        # ==================== СИСТЕМНЫЕ ПАРАМЕТРЫ ====================
        
        # Время дня (для анимации)
        self.time_of_day = 0
        
        # Счетчик кадров для FPS
        self.frame_count = 0
        
        # Текущий FPS
        self.fps = 0
        
        # Время последнего замера FPS
        self.last_time = time.time()
        
        # Смещение звездного поля
        self.starfield_offset = 0
        
        # Космическая радиация (для эффектов)
        self.cosmic_radiation = 0
        
        # Искривление пространства-времени (для эффектов)
        self.space_time_distortion = 0
        
        # Время симуляции (секунды)
        self.simulation_time = 0
        
        # Общее пройденное расстояние
        self.total_distance_traveled = 0
        
        # ==================== ГЕНЕРАЦИЯ ВСЕЛЕННОЙ ====================
        
        # Генерируем звездное поле (3000 звезд)
        self.stars = self.generate_stars(3000)
        
        # Генерируем объекты глубокого космоса (100 объектов)
        self.deep_space_objects = self.generate_deep_space(100)
        
        # Генерируем туманности (30 туманностей)
        self.nebulae = self.generate_nebulae(30)
        
        # Генерируем пояс астероидов (500 астероидов)
        self.asteroids = self.generate_asteroid_belt(500)
        
        # Генерируем кометы (20 комет)
        self.comets = self.generate_comets(20)
        
        # Генерируем созвездия
        self.constellations = self.generate_constellations()
        
        # Генерируем черные дыры (3 черные дыры)
        self.black_holes = self.generate_black_holes(3)
        
        # ==================== ДАННЫЕ О ПЛАНЕТАХ ====================
        
        # Создаем список с данными о планетах
        self.planets_data = [
            # Меркурий
            {
                "name": "Меркурий",                          # Русское название
                "name_en": "Mercury",                         # Английское название
                "distance": 0.4,                               # Расстояние от Солнца в АЕ
                "radius": 8,                                   # Радиус в пикселях
                "base_radius": 8,                              # Базовый радиус
                "color": "#A5A5A5",                            # Основной цвет
                "color2": "#696969",                           # Вторичный цвет
                "color3": "#D3D3D3",                           # Третичный цвет
                "speed": 1/0.24,                               # Орбитальная скорость (1/период в годах)
                "angle": random.uniform(0, 2*math.pi),        # Начальный угол на орбите
                "rotation": 0,                                 # Текущий угол вращения
                "rotation_speed": 0.02,                        # Скорость вращения
                "orbit_tilt": 0.1,                             # Наклон орбиты
                "texture": "rocky",                            # Тип текстуры
                "atmosphere": None,                            # Наличие атмосферы
                "atmosphere_color": None,                       # Цвет атмосферы
                "has_rings": False,                             # Наличие колец
                "has_moons": False,                             # Наличие спутников
                "moon_count": 0,                                # Количество спутников
                "moons": [],                                    # Список спутников
                "temperature": "-173°C до +427°C",              # Температура
                "mass": "3.30×10²³ кг",                         # Масса
                "density": "5.43 г/см³",                        # Плотность
                "gravity": "3.7",                               # Сила тяжести
                "gravity_unit": "м/с²",                         # Единицы измерения гравитации
                "discovery": "Древние цивилизации",             # История открытия
                "description": "Самая близкая к Солнцу планета", # Описание
                "fun_fact": "Сутки на Меркурии длятся 176 земных дней!", # Интересный факт
                "image_path": "photo_5260428536751788520_x (1)-no-bg-preview (carve.photos).png", # Путь к изображению
                "emissivity": 0.1,                              # Альбедо
                "volume": "6.08×10¹⁰ км³",                      # Объем
                "escape_velocity": "4.3 км/с"                    # Вторая космическая скорость
            },
            
            # Венера
            {
                "name": "Венера",
                "name_en": "Venus",
                "distance": 0.7,
                "radius": 10,
                "base_radius": 10,
                "color": "#E6B800",
                "color2": "#CC9900",
                "color3": "#FFD700",
                "speed": 1/0.62,
                "angle": random.uniform(0, 2*math.pi),
                "rotation": 0,
                "rotation_speed": -0.01,  # Отрицательная скорость = обратное вращение
                "orbit_tilt": 0.2,
                "texture": "volcanic",
                "atmosphere": "#F0E68C",
                "atmosphere_color": "#F0E68C",
                "atmosphere_opacity": 0.8,
                "has_rings": False,
                "has_moons": False,
                "moon_count": 0,
                "moons": [],
                "temperature": "+462°C",
                "mass": "4.87×10²⁴ кг",
                "density": "5.24 г/см³",
                "gravity": "8.9",
                "gravity_unit": "м/с²",
                "discovery": "Древние цивилизации",
                "description": "Самая горячая планета",
                "fun_fact": "Венера вращается в обратную сторону!",
                "image_path": "photo_5260428536751788522_x (1)-no-bg-preview (carve.photos).png",
                "emissivity": 0.2,
                "volume": "9.28×10¹¹ км³",
                "escape_velocity": "10.4 км/с"
            },
            
            # Земля
            {
                "name": "Земля",
                "name_en": "Earth",
                "distance": 1.0,
                "radius": 11,
                "base_radius": 11,
                "color": "#2E86C1",
                "color2": "#1F618D",
                "color3": "#85C1E9",
                "speed": 1.0,  # Скорость Земли = 1 (базовая)
                "angle": random.uniform(0, 2*math.pi),
                "rotation": 0,
                "rotation_speed": 0.015,
                "orbit_tilt": 0.0,
                "texture": "earth",
                "atmosphere": "#A9DFBF",
                "atmosphere_color": "#A9DFBF",
                "atmosphere_opacity": 0.4,
                "has_rings": False,
                "has_moons": True,
                "moon_count": 1,
                "moons": [
                    # Луна - спутник Земли
                    {"name": "Луна", "distance": 2.5, "radius": 3, "speed": 13.0, 
                     "angle": random.uniform(0, 2*math.pi), "color": "#C0C0C0", "phase": 0}
                ],
                "temperature": "-89°C до +58°C",
                "mass": "5.97×10²⁴ кг",
                "density": "5.52 г/см³",
                "gravity": "9.8",
                "gravity_unit": "м/с²",
                "discovery": "Наш дом",
                "description": "Единственная известная планета с жизнью",
                "fun_fact": "Земля - единственная планета не названная в честь бога",
                "image_path": "photo_5260428536751788523_y-no-bg-preview (carve.photos).png",
                "emissivity": 0.1,
                "volume": "1.08×10¹² км³",
                "escape_velocity": "11.2 км/с"
            },
            
            # Марс
            {
                "name": "Марс",
                "name_en": "Mars",
                "distance": 1.5,
                "radius": 9,
                "base_radius": 9,
                "color": "#C0392B",
                "color2": "#A93226",
                "color3": "#E6B0AA",
                "speed": 1/1.88,
                "angle": random.uniform(0, 2*math.pi),
                "rotation": 0,
                "rotation_speed": 0.016,
                "orbit_tilt": 0.3,
                "texture": "martian",
                "atmosphere": "#E6B0AA",
                "atmosphere_color": "#E6B0AA",
                "atmosphere_opacity": 0.2,
                "has_rings": False,
                "has_moons": True,
                "moon_count": 2,
                "moons": [
                    # Фобос - спутник Марса
                    {"name": "Фобос", "distance": 2.0, "radius": 2, "speed": 7.0,
                     "angle": random.uniform(0, 2*math.pi), "color": "#808080"},
                    # Деймос - спутник Марса
                    {"name": "Деймос", "distance": 3.0, "radius": 1.5, "speed": 5.0,
                     "angle": random.uniform(0, 2*math.pi), "color": "#808080"}
                ],
                "temperature": "-63°C",
                "mass": "6.42×10²³ кг",
                "density": "3.93 г/см³",
                "gravity": "3.7",
                "gravity_unit": "м/с²",
                "discovery": "Древние цивилизации",
                "description": "Красная планета",
                "fun_fact": "На Марсе находится самый высокий вулкан - Олимп (21 км)",
                "image_path": "photo_5260428536751788525_y (1)-no-bg-preview (carve.photos).png",
                "emissivity": 0.15,
                "volume": "1.63×10¹¹ км³",
                "escape_velocity": "5.0 км/с"
            },
            
            # Юпитер
            {
                "name": "Юпитер",
                "name_en": "Jupiter",
                "distance": 5.2,
                "radius": 22,
                "base_radius": 22,
                "color": "#D4AC0D",
                "color2": "#B7950B",
                "color3": "#F7DC6F",
                "speed": 1/11.86,
                "angle": random.uniform(0, 2*math.pi),
                "rotation": 0,
                "rotation_speed": 0.03,
                "orbit_tilt": 0.5,
                "texture": "gas_giant",
                "atmosphere": "#F7DC6F",
                "atmosphere_color": "#F7DC6F",
                "atmosphere_opacity": 0.5,
                "has_rings": True,
                "has_moons": True,
                "moon_count": 79,
                "moons": [
                    # Четыре главных спутника Юпитера (Галилеевы спутники)
                    {"name": "Ио", "distance": 3.5, "radius": 3, "speed": 8.0,
                     "angle": random.uniform(0, 2*math.pi), "color": "#FFD700"},
                    {"name": "Европа", "distance": 4.5, "radius": 3, "speed": 6.0,
                     "angle": random.uniform(0, 2*math.pi), "color": "#87CEEB"},
                    {"name": "Ганимед", "distance": 5.5, "radius": 4, "speed": 4.0,
                     "angle": random.uniform(0, 2*math.pi), "color": "#D2B48C"},
                    {"name": "Каллисто", "distance": 6.5, "radius": 4, "speed": 3.0,
                     "angle": random.uniform(0, 2*math.pi), "color": "#808080"}
                ],
                "temperature": "-145°C",
                "mass": "1.90×10²⁷ кг",
                "density": "1.33 г/см³",
                "gravity": "24.8",
                "gravity_unit": "м/с²",
                "discovery": "Древние цивилизации",
                "description": "Самая большая планета",
                "fun_fact": "Большое Красное Пятно - шторм, бушующий 400 лет!",
                "image_path": "photo_5260428536751788526_y (2)-no-bg-preview (carve.photos).png",
                "emissivity": 0.3,
                "volume": "1.43×10¹⁵ км³",
                "escape_velocity": "59.5 км/с"
            },
            
            # Сатурн
            {
                "name": "Сатурн",
                "name_en": "Saturn",
                "distance": 9.5,
                "radius": 19,
                "base_radius": 19,
                "color": "#E67E22",
                "color2": "#CA6F1E",
                "color3": "#FAD7A0",
                "speed": 1/29.46,
                "angle": random.uniform(0, 2*math.pi),
                "rotation": 0,
                "rotation_speed": 0.025,
                "orbit_tilt": 0.7,
                "texture": "ringed",
                "atmosphere": "#FAD7A0",
                "atmosphere_color": "#FAD7A0",
                "atmosphere_opacity": 0.4,
                "has_rings": True,
                "ring_count": 7,
                "ring_width": 2.8,
                "ring_particles": 1000,
                "has_moons": True,
                "moon_count": 83,
                "moons": [
                    # Основные спутники Сатурна
                    {"name": "Титан", "distance": 4.0, "radius": 5, "speed": 3.0,
                     "angle": random.uniform(0, 2*math.pi), "color": "#CD853F"},
                    {"name": "Рея", "distance": 5.0, "radius": 3, "speed": 2.5,
                     "angle": random.uniform(0, 2*math.pi), "color": "#A9A9A9"},
                    {"name": "Диона", "distance": 6.0, "radius": 2.5, "speed": 2.0,
                     "angle": random.uniform(0, 2*math.pi), "color": "#D3D3D3"}
                ],
                "temperature": "-178°C",
                "mass": "5.68×10²⁶ кг",
                "density": "0.69 г/см³",
                "gravity": "10.4",
                "gravity_unit": "м/с²",
                "discovery": "Древние цивилизации",
                "description": "Планета с кольцами",
                "fun_fact": "Сатурн настолько лёгкий, что плавал бы в воде!",
                "image_path": "photo_5260428536751788527_y (1)-no-bg-preview (carve.photos).png",
                "emissivity": 0.25,
                "volume": "8.27×10¹⁴ км³",
                "escape_velocity": "35.5 км/с"
            },
            
            # Уран
            {
                "name": "Уран",
                "name_en": "Uranus",
                "distance": 19.0,
                "radius": 15,
                "base_radius": 15,
                "color": "#5DADE2",
                "color2": "#3498DB",
                "color3": "#D4E6F1",
                "speed": 1/84.01,
                "angle": random.uniform(0, 2*math.pi),
                "rotation": 0,
                "rotation_speed": 0.02,
                "orbit_tilt": 1.5,
                "texture": "ice_giant",
                "atmosphere": "#D4E6F1",
                "atmosphere_color": "#D4E6F1",
                "atmosphere_opacity": 0.5,
                "has_rings": True,
                "ring_count": 2,
                "has_moons": True,
                "moon_count": 27,
                "moons": [
                    # Основные спутники Урана
                    {"name": "Титания", "distance": 3.5, "radius": 3, "speed": 2.0,
                     "angle": random.uniform(0, 2*math.pi), "color": "#C0C0C0"},
                    {"name": "Оберон", "distance": 4.5, "radius": 3, "speed": 1.5,
                     "angle": random.uniform(0, 2*math.pi), "color": "#A9A9A9"}
                ],
                "temperature": "-224°C",
                "mass": "8.68×10²⁵ кг",
                "density": "1.27 г/см³",
                "gravity": "8.7",
                "gravity_unit": "м/с²",
                "discovery": "1781, Уильям Гершель",
                "description": "Ледяной гигант",
                "fun_fact": "Уран вращается на боку, ось наклонена на 98°",
                "image_path": "photo_5260428536751788528_x (1)-no-bg-preview (carve.photos).png",
                "emissivity": 0.2,
                "volume": "6.83×10¹³ км³",
                "escape_velocity": "21.3 км/с"
            },
            
            # Нептун
            {
                "name": "Нептун",
                "name_en": "Neptune",
                "distance": 30.0,
                "radius": 15,
                "base_radius": 15,
                "color": "#2471A3",
                "color2": "#1B4F72",
                "color3": "#A9CCE3",
                "speed": 1/164.8,
                "angle": random.uniform(0, 2*math.pi),
                "rotation": 0,
                "rotation_speed": 0.018,
                "orbit_tilt": 0.8,
                "texture": "ice_giant",
                "atmosphere": "#A9CCE3",
                "atmosphere_color": "#A9CCE3",
                "atmosphere_opacity": 0.5,
                "has_rings": True,
                "ring_count": 1,
                "has_moons": True,
                "moon_count": 14,
                "moons": [
                    # Тритон - главный спутник Нептуна
                    {"name": "Тритон", "distance": 3.5, "radius": 4, "speed": 2.0,
                     "angle": random.uniform(0, 2*math.pi), "color": "#C0C0C0"}
                ],
                "temperature": "-218°C",
                "mass": "1.02×10²⁶ кг",
                "density": "1.64 г/см³",
                "gravity": "11.2",
                "gravity_unit": "м/с²",
                "discovery": "1846, Галле и д'Арре",
                "description": "Самая ветреная планета",
                "fun_fact": "Ветры на Нептуне достигают 2100 км/ч!",
                "image_path": "photo_5260428536751788529_x (1)-no-bg-preview (carve.photos).png",
                "emissivity": 0.2,
                "volume": "6.25×10¹³ км³",
                "escape_velocity": "23.5 км/с"
            }
        ]
        
        # Добавляем Плутон (карликовая планета)
        self.planets_data.append({
            "name": "Плутон",
            "name_en": "Pluto",
            "distance": 39.5,
            "radius": 4,
            "base_radius": 4,
            "color": "#A0522D",
            "color2": "#8B4513",
            "color3": "#CD853F",
            "speed": 1/248.0,
            "angle": random.uniform(0, 2*math.pi),
            "rotation": 0,
            "rotation_speed": 0.01,
            "orbit_tilt": 2.0,
            "texture": "dwarf",
            "atmosphere": None,
            "has_rings": False,
            "has_moons": True,
            "moon_count": 5,
            "moons": [
                # Харон - спутник Плутона
                {"name": "Харон", "distance": 2.0, "radius": 2, "speed": 6.0,
                 "angle": random.uniform(0, 2*math.pi), "color": "#808080"}
            ],
            "temperature": "-233°C",
            "mass": "1.31×10²² кг",
            "density": "1.85 г/см³",
            "gravity": "0.62",
            "gravity_unit": "м/с²",
            "discovery": "1930, Клайд Томбо",
            "description": "Карликовая планета",
            "fun_fact": "Плутон меньше России!",
            "image_path": "images/pluto.png",
            "emissivity": 0.1,
            "volume": "7.0×10⁹ км³",
            "escape_velocity": "1.2 км/с"
        })
        
        # Добавляем Цереру (карликовая планета в поясе астероидов)
        self.planets_data.append({
            "name": "Церера",
            "name_en": "Ceres",
            "distance": 2.8,
            "radius": 3,
            "base_radius": 3,
            "color": "#8B7355",
            "color2": "#6B4F3A",
            "color3": "#A87B5A",
            "speed": 1/4.6,
            "angle": random.uniform(0, 2*math.pi),
            "rotation": 0,
            "rotation_speed": 0.02,
            "orbit_tilt": 0.5,
            "texture": "dwarf",
            "atmosphere": None,
            "has_rings": False,
            "has_moons": False,
            "moon_count": 0,
            "moons": [],
            "temperature": "-105°C",
            "mass": "9.4×10²⁰ кг",
            "density": "2.16 г/см³",
            "gravity": "0.27",
            "gravity_unit": "м/с²",
            "discovery": "1801, Джузеппе Пиацци",
            "description": "Карликовая планета в поясе астероидов",
            "fun_fact": "Церера составляет 1/3 массы пояса астероидов",
            "image_path": "images/ceres.png",
            "emissivity": 0.1,
            "volume": "4.3×10⁸ км³",
            "escape_velocity": "0.5 км/с"
        })
        
        # ==================== ЗАГРУЗКА ИЗОБРАЖЕНИЙ ====================
        
        # Словарь для хранения изображений планет
        self.planet_images = {}
        
        # Словарь для хранения сгенерированных текстур
        self.textures = {}
        
        # Кэш для эффектов
        self.effects_cache = {}
        
        # Список фоновых изображений
        self.background_images = []
        
        # Список для хранения фото в описании (чтобы не удалялись сборщиком мусора)
        self.info_photos = []
        
        # Создаем необходимые папки, если их нет
        os.makedirs("images", exist_ok=True)        # Для изображений планет
        os.makedirs("textures", exist_ok=True)      # Для текстур
        os.makedirs("saves", exist_ok=True)          # Для сохранений
        os.makedirs("screenshots", exist_ok=True)    # Для скриншотов
        os.makedirs("backgrounds", exist_ok=True)    # Для фонов
        
        # Загружаем изображение Солнца
        self.load_sun_image()
        
        # Загружаем изображения планет
        self.load_planet_images()
        
        # Генерируем текстуры
        self.generate_textures()
        
        # Загружаем фоновые изображения
        self.load_backgrounds()
        
        # ==================== ИНФОРМАЦИЯ О ПЛАНЕТАХ ====================
        
        # Собираем подробную информацию о планетах
        self.planet_info = self.collect_mega_info()
        
        # ==================== СОЗДАНИЕ ИНТЕРФЕЙСА ====================
        
        # Создаем пользовательский интерфейс
        self.create_mega_interface()
        
        # ==================== ЗАПУСК АНИМАЦИИ ====================
        
        # Запускаем главный цикл анимации
        self.animate()
        
        # ==================== ЗАПУСК ФОНОВЫХ ЗАДАЧ ====================
        
        # Запускаем фоновые задачи (подсчет FPS)
        self.start_background_tasks()
    
    def load_sun_image(self):
        """Загрузка изображения Солнца из предоставленного файла"""
        
        # Проверяем, установлена ли библиотека Pillow
        if not HAS_PIL:
            print("⚠️ PIL не установлен, не могу загрузить изображение Солнца")
            return
        
        # Путь к файлу с изображением Солнца
        sun_image_path = "photo_5260428536751788519_y (1)-no-bg-preview (carve.photos).png"
        
        # Проверяем, существует ли файл с изображением
        if os.path.exists("photo_5260428536751788519_y (1)-no-bg-preview (carve.photos).png"):
            try:
                # Загружаем изображение
                img = Image.open("photo_5260428536751788519_y (1)-no-bg-preview (carve.photos).png")
                
                # Конвертируем в формат RGBA (с альфа-каналом для прозрачности)
                if img.mode != 'RGBA':
                    img = img.convert('RGBA')
                
                # Улучшаем контрастность изображения
                enhancer = ImageEnhance.Contrast(img)
                img = enhancer.enhance(1.2)  # Увеличиваем контраст на 20%
                
                # Улучшаем яркость изображения
                enhancer = ImageEnhance.Brightness(img)
                img = enhancer.enhance(1.1)  # Увеличиваем яркость на 10%
                
                # Сохраняем оригинальное изображение
                self.sun_image_original = img
                
                # Создаем кэш для разных размеров (чтобы не масштабировать каждый кадр)
                self.sun_images_cache = {}
                
                print("✅ Загружено пользовательское изображение Солнца")
                
            except Exception as e:
                # В случае ошибки выводим сообщение и устанавливаем None
                print(f"❌ Ошибка загрузки изображения Солнца: {e}")
                self.sun_image_original = None
                self.sun_images_cache = {}
        else:
            # Если файл не найден
            print("⚠️ Файл с изображением Солнца не найден")
            self.sun_image_original = None
            self.sun_images_cache = {}
    
    def generate_stars(self, count):
        """Генерация улучшенного звездного поля"""
        
        # Создаем пустой список для звезд
        stars = []
        
        # Генерируем указанное количество звезд
        for _ in range(count):
            # Случайная позиция X (0-2000 пикселей)
            x = random.randint(0, 2000)
            
            # Случайная позиция Y (0-1500 пикселей)
            y = random.randint(0, 1500)
            
            # Глубина звезды (0.1 - далеко, 1.0 - близко) для эффекта параллакса
            z = random.uniform(0.1, 1.0)
            
            # Размер звезды с учетом глубины (ближние кажутся больше)
            size = random.uniform(0.5, 3.0) * z
            
            # Базовая яркость (100-255)
            brightness = random.randint(100, 255)
            
            # Скорость мерцания
            twinkle_speed = random.uniform(0.01, 0.1)
            
            # Смещение фазы мерцания
            twinkle_offset = random.uniform(0, 2*math.pi)
            
            # Цветовая температура
            color_temp = random.choice(['white', 'blue', 'red', 'yellow', 'orange'])
            
            # Спектральный класс (астрономическая классификация)
            spectral_class = random.choice(['O', 'B', 'A', 'F', 'G', 'K', 'M'])
            
            # Переменная звезда (мерцает) - 10% вероятность
            variable = random.random() < 0.1
            
            # Есть ли экзопланеты - 1% вероятность
            has_planet = random.random() < 0.01
            
            # Добавляем звезду в список
            stars.append({
                'x': x,                       # Координата X
                'y': y,                       # Координата Y
                'z': z,                       # Глубина
                'size': size,                  # Текущий размер
                'base_size': size,              # Базовый размер
                'brightness': brightness,       # Текущая яркость
                'base_brightness': brightness,   # Базовая яркость
                'twinkle_speed': twinkle_speed,  # Скорость мерцания
                'twinkle_offset': twinkle_offset, # Смещение мерцания
                'color_temp': color_temp,        # Цветовая температура
                'spectral_class': spectral_class, # Спектральный класс
                'variable': variable,            # Флаг переменности
                'has_planet': has_planet         # Наличие экзопланет
            })
        
        # Возвращаем сгенерированный список звезд
        return stars
    
    def generate_deep_space(self, count):
        """Генерация улучшенных объектов глубокого космоса"""
        
        # Создаем пустой список для объектов
        objects = []
        
        # Возможные типы объектов
        types = ['galaxy', 'nebula', 'globular_cluster', 'quasar', 'pulsar']
        
        # Генерируем указанное количество объектов
        for _ in range(count):
            # Случайная позиция X
            x = random.randint(0, 2000)
            
            # Случайная позиция Y
            y = random.randint(0, 1500)
            
            # Случайный радиус (30-150 пикселей)
            radius = random.randint(30, 150)
            
            # Случайный тип объекта
            obj_type = random.choice(types)
            
            # Случайный цвет в формате RGB (0-1)
            r, g, b = random.choice([
                (0.8, 0.2, 0.3), (0.3, 0.4, 0.8), (0.2, 0.8, 0.4),
                (0.6, 0.3, 0.7), (0.9, 0.5, 0.2), (0.4, 0.8, 0.8),
                (0.7, 0.2, 0.5), (0.3, 0.6, 0.9)
            ])
            
            # Добавляем объект в список
            objects.append({
                'x': x,                         # Координата X
                'y': y,                         # Координата Y
                'radius': radius,                 # Радиус
                'type': obj_type,                 # Тип объекта
                'color': (r, g, b),               # Цвет
                'opacity': random.uniform(0.1, 0.3), # Прозрачность
                'rotation': random.uniform(0, 2*math.pi) # Начальный угол поворота
            })
        
        # Возвращаем сгенерированный список объектов
        return objects
    
    def generate_nebulae(self, count):
        """Генерация улучшенных туманностей"""
        
        # Создаем пустой список для туманностей
        nebulae = []
        
        # Генерируем указанное количество туманностей
        for _ in range(count):
            # Случайная позиция X
            x = random.randint(0, 2000)
            
            # Случайная позиция Y
            y = random.randint(0, 1500)
            
            # Случайный радиус (100-300 пикселей)
            radius = random.randint(100, 300)
            
            # Случайная форма
            shape = random.choice(['spiral', 'circle', 'irregular', 'ring', 'bipolar'])
            
            # Случайный цвет
            r, g, b = random.choice([
                (0.9, 0.3, 0.4), (0.3, 0.4, 0.9), (0.4, 0.9, 0.5),
                (0.8, 0.5, 0.2), (0.6, 0.3, 0.8), (0.2, 0.5, 0.9)
            ])
            
            # Добавляем туманность в список
            nebulae.append({
                'x': x,                         # Координата X
                'y': y,                         # Координата Y
                'radius': radius,                 # Радиус
                'shape': shape,                   # Форма
                'color': (r, g, b),               # Цвет
                'opacity': random.uniform(0.1, 0.3), # Прозрачность
                'pulse': random.uniform(0.05, 0.15), # Скорость пульсации
                'rotation': 0                      # Текущий угол поворота
            })
        
        # Возвращаем сгенерированный список туманностей
        return nebulae
    
    def generate_asteroid_belt(self, count):
        """Генерация улучшенного пояса астероидов"""
        
        # Создаем пустой список для астероидов
        asteroids = []
        
        # Генерируем указанное количество астероидов
        for _ in range(count):
            # Расстояние от Солнца (2.0-3.5 АЕ) - между Марсом и Юпитером
            distance = random.uniform(2.0, 3.5)
            
            # Начальный угол на орбите
            angle = random.uniform(0, 2*math.pi)
            
            # Размер астероида (0.5-3.0 пикселя)
            size = random.uniform(0.5, 3.0)
            
            # Цвет астероида
            color = random.choice(['#808080', '#A0522D', '#8B4513', '#696969', '#C0C0C0'])
            
            # Скорость движения (медленнее планет)
            speed = random.uniform(0.8, 1.2) * 0.5
            
            # Состав астероида (для будущих расширений)
            composition = random.choice(['rocky', 'metallic', 'carbonaceous'])
            
            # Добавляем астероид в список
            asteroids.append({
                'distance': distance,   # Расстояние от Солнца
                'angle': angle,         # Угол на орбите
                'size': size,           # Размер
                'color': color,         # Цвет
                'speed': speed,         # Скорость
                'composition': composition # Состав
            })
        
        # Возвращаем сгенерированный список астероидов
        return asteroids
    
    def generate_comets(self, count):
        """Генерация улучшенных комет"""
        
        # Создаем пустой список для комет
        comets = []
        
        # Генерируем указанное количество комет
        for _ in range(count):
            # Добавляем комету в список
            comets.append({
                'active': False,        # Активна ли комета
                'x': 0,                  # Текущая позиция X
                'y': 0,                  # Текущая позиция Y
                'vx': 0,                 # Скорость по X
                'vy': 0,                 # Скорость по Y
                'tail': [],              # Массив для хвоста (предыдущие позиции)
                'life': 0,               # Текущее время жизни
                'max_life': random.randint(300, 800), # Максимальное время жизни
                'color': random.choice(['#00FFFF', '#FFD700', '#FF69B4', '#87CEEB']), # Цвет
                'tail_length': random.randint(30, 100) # Длина хвоста
            })
        
        # Возвращаем сгенерированный список комет
        return comets
    
    def generate_constellations(self):
        """Генерация реалистичных созвездий"""
        
        # Создаем пустой список для созвездий
        constellations = []
        
        # Названия созвездий
        names = ['Орион', 'Большая Медведица', 'Малая Медведица', 'Кассиопея', 'Лебедь', 
                 'Дракон', 'Геркулес', 'Андромеда', 'Персей', 'Цефей']
        
        # Для каждого названия создаем созвездие
        for name in names:
            # Список звезд в созвездии
            stars = []
            
            # Генерируем от 5 до 15 звезд в созвездии
            for _ in range(random.randint(5, 15)):
                # Случайная позиция X
                x = random.randint(200, 1800)
                
                # Случайная позиция Y
                y = random.randint(100, 900)
                
                # Яркость звезды
                brightness = random.randint(150, 255)
                
                # Добавляем звезду в список
                stars.append((x, y, brightness))
            
            # Добавляем созвездие в список
            constellations.append({'name': name, 'stars': stars})
        
        # Возвращаем сгенерированный список созвездий
        return constellations
    
    def generate_black_holes(self, count):
        """Генерация черных дыр с эффектами"""
        
        # Создаем пустой список для черных дыр
        holes = []
        
        # Генерируем указанное количество черных дыр
        for _ in range(count):
            # Добавляем черную дыру в список
            holes.append({
                'x': random.randint(200, 1800),      # Координата X
                'y': random.randint(100, 900),       # Координата Y
                'mass': random.uniform(10, 100),      # Масса
                'active': random.choice([True, False]), # Активна ли
                'accretion_disk': random.random() < 0.7, # Есть ли аккреционный диск
                'pulse': random.uniform(0.05, 0.2),    # Скорость пульсации
                'phase': random.uniform(0, 2*math.pi)  # Фаза пульсации
            })
        
        # Возвращаем сгенерированный список черных дыр
        return holes
    
    def load_planet_images(self):
        """Улучшенная загрузка изображений планет"""
        
        # Проверяем, установлена ли библиотека Pillow
        if not HAS_PIL:
            return
        
        # Для каждой планеты пытаемся загрузить изображение
        for planet in self.planets_data:
            try:
                # Проверяем, существует ли файл с изображением
                if os.path.exists(planet["image_path"]):
                    # Открываем изображение
                    img = Image.open(planet["image_path"])
                    
                    # Конвертируем в RGBA если нужно
                    if img.mode != 'RGBA':
                        img = img.convert('RGBA')
                    
                    # Улучшаем резкость
                    enhancer = ImageEnhance.Sharpness(img)
                    img = enhancer.enhance(1.3)  # +30% резкости
                    
                    # Улучшаем контрастность
                    enhancer = ImageEnhance.Contrast(img)
                    img = enhancer.enhance(1.2)  # +20% контраста
                    
                    # Улучшаем яркость
                    enhancer = ImageEnhance.Brightness(img)
                    img = enhancer.enhance(1.1)  # +10% яркости
                    
                    # Сохраняем изображение в словарь
                    self.planet_images[planet["name"]] = img
                    print(f"✅ Загружено изображение для {planet['name']}")
                else:
                    print(f"⚠️ Изображение не найдено: {planet['image_path']}")
            except Exception as e:
                # В случае ошибки выводим сообщение
                print(f"❌ Ошибка загрузки {planet['name']}: {e}")
    
    def load_backgrounds(self):
        """Загрузка фоновых изображений"""
        
        # Проверяем, установлена ли библиотека Pillow
        if not HAS_PIL:
            return
        
        # Список файлов фонов
        bg_files = ['bg1.jpg', 'bg2.jpg', 'bg3.jpg', 'bg4.jpg']
        
        # Для каждого файла пытаемся загрузить
        for bg_file in bg_files:
            # Формируем полный путь
            bg_path = os.path.join('backgrounds', bg_file)
            
            # Проверяем, существует ли файл
            if os.path.exists(bg_path):
                try:
                    # Открываем изображение
                    img = Image.open(bg_path)
                    
                    # Масштабируем под размер окна
                    img = img.resize((1900, 1000), Image.Resampling.LANCZOS)
                    
                    # Конвертируем в формат Tkinter и добавляем в список
                    self.background_images.append(ImageTk.PhotoImage(img))
                except:
                    # Игнорируем ошибки загрузки
                    pass
    
    def generate_textures(self):
        """Генерация улучшенных текстур для планет"""
        
        # Проверяем, установлена ли библиотека Pillow
        if not HAS_PIL:
            return
        
        try:
            # ===== Текстура Земли =====
            # Создаем новое изображение 256x256 с синим фоном
            earth_tex = Image.new('RGBA', (256, 256), (46, 134, 193, 255))
            
            # Создаем объект для рисования
            draw = ImageDraw.Draw(earth_tex)
            
            # Рисуем 500 случайных пятен для имитации материков
            for _ in range(500):
                # Случайная позиция
                x = random.randint(0, 255)
                y = random.randint(0, 255)
                
                # Случайный радиус
                r = random.randint(2, 5)
                
                # Цвет: зеленый с 70% вероятностью, темно-зеленый с 30%
                color = (46, 200, 100, 255) if random.random() > 0.7 else (0, 100, 0, 255)
                
                # Рисуем эллипс (пятно)
                draw.ellipse([x-r, y-r, x+r, y+r], fill=color)
            
            # Применяем размытие для плавности
            earth_tex = earth_tex.filter(ImageFilter.GaussianBlur(2))
            
            # Сохраняем текстуру
            self.textures['earth'] = earth_tex
            
            # ===== Текстура Марса =====
            # Создаем изображение с красным фоном
            mars_tex = Image.new('RGBA', (256, 256), (192, 57, 43, 255))
            draw = ImageDraw.Draw(mars_tex)
            
            # Рисуем 500 пятен
            for _ in range(500):
                x = random.randint(0, 255)
                y = random.randint(0, 255)
                r = random.randint(2, 6)
                # Темные пятна с 80% вероятностью, фиолетовые с 20%
                color = (155, 89, 182, 255) if random.random() > 0.8 else (142, 68, 173, 255)
                draw.ellipse([x-r, y-r, x+r, y+r], fill=color)
            
            # Размытие
            mars_tex = mars_tex.filter(ImageFilter.GaussianBlur(2))
            self.textures['mars'] = mars_tex
            
            # ===== Текстура Юпитера =====
            # Создаем изображение с желтым фоном
            jupiter_tex = Image.new('RGBA', (256, 256), (212, 172, 13, 255))
            draw = ImageDraw.Draw(jupiter_tex)
            
            # Рисуем полосы (характерные для Юпитера)
            for i in range(10):
                # Позиция полосы со случайным смещением
                y = i * 25 + random.randint(-5, 5)
                # Рисуем горизонтальную полосу
                draw.rectangle([0, y, 255, y+5], fill=(184, 115, 51, 255))
            
            # Размытие для смешивания
            jupiter_tex = jupiter_tex.filter(ImageFilter.GaussianBlur(3))
            self.textures['jupiter'] = jupiter_tex
            
        except Exception as e:
            print(f"Ошибка генерации текстур: {e}")
    
    def extract_number(self, value):
        """Улучшенное извлечение числа из строки"""
        
        # Если это уже число, просто возвращаем его
        if isinstance(value, (int, float)):
            return float(value)
        
        try:
            # Импортируем модуль для регулярных выражений
            import re
            
            # Ищем число в строке (возможно с минусом и точкой)
            match = re.search(r'[-+]?\d*\.?\d+', str(value))
            
            # Если нашли, конвертируем в float
            if match:
                return float(match.group())
            
            # Если не нашли, возвращаем 0
            return 0.0
        except:
            # В случае ошибки возвращаем 0
            return 0.0
    
    def collect_mega_info(self):
        """Сбор ультра-информации о планетах"""
        
        # Создаем словарь для информации
        info = {}
        
        # Для каждой планеты собираем данные
        for planet in self.planets_data:
            # Извлекаем числовое значение гравитации
            gravity_val = self.extract_number(planet['gravity'])
            
            # Вычисляем орбитальную скорость (упрощенная формула)
            if planet['speed'] > 0:
                orbital_velocity = 2 * math.pi * planet['distance'] * 149.6 / (planet['speed'] * 365)
            else:
                orbital_velocity = 0
            
            # Вычисляем скорость убегания (вторая космическая)
            if gravity_val > 0:
                escape_velocity = math.sqrt(2 * gravity_val * 1000)
            else:
                escape_velocity = 0
            
            # Формируем структурированную информацию
            info[planet['name']] = {
                # Основная информация
                "Название": planet['name'],
                "Английское название": planet.get('name_en', ''),
                "Тип": "Планета" if planet['radius'] > 5 else "Карликовая планета",
                
                # Физические характеристики
                "Физические характеристики": {
                    "Радиус (км)": f"{planet['base_radius'] * 600:.0f}",
                    "Радиус (от Земли)": f"{planet['base_radius']/11:.2f}",
                    "Масса": planet['mass'],
                    "Объем": planet.get('volume', 'Неизвестно'),
                    "Плотность": planet['density'],
                    "Сила тяжести": f"{planet['gravity']} {planet.get('gravity_unit', 'м/с²')}",
                    "Температура": planet['temperature'],
                    "Скорость убегания": planet.get('escape_velocity', f"{escape_velocity:.1f} км/с")
                },
                
                # Орбитальные характеристики
                "Орбитальные характеристики": {
                    "Расстояние от Солнца": f"{planet['distance']} АЕ ({planet['distance']*149.6:.1f} млн км)",
                    "Орбитальный период": f"{1/planet['speed']:.2f} земных лет" if planet['speed'] > 0 else "Неизвестно",
                    "Орбитальная скорость": f"{orbital_velocity:.1f} км/с",
                    "Наклон орбиты": f"{planet.get('orbit_tilt', 0) * 10:.1f}°"
                },
                
                # Вращение
                "Вращение": {
                    "Период вращения": f"{24/abs(planet['rotation_speed']):.1f} часов" if planet['rotation_speed'] != 0 else "Синхронное",
                    "Направление вращения": "Прямое" if planet['rotation_speed'] > 0 else "Обратное"
                },
                
                # Состав и структура
                "Состав": {
                    "Атмосфера": "Есть" if planet.get('atmosphere') else "Нет",
                    "Состав атмосферы": planet.get('atmosphere', 'Отсутствует'),
                    "Кольца": "Есть" if planet.get('has_rings') else "Нет",
                    "Количество колец": planet.get('ring_count', 0),
                    "Спутники": planet['moon_count']
                },
                
                # История
                "История": {
                    "Открытие": planet['discovery'],
                    "Названа в честь": self.get_name_origin(planet['name'])
                },
                
                # Интересное
                "Интересное": {
                    "Описание": planet['description'],
                    "Интересный факт": planet['fun_fact']
                },
                
                # Технические параметры
                "Технические": {
                    "Альбедо": f"{planet.get('emissivity', 0.2):.2f}",
                    "Видимая звездная величина": f"{-2.5 * math.log10(max(0.01, planet['emissivity'])):.1f}"
                }
            }
        
        # Возвращаем собранную информацию
        return info
    
    def get_name_origin(self, name):
        """Возвращает происхождение названия планеты"""
        
        # Словарь с происхождением названий
        origins = {
            "Меркурий": "Римский бог торговли",
            "Венера": "Римская богиня любви",
            "Земля": "Почва, суша",
            "Марс": "Римский бог войны",
            "Юпитер": "Верховный римский бог",
            "Сатурн": "Римский бог земледелия",
            "Уран": "Греческий бог неба",
            "Нептун": "Римский бог морей",
            "Плутон": "Римский бог подземного мира",
            "Церера": "Римская богиня земледелия"
        }
        
        # Возвращаем происхождение или "Неизвестно"
        return origins.get(name, "Неизвестно")
    
    def create_mega_interface(self):
        """Создание ультимативного интерфейса"""
        
        # ===== ГЛАВНЫЙ КОНТЕЙНЕР =====
        # Создаем фрейм для всего содержимого
        main_frame = tk.Frame(self.root, bg='#000000')
        main_frame.pack(fill=tk.BOTH, expand=True)  # Заполняет все окно
        
        # ===== ВЕРХНЯЯ ПАНЕЛЬ =====
        # Создаем верхнюю панель с темно-синим фоном
        top_bar = tk.Frame(main_frame, bg='#0a0a2a', height=80)
        top_bar.pack(fill=tk.X)  # Растягивается по горизонтали
        top_bar.pack_propagate(False)  # Запрещаем изменение размера
        
        # ===== ЛОГОТИП =====
        # Фрейм для логотипа
        title_frame = tk.Frame(top_bar, bg='#0a0a2a')
        title_frame.pack(side=tk.LEFT, padx=20)  # Слева с отступом
        
        # Иконка галактики
        tk.Label(title_frame, text="🌌", bg='#0a0a2a', fg='#FFD700',
                font=('Arial', 36)).pack(side=tk.LEFT)
        
        # Текст заголовка
        tk.Label(title_frame, text="МЕГА-СИМУЛЯЦИЯ\nСОЛНЕЧНОЙ СИСТЕМЫ 3000 ULTIMATE", 
                bg='#0a0a2a', fg='#FFD700', font=('Arial', 16, 'bold'),
                justify=tk.LEFT).pack(side=tk.LEFT, padx=10)
        
        # ===== СТАТУС БАР =====
        # Фрейм для статуса
        status_frame = tk.Frame(top_bar, bg='#0a0a2a')
        status_frame.pack(side=tk.RIGHT, padx=20)  # Справа с отступом
        
        # Метка для FPS
        self.fps_label = tk.Label(status_frame, text="FPS: 60", bg='#0a0a2a', fg='#00FF00',
                                 font=('Arial', 10, 'bold'))
        self.fps_label.pack(anchor='e')  # Выравнивание справа
        
        # Метка для времени
        self.time_label = tk.Label(status_frame, text="Время: 0", bg='#0a0a2a', fg='#00FF00',
                                  font=('Arial', 10, 'bold'))
        self.time_label.pack(anchor='e')
        
        # Метка для зума
        self.zoom_status = tk.Label(status_frame, text="Зум: 1.0x", bg='#0a0a2a', fg='#00FF00',
                                   font=('Arial', 10, 'bold'))
        self.zoom_status.pack(anchor='e')
        
        # Метка для координат мыши
        self.coord_label = tk.Label(status_frame, text="X: 0 Y: 0", bg='#0a0a2a', fg='#00FF00',
                                   font=('Arial', 10, 'bold'))
        self.coord_label.pack(anchor='e')
        
        # ===== КНОПКИ УПРАВЛЕНИЯ ИНТЕРФЕЙСОМ =====
        # Фрейм для кнопок
        ui_buttons = tk.Frame(top_bar, bg='#0a0a2a')
        ui_buttons.pack(side=tk.RIGHT, padx=10)
        
        # Кнопка полноэкранного режима
        self.fullscreen_btn = tk.Button(ui_buttons, text="⛶", command=self.toggle_fullscreen,
                                       bg='#4a6a9a', fg='white', font=('Arial', 12, 'bold'),
                                       width=3, relief=tk.RAISED, bd=2)
        self.fullscreen_btn.pack(side=tk.LEFT, padx=2)
        
        # Кнопка скрытия/показа панели управления
        self.controls_btn = tk.Button(ui_buttons, text="▼", command=self.toggle_control_panel,
                                     bg='#4a6a9a', fg='white', font=('Arial', 12, 'bold'),
                                     width=3, relief=tk.RAISED, bd=2)
        self.controls_btn.pack(side=tk.LEFT, padx=2)
        
        # ===== ОСНОВНОЙ КОНТЕЙНЕР =====
        # Фрейм для основного содержимого
        content_frame = tk.Frame(main_frame, bg='#000000')
        content_frame.pack(fill=tk.BOTH, expand=True)
        
        # ===== ЛЕВЫЙ ФРЕЙМ С КАНВАСОМ =====
        # Фрейм для канваса
        canvas_frame = tk.Frame(content_frame, bg='#000000')
        canvas_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # ===== КАНВАС =====
        # Создаем холст для рисования
        self.canvas = tk.Canvas(canvas_frame, width=1300, height=800,
                               bg='#000000', highlightthickness=0,
                               cursor='crosshair')  # Курсор в виде перекрестия
        self.canvas.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)
        
        # ===== ПРИВЯЗКА СОБЫТИЙ =====
        # Клик левой кнопкой мыши
        self.canvas.bind("<Button-1>", self.on_canvas_click)
        
        # Перетаскивание с зажатой левой кнопкой
        self.canvas.bind("<B1-Motion>", self.on_canvas_drag)
        
        # Отпускание левой кнопки
        self.canvas.bind("<ButtonRelease-1>", self.on_canvas_release)
        
        # Колесико мыши (Windows)
        self.canvas.bind("<MouseWheel>", self.on_mousewheel)
        
        # Движение мыши
        self.canvas.bind("<Motion>", self.on_mouse_move)
        
        # Правая кнопка мыши
        self.canvas.bind("<Button-3>", self.on_right_click)
        
        # Двойной клик левой кнопкой
        self.canvas.bind("<Double-Button-1>", self.on_double_click)
        
        # Колесико с зажатым Ctrl (точный зум)
        self.canvas.bind("<Control-MouseWheel>", self.on_control_mousewheel)
        
        # Колесико с зажатым Shift (горизонтальный скролл)
        self.canvas.bind("<Shift-MouseWheel>", self.on_shift_mousewheel)
        
        # Колесико вверх (Linux)
        self.canvas.bind("<Button-4>", self.on_mousewheel_linux_up)
        
        # Колесико вниз (Linux)
        self.canvas.bind("<Button-5>", self.on_mousewheel_linux_down)
        
        # ===== ПАНЕЛЬ УПРАВЛЕНИЯ =====
        # Создаем панель управления
        self.control_panel = tk.Frame(canvas_frame, bg='#0a0a2a', height=200, relief=tk.RAISED, bd=3)
        self.control_panel.pack(fill=tk.X, padx=10, pady=(0, 10))
        self.control_panel.pack_propagate(False)  # Запрещаем изменение размера
        
        # ===== НОУТБУК С ВКЛАДКАМИ =====
        # Создаем виджет с вкладками
        notebook = ttk.Notebook(self.control_panel)
        notebook.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Настраиваем стиль вкладок
        style = ttk.Style()
        style.theme_use('clam')  # Используем тему clam
        style.configure("TNotebook", background='#0a0a2a', borderwidth=0)
        style.configure("TNotebook.Tab", background='#1a1a3a', foreground='white', padding=[15, 5])
        style.map("TNotebook.Tab", background=[("selected", '#4a6a9a')])
        
        # ===== ВКЛАДКА УПРАВЛЕНИЯ =====
        control_tab = tk.Frame(notebook, bg='#0a0a2a')
        notebook.add(control_tab, text="⚙️ УПРАВЛЕНИЕ")
        
        # ----- Настройка скорости -----
        speed_frame = tk.Frame(control_tab, bg='#0a0a2a')
        speed_frame.pack(fill=tk.X, pady=5, padx=10)
        
        # Метка
        tk.Label(speed_frame, text="⏱️ СКОРОСТЬ:", bg='#0a0a2a', fg='#FFD700',
                font=('Arial', 10, 'bold'), width=12).pack(side=tk.LEFT)
        
        # Ползунок скорости
        self.time_scale = tk.Scale(speed_frame, from_=0.1, to=100, orient=tk.HORIZONTAL,
                                   length=300, command=self.change_time_speed,
                                   bg='#0a0a2a', fg='white', highlightbackground='#4a6a9a',
                                   troughcolor='#1a1a3a', resolution=0.1)
        self.time_scale.set(1.0)  # Начальное значение
        self.time_scale.pack(side=tk.LEFT, padx=5)
        
        # Метка со значением
        self.speed_label = tk.Label(speed_frame, text="1.0x", bg='#0a0a2a', fg='#00FF00',
                                   font=('Arial', 12, 'bold'), width=8)
        self.speed_label.pack(side=tk.LEFT)
        
        # ----- Настройка зума -----
        zoom_frame = tk.Frame(control_tab, bg='#0a0a2a')
        zoom_frame.pack(fill=tk.X, pady=5, padx=10)
        
        # Метка
        tk.Label(zoom_frame, text="🔍 ЗУМ:", bg='#0a0a2a', fg='#FFD700',
                font=('Arial', 10, 'bold'), width=12).pack(side=tk.LEFT)
        
        # Ползунок зума
        self.zoom_scale = tk.Scale(zoom_frame, from_=0.1, to=10.0, orient=tk.HORIZONTAL,
                                   length=300, command=self.change_zoom,
                                   bg='#0a0a2a', fg='white', highlightbackground='#4a6a9a',
                                   troughcolor='#1a1a3a', resolution=0.1)
        self.zoom_scale.set(1.0)  # Начальное значение
        self.zoom_scale.pack(side=tk.LEFT, padx=5)
        
        # Метка со значением
        self.zoom_label = tk.Label(zoom_frame, text="1.0x", bg='#0a0a2a', fg='#00FF00',
                                  font=('Arial', 12, 'bold'), width=8)
        self.zoom_label.pack(side=tk.LEFT)
        
        # ----- Кнопки точной настройки зума -----
        zoom_buttons = tk.Frame(zoom_frame, bg='#0a0a2a')
        zoom_buttons.pack(side=tk.LEFT, padx=10)
        
        # Кнопка увеличения
        tk.Button(zoom_buttons, text="+", command=self.zoom_in,
                 bg='#4a6a9a', fg='white', font=('Arial', 10, 'bold'),
                 width=3).pack(side=tk.LEFT, padx=2)
        
        # Кнопка уменьшения
        tk.Button(zoom_buttons, text="-", command=self.zoom_out,
                 bg='#4a6a9a', fg='white', font=('Arial', 10, 'bold'),
                 width=3).pack(side=tk.LEFT, padx=2)
        
        # Кнопка сброса зума
        tk.Button(zoom_buttons, text="1x", command=self.zoom_reset,
                 bg='#4a6a9a', fg='white', font=('Arial', 10, 'bold'),
                 width=3).pack(side=tk.LEFT, padx=2)
        
        # Кнопка автоматического зума
        tk.Button(zoom_buttons, text="🌍 ВСЕ", command=self.zoom_to_all_planets,
                 bg='#4a6a9a', fg='white', font=('Arial', 10, 'bold'),
                 width=3).pack(side=tk.LEFT, padx=2)
        
        # ----- Основные кнопки управления -----
        buttons_frame = tk.Frame(control_tab, bg='#0a0a2a')
        buttons_frame.pack(fill=tk.X, pady=10, padx=10)
        
        # Кнопка паузы
        self.pause_btn = tk.Button(buttons_frame, text="⏸️ ПАУЗА", command=self.toggle_pause,
                                  bg='#4a6a9a', fg='white', font=('Arial', 11, 'bold'),
                                  width=12, relief=tk.RAISED, bd=3)
        self.pause_btn.pack(side=tk.LEFT, padx=5)
        
        # Кнопка сброса
        reset_btn = tk.Button(buttons_frame, text="🔄 СБРОС", command=self.reset_simulation,
                             bg='#4a6a9a', fg='white', font=('Arial', 11, 'bold'),
                             width=12, relief=tk.RAISED, bd=3)
        reset_btn.pack(side=tk.LEFT, padx=5)
        
        # Кнопка центрирования
        center_btn = tk.Button(buttons_frame, text="🎯 ЦЕНТР", command=self.center_view,
                              bg='#4a6a9a', fg='white', font=('Arial', 11, 'bold'),
                              width=12, relief=tk.RAISED, bd=3)
        center_btn.pack(side=tk.LEFT, padx=5)
        
        # Кнопка следования за планетой
        self.follow_btn = tk.Button(buttons_frame, text="👁️ СЛЕДИТЬ", command=self.toggle_follow,
                                   bg='#4a6a9a', fg='white', font=('Arial', 11, 'bold'),
                                   width=12, relief=tk.RAISED, bd=3)
        self.follow_btn.pack(side=tk.LEFT, padx=5)
        
        # ===== ВКЛАДКА ОТОБРАЖЕНИЯ =====
        display_tab = tk.Frame(notebook, bg='#0a0a2a')
        notebook.add(display_tab, text="🎨 ОТОБРАЖЕНИЕ")
        
        # Переменные для чекбоксов
        self.orbits_var = tk.BooleanVar(value=True)        # Орбиты
        self.labels_var = tk.BooleanVar(value=True)        # Названия
        self.effects_var = tk.BooleanVar(value=True)       # Эффекты
        self.grid_var = tk.BooleanVar(value=False)         # Сетка
        self.asteroids_var = tk.BooleanVar(value=True)     # Астероиды
        self.nebula_var = tk.BooleanVar(value=True)        # Туманности
        self.trails_var = tk.BooleanVar(value=False)       # Траектории
        self.hdr_var = tk.BooleanVar(value=True)           # HDR режим
        self.minimap_var = tk.BooleanVar(value=True)       # Миникарта
        self.legend_var = tk.BooleanVar(value=True)        # Легенда
        self.constellations_var = tk.BooleanVar(value=False) # Созвездия
        
        # Создаем три колонки для чекбоксов
        check_frame1 = tk.Frame(display_tab, bg='#0a0a2a')
        check_frame1.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        check_frame2 = tk.Frame(display_tab, bg='#0a0a2a')
        check_frame2.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        check_frame3 = tk.Frame(display_tab, bg='#0a0a2a')
        check_frame3.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Первая колонка чекбоксов
        checks1 = [
            ("🔄 Орбиты", self.orbits_var, self.toggle_orbits),
            ("📝 Названия", self.labels_var, self.toggle_labels),
            ("✨ Эффекты", self.effects_var, self.toggle_effects),
            ("🔲 Сетка", self.grid_var, self.toggle_grid),
            ("☄️ Астероиды", self.asteroids_var, self.toggle_asteroids)
        ]
        
        # Добавляем чекбоксы в первую колонку
        for text, var, cmd in checks1:
            tk.Checkbutton(check_frame1, text=text, variable=var, command=cmd,
                          bg='#0a0a2a', fg='white', selectcolor='#0a0a2a',
                          activebackground='#0a0a2a', font=('Arial', 10)).pack(anchor='w', pady=3)
        
        # Вторая колонка чекбоксов
        checks2 = [
            ("🌌 Туманности", self.nebula_var, self.toggle_nebula),
            ("📈 Траектории", self.trails_var, self.toggle_trails),
            ("🌈 HDR режим", self.hdr_var, self.toggle_hdr),
            ("🗺️ Миникарта", self.minimap_var, self.toggle_minimap),
            ("📋 Легенда", self.legend_var, self.toggle_legend)
        ]
        
        # Добавляем чекбоксы во вторую колонку
        for text, var, cmd in checks2:
            tk.Checkbutton(check_frame2, text=text, variable=var, command=cmd,
                          bg='#0a0a2a', fg='white', selectcolor='#0a0a2a',
                          activebackground='#0a0a2a', font=('Arial', 10)).pack(anchor='w', pady=3)
        
        # Третья колонка чекбоксов (дополнительные эффекты)
        checks3 = [
            ("✨ Созвездия", self.constellations_var, self.toggle_constellations),
            ("⚫ Черные дыры", tk.BooleanVar(value=True), lambda: None),
            ("🛰️ Спутники", tk.BooleanVar(value=True), lambda: None),
            ("🚀 Станции", tk.BooleanVar(value=True), lambda: None)
        ]
        
        # Добавляем чекбоксы в третью колонку
        for text, var, cmd in checks3:
            tk.Checkbutton(check_frame3, text=text, variable=var, command=cmd,
                          bg='#0a0a2a', fg='white', selectcolor='#0a0a2a',
                          activebackground='#0a0a2a', font=('Arial', 10)).pack(anchor='w', pady=3)
        
        # ===== ВКЛАДКА ИНФОРМАЦИИ =====
        info_tab = tk.Frame(notebook, bg='#0a0a2a')
        notebook.add(info_tab, text="ℹ️ ИНФОРМАЦИЯ")
        
        # Фрейм для текста с прокруткой
        info_text_frame = tk.Frame(info_tab, bg='#0a0a2a')
        info_text_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Текстовое поле для информации
        self.info_text = tk.Text(info_text_frame, bg='#1a1a3a', fg='white',
                                 font=('Arial', 10), wrap=tk.WORD,
                                 height=10, width=60)
        self.info_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Полоса прокрутки
        scrollbar = tk.Scrollbar(info_text_frame, command=self.info_text.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.info_text.config(yscrollcommand=scrollbar.set)
        
        # ===== ВКЛАДКА СОХРАНЕНИЙ =====
        save_tab = tk.Frame(notebook, bg='#0a0a2a')
        notebook.add(save_tab, text="💾 СОХРАНЕНИЯ")
        
        # Фрейм для кнопок
        save_buttons_frame = tk.Frame(save_tab, bg='#0a0a2a')
        save_buttons_frame.pack(expand=True, pady=20)
        
        # Кнопка сохранения
        tk.Button(save_buttons_frame, text="💾 Сохранить симуляцию", command=self.save_simulation,
                 bg='#4a6a9a', fg='white', font=('Arial', 11, 'bold'),
                 width=25, height=2, relief=tk.RAISED, bd=3).pack(pady=5)
        
        # Кнопка загрузки
        tk.Button(save_buttons_frame, text="📂 Загрузить симуляцию", command=self.load_simulation,
                 bg='#4a6a9a', fg='white', font=('Arial', 11, 'bold'),
                 width=25, height=2, relief=tk.RAISED, bd=3).pack(pady=5)
        
        # Кнопка скриншота
        tk.Button(save_buttons_frame, text="📸 Сделать скриншот", command=self.take_screenshot,
                 bg='#4a6a9a', fg='white', font=('Arial', 11, 'bold'),
                 width=25, height=2, relief=tk.RAISED, bd=3).pack(pady=5)
        
        # Кнопка экспорта данных
        tk.Button(save_buttons_frame, text="📊 Экспорт данных", command=self.export_data,
                 bg='#4a6a9a', fg='white', font=('Arial', 11, 'bold'),
                 width=25, height=2, relief=tk.RAISED, bd=3).pack(pady=5)
        
        # ===== ПРАВАЯ ПАНЕЛЬ С ДЕТАЛЬНОЙ ИНФОРМАЦИЕЙ =====
        right_panel = tk.Frame(content_frame, width=400, bg='#0a0a2a', relief=tk.RAISED, bd=3)
        right_panel.pack(side=tk.RIGHT, fill=tk.Y, padx=10, pady=10)
        right_panel.pack_propagate(False)  # Запрещаем изменение размера
        
        # Заголовок панели
        tk.Label(right_panel, text="📊 ДЕТАЛЬНАЯ ИНФОРМАЦИЯ",
                bg='#1a1a3a', fg='#FFD700', font=('Arial', 14, 'bold')).pack(fill=tk.X, pady=5)
        
        # ===== ФРЕЙМ С ПРОКРУТКОЙ =====
        # Создаем Canvas для прокрутки
        canvas_right = tk.Canvas(right_panel, bg='#0a0a2a', highlightthickness=0)
        scrollbar_right = tk.Scrollbar(right_panel, orient="vertical", command=canvas_right.yview)
        
        # Создаем прокручиваемый фрейм
        self.scrollable_frame = tk.Frame(canvas_right, bg='#0a0a2a')
        
        # При изменении размера обновляем область прокрутки
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas_right.configure(scrollregion=canvas_right.bbox("all"))
        )
        
        # Добавляем фрейм в Canvas
        canvas_right.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        canvas_right.configure(yscrollcommand=scrollbar_right.set)
        
        # Размещаем Canvas и полосу прокрутки
        canvas_right.pack(side="left", fill="both", expand=True, padx=(5,0))
        scrollbar_right.pack(side="right", fill="y")
        
        # Показываем приветствие
        self.show_mega_welcome()
        
        # ===== ЛЕГЕНДА =====
        self.create_legend()
    
    def draw_sun_mega(self, center_x, center_y):
        """Рисует ультра-солнце с пользовательским изображением"""
        
        # Радиус Солнца с учетом зума (базовый радиус 50 пикселей)
        sun_radius = 50 * self.zoom_factor
        
        # Используем пользовательское изображение если доступно
        if HAS_PIL and hasattr(self, 'sun_image_original') and self.sun_image_original is not None:
            try:
                # Вычисляем целевой размер (диаметр)
                target_size = int(sun_radius * 2)
                
                # Рисуем только если размер достаточный
                if target_size > 10:
                    # Ключ для кэша
                    cache_key = f"sun_{target_size}"
                    
                    # Проверяем, есть ли изображение в кэше
                    if cache_key in self.sun_images_cache:
                        img_resized = self.sun_images_cache[cache_key]
                    else:
                        # Получаем оригинальное изображение
                        img = self.sun_image_original
                        
                        # Получаем оригинальные размеры
                        orig_width, orig_height = img.size
                        
                        # Вычисляем новый размер с сохранением пропорций
                        if orig_width > orig_height:
                            new_width = target_size
                            new_height = int(orig_height * (target_size / orig_width))
                        else:
                            new_height = target_size
                            new_width = int(orig_width * (target_size / orig_height))
                        
                        # Масштабируем изображение
                        img_resized = img.resize((new_width, new_height), Image.Resampling.LANCZOS)
                        
                        # Создаем квадратное полотно с прозрачным фоном
                        square_img = Image.new('RGBA', (target_size, target_size), (0, 0, 0, 0))
                        
                        # Вставляем изображение в центр
                        x_offset = (target_size - new_width) // 2
                        y_offset = (target_size - new_height) // 2
                        square_img.paste(img_resized, (x_offset, y_offset), img_resized)
                        
                        # Добавляем свечение (эффект короны)
                        glow = Image.new('RGBA', (target_size, target_size), (0, 0, 0, 0))
                        draw = ImageDraw.Draw(glow)
                        
                        # Рисуем несколько колец свечения
                        for i in range(5):
                            r = target_size//2 + i*3  # Радиус кольца
                            alpha = 100 - i*20        # Прозрачность уменьшается с удалением
                            draw.ellipse([target_size//2 - r, target_size//2 - r, 
                                         target_size//2 + r, target_size//2 + r], 
                                        outline=(255, 200, 0, alpha), width=2)
                        
                        # Накладываем свечение на изображение
                        img_resized = Image.alpha_composite(square_img, glow)
                        
                        # Сохраняем в кэш
                        self.sun_images_cache[cache_key] = img_resized
                    
                    # Конвертируем в формат Tkinter
                    self.sun_photo = ImageTk.PhotoImage(img_resized)
                    
                    # Отображаем на канвасе
                    self.canvas.create_image(center_x, center_y, image=self.sun_photo, anchor='center')
                    
                    # Добавляем эффекты поверх изображения (если включены)
                    if self.show_effects:
                        # Рисуем корону
                        for i in range(36):  # 36 лучей
                            angle = i * 10 * math.pi/180 + self.time_of_day
                            for j in range(3):  # 3 слоя
                                r_mult = 1.3 + j * 0.2
                                width = 3 - j
                                x1 = center_x + sun_radius * r_mult * math.cos(angle)
                                y1 = center_y + sun_radius * r_mult * math.sin(angle)
                                x2 = center_x + sun_radius * (r_mult + 0.5) * math.cos(angle + 0.1)
                                y2 = center_y + sun_radius * (r_mult + 0.5) * math.sin(angle + 0.1)
                                
                                color = ['#FFD700', '#FFA500', '#FF8C00'][j]
                                self.canvas.create_line(x1, y1, x2, y2, fill=color, width=width, smooth=True)
                        
                        # Рисуем вспышки
                        for _ in range(3):
                            angle = random.uniform(0, 2*math.pi)
                            dist = sun_radius * random.uniform(1.5, 2.5)
                            x = center_x + dist * math.cos(angle)
                            y = center_y + dist * math.sin(angle)
                            
                            self.canvas.create_line(center_x, center_y, x, y,
                                                   fill='#FFFF00', width=random.randint(2, 4),
                                                   dash=(2, 4))
                    
                    # Возвращаем радиус
                    return sun_radius
                    
            except Exception as e:
                # В случае ошибки выводим сообщение и продолжаем стандартным рисованием
                print(f"Ошибка при рисовании Солнца: {e}")
                pass
        
        # ===== СТАНДАРТНОЕ РИСОВАНИЕ СОЛНЦА =====
        # (используется если нет изображения или ошибка)
        
        # Рисуем внутреннее ядро с градиентом
        for i in range(15):
            r = sun_radius * (1 - i * 0.03)
            intensity = 255 - i * 12
            color = f'#{intensity:02x}{intensity-30:02x}00'
            self.canvas.create_oval(center_x - r, center_y - r,
                                    center_x + r, center_y + r,
                                    fill=color, outline='')
        
        # Рисуем корону (если включены эффекты)
        if self.show_effects:
            for i in range(72):  # 72 луча для плавности
                angle = i * 5 * math.pi/180 + self.time_of_day
                for j in range(4):  # 4 слоя
                    r_mult = 1.3 + j * 0.15
                    width = 4 - j
                    x1 = center_x + sun_radius * r_mult * math.cos(angle)
                    y1 = center_y + sun_radius * r_mult * math.sin(angle)
                    x2 = center_x + sun_radius * (r_mult + 0.4) * math.cos(angle + 0.15)
                    y2 = center_y + sun_radius * (r_mult + 0.4) * math.sin(angle + 0.15)
                    
                    color = ['#FFD700', '#FFA500', '#FF8C00', '#FF4500'][j]
                    self.canvas.create_line(x1, y1, x2, y2, fill=color, width=width, smooth=True)
            
            # Рисуем вспышки
            for _ in range(5):
                angle = random.uniform(0, 2*math.pi)
                dist = sun_radius * random.uniform(1.5, 3.0)
                x = center_x + dist * math.cos(angle)
                y = center_y + dist * math.sin(angle)
                
                self.canvas.create_line(center_x, center_y, x, y,
                                       fill='#FFFF00', width=random.randint(2, 6),
                                       dash=(2, 4))
        
        # Рисуем солнечные пятна
        for _ in range(8):
            spot_angle = random.uniform(0, 2*math.pi)
            spot_dist = random.uniform(0, sun_radius * 0.7)
            spot_x = center_x + spot_dist * math.cos(spot_angle)
            spot_y = center_y + spot_dist * math.sin(spot_angle)
            spot_r = random.uniform(5, 20) * self.zoom_factor
            
            self.canvas.create_oval(spot_x - spot_r, spot_y - spot_r,
                                    spot_x + spot_r, spot_y + spot_r,
                                    fill='#8B4513', outline='#CD853F', stipple='gray50')
        
        # Возвращаем радиус
        return sun_radius
    
    def zoom_to_all_planets(self):
        """Автоматический зум, чтобы были видны все планеты"""
        
        # Находим максимальное расстояние планеты от Солнца
        max_distance = max(planet["distance"] for planet in self.planets_data)
        
        # Добавляем запас для Плутона и колец (20%)
        max_distance = max(max_distance, 40) * 1.2
        
        # Ширина канваса
        canvas_width = 1300
        
        # Вычисляем нужный зум (чтобы вся система поместилась)
        # Формула: ширина / (макс_расстояние * 2 * АЕ)
        required_zoom = canvas_width / (max_distance * self.AU * 2)
        
        # Применяем зум с ограничениями
        self.zoom_scale.set(min(10.0, max(0.1, required_zoom)))
        
        # Центрируем вид
        self.center_view()
        
        # Показываем сообщение в информационном поле
        self.info_text.config(state=tk.NORMAL)
        self.info_text.delete(1.0, tk.END)
        self.info_text.insert(tk.END, "✅ Автоматический зум активирован!\n")
        self.info_text.insert(tk.END, f"Видно все планеты до Плутона\n")
        self.info_text.insert(tk.END, f"Масштаб: {self.zoom_factor:.2f}x")
        self.info_text.config(state=tk.DISABLED)
    
    def toggle_follow(self):
        """Включение/выключение следования за планетой"""
        
        # Проверяем, выбрана ли планета
        if not self.selected_planet:
            messagebox.showinfo("Внимание", "Сначала выберите планету!")
            return
        
        # Переключаем режим следования
        self.follow_selected = not self.follow_selected
        
        # Обновляем внешний вид кнопки
        if self.follow_selected:
            self.follow_btn.config(text="👁️ СЛЕДИТЬ (ВКЛ)", bg='#2a9a2a')
        else:
            self.follow_btn.config(text="👁️ СЛЕДИТЬ", bg='#4a6a9a')
    
    def create_legend(self):
        """Создание легенды (обозначений объектов)"""
        
        # Создаем фрейм для легенды
        self.legend_frame = tk.Frame(self.root, bg='#0a0a2a', relief=tk.RAISED, bd=2)
        self.legend_frame.place(x=10, y=100)  # Размещаем в левом верхнем углу
        
        # Заголовок легенды
        tk.Label(self.legend_frame, text="📋 ЛЕГЕНДА", bg='#1a1a3a', fg='#FFD700',
                font=('Arial', 10, 'bold')).pack(fill=tk.X, pady=2)
        
        # Элементы легенды (символ и описание)
        legend_items = [
            ("🟡", "Солнце (пользовательское)"),
            ("⚪", "Планета"),
            ("⚫", "Спутник"),
            ("☄️", "Астероид"),
            ("💫", "Комета"),
            ("🌌", "Туманность")
        ]
        
        # Добавляем каждый элемент
        for symbol, text in legend_items:
            item_frame = tk.Frame(self.legend_frame, bg='#0a0a2a')
            item_frame.pack(fill=tk.X, padx=5, pady=1)
            tk.Label(item_frame, text=symbol, bg='#0a0a2a', fg='white',
                    font=('Arial', 10)).pack(side=tk.LEFT)
            tk.Label(item_frame, text=text, bg='#0a0a2a', fg='white',
                    font=('Arial', 9)).pack(side=tk.LEFT, padx=5)
    
    def show_mega_welcome(self):
        """Показывает улучшенное приветствие в правой панели"""
        
        # Очищаем панель
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()
        
        # Заголовок
        tk.Label(self.scrollable_frame, text="🌌 ДОБРО ПОЖАЛОВАТЬ!",
                bg='#0a0a2a', fg='#FFD700', font=('Arial', 18, 'bold')).pack(pady=20)
        
        # Декоративные символы
        tk.Label(self.scrollable_frame, text="🪐✨🌟☄️🌠🚀",
                bg='#0a0a2a', fg='white', font=('Arial', 40)).pack(pady=10)
        
        # Фрейм со статистикой
        stats_frame = tk.Frame(self.scrollable_frame, bg='#1a1a3a', relief=tk.RIDGE, bd=2)
        stats_frame.pack(fill=tk.X, padx=15, pady=10)
        
        # Подсчитываем общее количество объектов
        total_moons = self.total_moons()
        total_objects = len(self.planets_data) + total_moons + len(self.asteroids) + len(self.stars)
        
        # Статистические данные
        stats = [
            f"Планет: {len(self.planets_data)}",
            f"Спутников: {total_moons}",
            f"Астероидов: {len(self.asteroids)}",
            f"Звезд: {len(self.stars)}",
            f"Всего объектов: {total_objects}",
            f"Возраст системы: 4.6 млрд лет",
            f"Галактика: Млечный Путь"
        ]
        
        # Отображаем статистику
        for stat in stats:
            tk.Label(stats_frame, text=f"• {stat}", bg='#1a1a3a', fg='#87CEEB',
                    font=('Arial', 10)).pack(anchor='w', padx=10, pady=2)
        
        # Фрейм с управлением
        guide_frame = tk.Frame(self.scrollable_frame, bg='#0a0a2a')
        guide_frame.pack(fill=tk.X, padx=15, pady=10)
        
        # Заголовок раздела управления
        tk.Label(guide_frame, text="📖 УПРАВЛЕНИЕ:",
                bg='#0a0a2a', fg='#FFD700', font=('Arial', 12, 'bold')).pack(anchor='w')
        
        # Список команд
        controls = [
            "• ЛКМ: выбрать планету",
            "• Перетаскивание: переместить вид",
            "• Колесико: изменить масштаб",
            "• Ctrl+Колесико: точная настройка зума",
            "• Shift+Колесико: горизонтальный скролл",
            "• ПКМ: контекстное меню",
            "• Двойной клик: центрировать на планете",
            "• + / -: быстрый зум",
            "• Пробел: пауза",
            "• C: центрировать вид",
            "• R: сброс симуляции",
            "• F: следовать за планетой",
            "• A: автоматический зум"
        ]
        
        # Отображаем команды
        for control in controls:
            tk.Label(guide_frame, text=control, bg='#0a0a2a', fg='white',
                    font=('Arial', 9)).pack(anchor='w')
        
        # Привязываем горячие клавиши
        self.bind_hotkeys()
    
    def bind_hotkeys(self):
        """Привязка горячих клавиш к функциям"""
        
        # Пробел - пауза
        self.root.bind("<Key-space>", lambda e: self.toggle_pause())
        
        # C - центрировать вид
        self.root.bind("<Key-c>", lambda e: self.center_view())
        
        # R - сброс симуляции
        self.root.bind("<Key-r>", lambda e: self.reset_simulation())
        
        # + - увеличение
        self.root.bind("<Key-plus>", lambda e: self.zoom_in())
        self.root.bind("<Key-equal>", lambda e: self.zoom_in())  # На некоторых клавиатурах
        
        # - - уменьшение
        self.root.bind("<Key-minus>", lambda e: self.zoom_out())
        
        # F - следовать за планетой
        self.root.bind("<Key-f>", lambda e: self.toggle_follow())
        
        # A - автоматический зум
        self.root.bind("<Key-a>", lambda e: self.zoom_to_all_planets())
        
        # H - скрыть/показать панель управления
        self.root.bind("<Key-h>", lambda e: self.toggle_control_panel())
        
        # Escape - выход из полноэкранного режима или закрытие
        self.root.bind("<Escape>", lambda e: self.root.quit() if self.fullscreen else None)
    
    def show_mega_planet_info(self, planet_name):
        """Показывает улучшенную информацию о планете с фото"""
        
        # Находим планету по имени
        planet = next((p for p in self.planets_data if p["name"] == planet_name), None)
        
        # Если планета не найдена или нет информации - выходим
        if not planet or planet_name not in self.planet_info:
            return
        
        # Получаем информацию о планете
        info = self.planet_info[planet_name]
        
        # Очищаем панель
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()
        
        # ===== ВЕРХНЯЯ ЧАСТЬ С НАЗВАНИЕМ =====
        title_frame = tk.Frame(self.scrollable_frame, bg='#0a0a2a')
        title_frame.pack(fill=tk.X, pady=10, padx=10)
        
        # Цветной кружок (соответствует цвету планеты)
        color_label = tk.Label(title_frame, text="●", bg='#0a0a2a', fg=planet["color"],
                              font=('Arial', 36))
        color_label.pack(side=tk.LEFT)
        
        # Название планеты
        tk.Label(title_frame, text=planet_name, bg='#0a0a2a', fg='#FFD700',
                font=('Arial', 24, 'bold')).pack(side=tk.LEFT, padx=10)
        
        # ===== ФОТО ПЛАНЕТЫ =====
        if HAS_PIL and planet["name"] in self.planet_images:
            try:
                # Создаем фрейм для фото
                photo_frame = tk.Frame(self.scrollable_frame, bg='#1a1a3a', relief=tk.RIDGE, bd=3)
                photo_frame.pack(pady=10, padx=10, fill=tk.X)
                
                # Заголовок
                tk.Label(photo_frame, text="🖼️ ФОТО ПЛАНЕТЫ", 
                        bg='#1a1a3a', fg='#FFD700', font=('Arial', 12, 'bold')).pack(pady=5)
                
                # Получаем изображение
                img = self.planet_images[planet["name"]]
                
                # Целевой размер для отображения
                target_size = 200
                
                # Получаем оригинальные размеры
                orig_width, orig_height = img.size
                
                # Вычисляем новый размер с сохранением пропорций
                if orig_width > orig_height:
                    new_width = target_size
                    new_height = int(orig_height * (target_size / orig_width))
                else:
                    new_height = target_size
                    new_width = int(orig_width * (target_size / orig_height))
                
                # Масштабируем изображение
                img_resized = img.resize((new_width, new_height), Image.Resampling.LANCZOS)
                
                # Создаем квадратное полотно с прозрачным фоном
                square_img = Image.new('RGBA', (target_size, target_size), (0, 0, 0, 0))
                
                # Вставляем изображение в центр
                x_offset = (target_size - new_width) // 2
                y_offset = (target_size - new_height) // 2
                square_img.paste(img_resized, (x_offset, y_offset), img_resized)
                
                # Конвертируем в формат Tkinter
                photo = ImageTk.PhotoImage(square_img)
                
                # Сохраняем ссылку на фото (чтобы не удалилось сборщиком мусора)
                self.info_photos.append(photo)
                
                # Отображаем фото
                tk.Label(photo_frame, image=photo, bg='#1a1a3a').pack(pady=10)
                
                # Информация о размере
                size_text = f"Оригинальный размер: {orig_width} x {orig_height}"
                tk.Label(photo_frame, text=size_text, bg='#1a1a3a', fg='#87CEEB',
                        font=('Arial', 8)).pack(pady=(0, 5))
                
            except Exception as e:
                # В случае ошибки выводим сообщение
                print(f"Ошибка при отображении фото {planet_name}: {e}")
                error_frame = tk.Frame(self.scrollable_frame, bg='#1a1a3a', relief=tk.RIDGE, bd=3)
                error_frame.pack(pady=10, padx=10, fill=tk.X)
                tk.Label(error_frame, text="❌ Не удалось загрузить фото", 
                        bg='#1a1a3a', fg='#FF6B6B', font=('Arial', 10)).pack(pady=10)
        
        # Английское название (если есть)
        if info["Английское название"]:
            tk.Label(self.scrollable_frame, text=info["Английское название"],
                    bg='#0a0a2a', fg='#87CEEB', font=('Arial', 14, 'italic')).pack()
        
        # Добавляем разделитель
        self.add_mega_separator()
        
        # Тип планеты
        tk.Label(self.scrollable_frame, text=f"📌 {info['Тип']}",
                bg='#0a0a2a', fg='#FFA500', font=('Arial', 12, 'bold')).pack(pady=5)
        
        # Физические характеристики
        if "Физические характеристики" in info:
            self.add_mega_section("📏 ФИЗИЧЕСКИЕ ПАРАМЕТРЫ", info["Физические характеристики"])
        
        # Орбитальные характеристики
        if "Орбитальные характеристики" in info:
            self.add_mega_section("🔄 ОРБИТАЛЬНЫЕ ХАРАКТЕРИСТИКИ", info["Орбитальные характеристики"])
        
        # Вращение
        if "Вращение" in info:
            self.add_mega_section("⚡ ВРАЩЕНИЕ", info["Вращение"])
        
        # Состав
        if "Состав" in info:
            self.add_mega_section("🌍 СОСТАВ", info["Состав"])
        
        # История
        if "История" in info:
            self.add_mega_section("📜 ИСТОРИЯ", info["История"])
        
        # Описание и интересный факт
        if "Интересное" in info:
            # Фрейм с описанием
            desc_frame = tk.Frame(self.scrollable_frame, bg='#1a1a3a', relief=tk.RIDGE, bd=2)
            desc_frame.pack(fill=tk.X, padx=10, pady=10)
            
            tk.Label(desc_frame, text="📝 ОПИСАНИЕ",
                    bg='#1a1a3a', fg='#FFD700', font=('Arial', 11, 'bold')).pack(pady=5)
            
            tk.Label(desc_frame, text=info["Интересное"]["Описание"],
                    bg='#1a1a3a', fg='white', font=('Arial', 10), wraplength=350).pack(pady=5, padx=10)
            
            # Фрейм с интересным фактом
            fact_frame = tk.Frame(self.scrollable_frame, bg='#2a1a3a', relief=tk.RIDGE, bd=2)
            fact_frame.pack(fill=tk.X, padx=10, pady=10)
            
            tk.Label(fact_frame, text="✨ ИНТЕРЕСНЫЙ ФАКТ ✨",
                    bg='#2a1a3a', fg='#FF69B4', font=('Arial', 11, 'bold')).pack(pady=5)
            
            tk.Label(fact_frame, text=info["Интересное"]["Интересный факт"],
                    bg='#2a1a3a', fg='white', font=('Arial', 10), wraplength=350).pack(pady=5, padx=10)
    
    def add_mega_separator(self):
        """Добавляет разделительную линию в информацию о планете"""
        tk.Frame(self.scrollable_frame, height=2, bg='#1a1a3a').pack(fill=tk.X, pady=5, padx=10)
    
    def add_mega_section(self, title, items):
        """Добавляет секцию с информацией о планете"""
        
        # Заголовок секции
        tk.Label(self.scrollable_frame, text=title,
                bg='#0a0a2a', fg='#87CEEB', font=('Arial', 11, 'bold')).pack(pady=(10, 5), anchor='w', padx=10)
        
        # Если items - словарь (пары ключ-значение)
        if isinstance(items, dict):
            for key, value in items.items():
                tk.Label(self.scrollable_frame, text=f"• {key}: {value}",
                        bg='#0a0a2a', fg='white', font=('Arial', 9),
                        wraplength=350, justify=tk.LEFT, anchor='w').pack(pady=1, padx=20, fill=tk.X)
        else:
            # Если items - список
            for item in items:
                tk.Label(self.scrollable_frame, text=f"• {item}",
                        bg='#0a0a2a', fg='white', font=('Arial', 9),
                        wraplength=350, justify=tk.LEFT, anchor='w').pack(pady=1, padx=20, fill=tk.X)
        
        # Добавляем разделитель после секции
        self.add_mega_separator()
    
    def total_moons(self):
        """Подсчет общего количества спутников"""
        count = 0
        for planet in self.planets_data:
            count += len(planet.get('moons', []))
        return count
    
    def zoom_in(self):
        """Увеличение масштаба"""
        self.zoom_scale.set(min(10.0, self.zoom_factor + 0.2))
    
    def zoom_out(self):
        """Уменьшение масштаба"""
        self.zoom_scale.set(max(0.1, self.zoom_factor - 0.2))
    
    def zoom_reset(self):
        """Сброс масштаба к 1.0"""
        self.zoom_scale.set(1.0)
    
    def change_time_speed(self, val):
        """Изменение скорости симуляции"""
        self.time_multiplier = float(val)
        self.speed_label.config(text=f"{self.time_multiplier:.1f}x")
    
    def change_zoom(self, val):
        """Изменение масштаба"""
        self.zoom_factor = float(val)
        self.zoom_label.config(text=f"{self.zoom_factor:.1f}x")
        self.zoom_status.config(text=f"Зум: {self.zoom_factor:.1f}x")
    
    def toggle_pause(self):
        """Включение/выключение паузы"""
        self.paused = not self.paused
        self.pause_btn.config(text="▶️ ПУСК" if self.paused else "⏸️ ПАУЗА")
    
    def toggle_orbits(self):
        """Включение/выключение отображения орбит"""
        self.show_orbits = self.orbits_var.get()
    
    def toggle_labels(self):
        """Включение/выключение отображения названий"""
        self.show_labels = self.labels_var.get()
    
    def toggle_effects(self):
        """Включение/выключение спецэффектов"""
        self.show_effects = self.effects_var.get()
    
    def toggle_grid(self):
        """Включение/выключение отображения сетки"""
        self.show_grid = self.grid_var.get()
    
    def toggle_asteroids(self):
        """Включение/выключение отображения астероидов"""
        self.show_asteroids = self.asteroids_var.get()
    
    def toggle_nebula(self):
        """Включение/выключение отображения туманностей"""
        self.show_nebula = self.nebula_var.get()
    
    def toggle_trails(self):
        """Включение/выключение отображения траекторий"""
        self.trails_enabled = self.trails_var.get()
        if not self.trails_enabled:
            self.trails.clear()  # Очищаем траектории при выключении
    
    def toggle_hdr(self):
        """Включение/выключение HDR режима"""
        self.hdr_mode = self.hdr_var.get()
    
    def toggle_minimap(self):
        """Включение/выключение отображения миникарты"""
        self.show_minimap = self.minimap_var.get()
    
    def toggle_legend(self):
        """Включение/выключение отображения легенды"""
        self.show_legend = self.legend_var.get()
        if self.show_legend:
            self.legend_frame.place(x=10, y=100)
        else:
            self.legend_frame.place_forget()
    
    def toggle_constellations(self):
        """Включение/выключение отображения созвездий"""
        self.show_constellations = self.constellations_var.get()
    
    def toggle_fullscreen(self):
        """Включение/выключение полноэкранного режима"""
        self.fullscreen = not self.fullscreen
        self.root.attributes("-fullscreen", self.fullscreen)
    
    def toggle_control_panel(self):
        """Скрытие/показ панели управления"""
        if self.control_panel_visible:
            self.control_panel.pack_forget()
            self.control_panel_visible = False
            self.controls_btn.config(text="▲")
        else:
            self.control_panel.pack(fill=tk.X, padx=10, pady=(0, 10))
            self.control_panel_visible = True
            self.controls_btn.config(text="▼")
    
    def center_view(self):
        """Центрирование вида на Солнце"""
        self.pan_x = 0
        self.pan_y = 0
    
    def reset_simulation(self):
        """Сброс симуляции к начальному состоянию"""
        
        # Сбрасываем углы планет на случайные
        for planet in self.planets_data:
            planet["angle"] = random.uniform(0, 2*math.pi)
            planet["rotation"] = 0
        
        # Сбрасываем параметры
        self.time_scale.set(1.0)
        self.zoom_scale.set(1.0)
        self.pan_x = 0
        self.pan_y = 0
        self.selected_planet = None
        self.follow_selected = False
        self.follow_btn.config(text="👁️ СЛЕДИТЬ", bg='#4a6a9a')
        
        # Показываем приветствие
        self.show_mega_welcome()
        
        # Очищаем информационное поле
        self.info_text.config(state=tk.NORMAL)
        self.info_text.delete(1.0, tk.END)
        self.info_text.insert(tk.END, "Симуляция сброшена. Выберите планету для информации.")
        self.info_text.config(state=tk.DISABLED)
    
    def save_simulation(self):
        """Сохранение текущего состояния симуляции в JSON файл"""
        
        # Генерируем имя файла с текущей датой и временем
        filename = f"saves/solar_system_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        # Собираем данные для сохранения
        data = {
            'time_multiplier': self.time_multiplier,
            'zoom_factor': self.zoom_factor,
            'pan_x': self.pan_x,
            'pan_y': self.pan_y,
            'planets': []
        }
        
        # Сохраняем углы всех планет
        for planet in self.planets_data:
            data['planets'].append({
                'name': planet['name'],
                'angle': planet['angle']
            })
        
        # Записываем в файл
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        
        # Показываем сообщение об успехе
        messagebox.showinfo("Сохранение", f"Симуляция сохранена в {filename}")
    
    def load_simulation(self):
        """Загрузка ранее сохраненного состояния симуляции"""
        
        # Открываем диалог выбора файла
        filename = filedialog.askopenfilename(
            title="Загрузить симуляцию",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
        )
        
        # Если файл выбран
        if filename:
            try:
                # Читаем файл
                with open(filename, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                
                # Восстанавливаем параметры
                self.time_multiplier = data['time_multiplier']
                self.zoom_factor = data['zoom_factor']
                self.pan_x = data['pan_x']
                self.pan_y = data['pan_y']
                
                # Восстанавливаем углы планет
                for planet_data in data['planets']:
                    for planet in self.planets_data:
                        if planet['name'] == planet_data['name']:
                            planet['angle'] = planet_data['angle']
                
                # Обновляем ползунки
                self.time_scale.set(self.time_multiplier)
                self.zoom_scale.set(self.zoom_factor)
                
                # Показываем сообщение об успехе
                messagebox.showinfo("Загрузка", "Симуляция загружена!")
                
            except Exception as e:
                # В случае ошибки показываем сообщение
                messagebox.showerror("Ошибка", f"Не удалось загрузить: {e}")
    
    def take_screenshot(self):
        """Создание скриншота текущего вида"""
        
        try:
            # Генерируем имя файла
            filename = f"screenshots/solarsystem_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
            
            # Получаем координаты и размер канваса
            x = self.canvas.winfo_rootx()
            y = self.canvas.winfo_rooty()
            width = self.canvas.winfo_width()
            height = self.canvas.winfo_height()
            
            # Если есть Pillow, пытаемся использовать pyautogui
            if HAS_PIL:
                try:
                    import pyautogui
                    screenshot = pyautogui.screenshot(region=(x, y, width, height))
                    screenshot.save(filename)
                    messagebox.showinfo("Скриншот", f"Скриншот сохранен: {filename}")
                except:
                    messagebox.showinfo("Информация", "Установите pyautogui: pip install pyautogui")
            else:
                messagebox.showinfo("Информация", "Скриншот можно сделать клавишей Print Screen")
            
        except Exception as e:
            messagebox.showinfo("Информация", "Используйте Print Screen для скриншота")
    
    def export_data(self):
        """Экспорт данных о планетах в CSV файл"""
        
        # Генерируем имя файла
        filename = f"saves/planet_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        
        try:
            # Открываем файл для записи
            with open(filename, 'w', encoding='utf-8') as f:
                # Записываем заголовок
                f.write("Название,Расстояние (АЕ),Радиус (от Земли),Температура,Спутники\n")
                
                # Записываем данные каждой планеты
                for planet in self.planets_data:
                    f.write(f"{planet['name']},{planet['distance']},{planet['base_radius']/11},{planet['temperature']},{planet['moon_count']}\n")
            
            # Показываем сообщение об успехе
            messagebox.showinfo("Экспорт", f"Данные экспортированы в {filename}")
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось экспортировать: {e}")
    
    def on_mousewheel(self, event):
        """Обработка колесика мыши для зума (Windows)"""
        if event.delta > 0:
            self.zoom_scale.set(min(10.0, self.zoom_factor + 0.1))
        else:
            self.zoom_scale.set(max(0.1, self.zoom_factor - 0.1))
    
    def on_mousewheel_linux_up(self, event):
        """Обработка колесика вверх для Linux"""
        self.zoom_scale.set(min(10.0, self.zoom_factor + 0.1))
    
    def on_mousewheel_linux_down(self, event):
        """Обработка колесика вниз для Linux"""
        self.zoom_scale.set(max(0.1, self.zoom_factor - 0.1))
    
    def on_control_mousewheel(self, event):
        """Точная настройка зума с зажатым Ctrl"""
        if event.delta > 0:
            self.zoom_scale.set(min(10.0, self.zoom_factor + 0.05))
        else:
            self.zoom_scale.set(max(0.1, self.zoom_factor - 0.05))
    
    def on_shift_mousewheel(self, event):
        """Горизонтальный скролл с зажатым Shift"""
        if event.delta > 0:
            self.pan_x += 50
        else:
            self.pan_x -= 50
    
    def on_canvas_drag(self, event):
        """Перетаскивание мыши для панорамирования"""
        if not self.dragging:
            # Начало перетаскивания
            self.dragging = True
            self.drag_start_x = event.x
            self.drag_start_y = event.y
        else:
            # Вычисляем смещение
            dx = event.x - self.drag_start_x
            dy = event.y - self.drag_start_y
            # Применяем смещение
            self.pan_x += dx
            self.pan_y += dy
            # Обновляем начальную точку
            self.drag_start_x = event.x
            self.drag_start_y = event.y
    
    def on_canvas_release(self, event):
        """Отпускание кнопки мыши - окончание перетаскивания"""
        self.dragging = False
    
    def on_mouse_move(self, event):
        """Обновление координат мыши и подсветка планет при наведении"""
        
        # Обновляем метку с координатами
        self.coord_label.config(text=f"X: {event.x} Y: {event.y}")
        
        # Координаты центра Солнца с учетом панорамирования
        center_x = 650 + self.pan_x
        center_y = 400 + self.pan_y
        
        # Сбрасываем подсветку
        self.mouse_over_planet = None
        
        # Проверяем каждую планету
        for planet in self.planets_data:
            # Вычисляем позицию планеты
            distance = planet["distance"] * self.AU * self.zoom_factor
            x = center_x + distance * math.cos(planet["angle"])
            y = center_y + distance * math.sin(planet["angle"])
            radius = planet["radius"] * self.zoom_factor
            
            # Проверяем, находится ли мышь над планетой
            if math.sqrt((event.x - x)**2 + (event.y - y)**2) < radius + 5:
                self.mouse_over_planet = planet["name"]
                break
    
    def on_right_click(self, event):
        """Обработка правого клика - контекстное меню"""
        
        # Создаем меню
        menu = tk.Menu(self.root, tearoff=0)
        
        # Добавляем пункты
        menu.add_command(label="🎯 Центрировать вид", command=self.center_view)
        menu.add_command(label="🔍 Сбросить зум", command=self.zoom_reset)
        menu.add_command(label="🔍 Увеличить", command=self.zoom_in)
        menu.add_command(label="🔍 Уменьшить", command=self.zoom_out)
        menu.add_command(label="🌍 Показать все планеты", command=self.zoom_to_all_planets)
        menu.add_separator()
        menu.add_command(label="⏸️ Пауза", command=self.toggle_pause)
        menu.add_command(label="🔄 Сброс", command=self.reset_simulation)
        menu.add_separator()
        menu.add_command(label="💾 Сохранить", command=self.save_simulation)
        menu.add_command(label="📂 Загрузить", command=self.load_simulation)
        menu.add_command(label="📸 Скриншот", command=self.take_screenshot)
        menu.add_separator()
        menu.add_command(label="❌ Выход", command=self.root.quit)
        
        # Отображаем меню в позиции курсора
        menu.post(event.x_root, event.y_root)
    
    def on_double_click(self, event):
        """Двойной клик для центрирования на планете"""
        
        # Координаты центра Солнца
        center_x = 650 + self.pan_x
        center_y = 400 + self.pan_y
        
        # Проверяем каждую планету
        for planet in self.planets_data:
            # Вычисляем позицию планеты
            distance = planet["distance"] * self.AU * self.zoom_factor
            x = center_x + distance * math.cos(planet["angle"])
            y = center_y + distance * math.sin(planet["angle"])
            radius = planet["radius"] * self.zoom_factor
            
            # Если кликнули по планете
            if math.sqrt((event.x - x)**2 + (event.y - y)**2) < radius + 10:
                # Центрируем вид на планете
                self.pan_x = 650 - x
                self.pan_y = 400 - y
                # Выбираем планету
                self.selected_planet = planet["name"]
                # Показываем информацию
                self.show_mega_planet_info(planet["name"])
                break
    
    def on_canvas_click(self, event):
        """Обработка клика левой кнопкой мыши - выбор планеты"""
        
        # Координаты центра Солнца
        center_x = 650 + self.pan_x
        center_y = 400 + self.pan_y
        
        found = False
        
        # Проверяем каждую планету
        for planet in self.planets_data:
            # Вычисляем позицию планеты
            distance = planet["distance"] * self.AU * self.zoom_factor
            x = center_x + distance * math.cos(planet["angle"])
            y = center_y + distance * math.sin(planet["angle"])
            radius = planet["radius"] * self.zoom_factor
            
            # Если кликнули по планете
            if math.sqrt((event.x - x)**2 + (event.y - y)**2) < radius + 10:
                # Выбираем планету
                self.selected_planet = planet["name"]
                # Показываем информацию
                self.show_mega_planet_info(planet["name"])
                found = True
                
                # Обновляем информационное поле
                self.info_text.config(state=tk.NORMAL)
                self.info_text.delete(1.0, tk.END)
                self.info_text.insert(tk.END, f"ВЫБРАНА ПЛАНЕТА: {planet['name']}\n\n")
                self.info_text.insert(tk.END, f"Расстояние: {planet['distance']} АЕ\n")
                self.info_text.insert(tk.END, f"Температура: {planet['temperature']}\n")
                self.info_text.insert(tk.END, f"Спутников: {planet['moon_count']}\n")
                self.info_text.insert(tk.END, f"Описание: {planet['description']}")
                self.info_text.config(state=tk.DISABLED)
                
                break
        
        # Если не кликнули ни по одной планете, сбрасываем выбор
        if not found:
            self.selected_planet = None
    
    def draw_minimap(self):
        """Рисует миникарту для навигации"""
        
        if not self.show_minimap:
            return
        
        # Позиция и размер миникарты
        minimap_x = 1200
        minimap_y = 100
        minimap_size = 150
        
        # Фон миникарты
        self.canvas.create_rectangle(minimap_x, minimap_y, 
                                     minimap_x + minimap_size, minimap_y + minimap_size,
                                     fill='#0a0a2a', outline='#4a6a9a', width=2)
        
        # Солнце в центре миникарты
        sun_x = minimap_x + minimap_size/2
        sun_y = minimap_y + minimap_size/2
        self.canvas.create_oval(sun_x - 5, sun_y - 5, sun_x + 5, sun_y + 5, fill='#FFD700', outline='')
        
        # Масштаб миникарты (150 пикселей = 60 АЕ)
        scale = minimap_size / 60
        
        # Рисуем планеты
        for planet in self.planets_data:
            # Вычисляем позицию на миникарте
            dist = planet["distance"] * scale
            x = sun_x + dist * math.cos(planet["angle"])
            y = sun_y + dist * math.sin(planet["angle"])
            
            # Проверяем, входит ли планета в границы миникарты
            if minimap_x <= x <= minimap_x + minimap_size and minimap_y <= y <= minimap_y + minimap_size:
                self.canvas.create_oval(x - 2, y - 2, x + 2, y + 2, fill=planet["color"], outline='')
        
        # Область просмотра на миникарте
        view_width = 1300 / (self.AU * self.zoom_factor) * 10
        view_height = 800 / (self.AU * self.zoom_factor) * 10
        
        # Позиция центра просмотра
        view_x = sun_x - (self.pan_x / (self.AU * self.zoom_factor)) * 10
        view_y = sun_y - (self.pan_y / (self.AU * self.zoom_factor)) * 10
        
        # Рисуем прямоугольник области просмотра
        self.canvas.create_rectangle(view_x - view_width/2, view_y - view_height/2,
                                     view_x + view_width/2, view_y + view_height/2,
                                     outline='#FFD700', width=2, dash=(2, 2))
    
    def draw_planet_mega(self, center_x, center_y, planet):
        """Рисует ультра-планету со всеми деталями"""
        
        # Вычисляем позицию планеты
        distance = planet["distance"] * self.AU * self.zoom_factor
        x = center_x + distance * math.cos(planet["angle"])
        y = center_y + distance * math.sin(planet["angle"])
        radius = planet["radius"] * self.zoom_factor
        
        # Обновляем вращение планеты (если не на паузе)
        if not self.paused:
            planet["rotation"] += planet["rotation_speed"] * self.time_multiplier
        
        # Следование за планетой (если включено)
        if self.follow_selected and self.selected_planet == planet["name"]:
            self.pan_x = 650 - x
            self.pan_y = 400 - y
        
        # Рисуем траектории (если включены)
        if self.trails_enabled:
            self.trails.append((x, y))
            if len(self.trails) > 100:
                self.trails.popleft()
            
            if len(self.trails) > 5:
                points = list(self.trails)
                for i in range(len(points)-1):
                    alpha = i / len(points)
                    self.canvas.create_line(points[i][0], points[i][1],
                                           points[i+1][0], points[i+1][1],
                                           fill=f'#FFFF{int(alpha*255):02x}',
                                           width=1)
        
        # Рисуем планету (изображение или градиент)
        if HAS_PIL and planet["name"] in self.planet_images:
            try:
                # Получаем изображение
                img = self.planet_images[planet["name"]]
                
                # Целевой размер
                target_size = int(radius * 2)
                
                if target_size > 10:
                    # Получаем оригинальные размеры
                    orig_width, orig_height = img.size
                    
                    # Вычисляем новый размер с сохранением пропорций
                    if orig_width > orig_height:
                        new_width = target_size
                        new_height = int(orig_height * (target_size / orig_width))
                    else:
                        new_height = target_size
                        new_width = int(orig_width * (target_size / orig_height))
                    
                    # Масштабируем изображение
                    img_resized = img.resize((new_width, new_height), Image.Resampling.LANCZOS)
                    
                    # Создаем квадратное полотно
                    square_img = Image.new('RGBA', (target_size, target_size), (0, 0, 0, 0))
                    
                    # Вставляем изображение в центр
                    x_offset = (target_size - new_width) // 2
                    y_offset = (target_size - new_height) // 2
                    square_img.paste(img_resized, (x_offset, y_offset), img_resized)
                    
                    # Поворачиваем если нужно
                    if abs(planet["rotation"]) > 0.01:
                        square_img = square_img.rotate(planet["rotation"] * 180/math.pi, expand=0)
                    
                    # Конвертируем в формат Tkinter
                    self.photo = ImageTk.PhotoImage(square_img)
                    self.canvas.create_image(x, y, image=self.photo, anchor='center')
                    
                    # Сохраняем ссылку на фото
                    if not hasattr(planet, 'photo_ref'):
                        planet['photo_ref'] = self.photo
                    else:
                        planet['photo_ref'] = self.photo
                    
            except Exception as e:
                # В случае ошибки рисуем градиент
                print(f"Ошибка при отображении планеты {planet['name']}: {e}")
                self.draw_planet_gradient(x, y, radius, planet)
        else:
            # Рисуем градиент
            self.draw_planet_gradient(x, y, radius, planet)
        
        # Атмосфера (если есть)
        if planet.get("atmosphere") and radius > 5:
            for i in range(4):
                atmos_radius = radius * (1.1 + i * 0.05)
                alpha = 100 - i * 20
                self.canvas.create_oval(x - atmos_radius, y - atmos_radius,
                                        x + atmos_radius, y + atmos_radius,
                                        outline=planet["atmosphere_color"],
                                        width=2, dash=(4, 4))
        
        # Кольца Сатурна (особая обработка)
        if planet["name"] == "Сатурн" and radius > 10:
            for i, ring_r in enumerate([radius*1.8, radius*2.2, radius*2.5, radius*2.8]):
                color = ['#C0C0C0', '#D2B48C', '#A9A9A9', '#808080'][i]
                width = [4, 3, 2, 1][i]
                dash = (2, 4) if i > 1 else None
                self.canvas.create_oval(x - ring_r, y - ring_r*0.2,
                                        x + ring_r, y + ring_r*0.2,
                                        outline=color, width=width, dash=dash)
        
        # Кольца для других планет
        if planet.get("has_rings") and planet["name"] != "Сатурн":
            for i, ring_r in enumerate([radius*1.3, radius*1.6]):
                self.canvas.create_oval(x - ring_r, y - ring_r*0.2,
                                        x + ring_r, y + ring_r*0.2,
                                        outline='#808080', width=2-i, dash=(3, 3))
        
        # Спутники
        if planet.get("moons"):
            for moon in planet["moons"]:
                # Обновляем угол спутника
                if not self.paused:
                    moon["angle"] += self.BASE_SPEED * moon["speed"] * self.time_multiplier * 10
                
                # Вычисляем позицию спутника
                moon_dist = moon["distance"] * radius
                moon_x = x + moon_dist * math.cos(moon["angle"])
                moon_y = y + moon_dist * math.sin(moon["angle"])
                moon_r = moon["radius"] * self.zoom_factor
                moon_color = moon.get("color", "#808080")
                
                # Рисуем спутник
                self.canvas.create_oval(moon_x - moon_r, moon_y - moon_r,
                                        moon_x + moon_r, moon_y + moon_r,
                                        fill=moon_color, outline='#A9A9A9')
        
        # Большое Красное Пятно (Юпитер)
        if planet["name"] == "Юпитер" and self.show_effects:
            spot_x = x + radius * 0.3 * math.cos(planet["rotation"])
            spot_y = y - radius * 0.2 * math.sin(planet["rotation"])
            spot_r = radius * 0.15
            
            self.canvas.create_oval(spot_x - spot_r, spot_y - spot_r,
                                    spot_x + spot_r, spot_y + spot_r,
                                    fill='#CD5C5C', outline='#8B3A3A', width=2)
        
        # Черные дыры
        for bh in self.black_holes:
            if bh['active']:
                bh_x = bh['x'] + self.pan_x
                bh_y = bh['y'] + self.pan_y
                bh_r = bh['mass'] * self.zoom_factor * 0.1
                
                # Аккреционный диск
                if bh['accretion_disk']:
                    for i in range(3):
                        r = bh_r * (1.5 + i * 0.5)
                        self.canvas.create_oval(bh_x - r, bh_y - r,
                                                bh_x + r, bh_y + r,
                                                outline='#FF4500', width=2, dash=(2, 4))
                
                # Черная дыра
                self.canvas.create_oval(bh_x - bh_r, bh_y - bh_r,
                                        bh_x + bh_r, bh_y + bh_r,
                                        fill='#000000', outline='#FFD700', width=2)
        
        # Подсветка выбранной планеты
        if self.selected_planet == planet["name"]:
            for i in range(4):
                glow_radius = radius + 5 + i*4
                alpha = 100 - i*20
                self.canvas.create_oval(x - glow_radius, y - glow_radius,
                                        x + glow_radius, y + glow_radius,
                                        outline=f'#FFFF{alpha:02x}', width=2,
                                        dash=(4, 4))
        
        # Подсветка при наведении
        if self.mouse_over_planet == planet["name"] and planet["name"] != self.selected_planet:
            self.canvas.create_oval(x - radius - 3, y - radius - 3,
                                    x + radius + 3, y + radius + 3,
                                    outline='#87CEEB', width=2, dash=(2, 2))
        
        return x, y, radius
    
    def draw_planet_gradient(self, x, y, radius, planet):
        """Рисует планету с улучшенным градиентом"""
        
        # Основной градиент (8 слоев)
        for i in range(8):
            r = radius * (1 - i * 0.08)
            if r < 2:
                break
            
            # Определяем цвет в зависимости от слоя
            t = i / 8
            if t < 0.3:
                color = planet["color"]
            elif t < 0.7:
                color = planet.get("color2", planet["color"])
            else:
                color = planet.get("color3", planet["color"])
            
            # Рисуем слой
            self.canvas.create_oval(x - r, y - r, x + r, y + r,
                                    fill=color, outline='')
        
        # Полосы для Юпитера
        if planet["name"] == "Юпитер" and radius > 15:
            for j in range(4):
                y_offset = (j - 1.5) * radius * 0.2
                width = 3 if j in [1,2] else 2
                self.canvas.create_line(x - radius*0.8, y + y_offset,
                                       x + radius*0.8, y + y_offset,
                                       fill='#8B6914', width=width)
        
        # Блик (светлая точка)
        self.canvas.create_oval(x - radius*0.2, y - radius*0.2,
                                x, y, fill='#FFFFFF', outline='')
        
        # Тень (темная область)
        self.canvas.create_oval(x + radius*0.1, y + radius*0.1,
                                x + radius*0.3, y + radius*0.3,
                                fill='#000000', outline='')
    
    def draw_asteroids(self, center_x, center_y):
        """Рисует улучшенный пояс астероидов"""
        
        if not self.show_asteroids:
            return
        
        for asteroid in self.asteroids:
            # Обновляем угол астероида
            if not self.paused:
                asteroid["angle"] += self.BASE_SPEED * asteroid["speed"] * self.time_multiplier
            
            # Вычисляем позицию
            distance = asteroid["distance"] * self.AU * self.zoom_factor
            x = center_x + distance * math.cos(asteroid["angle"])
            y = center_y + distance * math.sin(asteroid["angle"])
            size = asteroid["size"] * self.zoom_factor
            
            # Рисуем только если размер достаточный
            if size > 0.5:
                self.canvas.create_oval(x - size, y - size,
                                        x + size, y + size,
                                        fill=asteroid["color"], outline='')
    
    def draw_nebulae(self):
        """Рисует улучшенные туманности"""
        
        if not self.show_nebula:
            return
        
        for nebula in self.nebulae:
            # Позиция с учетом параллакса
            x = nebula['x'] + self.pan_x * 0.1
            y = nebula['y'] + self.pan_y * 0.1
            
            # Преобразуем цвет
            r, g, b = nebula['color']
            color = f'#{int(r*255):02x}{int(g*255):02x}{int(b*255):02x}'
            
            # Вращение
            nebula['rotation'] += 0.001
            
            # Пульсация
            pulse = 1 + math.sin(self.time_of_day * nebula['pulse']) * 0.1
            radius = nebula['radius'] * pulse
            
            # Рисуем в зависимости от формы
            if nebula['shape'] == 'spiral':
                for i in range(3):
                    r2 = radius * (1 - i*0.2)
                    self.canvas.create_oval(x - r2, y - r2,
                                            x + r2, y + r2,
                                            fill=color, outline='', stipple='gray50')
            else:
                self.canvas.create_oval(x - radius, y - radius,
                                        x + radius, y + radius,
                                        fill=color, outline='', stipple='gray50')
    
    def draw_constellations(self, center_x, center_y):
        """Рисует созвездия"""
        
        if not self.show_constellations:
            return
        
        for constellation in self.constellations:
            stars = constellation['stars']
            for i in range(len(stars)-1):
                # Соединяем звезды линиями
                x1 = stars[i][0] + self.pan_x * 0.2
                y1 = stars[i][1] + self.pan_y * 0.2
                x2 = stars[i+1][0] + self.pan_x * 0.2
                y2 = stars[i+1][1] + self.pan_y * 0.2
                
                self.canvas.create_line(x1, y1, x2, y2,
                                       fill='#87CEEB', width=1, dash=(2, 4))
    
    def draw_deep_space(self):
        """Рисует объекты глубокого космоса"""
        
        for obj in self.deep_space_objects:
            # Позиция с учетом параллакса
            x = obj['x'] + self.pan_x * 0.05
            y = obj['y'] + self.pan_y * 0.05
            
            # Преобразуем цвет
            r, g, b = obj['color']
            color = f'#{int(r*255):02x}{int(g*255):02x}{int(b*255):02x}'
            
            # Рисуем в зависимости от типа
            if obj['type'] == 'galaxy':
                for i in range(2):
                    r2 = obj['radius'] * (1 + i*0.2)
                    self.canvas.create_oval(x - r2, y - r2,
                                            x + r2, y + r2,
                                            fill=color, outline='', stipple='gray25')
            else:
                self.canvas.create_oval(x - obj['radius'], y - obj['radius'],
                                        x + obj['radius'], y + obj['radius'],
                                        fill=color, outline='', stipple='gray50')
    
    def start_background_tasks(self):
        """Запуск улучшенных фоновых задач"""
        
        def update_fps():
            """Функция для подсчета FPS в отдельном потоке"""
            while True:
                # Увеличиваем счетчик кадров
                self.frame_count += 1
                
                # Каждую секунду обновляем FPS
                if time.time() - self.last_time >= 1:
                    self.fps = self.frame_count
                    self.frame_count = 0
                    self.last_time = time.time()
                    self.simulation_time += 1
                    
                    # Обновляем метки в главном потоке
                    try:
                        self.root.after(0, lambda: self.fps_label.config(text=f"FPS: {self.fps}"))
                        self.root.after(0, lambda: self.time_label.config(
                            text=f"Время: {self.simulation_time}s"
                        ))
                    except:
                        pass
                
                # Небольшая пауза
                time.sleep(0.1)
        
        # Запускаем поток
        thread = threading.Thread(target=update_fps, daemon=True)
        thread.start()
    
    def animate(self):
        """Основной улучшенный цикл анимации"""
        
        # Если пауза, просто планируем следующий кадр
        if self.paused:
            self.animation_id = self.root.after(50, self.animate)
            return
        
        # Очищаем канвас
        self.canvas.delete("all")
        
        # Обновляем системные параметры
        self.time_of_day += 0.01 * self.time_multiplier
        self.total_distance_traveled += self.time_multiplier * 1000
        
        # ===== ФОНОВЫЕ ОБЪЕКТЫ =====
        self.draw_deep_space()
        self.draw_nebulae()
        
        # ===== ЗВЕЗДЫ С ПАРАЛЛАКСОМ =====
        for star in self.stars:
            # Позиция с учетом параллакса
            parallax_x = star['x'] + self.pan_x * (1 - star['z'])
            parallax_y = star['y'] + self.pan_y * (1 - star['z'])
            
            # Мерцание для переменных звезд
            if star['variable']:
                brightness = star['base_brightness'] * (0.7 + 0.3 * math.sin(self.time_of_day * star['twinkle_speed']))
            else:
                brightness = star['base_brightness']
            
            # Определяем цвет в зависимости от температуры
            if star['color_temp'] == 'blue':
                color = f'#88{int(brightness*0.5):02x}FF'
            elif star['color_temp'] == 'red':
                color = f'#FF{int(brightness*0.3):02x}{int(brightness*0.3):02x}'
            elif star['color_temp'] == 'yellow':
                color = f'#FF{int(brightness*0.8):02x}00'
            elif star['color_temp'] == 'orange':
                color = f'#FF{int(brightness*0.6):02x}00'
            else:  # white
                color = f'#{int(brightness):02x}{int(brightness):02x}{int(brightness):02x}'
            
            # Рисуем звезду
            self.canvas.create_oval(parallax_x, parallax_y,
                                    parallax_x + star['size'], parallax_y + star['size'],
                                    fill=color, outline='')
            
            # Если есть экзопланеты, рисуем маленькую точку
            if star['has_planet'] and self.show_effects:
                self.canvas.create_oval(parallax_x - 1, parallax_y - 1,
                                        parallax_x + 1, parallax_y + 1,
                                        fill='#87CEEB', outline='')
        
        # ===== СОЗВЕЗДИЯ =====
        self.draw_constellations(650, 400)
        
        # Координаты центра Солнца
        center_x = 650 + self.pan_x
        center_y = 400 + self.pan_y
        
        # ===== СЕТКА =====
        if self.show_grid:
            # Вертикальные линии
            for i in range(-15, 16):
                grid_x = center_x + i * 100 * self.zoom_factor
                self.canvas.create_line(grid_x, center_y - 600, grid_x, center_y + 600,
                                       fill='#1a3a5a', width=1, dash=(2, 4))
            
            # Горизонтальные линии
            for i in range(-15, 16):
                grid_y = center_y + i * 100 * self.zoom_factor
                self.canvas.create_line(center_x - 600, grid_y, center_x + 600, grid_y,
                                       fill='#1a3a5a', width=1, dash=(2, 4))
        
        # ===== ОРБИТЫ =====
        if self.show_orbits:
            for planet in self.planets_data:
                distance = planet["distance"] * self.AU * self.zoom_factor
                self.canvas.create_oval(center_x - distance, center_y - distance,
                                        center_x + distance, center_y + distance,
                                        outline='#2a4a6a', width=1, dash=(3, 6))
        
        # ===== СОЛНЦЕ =====
        sun_radius = self.draw_sun_mega(center_x, center_y)
        
        # ===== АСТЕРОИДЫ =====
        self.draw_asteroids(center_x, center_y)
        
        # ===== ПЛАНЕТЫ =====
        planet_positions = []
        for planet in self.planets_data:
            # Обновляем угол планеты
            if not self.paused:
                planet["angle"] += self.BASE_SPEED * planet["speed"] * self.time_multiplier
            
            # Рисуем планету
            x, y, radius = self.draw_planet_mega(center_x, center_y, planet)
            planet_positions.append((planet["name"], x, y, radius))
        
        # ===== НАЗВАНИЯ ПЛАНЕТ =====
        if self.show_labels:
            for name, x, y, radius in planet_positions:
                # Тень для текста
                self.canvas.create_text(x + 2, y - radius - 16, text=name,
                                       fill='#000000', font=('Arial', 10, 'bold'))
                # Основной текст
                self.canvas.create_text(x, y - radius - 18, text=name,
                                       fill='white', font=('Arial', 10, 'bold'))
        
        # ===== КОМЕТЫ =====
        # С вероятностью 1% активируем новую комету
        if self.show_effects and random.random() < 0.01:
            for comet in self.comets:
                if not comet['active']:
                    comet['active'] = True
                    comet['x'] = random.randint(0, 1300)
                    comet['y'] = random.randint(0, 800)
                    angle = random.uniform(0, 2*math.pi)
                    speed = random.uniform(2, 6)
                    comet['vx'] = math.cos(angle) * speed
                    comet['vy'] = math.sin(angle) * speed
                    comet['life'] = comet['max_life']
                    comet['tail'] = []
                    break
        
        # Обновляем и рисуем активные кометы
        for comet in self.comets:
            if comet['active']:
                # Движение
                comet['x'] += comet['vx']
                comet['y'] += comet['vy']
                comet['life'] -= 1
                
                # Добавляем точку в хвост
                comet['tail'].append((comet['x'], comet['y']))
                if len(comet['tail']) > comet.get('tail_length', 30):
                    comet['tail'].pop(0)
                
                # Рисуем хвост
                for i, (tx, ty) in enumerate(comet['tail']):
                    alpha = i / len(comet['tail'])
                    self.canvas.create_line(tx, ty, comet['x'], comet['y'],
                                           fill=f'#FFFF{int(alpha*255):02x}',
                                           width=2)
                
                # Рисуем ядро кометы
                self.canvas.create_oval(comet['x'] - 4, comet['y'] - 4,
                                        comet['x'] + 4, comet['y'] + 4,
                                        fill=comet.get('color', '#FFD700'), outline='white')
                
                # Деактивируем если время жизни истекло
                if comet['life'] <= 0:
                    comet['active'] = False
        
        # ===== МИНИКАРТА =====
        self.draw_minimap()
        
        # ===== СТАТИСТИКА =====
        if self.show_stats:
            stats_text = f"Объектов: {len(self.planets_data) + self.total_moons() + len(self.asteroids) + len(self.stars)}"
            self.canvas.create_text(50, 50, text=stats_text, fill='#00FF00',
                                   font=('Arial', 10), anchor='w')
        
        # Планируем следующий кадр через 50 мс (20 FPS)
        self.animation_id = self.root.after(50, self.animate)


# ===== ТОЧКА ВХОДА В ПРОГРАММУ =====
if __name__ == "__main__":
    # Создаем главное окно
    root = tk.Tk()
    
    # Пытаемся установить иконку
    try:
        if HAS_PIL:
            # Создаем простую иконку
            icon = Image.new('RGBA', (32, 32), (0, 0, 0, 0))
            draw = ImageDraw.Draw(icon)
            draw.ellipse([8, 8, 24, 24], fill='#FFD700')
            photo = ImageTk.PhotoImage(icon)
            root.iconphoto(True, photo)
    except:
        # Игнорируем ошибки с иконкой
        pass
    
    # Создаем и запускаем приложение
    app = MegaSolarSystem(root)
    root.mainloop()