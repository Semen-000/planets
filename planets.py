import tkinter as tk
from tkinter import ttk, filedialog, messagebox, colorchooser
import math
import random
import time
import json
import os
import sys
import threading
from datetime import datetime, timedelta
from collections import deque
import colorsys
import hashlib
import io
import webbrowser

try:
    from PIL import Image, ImageTk, ImageDraw, ImageFilter, ImageEnhance, ImageFont
    HAS_PIL = True
except ImportError:
    HAS_PIL = False
    print("Для максимальной визуализации установите Pillow: pip install Pillow")

class MegaSolarSystem:
    def __init__(self, root):
        self.root = root
        self.root.title("🚀 МЕГА-СИМУЛЯЦИЯ СОЛНЕЧНОЙ СИСТЕМЫ 3000 - КОСМИЧЕСКИЙ ЭПОС 🌌")
        self.root.geometry("1900x1000")
        self.root.configure(bg='#000000')
        self.root.resizable(True, True)
        
        # ==================== КОНСТАНТЫ И ПАРАМЕТРЫ ====================
        self.AU = 150  # астрономическая единица в пикселях
        self.BASE_SPEED = 0.0002  # базовая скорость
        self.time_multiplier = 1.0
        self.zoom_factor = 1.0
        self.pan_x = 0
        self.pan_y = 0
        self.dragging = False
        self.drag_start_x = 0
        self.drag_start_y = 0
        self.last_mouse_x = 0
        self.last_mouse_y = 0
        self.mouse_over_planet = None
        self.show_controls = True
        self.control_panel_visible = True
        self.fullscreen = False
        
        # Режимы и состояния
        self.selected_planet = None
        self.paused = False
        self.show_orbits = True
        self.show_labels = True
        self.show_effects = True
        self.show_grid = False
        self.show_asteroids = True
        self.show_nebula = True
        self.show_constellations = False
        self.night_mode = False
        self.hdr_mode = True
        self.motion_blur = False
        self.rainbow_mode = False
        self.trails_enabled = False
        self.trails = deque(maxlen=100)
        self.show_stats = True
        self.show_minimap = True
        self.show_legend = True
        
        # Системные параметры
        self.time_of_day = 0
        self.frame_count = 0
        self.fps = 0
        self.last_time = time.time()
        self.starfield_offset = 0
        self.cosmic_radiation = 0
        self.space_time_distortion = 0
        self.simulation_time = 0
        self.total_distance_traveled = 0
        
        # ==================== ГЕНЕРАЦИЯ ВСЕЛЕННОЙ ====================
        self.stars = self.generate_stars(3000)  # Увеличено до 3000
        self.deep_space_objects = self.generate_deep_space(100)
        self.nebulae = self.generate_nebulae(30)
        self.asteroids = self.generate_asteroid_belt(500)  # Увеличено до 500
        self.comets = self.generate_comets(20)
        self.constellations = self.generate_constellations()
        self.black_holes = self.generate_black_holes(3)
        self.satellites = self.generate_satellites()  # Новое: искусственные спутники
        self.space_stations = self.generate_space_stations()  # Новое: космические станции
        
        # ==================== ДАННЫЕ О ПЛАНЕТАХ ====================
        self.planets_data = [
            {
                "name": "Меркурий",
                "name_en": "Mercury",
                "distance": 0.4,
                "radius": 8,
                "base_radius": 8,
                "color": "#A5A5A5",
                "color2": "#696969",
                "color3": "#D3D3D3",
                "speed": 1/0.24,
                "angle": random.uniform(0, 2*math.pi),
                "rotation": 0,
                "rotation_speed": 0.02,
                "orbit_tilt": 0.1,
                "texture": "rocky",
                "atmosphere": None,
                "atmosphere_color": None,
                "has_rings": False,
                "has_moons": False,
                "moon_count": 0,
                "moons": [],
                "temperature": "-173°C до +427°C",
                "mass": "3.30×10²³ кг",
                "density": "5.43 г/см³",
                "gravity": "3.7",
                "gravity_unit": "м/с²",
                "discovery": "Древние цивилизации",
                "description": "Самая близкая к Солнцу планета",
                "fun_fact": "Сутки на Меркурии длятся 176 земных дней!",
                "image_path": "images/mercury.png",
                "emissivity": 0.1,
                "volume": "6.08×10¹⁰ км³",
                "escape_velocity": "4.3 км/с"
            },
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
                "rotation_speed": -0.01,
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
                "image_path": "images/venus.png",
                "emissivity": 0.2,
                "volume": "9.28×10¹¹ км³",
                "escape_velocity": "10.4 км/с"
            },
            {
                "name": "Земля",
                "name_en": "Earth",
                "distance": 1.0,
                "radius": 11,
                "base_radius": 11,
                "color": "#2E86C1",
                "color2": "#1F618D",
                "color3": "#85C1E9",
                "speed": 1.0,
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
                    {"name": "Луна", "distance": 2.5, "radius": 3, "speed": 13.0, "angle": random.uniform(0, 2*math.pi), "color": "#C0C0C0", "phase": 0}
                ],
                "temperature": "-89°C до +58°C",
                "mass": "5.97×10²⁴ кг",
                "density": "5.52 г/см³",
                "gravity": "9.8",
                "gravity_unit": "м/с²",
                "discovery": "Наш дом",
                "description": "Единственная известная планета с жизнью",
                "fun_fact": "Земля - единственная планета не названная в честь бога",
                "image_path": "images/earth.png",
                "emissivity": 0.1,
                "volume": "1.08×10¹² км³",
                "escape_velocity": "11.2 км/с"
            },
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
                    {"name": "Фобос", "distance": 2.0, "radius": 2, "speed": 7.0, "angle": random.uniform(0, 2*math.pi), "color": "#808080"},
                    {"name": "Деймос", "distance": 3.0, "radius": 1.5, "speed": 5.0, "angle": random.uniform(0, 2*math.pi), "color": "#808080"}
                ],
                "temperature": "-63°C",
                "mass": "6.42×10²³ кг",
                "density": "3.93 г/см³",
                "gravity": "3.7",
                "gravity_unit": "м/с²",
                "discovery": "Древние цивилизации",
                "description": "Красная планета",
                "fun_fact": "На Марсе находится самый высокий вулкан - Олимп (21 км)",
                "image_path": "images/mars.png",
                "emissivity": 0.15,
                "volume": "1.63×10¹¹ км³",
                "escape_velocity": "5.0 км/с"
            },
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
                    {"name": "Ио", "distance": 3.5, "radius": 3, "speed": 8.0, "angle": random.uniform(0, 2*math.pi), "color": "#FFD700"},
                    {"name": "Европа", "distance": 4.5, "radius": 3, "speed": 6.0, "angle": random.uniform(0, 2*math.pi), "color": "#87CEEB"},
                    {"name": "Ганимед", "distance": 5.5, "radius": 4, "speed": 4.0, "angle": random.uniform(0, 2*math.pi), "color": "#D2B48C"},
                    {"name": "Каллисто", "distance": 6.5, "radius": 4, "speed": 3.0, "angle": random.uniform(0, 2*math.pi), "color": "#808080"}
                ],
                "temperature": "-145°C",
                "mass": "1.90×10²⁷ кг",
                "density": "1.33 г/см³",
                "gravity": "24.8",
                "gravity_unit": "м/с²",
                "discovery": "Древние цивилизации",
                "description": "Самая большая планета",
                "fun_fact": "Большое Красное Пятно - шторм, бушующий 400 лет!",
                "image_path": "images/jupiter.png",
                "emissivity": 0.3,
                "volume": "1.43×10¹⁵ км³",
                "escape_velocity": "59.5 км/с"
            },
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
                    {"name": "Титан", "distance": 4.0, "radius": 5, "speed": 3.0, "angle": random.uniform(0, 2*math.pi), "color": "#CD853F"},
                    {"name": "Рея", "distance": 5.0, "radius": 3, "speed": 2.5, "angle": random.uniform(0, 2*math.pi), "color": "#A9A9A9"},
                    {"name": "Диона", "distance": 6.0, "radius": 2.5, "speed": 2.0, "angle": random.uniform(0, 2*math.pi), "color": "#D3D3D3"}
                ],
                "temperature": "-178°C",
                "mass": "5.68×10²⁶ кг",
                "density": "0.69 г/см³",
                "gravity": "10.4",
                "gravity_unit": "м/с²",
                "discovery": "Древние цивилизации",
                "description": "Планета с кольцами",
                "fun_fact": "Сатурн настолько лёгкий, что плавал бы в воде!",
                "image_path": "images/saturn.png",
                "emissivity": 0.25,
                "volume": "8.27×10¹⁴ км³",
                "escape_velocity": "35.5 км/с"
            },
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
                    {"name": "Титания", "distance": 3.5, "radius": 3, "speed": 2.0, "angle": random.uniform(0, 2*math.pi), "color": "#C0C0C0"},
                    {"name": "Оберон", "distance": 4.5, "radius": 3, "speed": 1.5, "angle": random.uniform(0, 2*math.pi), "color": "#A9A9A9"}
                ],
                "temperature": "-224°C",
                "mass": "8.68×10²⁵ кг",
                "density": "1.27 г/см³",
                "gravity": "8.7",
                "gravity_unit": "м/с²",
                "discovery": "1781, Уильям Гершель",
                "description": "Ледяной гигант",
                "fun_fact": "Уран вращается на боку, ось наклонена на 98°",
                "image_path": "images/uranus.png",
                "emissivity": 0.2,
                "volume": "6.83×10¹³ км³",
                "escape_velocity": "21.3 км/с"
            },
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
                    {"name": "Тритон", "distance": 3.5, "radius": 4, "speed": 2.0, "angle": random.uniform(0, 2*math.pi), "color": "#C0C0C0"}
                ],
                "temperature": "-218°C",
                "mass": "1.02×10²⁶ кг",
                "density": "1.64 г/см³",
                "gravity": "11.2",
                "gravity_unit": "м/с²",
                "discovery": "1846, Галле и д'Арре",
                "description": "Самая ветреная планета",
                "fun_fact": "Ветры на Нептуне достигают 2100 км/ч!",
                "image_path": "images/neptune.png",
                "emissivity": 0.2,
                "volume": "6.25×10¹³ км³",
                "escape_velocity": "23.5 км/с"
            }
        ]
        
        # Добавляем Плутон и другие карликовые планеты
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
                {"name": "Харон", "distance": 2.0, "radius": 2, "speed": 6.0, "angle": random.uniform(0, 2*math.pi), "color": "#808080"}
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
        self.planet_images = {}
        self.textures = {}
        self.effects_cache = {}
        self.background_images = []
        
        # Создание папок
        os.makedirs("images", exist_ok=True)
        os.makedirs("textures", exist_ok=True)
        os.makedirs("saves", exist_ok=True)
        os.makedirs("screenshots", exist_ok=True)
        os.makedirs("backgrounds", exist_ok=True)
        
        self.load_planet_images()
        self.generate_textures()
        self.load_backgrounds()
        
        # ==================== ИНФОРМАЦИЯ О ПЛАНЕТАХ ====================
        self.planet_info = self.collect_mega_info()
        
        # ==================== СОЗДАНИЕ ИНТЕРФЕЙСА ====================
        self.create_mega_interface()
        
        # ==================== ЗАПУСК АНИМАЦИИ ====================
        self.animate()
        
        # ==================== ЗАПУСК ФОНОВЫХ ЗАДАЧ ====================
        self.start_background_tasks()
    
    def generate_satellites(self):
        """Генерация искусственных спутников Земли"""
        satellites = []
        for i in range(10):
            satellites.append({
                "name": f"Sat-{i+1}",
                "distance": 1.1,
                "radius": 1,
                "color": "#C0C0C0",
                "speed": random.uniform(10, 20),
                "angle": random.uniform(0, 2*math.pi),
                "parent": "Земля"
            })
        return satellites
    
    def generate_space_stations(self):
        """Генерация космических станций"""
        stations = [
            {
                "name": "МКС",
                "distance": 1.08,
                "radius": 2,
                "color": "#FFD700",
                "speed": 15.5,
                "angle": random.uniform(0, 2*math.pi),
                "parent": "Земля"
            },
            {
                "name": "Тяньгун",
                "distance": 1.09,
                "radius": 1.8,
                "color": "#FF4500",
                "speed": 15.4,
                "angle": random.uniform(0, 2*math.pi),
                "parent": "Земля"
            }
        ]
        return stations
    
    def generate_stars(self, count):
        """Генерация улучшенного звездного поля"""
        stars = []
        for _ in range(count):
            x = random.randint(0, 2000)
            y = random.randint(0, 1500)
            z = random.uniform(0.1, 1.0)
            size = random.uniform(0.5, 3.0) * z
            brightness = random.randint(100, 255)
            twinkle_speed = random.uniform(0.01, 0.1)
            twinkle_offset = random.uniform(0, 2*math.pi)
            color_temp = random.choice(['white', 'blue', 'red', 'yellow', 'orange'])
            spectral_class = random.choice(['O', 'B', 'A', 'F', 'G', 'K', 'M'])
            variable = random.random() < 0.1
            has_planet = random.random() < 0.01  # 1% звезд имеют экзопланеты
            
            stars.append({
                'x': x, 'y': y, 'z': z,
                'size': size, 'base_size': size,
                'brightness': brightness, 'base_brightness': brightness,
                'twinkle_speed': twinkle_speed, 'twinkle_offset': twinkle_offset,
                'color_temp': color_temp, 'spectral_class': spectral_class,
                'variable': variable, 'has_planet': has_planet
            })
        return stars
    
    def generate_deep_space(self, count):
        """Генерация улучшенных объектов глубокого космоса"""
        objects = []
        types = ['galaxy', 'nebula', 'globular_cluster', 'quasar', 'pulsar']
        for _ in range(count):
            x = random.randint(0, 2000)
            y = random.randint(0, 1500)
            radius = random.randint(30, 150)
            obj_type = random.choice(types)
            r, g, b = random.choice([
                (0.8, 0.2, 0.3), (0.3, 0.4, 0.8), (0.2, 0.8, 0.4),
                (0.6, 0.3, 0.7), (0.9, 0.5, 0.2), (0.4, 0.8, 0.8),
                (0.7, 0.2, 0.5), (0.3, 0.6, 0.9)
            ])
            objects.append({
                'x': x, 'y': y, 'radius': radius,
                'type': obj_type, 'color': (r, g, b),
                'opacity': random.uniform(0.1, 0.3),
                'rotation': random.uniform(0, 2*math.pi)
            })
        return objects
    
    def generate_nebulae(self, count):
        """Генерация улучшенных туманностей"""
        nebulae = []
        for _ in range(count):
            x = random.randint(0, 2000)
            y = random.randint(0, 1500)
            radius = random.randint(100, 300)
            shape = random.choice(['spiral', 'circle', 'irregular', 'ring', 'bipolar'])
            r, g, b = random.choice([
                (0.9, 0.3, 0.4), (0.3, 0.4, 0.9), (0.4, 0.9, 0.5),
                (0.8, 0.5, 0.2), (0.6, 0.3, 0.8), (0.2, 0.5, 0.9)
            ])
            nebulae.append({
                'x': x, 'y': y, 'radius': radius,
                'shape': shape, 'color': (r, g, b),
                'opacity': random.uniform(0.1, 0.3),
                'pulse': random.uniform(0.05, 0.15),
                'rotation': 0
            })
        return nebulae
    
    def generate_asteroid_belt(self, count):
        """Генерация улучшенного пояса астероидов"""
        asteroids = []
        for _ in range(count):
            distance = random.uniform(2.0, 3.5)
            angle = random.uniform(0, 2*math.pi)
            size = random.uniform(0.5, 3.0)
            color = random.choice(['#808080', '#A0522D', '#8B4513', '#696969', '#C0C0C0'])
            speed = random.uniform(0.8, 1.2) * 0.5
            composition = random.choice(['rocky', 'metallic', 'carbonaceous'])
            asteroids.append({
                'distance': distance, 'angle': angle,
                'size': size, 'color': color,
                'speed': speed, 'composition': composition
            })
        return asteroids
    
    def generate_comets(self, count):
        """Генерация улучшенных комет"""
        comets = []
        for _ in range(count):
            comets.append({
                'active': False,
                'x': 0, 'y': 0,
                'vx': 0, 'vy': 0,
                'tail': [],
                'life': 0,
                'max_life': random.randint(300, 800),
                'color': random.choice(['#00FFFF', '#FFD700', '#FF69B4', '#87CEEB']),
                'tail_length': random.randint(30, 100)
            })
        return comets
    
    def generate_constellations(self):
        """Генерация реалистичных созвездий"""
        constellations = []
        names = ['Орион', 'Большая Медведица', 'Малая Медведица', 'Кассиопея', 'Лебедь', 
                 'Дракон', 'Геркулес', 'Андромеда', 'Персей', 'Цефей']
        
        for name in names:
            stars = []
            for _ in range(random.randint(5, 15)):
                x = random.randint(200, 1800)
                y = random.randint(100, 900)
                brightness = random.randint(150, 255)
                stars.append((x, y, brightness))
            constellations.append({'name': name, 'stars': stars})
        
        return constellations
    
    def generate_black_holes(self, count):
        """Генерация черных дыр с эффектами"""
        holes = []
        for _ in range(count):
            holes.append({
                'x': random.randint(200, 1800),
                'y': random.randint(100, 900),
                'mass': random.uniform(10, 100),
                'active': random.choice([True, False]),
                'accretion_disk': random.random() < 0.7,
                'pulse': random.uniform(0.05, 0.2),
                'phase': random.uniform(0, 2*math.pi)
            })
        return holes
    
    def load_planet_images(self):
        """Улучшенная загрузка изображений"""
        if not HAS_PIL:
            return
        
        for planet in self.planets_data:
            try:
                if os.path.exists(planet["image_path"]):
                    img = Image.open(planet["image_path"])
                    
                    if img.mode != 'RGBA':
                        img = img.convert('RGBA')
                    
                    enhancer = ImageEnhance.Sharpness(img)
                    img = enhancer.enhance(1.3)
                    
                    enhancer = ImageEnhance.Contrast(img)
                    img = enhancer.enhance(1.2)
                    
                    enhancer = ImageEnhance.Brightness(img)
                    img = enhancer.enhance(1.1)
                    
                    self.planet_images[planet["name"]] = img
                    print(f"✅ Загружено изображение для {planet['name']}")
                else:
                    print(f"⚠️ Изображение не найдено: {planet['image_path']}")
            except Exception as e:
                print(f"❌ Ошибка загрузки {planet['name']}: {e}")
    
    def load_backgrounds(self):
        """Загрузка фоновых изображений"""
        if not HAS_PIL:
            return
        
        bg_files = ['bg1.jpg', 'bg2.jpg', 'bg3.jpg', 'bg4.jpg']
        for bg_file in bg_files:
            bg_path = os.path.join('backgrounds', bg_file)
            if os.path.exists(bg_path):
                try:
                    img = Image.open(bg_path)
                    img = img.resize((1900, 1000), Image.Resampling.LANCZOS)
                    self.background_images.append(ImageTk.PhotoImage(img))
                except:
                    pass
    
    def generate_textures(self):
        """Генерация улучшенных текстур"""
        if not HAS_PIL:
            return
        
        try:
            # Текстура Земли
            earth_tex = Image.new('RGBA', (256, 256), (46, 134, 193, 255))
            draw = ImageDraw.Draw(earth_tex)
            for _ in range(500):
                x = random.randint(0, 255)
                y = random.randint(0, 255)
                r = random.randint(2, 5)
                color = (46, 200, 100, 255) if random.random() > 0.7 else (0, 100, 0, 255)
                draw.ellipse([x-r, y-r, x+r, y+r], fill=color)
            earth_tex = earth_tex.filter(ImageFilter.GaussianBlur(2))
            self.textures['earth'] = earth_tex
            
            # Текстура Марса
            mars_tex = Image.new('RGBA', (256, 256), (192, 57, 43, 255))
            draw = ImageDraw.Draw(mars_tex)
            for _ in range(500):
                x = random.randint(0, 255)
                y = random.randint(0, 255)
                r = random.randint(2, 6)
                color = (155, 89, 182, 255) if random.random() > 0.8 else (142, 68, 173, 255)
                draw.ellipse([x-r, y-r, x+r, y+r], fill=color)
            mars_tex = mars_tex.filter(ImageFilter.GaussianBlur(2))
            self.textures['mars'] = mars_tex
            
            # Текстура Юпитера
            jupiter_tex = Image.new('RGBA', (256, 256), (212, 172, 13, 255))
            draw = ImageDraw.Draw(jupiter_tex)
            for i in range(10):
                y = i * 25 + random.randint(-5, 5)
                draw.rectangle([0, y, 255, y+5], fill=(184, 115, 51, 255))
            jupiter_tex = jupiter_tex.filter(ImageFilter.GaussianBlur(3))
            self.textures['jupiter'] = jupiter_tex
            
        except Exception as e:
            print(f"Ошибка генерации текстур: {e}")
    
    def extract_number(self, value):
        """Улучшенное извлечение числа"""
        if isinstance(value, (int, float)):
            return float(value)
        try:
            import re
            match = re.search(r'[-+]?\d*\.?\d+', str(value))
            if match:
                return float(match.group())
            return 0.0
        except:
            return 0.0
    
    def collect_mega_info(self):
        """Сбор ультра-информации о планетах"""
        info = {}
        
        for planet in self.planets_data:
            gravity_val = self.extract_number(planet['gravity'])
            
            orbital_velocity = 2 * math.pi * planet['distance'] * 149.6 / (planet['speed'] * 365) if planet['speed'] > 0 else 0
            escape_velocity = math.sqrt(2 * gravity_val * 1000) if gravity_val > 0 else 0
            
            info[planet['name']] = {
                "Название": planet['name'],
                "Английское название": planet.get('name_en', ''),
                "Тип": "Планета" if planet['radius'] > 5 else "Карликовая планета",
                
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
                
                "Орбитальные характеристики": {
                    "Расстояние от Солнца": f"{planet['distance']} АЕ ({planet['distance']*149.6:.1f} млн км)",
                    "Орбитальный период": f"{1/planet['speed']:.2f} земных лет" if planet['speed'] > 0 else "Неизвестно",
                    "Орбитальная скорость": f"{orbital_velocity:.1f} км/с",
                    "Наклон орбиты": f"{planet.get('orbit_tilt', 0) * 10:.1f}°"
                },
                
                "Вращение": {
                    "Период вращения": f"{24/abs(planet['rotation_speed']):.1f} часов" if planet['rotation_speed'] != 0 else "Синхронное",
                    "Направление вращения": "Прямое" if planet['rotation_speed'] > 0 else "Обратное"
                },
                
                "Состав": {
                    "Атмосфера": "Есть" if planet.get('atmosphere') else "Нет",
                    "Состав атмосферы": planet.get('atmosphere', 'Отсутствует'),
                    "Кольца": "Есть" if planet.get('has_rings') else "Нет",
                    "Количество колец": planet.get('ring_count', 0),
                    "Спутники": planet['moon_count']
                },
                
                "История": {
                    "Открытие": planet['discovery'],
                    "Названа в честь": self.get_name_origin(planet['name'])
                },
                
                "Интересное": {
                    "Описание": planet['description'],
                    "Интересный факт": planet['fun_fact']
                },
                
                "Технические": {
                    "Альбедо": f"{planet.get('emissivity', 0.2):.2f}",
                    "Видимая звездная величина": f"{-2.5 * math.log10(max(0.01, planet['emissivity'])):.1f}"
                }
            }
        
        return info
    
    def get_name_origin(self, name):
        """Происхождение названия"""
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
        return origins.get(name, "Неизвестно")
    
    def create_mega_interface(self):
        """Создание ультимативного интерфейса"""
        # Главный контейнер
        main_frame = tk.Frame(self.root, bg='#000000')
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Верхняя панель
        top_bar = tk.Frame(main_frame, bg='#0a0a2a', height=80)
        top_bar.pack(fill=tk.X)
        top_bar.pack_propagate(False)
        
        # Логотип
        title_frame = tk.Frame(top_bar, bg='#0a0a2a')
        title_frame.pack(side=tk.LEFT, padx=20)
        
        tk.Label(title_frame, text="🌌", bg='#0a0a2a', fg='#FFD700',
                font=('Arial', 36)).pack(side=tk.LEFT)
        
        tk.Label(title_frame, text="МЕГА-СИМУЛЯЦИЯ\nСОЛНЕЧНОЙ СИСТЕМЫ 3000 ULTIMATE", 
                bg='#0a0a2a', fg='#FFD700', font=('Arial', 16, 'bold'),
                justify=tk.LEFT).pack(side=tk.LEFT, padx=10)
        
        # Статус бар с дополнительной информацией
        status_frame = tk.Frame(top_bar, bg='#0a0a2a')
        status_frame.pack(side=tk.RIGHT, padx=20)
        
        self.fps_label = tk.Label(status_frame, text="FPS: 60", bg='#0a0a2a', fg='#00FF00',
                                 font=('Arial', 10, 'bold'))
        self.fps_label.pack(anchor='e')
        
        self.time_label = tk.Label(status_frame, text="Время: 0", bg='#0a0a2a', fg='#00FF00',
                                  font=('Arial', 10, 'bold'))
        self.time_label.pack(anchor='e')
        
        self.zoom_status = tk.Label(status_frame, text="Зум: 1.0x", bg='#0a0a2a', fg='#00FF00',
                                   font=('Arial', 10, 'bold'))
        self.zoom_status.pack(anchor='e')
        
        self.coord_label = tk.Label(status_frame, text="X: 0 Y: 0", bg='#0a0a2a', fg='#00FF00',
                                   font=('Arial', 10, 'bold'))
        self.coord_label.pack(anchor='e')
        
        # Кнопки управления интерфейсом
        ui_buttons = tk.Frame(top_bar, bg='#0a0a2a')
        ui_buttons.pack(side=tk.RIGHT, padx=10)
        
        self.fullscreen_btn = tk.Button(ui_buttons, text="⛶", command=self.toggle_fullscreen,
                                       bg='#4a6a9a', fg='white', font=('Arial', 12, 'bold'),
                                       width=3, relief=tk.RAISED, bd=2)
        self.fullscreen_btn.pack(side=tk.LEFT, padx=2)
        
        self.controls_btn = tk.Button(ui_buttons, text="▼", command=self.toggle_control_panel,
                                     bg='#4a6a9a', fg='white', font=('Arial', 12, 'bold'),
                                     width=3, relief=tk.RAISED, bd=2)
        self.controls_btn.pack(side=tk.LEFT, padx=2)
        
        # Основной контейнер
        content_frame = tk.Frame(main_frame, bg='#000000')
        content_frame.pack(fill=tk.BOTH, expand=True)
        
        # Левый фрейм с канвасом
        canvas_frame = tk.Frame(content_frame, bg='#000000')
        canvas_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Канвас с улучшенными параметрами
        self.canvas = tk.Canvas(canvas_frame, width=1300, height=800,
                               bg='#000000', highlightthickness=0,
                               cursor='crosshair')
        self.canvas.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)
        
        # Привязка событий с поддержкой зума
        self.canvas.bind("<Button-1>", self.on_canvas_click)
        self.canvas.bind("<B1-Motion>", self.on_canvas_drag)
        self.canvas.bind("<ButtonRelease-1>", self.on_canvas_release)
        self.canvas.bind("<MouseWheel>", self.on_mousewheel)
        self.canvas.bind("<Motion>", self.on_mouse_move)
        self.canvas.bind("<Button-3>", self.on_right_click)
        self.canvas.bind("<Double-Button-1>", self.on_double_click)
        self.canvas.bind("<Control-MouseWheel>", self.on_control_mousewheel)
        self.canvas.bind("<Shift-MouseWheel>", self.on_shift_mousewheel)
        
        # Панель управления с улучшенным дизайном
        self.control_panel = tk.Frame(canvas_frame, bg='#0a0a2a', height=200, relief=tk.RAISED, bd=3)
        self.control_panel.pack(fill=tk.X, padx=10, pady=(0, 10))
        self.control_panel.pack_propagate(False)
        
        # Ноутбук с вкладками
        notebook = ttk.Notebook(self.control_panel)
        notebook.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        style = ttk.Style()
        style.theme_use('clam')
        style.configure("TNotebook", background='#0a0a2a', borderwidth=0)
        style.configure("TNotebook.Tab", background='#1a1a3a', foreground='white', padding=[15, 5])
        style.map("TNotebook.Tab", background=[("selected", '#4a6a9a')])
        
        # Вкладка управления с улучшенным зумом
        control_tab = tk.Frame(notebook, bg='#0a0a2a')
        notebook.add(control_tab, text="⚙️ УПРАВЛЕНИЕ")
        
        # Скорость
        speed_frame = tk.Frame(control_tab, bg='#0a0a2a')
        speed_frame.pack(fill=tk.X, pady=5, padx=10)
        
        tk.Label(speed_frame, text="⏱️ СКОРОСТЬ:", bg='#0a0a2a', fg='#FFD700',
                font=('Arial', 10, 'bold'), width=12).pack(side=tk.LEFT)
        
        self.time_scale = tk.Scale(speed_frame, from_=0.1, to=100, orient=tk.HORIZONTAL,
                                   length=300, command=self.change_time_speed,
                                   bg='#0a0a2a', fg='white', highlightbackground='#4a6a9a',
                                   troughcolor='#1a1a3a', resolution=0.1)
        self.time_scale.set(1.0)
        self.time_scale.pack(side=tk.LEFT, padx=5)
        
        self.speed_label = tk.Label(speed_frame, text="1.0x", bg='#0a0a2a', fg='#00FF00',
                                   font=('Arial', 12, 'bold'), width=8)
        self.speed_label.pack(side=tk.LEFT)
        
        # Зум с точной настройкой
        zoom_frame = tk.Frame(control_tab, bg='#0a0a2a')
        zoom_frame.pack(fill=tk.X, pady=5, padx=10)
        
        tk.Label(zoom_frame, text="🔍 ЗУМ:", bg='#0a0a2a', fg='#FFD700',
                font=('Arial', 10, 'bold'), width=12).pack(side=tk.LEFT)
        
        self.zoom_scale = tk.Scale(zoom_frame, from_=0.1, to=10.0, orient=tk.HORIZONTAL,
                                   length=300, command=self.change_zoom,
                                   bg='#0a0a2a', fg='white', highlightbackground='#4a6a9a',
                                   troughcolor='#1a1a3a', resolution=0.1)
        self.zoom_scale.set(1.0)
        self.zoom_scale.pack(side=tk.LEFT, padx=5)
        
        self.zoom_label = tk.Label(zoom_frame, text="1.0x", bg='#0a0a2a', fg='#00FF00',
                                  font=('Arial', 12, 'bold'), width=8)
        self.zoom_label.pack(side=tk.LEFT)
        
        # Кнопки точной настройки зума
        zoom_buttons = tk.Frame(zoom_frame, bg='#0a0a2a')
        zoom_buttons.pack(side=tk.LEFT, padx=10)
        
        tk.Button(zoom_buttons, text="+", command=self.zoom_in,
                 bg='#4a6a9a', fg='white', font=('Arial', 10, 'bold'),
                 width=3).pack(side=tk.LEFT, padx=2)
        
        tk.Button(zoom_buttons, text="-", command=self.zoom_out,
                 bg='#4a6a9a', fg='white', font=('Arial', 10, 'bold'),
                 width=3).pack(side=tk.LEFT, padx=2)
        
        tk.Button(zoom_buttons, text="1x", command=self.zoom_reset,
                 bg='#4a6a9a', fg='white', font=('Arial', 10, 'bold'),
                 width=3).pack(side=tk.LEFT, padx=2)
        
        # Кнопки управления
        buttons_frame = tk.Frame(control_tab, bg='#0a0a2a')
        buttons_frame.pack(fill=tk.X, pady=10, padx=10)
        
        self.pause_btn = tk.Button(buttons_frame, text="⏸️ ПАУЗА", command=self.toggle_pause,
                                  bg='#4a6a9a', fg='white', font=('Arial', 11, 'bold'),
                                  width=12, relief=tk.RAISED, bd=3)
        self.pause_btn.pack(side=tk.LEFT, padx=5)
        
        reset_btn = tk.Button(buttons_frame, text="🔄 СБРОС", command=self.reset_simulation,
                             bg='#4a6a9a', fg='white', font=('Arial', 11, 'bold'),
                             width=12, relief=tk.RAISED, bd=3)
        reset_btn.pack(side=tk.LEFT, padx=5)
        
        center_btn = tk.Button(buttons_frame, text="🎯 ЦЕНТР", command=self.center_view,
                              bg='#4a6a9a', fg='white', font=('Arial', 11, 'bold'),
                              width=12, relief=tk.RAISED, bd=3)
        center_btn.pack(side=tk.LEFT, padx=5)
        
        # Вкладка отображения
        display_tab = tk.Frame(notebook, bg='#0a0a2a')
        notebook.add(display_tab, text="🎨 ОТОБРАЖЕНИЕ")
        
        # Переменные для чекбоксов
        self.orbits_var = tk.BooleanVar(value=True)
        self.labels_var = tk.BooleanVar(value=True)
        self.effects_var = tk.BooleanVar(value=True)
        self.grid_var = tk.BooleanVar(value=False)
        self.asteroids_var = tk.BooleanVar(value=True)
        self.nebula_var = tk.BooleanVar(value=True)
        self.trails_var = tk.BooleanVar(value=False)
        self.hdr_var = tk.BooleanVar(value=True)
        self.minimap_var = tk.BooleanVar(value=True)
        self.legend_var = tk.BooleanVar(value=True)
        self.constellations_var = tk.BooleanVar(value=False)
        
        check_frame1 = tk.Frame(display_tab, bg='#0a0a2a')
        check_frame1.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        check_frame2 = tk.Frame(display_tab, bg='#0a0a2a')
        check_frame2.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        check_frame3 = tk.Frame(display_tab, bg='#0a0a2a')
        check_frame3.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Чекбоксы
        checks1 = [
            ("🔄 Орбиты", self.orbits_var, self.toggle_orbits),
            ("📝 Названия", self.labels_var, self.toggle_labels),
            ("✨ Эффекты", self.effects_var, self.toggle_effects),
            ("🔲 Сетка", self.grid_var, self.toggle_grid),
            ("☄️ Астероиды", self.asteroids_var, self.toggle_asteroids)
        ]
        
        for text, var, cmd in checks1:
            tk.Checkbutton(check_frame1, text=text, variable=var, command=cmd,
                          bg='#0a0a2a', fg='white', selectcolor='#0a0a2a',
                          activebackground='#0a0a2a', font=('Arial', 10)).pack(anchor='w', pady=3)
        
        checks2 = [
            ("🌌 Туманности", self.nebula_var, self.toggle_nebula),
            ("📈 Траектории", self.trails_var, self.toggle_trails),
            ("🌈 HDR режим", self.hdr_var, self.toggle_hdr),
            ("🗺️ Миникарта", self.minimap_var, self.toggle_minimap),
            ("📋 Легенда", self.legend_var, self.toggle_legend)
        ]
        
        for text, var, cmd in checks2:
            tk.Checkbutton(check_frame2, text=text, variable=var, command=cmd,
                          bg='#0a0a2a', fg='white', selectcolor='#0a0a2a',
                          activebackground='#0a0a2a', font=('Arial', 10)).pack(anchor='w', pady=3)
        
        checks3 = [
            ("✨ Созвездия", self.constellations_var, self.toggle_constellations),
            ("⚫ Черные дыры", tk.BooleanVar(value=True), lambda: None),
            ("🛰️ Спутники", tk.BooleanVar(value=True), lambda: None),
            ("🚀 Станции", tk.BooleanVar(value=True), lambda: None)
        ]
        
        for text, var, cmd in checks3:
            tk.Checkbutton(check_frame3, text=text, variable=var, command=cmd,
                          bg='#0a0a2a', fg='white', selectcolor='#0a0a2a',
                          activebackground='#0a0a2a', font=('Arial', 10)).pack(anchor='w', pady=3)
        
        # Вкладка информации
        info_tab = tk.Frame(notebook, bg='#0a0a2a')
        notebook.add(info_tab, text="ℹ️ ИНФОРМАЦИЯ")
        
        info_text_frame = tk.Frame(info_tab, bg='#0a0a2a')
        info_text_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        self.info_text = tk.Text(info_text_frame, bg='#1a1a3a', fg='white',
                                 font=('Arial', 10), wrap=tk.WORD,
                                 height=10, width=60)
        self.info_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        scrollbar = tk.Scrollbar(info_text_frame, command=self.info_text.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.info_text.config(yscrollcommand=scrollbar.set)
        
        # Вкладка сохранений
        save_tab = tk.Frame(notebook, bg='#0a0a2a')
        notebook.add(save_tab, text="💾 СОХРАНЕНИЯ")
        
        save_buttons_frame = tk.Frame(save_tab, bg='#0a0a2a')
        save_buttons_frame.pack(expand=True, pady=20)
        
        tk.Button(save_buttons_frame, text="💾 Сохранить симуляцию", command=self.save_simulation,
                 bg='#4a6a9a', fg='white', font=('Arial', 11, 'bold'),
                 width=25, height=2, relief=tk.RAISED, bd=3).pack(pady=5)
        
        tk.Button(save_buttons_frame, text="📂 Загрузить симуляцию", command=self.load_simulation,
                 bg='#4a6a9a', fg='white', font=('Arial', 11, 'bold'),
                 width=25, height=2, relief=tk.RAISED, bd=3).pack(pady=5)
        
        tk.Button(save_buttons_frame, text="📸 Сделать скриншот", command=self.take_screenshot,
                 bg='#4a6a9a', fg='white', font=('Arial', 11, 'bold'),
                 width=25, height=2, relief=tk.RAISED, bd=3).pack(pady=5)
        
        tk.Button(save_buttons_frame, text="📊 Экспорт данных", command=self.export_data,
                 bg='#4a6a9a', fg='white', font=('Arial', 11, 'bold'),
                 width=25, height=2, relief=tk.RAISED, bd=3).pack(pady=5)
        
        # Правая панель с детальной информацией
        right_panel = tk.Frame(content_frame, width=400, bg='#0a0a2a', relief=tk.RAISED, bd=3)
        right_panel.pack(side=tk.RIGHT, fill=tk.Y, padx=10, pady=10)
        right_panel.pack_propagate(False)
        
        # Заголовок
        tk.Label(right_panel, text="📊 ДЕТАЛЬНАЯ ИНФОРМАЦИЯ",
                bg='#1a1a3a', fg='#FFD700', font=('Arial', 14, 'bold')).pack(fill=tk.X, pady=5)
        
        # Фрейм для прокрутки
        canvas_right = tk.Canvas(right_panel, bg='#0a0a2a', highlightthickness=0)
        scrollbar_right = tk.Scrollbar(right_panel, orient="vertical", command=canvas_right.yview)
        self.scrollable_frame = tk.Frame(canvas_right, bg='#0a0a2a')
        
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas_right.configure(scrollregion=canvas_right.bbox("all"))
        )
        
        canvas_right.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        canvas_right.configure(yscrollcommand=scrollbar_right.set)
        
        canvas_right.pack(side="left", fill="both", expand=True, padx=(5,0))
        scrollbar_right.pack(side="right", fill="y")
        
        # Показываем приветствие
        self.show_mega_welcome()
        
        # Легенда
        self.create_legend()
    
    def create_legend(self):
        """Создание легенды"""
        self.legend_frame = tk.Frame(self.root, bg='#0a0a2a', relief=tk.RAISED, bd=2)
        self.legend_frame.place(x=10, y=100)
        
        tk.Label(self.legend_frame, text="📋 ЛЕГЕНДА", bg='#1a1a3a', fg='#FFD700',
                font=('Arial', 10, 'bold')).pack(fill=tk.X, pady=2)
        
        legend_items = [
            ("🟡", "Солнце"),
            ("⚪", "Планета"),
            ("⚫", "Спутник"),
            ("☄️", "Астероид"),
            ("💫", "Комета"),
            ("🌌", "Туманность")
        ]
        
        for symbol, text in legend_items:
            item_frame = tk.Frame(self.legend_frame, bg='#0a0a2a')
            item_frame.pack(fill=tk.X, padx=5, pady=1)
            tk.Label(item_frame, text=symbol, bg='#0a0a2a', fg='white',
                    font=('Arial', 10)).pack(side=tk.LEFT)
            tk.Label(item_frame, text=text, bg='#0a0a2a', fg='white',
                    font=('Arial', 9)).pack(side=tk.LEFT, padx=5)
    
    def show_mega_welcome(self):
        """Показывает улучшенное приветствие"""
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()
        
        tk.Label(self.scrollable_frame, text="🌌 ДОБРО ПОЖАЛОВАТЬ!",
                bg='#0a0a2a', fg='#FFD700', font=('Arial', 18, 'bold')).pack(pady=20)
        
        tk.Label(self.scrollable_frame, text="🪐✨🌟☄️🌠🚀",
                bg='#0a0a2a', fg='white', font=('Arial', 40)).pack(pady=10)
        
        stats_frame = tk.Frame(self.scrollable_frame, bg='#1a1a3a', relief=tk.RIDGE, bd=2)
        stats_frame.pack(fill=tk.X, padx=15, pady=10)
        
        total_moons = self.total_moons()
        total_objects = len(self.planets_data) + total_moons + len(self.asteroids) + len(self.stars) + len(self.satellites) + len(self.space_stations)
        
        stats = [
            f"Планет: {len(self.planets_data)}",
            f"Спутников: {total_moons}",
            f"Астероидов: {len(self.asteroids)}",
            f"Звезд: {len(self.stars)}",
            f"Иск. спутников: {len(self.satellites)}",
            f"Косм. станций: {len(self.space_stations)}",
            f"Всего объектов: {total_objects}",
            f"Возраст системы: 4.6 млрд лет",
            f"Галактика: Млечный Путь"
        ]
        
        for stat in stats:
            tk.Label(stats_frame, text=f"• {stat}", bg='#1a1a3a', fg='#87CEEB',
                    font=('Arial', 10)).pack(anchor='w', padx=10, pady=2)
        
        guide_frame = tk.Frame(self.scrollable_frame, bg='#0a0a2a')
        guide_frame.pack(fill=tk.X, padx=15, pady=10)
        
        tk.Label(guide_frame, text="📖 УПРАВЛЕНИЕ:",
                bg='#0a0a2a', fg='#FFD700', font=('Arial', 12, 'bold')).pack(anchor='w')
        
        controls = [
            "• ЛКМ: выбрать планету",
            "• Перетаскивание: переместить вид",
            "• Колесико: изменить масштаб",
            "• Ctrl+Колесико: точная настройка зума",
            "• Shift+Колесико: горизонтальный скролл",
            "• ПКМ: контекстное меню",
            "• Двойной клик: центрировать на планете"
        ]
        
        for control in controls:
            tk.Label(guide_frame, text=control, bg='#0a0a2a', fg='white',
                    font=('Arial', 9)).pack(anchor='w')
    
    def show_mega_planet_info(self, planet_name):
        """Показывает улучшенную информацию о планете"""
        planet = next((p for p in self.planets_data if p["name"] == planet_name), None)
        if not planet or planet_name not in self.planet_info:
            return
        
        info = self.planet_info[planet_name]
        
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()
        
        title_frame = tk.Frame(self.scrollable_frame, bg='#0a0a2a')
        title_frame.pack(fill=tk.X, pady=10, padx=10)
        
        color_label = tk.Label(title_frame, text="●", bg='#0a0a2a', fg=planet["color"],
                              font=('Arial', 36))
        color_label.pack(side=tk.LEFT)
        
        tk.Label(title_frame, text=planet_name, bg='#0a0a2a', fg='#FFD700',
                font=('Arial', 24, 'bold')).pack(side=tk.LEFT, padx=10)
        
        if info["Английское название"]:
            tk.Label(self.scrollable_frame, text=info["Английское название"],
                    bg='#0a0a2a', fg='#87CEEB', font=('Arial', 14, 'italic')).pack()
        
        self.add_mega_separator()
        
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
        
        # Описание
        if "Интересное" in info:
            desc_frame = tk.Frame(self.scrollable_frame, bg='#1a1a3a', relief=tk.RIDGE, bd=2)
            desc_frame.pack(fill=tk.X, padx=10, pady=10)
            
            tk.Label(desc_frame, text="📝 ОПИСАНИЕ",
                    bg='#1a1a3a', fg='#FFD700', font=('Arial', 11, 'bold')).pack(pady=5)
            
            tk.Label(desc_frame, text=info["Интересное"]["Описание"],
                    bg='#1a1a3a', fg='white', font=('Arial', 10), wraplength=350).pack(pady=5, padx=10)
            
            fact_frame = tk.Frame(self.scrollable_frame, bg='#2a1a3a', relief=tk.RIDGE, bd=2)
            fact_frame.pack(fill=tk.X, padx=10, pady=10)
            
            tk.Label(fact_frame, text="✨ ИНТЕРЕСНЫЙ ФАКТ ✨",
                    bg='#2a1a3a', fg='#FF69B4', font=('Arial', 11, 'bold')).pack(pady=5)
            
            tk.Label(fact_frame, text=info["Интересное"]["Интересный факт"],
                    bg='#2a1a3a', fg='white', font=('Arial', 10), wraplength=350).pack(pady=5, padx=10)
    
    def add_mega_separator(self):
        """Добавляет разделитель"""
        tk.Frame(self.scrollable_frame, height=2, bg='#1a1a3a').pack(fill=tk.X, pady=5, padx=10)
    
    def add_mega_section(self, title, items):
        """Добавляет секцию с информацией"""
        tk.Label(self.scrollable_frame, text=title,
                bg='#0a0a2a', fg='#87CEEB', font=('Arial', 11, 'bold')).pack(pady=(10, 5), anchor='w', padx=10)
        
        if isinstance(items, dict):
            for key, value in items.items():
                tk.Label(self.scrollable_frame, text=f"• {key}: {value}",
                        bg='#0a0a2a', fg='white', font=('Arial', 9),
                        wraplength=350, justify=tk.LEFT, anchor='w').pack(pady=1, padx=20, fill=tk.X)
        else:
            for item in items:
                tk.Label(self.scrollable_frame, text=f"• {item}",
                        bg='#0a0a2a', fg='white', font=('Arial', 9),
                        wraplength=350, justify=tk.LEFT, anchor='w').pack(pady=1, padx=20, fill=tk.X)
        
        self.add_mega_separator()
    
    def total_moons(self):
        """Подсчет спутников"""
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
        """Сброс масштаба"""
        self.zoom_scale.set(1.0)
    
    def change_time_speed(self, val):
        self.time_multiplier = float(val)
        self.speed_label.config(text=f"{self.time_multiplier:.1f}x")
    
    def change_zoom(self, val):
        self.zoom_factor = float(val)
        self.zoom_label.config(text=f"{self.zoom_factor:.1f}x")
        self.zoom_status.config(text=f"Зум: {self.zoom_factor:.1f}x")
    
    def toggle_pause(self):
        self.paused = not self.paused
        self.pause_btn.config(text="▶️ ПУСК" if self.paused else "⏸️ ПАУЗА")
    
    def toggle_orbits(self):
        self.show_orbits = self.orbits_var.get()
    
    def toggle_labels(self):
        self.show_labels = self.labels_var.get()
    
    def toggle_effects(self):
        self.show_effects = self.effects_var.get()
    
    def toggle_grid(self):
        self.show_grid = self.grid_var.get()
    
    def toggle_asteroids(self):
        self.show_asteroids = self.asteroids_var.get()
    
    def toggle_nebula(self):
        self.show_nebula = self.nebula_var.get()
    
    def toggle_trails(self):
        self.trails_enabled = self.trails_var.get()
        if not self.trails_enabled:
            self.trails.clear()
    
    def toggle_hdr(self):
        self.hdr_mode = self.hdr_var.get()
    
    def toggle_minimap(self):
        self.show_minimap = self.minimap_var.get()
    
    def toggle_legend(self):
        self.show_legend = self.legend_var.get()
        if self.show_legend:
            self.legend_frame.place(x=10, y=100)
        else:
            self.legend_frame.place_forget()
    
    def toggle_constellations(self):
        self.show_constellations = self.constellations_var.get()
    
    def toggle_fullscreen(self):
        self.fullscreen = not self.fullscreen
        self.root.attributes("-fullscreen", self.fullscreen)
    
    def toggle_control_panel(self):
        if self.control_panel_visible:
            self.control_panel.pack_forget()
            self.control_panel_visible = False
            self.controls_btn.config(text="▲")
        else:
            self.control_panel.pack(fill=tk.X, padx=10, pady=(0, 10))
            self.control_panel_visible = True
            self.controls_btn.config(text="▼")
    
    def center_view(self):
        self.pan_x = 0
        self.pan_y = 0
    
    def reset_simulation(self):
        for planet in self.planets_data:
            planet["angle"] = random.uniform(0, 2*math.pi)
            planet["rotation"] = 0
        self.time_scale.set(1.0)
        self.zoom_scale.set(1.0)
        self.pan_x = 0
        self.pan_y = 0
        self.selected_planet = None
        self.show_mega_welcome()
        
        self.info_text.config(state=tk.NORMAL)
        self.info_text.delete(1.0, tk.END)
        self.info_text.insert(tk.END, "Симуляция сброшена. Выберите планету для информации.")
        self.info_text.config(state=tk.DISABLED)
    
    def save_simulation(self):
        filename = f"saves/solar_system_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        data = {
            'time_multiplier': self.time_multiplier,
            'zoom_factor': self.zoom_factor,
            'pan_x': self.pan_x,
            'pan_y': self.pan_y,
            'planets': []
        }
        
        for planet in self.planets_data:
            data['planets'].append({
                'name': planet['name'],
                'angle': planet['angle']
            })
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        
        messagebox.showinfo("Сохранение", f"Симуляция сохранена в {filename}")
    
    def load_simulation(self):
        filename = filedialog.askopenfilename(
            title="Загрузить симуляцию",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
        )
        
        if filename:
            try:
                with open(filename, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                
                self.time_multiplier = data['time_multiplier']
                self.zoom_factor = data['zoom_factor']
                self.pan_x = data['pan_x']
                self.pan_y = data['pan_y']
                
                for planet_data in data['planets']:
                    for planet in self.planets_data:
                        if planet['name'] == planet_data['name']:
                            planet['angle'] = planet_data['angle']
                
                self.time_scale.set(self.time_multiplier)
                self.zoom_scale.set(self.zoom_factor)
                
                messagebox.showinfo("Загрузка", "Симуляция загружена!")
                
            except Exception as e:
                messagebox.showerror("Ошибка", f"Не удалось загрузить: {e}")
    
    def take_screenshot(self):
        try:
            filename = f"screenshots/solarsystem_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
            
            x = self.canvas.winfo_rootx()
            y = self.canvas.winfo_rooty()
            width = self.canvas.winfo_width()
            height = self.canvas.winfo_height()
            
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
        """Экспорт данных в CSV"""
        filename = f"saves/planet_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                f.write("Название,Расстояние (АЕ),Радиус (от Земли),Температура,Спутники\n")
                for planet in self.planets_data:
                    f.write(f"{planet['name']},{planet['distance']},{planet['base_radius']/11},{planet['temperature']},{planet['moon_count']}\n")
            
            messagebox.showinfo("Экспорт", f"Данные экспортированы в {filename}")
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось экспортировать: {e}")
    
    def on_mousewheel(self, event):
        """Обработка колесика мыши для зума"""
        if event.delta > 0:
            self.zoom_scale.set(min(10.0, self.zoom_factor + 0.1))
        else:
            self.zoom_scale.set(max(0.1, self.zoom_factor - 0.1))
    
    def on_control_mousewheel(self, event):
        """Точная настройка зума с Ctrl"""
        if event.delta > 0:
            self.zoom_scale.set(min(10.0, self.zoom_factor + 0.05))
        else:
            self.zoom_scale.set(max(0.1, self.zoom_factor - 0.05))
    
    def on_shift_mousewheel(self, event):
        """Горизонтальный скролл с Shift"""
        if event.delta > 0:
            self.pan_x += 50
        else:
            self.pan_x -= 50
    
    def on_canvas_drag(self, event):
        """Перетаскивание для панорамирования"""
        if not self.dragging:
            self.dragging = True
            self.drag_start_x = event.x
            self.drag_start_y = event.y
        else:
            dx = event.x - self.drag_start_x
            dy = event.y - self.drag_start_y
            self.pan_x += dx
            self.pan_y += dy
            self.drag_start_x = event.x
            self.drag_start_y = event.y
    
    def on_canvas_release(self, event):
        self.dragging = False
    
    def on_mouse_move(self, event):
        """Обновление координат мыши"""
        self.coord_label.config(text=f"X: {event.x} Y: {event.y}")
        
        # Подсветка планеты при наведении
        center_x = 650 + self.pan_x
        center_y = 400 + self.pan_y
        
        for planet in self.planets_data:
            distance = planet["distance"] * self.AU * self.zoom_factor
            x = center_x + distance * math.cos(planet["angle"])
            y = center_y + distance * math.sin(planet["angle"])
            radius = planet["radius"] * self.zoom_factor
            
            if math.sqrt((event.x - x)**2 + (event.y - y)**2) < radius + 5:
                self.mouse_over_planet = planet["name"]
                break
            else:
                self.mouse_over_planet = None
    
    def on_right_click(self, event):
        """Контекстное меню"""
        menu = tk.Menu(self.root, tearoff=0)
        menu.add_command(label="🎯 Центрировать вид", command=self.center_view)
        menu.add_command(label="🔍 Сбросить зум", command=self.zoom_reset)
        menu.add_command(label="🔍 Увеличить", command=self.zoom_in)
        menu.add_command(label="🔍 Уменьшить", command=self.zoom_out)
        menu.add_separator()
        menu.add_command(label="⏸️ Пауза", command=self.toggle_pause)
        menu.add_command(label="🔄 Сброс", command=self.reset_simulation)
        menu.add_separator()
        menu.add_command(label="💾 Сохранить", command=self.save_simulation)
        menu.add_command(label="📂 Загрузить", command=self.load_simulation)
        menu.add_command(label="📸 Скриншот", command=self.take_screenshot)
        menu.add_separator()
        menu.add_command(label="❌ Выход", command=self.root.quit)
        menu.post(event.x_root, event.y_root)
    
    def on_double_click(self, event):
        """Двойной клик для центрирования на планете"""
        center_x = 650 + self.pan_x
        center_y = 400 + self.pan_y
        
        for planet in self.planets_data:
            distance = planet["distance"] * self.AU * self.zoom_factor
            x = center_x + distance * math.cos(planet["angle"])
            y = center_y + distance * math.sin(planet["angle"])
            radius = planet["radius"] * self.zoom_factor
            
            if math.sqrt((event.x - x)**2 + (event.y - y)**2) < radius + 10:
                self.pan_x = 650 - x
                self.pan_y = 400 - y
                break
    
    def on_canvas_click(self, event):
        """Выбор планеты"""
        center_x = 650 + self.pan_x
        center_y = 400 + self.pan_y
        
        found = False
        for planet in self.planets_data:
            distance = planet["distance"] * self.AU * self.zoom_factor
            x = center_x + distance * math.cos(planet["angle"])
            y = center_y + distance * math.sin(planet["angle"])
            radius = planet["radius"] * self.zoom_factor
            
            if math.sqrt((event.x - x)**2 + (event.y - y)**2) < radius + 10:
                self.selected_planet = planet["name"]
                self.show_mega_planet_info(planet["name"])
                found = True
                
                self.info_text.config(state=tk.NORMAL)
                self.info_text.delete(1.0, tk.END)
                self.info_text.insert(tk.END, f"ВЫБРАНА ПЛАНЕТА: {planet['name']}\n\n")
                self.info_text.insert(tk.END, f"Расстояние: {planet['distance']} АЕ\n")
                self.info_text.insert(tk.END, f"Температура: {planet['temperature']}\n")
                self.info_text.insert(tk.END, f"Спутников: {planet['moon_count']}\n")
                self.info_text.insert(tk.END, f"Описание: {planet['description']}")
                self.info_text.config(state=tk.DISABLED)
                
                break
        
        if not found:
            self.selected_planet = None
    
    def draw_minimap(self):
        """Рисует миникарту для навигации"""
        if not self.show_minimap:
            return
        
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
        
        # Планеты на миникарте
        for planet in self.planets_data:
            scale = minimap_size / 60  # Масштаб для миникарты
            dist = planet["distance"] * scale
            x = sun_x + dist * math.cos(planet["angle"])
            y = sun_y + dist * math.sin(planet["angle"])
            
            if minimap_x <= x <= minimap_x + minimap_size and minimap_y <= y <= minimap_y + minimap_size:
                self.canvas.create_oval(x - 2, y - 2, x + 2, y + 2, fill=planet["color"], outline='')
    
    def draw_sun_mega(self, center_x, center_y):
        """Рисует ультра-солнце"""
        sun_radius = 50 * self.zoom_factor
        
        # Внутреннее ядро с улучшенным градиентом
        for i in range(15):
            r = sun_radius * (1 - i * 0.03)
            intensity = 255 - i * 12
            color = f'#{intensity:02x}{intensity-30:02x}00'
            self.canvas.create_oval(center_x - r, center_y - r,
                                    center_x + r, center_y + r,
                                    fill=color, outline='')
        
        # Корона с улучшенной анимацией
        if self.show_effects:
            for i in range(72):
                angle = i * 5 * math.pi/180 + self.time_of_day
                for j in range(4):
                    r_mult = 1.3 + j * 0.15
                    width = 4 - j
                    x1 = center_x + sun_radius * r_mult * math.cos(angle)
                    y1 = center_y + sun_radius * r_mult * math.sin(angle)
                    x2 = center_x + sun_radius * (r_mult + 0.4) * math.cos(angle + 0.15)
                    y2 = center_y + sun_radius * (r_mult + 0.4) * math.sin(angle + 0.15)
                    
                    color = ['#FFD700', '#FFA500', '#FF8C00', '#FF4500'][j]
                    self.canvas.create_line(x1, y1, x2, y2, fill=color, width=width, smooth=True)
            
            # Вспышки
            for _ in range(5):
                angle = random.uniform(0, 2*math.pi)
                dist = sun_radius * random.uniform(1.5, 3.0)
                x = center_x + dist * math.cos(angle)
                y = center_y + dist * math.sin(angle)
                
                self.canvas.create_line(center_x, center_y, x, y,
                                       fill='#FFFF00', width=random.randint(2, 6),
                                       dash=(2, 4))
        
        # Солнечные пятна
        for _ in range(8):
            spot_angle = random.uniform(0, 2*math.pi)
            spot_dist = random.uniform(0, sun_radius * 0.7)
            spot_x = center_x + spot_dist * math.cos(spot_angle)
            spot_y = center_y + spot_dist * math.sin(spot_angle)
            spot_r = random.uniform(5, 20) * self.zoom_factor
            
            self.canvas.create_oval(spot_x - spot_r, spot_y - spot_r,
                                    spot_x + spot_r, spot_y + spot_r,
                                    fill='#8B4513', outline='#CD853F', stipple='gray50')
        
        return sun_radius
    
    def draw_planet_mega(self, center_x, center_y, planet):
        """Рисует ультра-планету"""
        distance = planet["distance"] * self.AU * self.zoom_factor
        x = center_x + distance * math.cos(planet["angle"])
        y = center_y + distance * math.sin(planet["angle"])
        radius = planet["radius"] * self.zoom_factor
        
        if not self.paused:
            planet["rotation"] += planet["rotation_speed"] * self.time_multiplier
        
        # Траектории
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
        
        # Изображение или градиент
        if HAS_PIL and planet["name"] in self.planet_images:
            try:
                img = self.planet_images[planet["name"]]
                img_size = int(radius * 2)
                if img_size > 10:
                    img_resized = img.resize((img_size, img_size), Image.Resampling.LANCZOS)
                    
                    if abs(planet["rotation"]) > 0.01:
                        img_resized = img_resized.rotate(planet["rotation"] * 180/math.pi, expand=1)
                    
                    self.photo = ImageTk.PhotoImage(img_resized)
                    self.canvas.create_image(x, y, image=self.photo, anchor='center')
                    
                    if not hasattr(planet, 'photo_ref'):
                        planet['photo_ref'] = self.photo
                    else:
                        planet['photo_ref'] = self.photo
                    
            except:
                self.draw_planet_gradient(x, y, radius, planet)
        else:
            self.draw_planet_gradient(x, y, radius, planet)
        
        # Атмосфера
        if planet.get("atmosphere") and radius > 5:
            for i in range(4):
                atmos_radius = radius * (1.1 + i * 0.05)
                alpha = 100 - i * 20
                self.canvas.create_oval(x - atmos_radius, y - atmos_radius,
                                        x + atmos_radius, y + atmos_radius,
                                        outline=planet["atmosphere_color"],
                                        width=2, dash=(4, 4))
        
        # Кольца Сатурна (ультра-версия)
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
                if not self.paused:
                    moon["angle"] += self.BASE_SPEED * moon["speed"] * self.time_multiplier * 10
                
                moon_dist = moon["distance"] * radius
                moon_x = x + moon_dist * math.cos(moon["angle"])
                moon_y = y + moon_dist * math.sin(moon["angle"])
                moon_r = moon["radius"] * self.zoom_factor
                moon_color = moon.get("color", "#808080")
                
                self.canvas.create_oval(moon_x - moon_r, moon_y - moon_r,
                                        moon_x + moon_r, moon_y + moon_r,
                                        fill=moon_color, outline='#A9A9A9')
        
        # Искусственные спутники для Земли
        if planet["name"] == "Земля" and self.show_effects:
            for sat in self.satellites:
                if not self.paused:
                    sat["angle"] += self.BASE_SPEED * sat["speed"] * self.time_multiplier
                
                sat_dist = sat["distance"] * radius * 0.5
                sat_x = x + sat_dist * math.cos(sat["angle"])
                sat_y = y + sat_dist * math.sin(sat["angle"])
                sat_r = sat["radius"] * self.zoom_factor
                
                self.canvas.create_oval(sat_x - sat_r, sat_y - sat_r,
                                        sat_x + sat_r, sat_y + sat_r,
                                        fill=sat["color"], outline='white')
            
            for station in self.space_stations:
                if not self.paused:
                    station["angle"] += self.BASE_SPEED * station["speed"] * self.time_multiplier
                
                station_dist = station["distance"] * radius * 0.5
                station_x = x + station_dist * math.cos(station["angle"])
                station_y = y + station_dist * math.sin(station["angle"])
                station_r = station["radius"] * self.zoom_factor
                
                self.canvas.create_oval(station_x - station_r, station_y - station_r,
                                        station_x + station_r, station_y + station_r,
                                        fill=station["color"], outline='white')
        
        # Большое Красное Пятно
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
        # Основной градиент
        for i in range(8):
            r = radius * (1 - i * 0.08)
            if r < 2: break
            
            t = i / 8
            if t < 0.3:
                color = planet["color"]
            elif t < 0.7:
                color = planet.get("color2", planet["color"])
            else:
                color = planet.get("color3", planet["color"])
            
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
        
        # Блик
        self.canvas.create_oval(x - radius*0.2, y - radius*0.2,
                                x, y, fill='#FFFFFF', outline='')
        
        # Тень
        self.canvas.create_oval(x + radius*0.1, y + radius*0.1,
                                x + radius*0.3, y + radius*0.3,
                                fill='#000000', outline='')
    
    def draw_asteroids(self, center_x, center_y):
        """Рисует улучшенный пояс астероидов"""
        if not self.show_asteroids:
            return
        
        for asteroid in self.asteroids:
            if not self.paused:
                asteroid["angle"] += self.BASE_SPEED * asteroid["speed"] * self.time_multiplier
            
            distance = asteroid["distance"] * self.AU * self.zoom_factor
            x = center_x + distance * math.cos(asteroid["angle"])
            y = center_y + distance * math.sin(asteroid["angle"])
            size = asteroid["size"] * self.zoom_factor
            
            if size > 0.5:
                self.canvas.create_oval(x - size, y - size,
                                        x + size, y + size,
                                        fill=asteroid["color"], outline='')
    
    def draw_nebulae(self):
        """Рисует улучшенные туманности"""
        if not self.show_nebula:
            return
        
        for nebula in self.nebulae:
            x = nebula['x'] + self.pan_x * 0.1
            y = nebula['y'] + self.pan_y * 0.1
            
            r, g, b = nebula['color']
            color = f'#{int(r*255):02x}{int(g*255):02x}{int(b*255):02x}'
            
            nebula['rotation'] += 0.001
            pulse = 1 + math.sin(self.time_of_day * nebula['pulse']) * 0.1
            radius = nebula['radius'] * pulse
            
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
                x1 = stars[i][0] + self.pan_x * 0.2
                y1 = stars[i][1] + self.pan_y * 0.2
                x2 = stars[i+1][0] + self.pan_x * 0.2
                y2 = stars[i+1][1] + self.pan_y * 0.2
                
                self.canvas.create_line(x1, y1, x2, y2,
                                       fill='#87CEEB', width=1, dash=(2, 4))
    
    def draw_deep_space(self):
        """Рисует объекты глубокого космоса"""
        for obj in self.deep_space_objects:
            x = obj['x'] + self.pan_x * 0.05
            y = obj['y'] + self.pan_y * 0.05
            r, g, b = obj['color']
            color = f'#{int(r*255):02x}{int(g*255):02x}{int(b*255):02x}'
            
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
            while True:
                self.frame_count += 1
                if time.time() - self.last_time >= 1:
                    self.fps = self.frame_count
                    self.frame_count = 0
                    self.last_time = time.time()
                    self.simulation_time += 1
                    
                    try:
                        self.root.after(0, lambda: self.fps_label.config(text=f"FPS: {self.fps}"))
                        self.root.after(0, lambda: self.time_label.config(
                            text=f"Время: {self.simulation_time}s"
                        ))
                    except:
                        pass
                time.sleep(0.1)
        
        thread = threading.Thread(target=update_fps, daemon=True)
        thread.start()
    
    def animate(self):
        """Основной улучшенный цикл анимации"""
        if self.paused:
            self.animation_id = self.root.after(50, self.animate)
            return
        
        self.canvas.delete("all")
        
        self.time_of_day += 0.01 * self.time_multiplier
        self.total_distance_traveled += self.time_multiplier * 1000
        
        # Фоновые объекты
        self.draw_deep_space()
        self.draw_nebulae()
        
        # Звезды с параллаксом
        for star in self.stars:
            parallax_x = star['x'] + self.pan_x * (1 - star['z'])
            parallax_y = star['y'] + self.pan_y * (1 - star['z'])
            
            if star['variable']:
                brightness = star['base_brightness'] * (0.7 + 0.3 * math.sin(self.time_of_day * star['twinkle_speed']))
            else:
                brightness = star['base_brightness']
            
            if star['color_temp'] == 'blue':
                color = f'#88{int(brightness*0.5):02x}FF'
            elif star['color_temp'] == 'red':
                color = f'#FF{int(brightness*0.3):02x}{int(brightness*0.3):02x}'
            elif star['color_temp'] == 'yellow':
                color = f'#FF{int(brightness*0.8):02x}00'
            elif star['color_temp'] == 'orange':
                color = f'#FF{int(brightness*0.6):02x}00'
            else:
                color = f'#{int(brightness):02x}{int(brightness):02x}{int(brightness):02x}'
            
            self.canvas.create_oval(parallax_x, parallax_y,
                                    parallax_x + star['size'], parallax_y + star['size'],
                                    fill=color, outline='')
            
            if star['has_planet'] and self.show_effects:
                self.canvas.create_oval(parallax_x - 1, parallax_y - 1,
                                        parallax_x + 1, parallax_y + 1,
                                        fill='#87CEEB', outline='')
        
        self.draw_constellations(650, 400)
        
        center_x = 650 + self.pan_x
        center_y = 400 + self.pan_y
        
        # Сетка
        if self.show_grid:
            for i in range(-15, 16):
                grid_x = center_x + i * 100 * self.zoom_factor
                self.canvas.create_line(grid_x, center_y - 600, grid_x, center_y + 600,
                                       fill='#1a3a5a', width=1, dash=(2, 4))
            
            for i in range(-15, 16):
                grid_y = center_y + i * 100 * self.zoom_factor
                self.canvas.create_line(center_x - 600, grid_y, center_x + 600, grid_y,
                                       fill='#1a3a5a', width=1, dash=(2, 4))
        
        # Орбиты
        if self.show_orbits:
            for planet in self.planets_data:
                distance = planet["distance"] * self.AU * self.zoom_factor
                self.canvas.create_oval(center_x - distance, center_y - distance,
                                        center_x + distance, center_y + distance,
                                        outline='#2a4a6a', width=1, dash=(3, 6))
        
        # Солнце
        sun_radius = self.draw_sun_mega(center_x, center_y)
        
        # Астероиды
        self.draw_asteroids(center_x, center_y)
        
        # Планеты
        planet_positions = []
        for planet in self.planets_data:
            if not self.paused:
                planet["angle"] += self.BASE_SPEED * planet["speed"] * self.time_multiplier
            
            x, y, radius = self.draw_planet_mega(center_x, center_y, planet)
            planet_positions.append((planet["name"], x, y, radius))
        
        # Названия
        if self.show_labels:
            for name, x, y, radius in planet_positions:
                self.canvas.create_text(x + 2, y - radius - 16, text=name,
                                       fill='#000000', font=('Arial', 10, 'bold'))
                self.canvas.create_text(x, y - radius - 18, text=name,
                                       fill='white', font=('Arial', 10, 'bold'))
        
        # Кометы
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
        
        for comet in self.comets:
            if comet['active']:
                comet['x'] += comet['vx']
                comet['y'] += comet['vy']
                comet['life'] -= 1
                
                comet['tail'].append((comet['x'], comet['y']))
                if len(comet['tail']) > comet.get('tail_length', 30):
                    comet['tail'].pop(0)
                
                for i, (tx, ty) in enumerate(comet['tail']):
                    alpha = i / len(comet['tail'])
                    self.canvas.create_line(tx, ty, comet['x'], comet['y'],
                                           fill=f'#FFFF{int(alpha*255):02x}',
                                           width=2)
                
                self.canvas.create_oval(comet['x'] - 4, comet['y'] - 4,
                                        comet['x'] + 4, comet['y'] + 4,
                                        fill=comet.get('color', '#FFD700'), outline='white')
                
                if comet['life'] <= 0:
                    comet['active'] = False
        
        # Миникарта
        self.draw_minimap()
        
        # Статистика
        if self.show_stats:
            stats_text = f"Объектов: {len(self.planets_data) + self.total_moons() + len(self.asteroids) + len(self.stars)}"
            self.canvas.create_text(50, 50, text=stats_text, fill='#00FF00',
                                   font=('Arial', 10), anchor='w')
        
        self.animation_id = self.root.after(50, self.animate)

if __name__ == "__main__":
    root = tk.Tk()
    
    try:
        if HAS_PIL:
            icon = Image.new('RGBA', (32, 32), (0, 0, 0, 0))
            draw = ImageDraw.Draw(icon)
            draw.ellipse([8, 8, 24, 24], fill='#FFD700')
            photo = ImageTk.PhotoImage(icon)
            root.iconphoto(True, photo)
    except:
        pass
    
    app = MegaSolarSystem(root)
    root.mainloop()