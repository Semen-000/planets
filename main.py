import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from PIL import Image, ImageTk
import csv
import os
import re
from datetime import datetime

class OperatorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Нейрободр")
        self.root.geometry("1000x700")
        self.root.configure(bg='#f0f0f0')
        self.root.resizable(False, False)
        
        # Создание папок и файлов
        self.setup_files()
        
        # Переменные
        self.current_operator_id = None
        self.operator_data = {}
        self.photo_label = None  # Добавляем ссылку на photo_label
        
        # Показываем стартовое окно
        self.show_start_window()
    
    def setup_files(self):
        """Создание необходимых папок и файлов"""
        if not os.path.exists('operations'):
            os.makedirs('operations')
        
        if not os.path.exists('operation_db.csv'):
            with open('operation_db.csv', 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow(['id', 'last_name', 'first_name', 'middle_name', 'age', 
                               'birth_date', 'birth_time', 'software_start_time', 'days_duration'])
    
    def add_header(self, parent):
        """Добавляет заголовок и подзаголовок в окно на зеленом фоне"""
        header_frame = tk.Frame(parent, bg="#20B427")
        header_frame.pack(fill=tk.X, pady=0)
        
        tk.Label(header_frame, text="Нейрободр", 
                font=('Arial', 26, 'bold'), bg='#20B427', fg='white').pack(pady=(15, 0))
        
        tk.Label(header_frame, text="Программа для мониторинга состояния водителей", 
                font=('Arial', 11), bg='#20B427', fg='white').pack(pady=(0, 15))
        
        # Тонкая линия-разделитель
        tk.Frame(parent, bg='#bdc3c7', height=1).pack(fill=tk.X, pady=0)
    
    def validate_name_input(self, text):
        """Валидация для имени (только буквы, пробелы и дефисы)"""
        if text == "":
            return True
        # Разрешаем русские и английские буквы, пробелы и дефисы
        return bool(re.match(r'^[а-яА-Яa-zA-Z\s-]*$', text))
    
    def validate_age_input(self, text):
        """Валидация для возраста (только цифры, от 18 до 120)"""
        if text == "":
            return True
        if not text.isdigit():
            return False
        value = int(text)
        return 18 <= value <= 120
    
    def validate_id_input(self, text):
        """Валидация для ID (только цифры)"""
        if text == "":
            return True
        return text.isdigit()
    
    def show_start_window(self):
        """Окно №1 - Стартовая форма"""
        for widget in self.root.winfo_children():
            widget.destroy()
        
        # Добавляем заголовок
        self.add_header(self.root)
        
        # Кнопки
        btn_frame = tk.Frame(self.root, bg='#f0f0f0')
        btn_frame.pack(expand=True)
        
        tk.Button(btn_frame, text="РЕГИСТРАЦИЯ", command=self.show_registration_form,
                 font=('Arial', 14, 'bold'), bg='#005BBB', fg='white',
                 width=20, height=2, bd=0, cursor='hand2', relief=tk.FLAT).pack(pady=10)
        
        tk.Button(btn_frame, text="АВТОРИЗАЦИЯ", command=self.show_auth_form,
                 font=('Arial', 14, 'bold'), bg='#00A36C', fg='white',
                 width=20, height=2, bd=0, cursor='hand2', relief=tk.FLAT).pack(pady=10)
    
    def show_registration_form(self):
        """Форма №1 - Регистрация оператора"""
        for widget in self.root.winfo_children():
            widget.destroy()
        
        # Добавляем заголовок
        self.add_header(self.root)
        
        # Основной контейнер для трех колонок
        main_frame = tk.Frame(self.root, bg='#f0f0f0')
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        # === КОЛОНКА 1: ИНФОРМАЦИЯ ОПЕРАТОРА (СИНЯЯ) ===
        self.col1 = tk.Frame(main_frame, bg='white', bd=1, relief=tk.SOLID)
        self.col1.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5)
        
        # Заголовок колонки
        tk.Label(self.col1, text="Регистрация оператора", 
                font=('Arial', 14, 'bold'), bg='#005BBB', fg='white',
                height=2).pack(fill=tk.X)
        
        # Содержимое колонки 1
        self.content1 = tk.Frame(self.col1, bg='white', padx=15, pady=15)
        self.content1.pack(fill=tk.BOTH, expand=True)
        
        # === КОЛОНКА 2: ИДЕНТИФИКАЦИЯ (ОРАНЖЕВАЯ) ===
        self.col2 = tk.Frame(main_frame, bg='white', bd=1, relief=tk.SOLID)
        self.col2.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5)
        
        # Заголовок колонки
        tk.Label(self.col2, text="Идентификация", 
                font=('Arial', 14, 'bold'), bg='#FF6B00', fg='white',
                height=2).pack(fill=tk.X)
        
        # Содержимое колонки 2
        self.content2 = tk.Frame(self.col2, bg='white', padx=15, pady=15)
        self.content2.pack(fill=tk.BOTH, expand=True)
        
        # === КОЛОНКА 3: ИНФОРМАЦИОННЫЙ БЛОК (ЗЕЛЕНАЯ) ===
        self.col3 = tk.Frame(main_frame, bg='white', bd=1, relief=tk.SOLID)
        self.col3.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5)
        
        # Заголовок колонки
        tk.Label(self.col3, text="Информационный блок", 
                font=('Arial', 14, 'bold'), bg='#00A36C', fg='white',
                height=2).pack(fill=tk.X)
        
        # Содержимое колонки 3
        self.content3 = tk.Frame(self.col3, bg='white', padx=15, pady=15)
        self.content3.pack(fill=tk.BOTH, expand=True)
        
        # Заполняем колонки начальным содержимым
        self.show_registration_content()
        self.show_identification_content()
        self.show_info_content("Ожидание\nверификации...")
        
        # Кнопка назад
        tk.Button(self.root, text="← Назад", command=self.show_start_window,
                 bg='#e74c3c', fg='white', font=('Arial', 11, 'bold'),
                 width=10, bd=0, cursor='hand2', relief=tk.FLAT).pack(pady=10)
    
    def show_registration_content(self):
        """Показывает содержимое колонки информации оператора"""
        for widget in self.content1.winfo_children():
            widget.destroy()
        
        # Поля ввода
        fields = [
            ('Фамилия:', 'last_name'),
            ('Имя:', 'first_name'),
            ('Отчество:', 'middle_name'),
            ('Возраст:', 'age')
        ]
        
        self.reg_entries = {}
        
        # Регистрируем валидацию
        vcmd_name = (self.root.register(self.validate_name_input), '%P')
        vcmd_age = (self.root.register(self.validate_age_input), '%P')
        
        for label_text, field_name in fields:
            row = tk.Frame(self.content1, bg='white')
            row.pack(fill=tk.X, pady=8)
            
            tk.Label(row, text=label_text, width=10, anchor='w', bg='white', 
                    font=('Arial', 11)).pack(side=tk.LEFT)
            
            if field_name == 'age':
                # Для возраста - только цифры от 18 до 120
                entry = tk.Entry(row, width=22, font=('Arial', 11), bd=1, relief=tk.SUNKEN,
                               validate='key', validatecommand=vcmd_age)
            else:
                # Для имени/фамилии/отчества - только буквы
                entry = tk.Entry(row, width=22, font=('Arial', 11), bd=1, relief=tk.SUNKEN,
                               validate='key', validatecommand=vcmd_name)
            
            entry.pack(side=tk.LEFT, padx=5)
            self.reg_entries[field_name] = entry
            
            # Добавляем подсказку
            if field_name == 'age':
                tk.Label(row, text="(18-120)", font=('Arial', 8), fg='#7f8c8d', 
                       bg='white').pack(side=tk.LEFT, padx=2)
        
        tk.Button(self.content1, text="Записать", command=self.save_operator,
                 bg='#005BBB', fg='white', font=('Arial', 11, 'bold'),
                 width=15, height=1, bd=0, cursor='hand2', relief=tk.FLAT).pack(pady=20)
    
    def show_identification_content(self):
        """Показывает содержимое колонки идентификации"""
        for widget in self.content2.winfo_children():
            widget.destroy()
        
        tk.Label(self.content2, text="ID", font=('Arial', 24, 'bold'), 
                bg='white', fg='#2c3e50').pack(pady=10)
        
        self.photo_frame = tk.Frame(self.content2, bg='#ecf0f1', bd=1, relief=tk.SUNKEN,
                                   width=220, height=160)
        self.photo_frame.pack(pady=10)
        self.photo_frame.pack_propagate(False)
        
        self.photo_label = tk.Label(self.photo_frame, bg='#ecf0f1')
        self.photo_label.pack(expand=True, fill=tk.BOTH)
        
        tk.Label(self.content2, text="Требование: 800 x 600 px", 
                font=('Arial', 9), fg='#FF6B00', bg='white').pack(pady=5)
        
        tk.Button(self.content2, text="Загрузить фото", command=self.upload_photo,
                 bg='#005BBB', fg='white', font=('Arial', 10),
                 width=15, bd=0, cursor='hand2', relief=tk.FLAT).pack(pady=10)
    
    def show_info_content(self, text):
        """Показывает содержимое колонки информационного блока"""
        for widget in self.content3.winfo_children():
            widget.destroy()
        
        tk.Label(self.content3, text=text, 
                font=('Arial', 12), bg='white', fg='#7f8c8d', justify='center').pack(expand=True)
    
    def save_operator(self):
        """Сохранение данных оператора"""
        last_name = self.reg_entries['last_name'].get().strip()
        first_name = self.reg_entries['first_name'].get().strip()
        middle_name = self.reg_entries['middle_name'].get().strip()
        age = self.reg_entries['age'].get().strip()
        
        # Дополнительная проверка на пустые значения
        if not last_name:
            messagebox.showerror("Ошибка", "Заполните фамилию!")
            return
        
        if not first_name:
            messagebox.showerror("Ошибка", "Заполните имя!")
            return
        
        if not age:
            messagebox.showerror("Ошибка", "Заполните возраст!")
            return
        
        # Проверка на допустимые символы для имени
        if not re.match(r'^[а-яА-Яa-zA-Z\s-]+$', last_name):
            messagebox.showerror("Ошибка", "Фамилия может содержать только буквы, пробелы и дефисы!")
            return
        
        if not re.match(r'^[а-яА-Яa-zA-Z\s-]+$', first_name):
            messagebox.showerror("Ошибка", "Имя может содержать только буквы, пробелы и дефисы!")
            return
        
        if middle_name and not re.match(r'^[а-яА-Яa-zA-Z\s-]*$', middle_name):
            messagebox.showerror("Ошибка", "Отчество может содержать только буквы, пробелы и дефисы!")
            return
        
        try:
            age = int(age)
            if age < 18 or age > 120:
                messagebox.showerror("Ошибка", "Возраст должен быть от 18 до 120 лет!")
                return
        except ValueError:
            messagebox.showerror("Ошибка", "Возраст должен быть числом!")
            return
        
        # Получаем следующий ID
        next_id = 1
        if os.path.exists('operation_db.csv'):
            with open('operation_db.csv', 'r', encoding='utf-8') as f:
                reader = csv.reader(f)
                rows = list(reader)
                if len(rows) > 1:
                    next_id = int(rows[-1][0]) + 1
        
        now = datetime.now()
        
        with open('operation_db.csv', 'a', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow([
                next_id,
                last_name,
                first_name,
                middle_name,
                age,
                now.strftime('%d.%m.%Y'),
                now.strftime('%H:%M:%S'),
                now.strftime('%H:%M:%S'),
                '00:00:00'
            ])
        
        self.current_operator_id = next_id
        self.operator_data = {
            'id': next_id,
            'last_name': last_name,
            'first_name': first_name,
            'middle_name': middle_name,
            'age': age
        }
        
        messagebox.showinfo("Успех", f"Оператор зарегистрирован с ID: {next_id}")
        
        # Очищаем поля ввода после успешной регистрации
        for entry in self.reg_entries.values():
            entry.delete(0, tk.END)
        
        # Обновляем ID в колонке идентификации
        for widget in self.content2.winfo_children():
            if isinstance(widget, tk.Label) and widget.cget('text') == "ID":
                widget.destroy()
        
        # Показываем новый ID
        tk.Label(self.content2, text=f"ID {next_id}", font=('Arial', 24, 'bold'), 
                bg='white', fg='#2c3e50').pack(pady=10)
    
    def upload_photo(self):
        """Загрузка фото"""
        if not self.current_operator_id:
            messagebox.showerror("Ошибка", "Сначала зарегистрируйте оператора!")
            return
        
        file_path = filedialog.askopenfilename(
            title="Выберите фото оператора",
            filetypes=[("Image files", "*.jpg *.jpeg *.png")]
        )
        
        if file_path:
            try:
                img = Image.open(file_path)
                width, height = img.size
                print(f"Размер фото: {width}x{height}")  # Отладка
                
                # Проверяем размер с погрешностью в 1 пиксель (некоторые фото могут быть 799x599)
                if abs(width - 800) <= 2 and abs(height - 600) <= 2:
                    save_path = f"operations/ID_{self.current_operator_id}.jpg"
                    img.save(save_path)
                    
                    # Если photo_label существует, обновляем его
                    if hasattr(self, 'photo_label') and self.photo_label:
                        img.thumbnail((200, 140))
                        photo = ImageTk.PhotoImage(img)
                        self.photo_label.config(image=photo, width=200, height=140)
                        self.photo_label.image = photo
                    
                    # Обновляем информационный блок
                    if hasattr(self, 'content3'):
                        self.show_success_verification()
                else:
                    messagebox.showerror("Ошибка", 
                                       f"Неверный размер!\nТребуется: 800x600\nПолучено: {width}x{height}")
                    if hasattr(self, 'content3'):
                        self.show_fail_verification()
                    
            except Exception as e:
                messagebox.showerror("Ошибка", f"Не удалось загрузить фото: {str(e)}")
    
    def show_success_verification(self):
        """Успешная верификация"""
        for widget in self.content3.winfo_children():
            widget.destroy()
        
        # Информация об операторе в зеленой колонке
        info_frame = tk.Frame(self.content3, bg='white')
        info_frame.pack(fill=tk.BOTH, expand=True)
        
        # ФИО жирным
        fio = f"{self.operator_data['last_name']} {self.operator_data['first_name']} {self.operator_data['middle_name']}"
        tk.Label(info_frame, text=fio, 
                font=('Arial', 14, 'bold'), bg='white', fg='#2c3e50').pack(pady=(5, 0), anchor='w')
        
        # Возраст
        tk.Label(info_frame, text=f"{self.operator_data['age']} лет", 
                font=('Arial', 12), bg='white', fg='#34495e').pack(pady=(0, 10), anchor='w')
        
        # Разделитель
        tk.Frame(info_frame, bg='#bdc3c7', height=1).pack(fill=tk.X, pady=5)
        
        # Дата и время
        now = datetime.now()
        tk.Label(info_frame, text=f"Дата/время: {now.strftime('%d.%m.%Y')} / {now.strftime('%H:%M:%S')}", 
                font=('Arial', 10), bg='white', fg='#2c3e50').pack(pady=2, anchor='w')
        
        tk.Label(info_frame, text=f"Время запуска ПО: {now.strftime('%H:%M:%S')}", 
                font=('Arial', 10), bg='white', fg='#2c3e50').pack(pady=2, anchor='w')
        
        tk.Label(info_frame, text="Время в дороге: 00:00:00", 
                font=('Arial', 10), bg='white', fg='#2c3e50').pack(pady=2, anchor='w')
        
        tk.Label(info_frame, text="Оставшееся время: 09:00:00", 
                font=('Arial', 10), bg='white', fg='#2c3e50').pack(pady=2, anchor='w')
        
        # Разделитель
        tk.Frame(info_frame, bg='#bdc3c7', height=1).pack(fill=tk.X, pady=10)
        
        # Зеленый блок с ID
        green_block = tk.Frame(info_frame, bg='#00A36C', padx=10, pady=10)
        green_block.pack(fill=tk.X, pady=5)
        
        tk.Label(green_block, text="Оператор определен", 
                font=('Arial', 11, 'bold'), bg='#00A36C', fg='white').pack()
        
        tk.Label(green_block, text=f"ID {self.operator_data['id']}", 
                font=('Arial', 11, 'bold'), bg='#00A36C', fg='white').pack()
        
        tk.Label(green_block, text="Для запуска программы нажмите \"Далее\"", 
                font=('Arial', 9), bg='#00A36C', fg='white').pack(pady=(5, 0))
        
        # Кнопка Далее
        tk.Button(info_frame, text="Далее →", command=self.next_step,
                 bg='#005BBB', fg='white', font=('Arial', 10, 'bold'),
                 width=12, bd=0, cursor='hand2', relief=tk.FLAT).pack(pady=10, anchor='w')
    
    def show_fail_verification(self):
        """Неудачная верификация"""
        for widget in self.content3.winfo_children():
            widget.destroy()
        
        tk.Label(self.content3, text="НЕУДАЧНАЯ ВЕРИФИКАЦИЯ", 
                font=('Arial', 12, 'bold'), fg='#c0392b', bg='white').pack(pady=10)
        
        table = tk.Frame(self.content3, bg='white', bd=1, relief=tk.SOLID)
        table.pack(pady=10, padx=5, fill=tk.X)
        
        headers = [
            ("Информация оператора", '#005BBB'),
            ("Идентификация", '#FF6B00'),
            ("Информационный блок", '#00A36C')
        ]
        
        for i, (text, color) in enumerate(headers):
            tk.Label(table, text=text, font=('Arial', 9, 'bold'), 
                    bg=color, fg='white', relief=tk.RAISED, 
                    width=18, height=2).grid(row=0, column=i, padx=1, pady=1)
        
        data = [
            ("Фамилия", "Иванов", "Оператор не определен"),
            ("Имя", "Иван", "ID не присвоен"),
            ("Отчество", "Иванович", "Запуск программы невозможен")
        ]
        
        for r, row in enumerate(data, 1):
            for c, val in enumerate(row):
                anchor = 'center' if c == 2 else 'w'
                tk.Label(table, text=val, bg='white', relief=tk.SUNKEN, 
                        width=18, height=2, anchor=anchor,
                        font=('Arial', 8)).grid(row=r, column=c, padx=1, pady=1)
        
        btn_frame = tk.Frame(self.content3, bg='white')
        btn_frame.pack(pady=15)
        
        tk.Button(btn_frame, text="Далее", command=self.retry_identification,
                 bg='#00A36C', fg='white', font=('Arial', 10, 'bold'),
                 width=8, bd=0, cursor='hand2', relief=tk.FLAT).pack(side=tk.LEFT, padx=5)
        
        tk.Button(btn_frame, text="Отмена", command=self.show_start_window,
                 bg='#c0392b', fg='white', font=('Arial', 10, 'bold'),
                 width=8, bd=0, cursor='hand2', relief=tk.FLAT).pack(side=tk.LEFT, padx=5)
    
    def next_step(self):
        """Следующий шаг - возврат на начальное окно"""
        messagebox.showinfo("Информация", "Возврат в главное меню")
        self.show_start_window()  # Возвращаемся на начальное окно
    
    def retry_identification(self):
        """Повтор идентификации"""
        if hasattr(self, 'photo_label') and self.photo_label:
            self.photo_label.config(image='', width=220, height=160)
            self.photo_label.image = None
        self.show_info_content("Ожидание\nверификации...")
    
    def show_auth_form(self):
        """Окно №2 - Авторизация оператора"""
        for widget in self.root.winfo_children():
            widget.destroy()
        
        # Добавляем заголовок
        self.add_header(self.root)
        
        # Форма авторизации
        auth_frame = tk.Frame(self.root, bg='white', bd=2, relief=tk.GROOVE, padx=40, pady=30)
        auth_frame.pack(expand=True)
        
        tk.Label(auth_frame, text="Авторизация оператора", 
                font=('Arial', 18, 'bold'), bg='white', fg='#2c3e50').pack(pady=10)
        
        tk.Label(auth_frame, text="введите ID", font=('Arial', 14), 
                bg='white', fg='#34495e').pack(pady=(20, 5))
        
        # Регистрируем валидацию для ID
        vcmd_id = (self.root.register(self.validate_id_input), '%P')
        
        self.auth_id_entry = tk.Entry(auth_frame, font=('Arial', 18), width=10, 
                                     justify='center', bd=1, relief=tk.SUNKEN,
                                     validate='key', validatecommand=vcmd_id)
        self.auth_id_entry.pack(pady=5)
        
        tk.Label(auth_frame, text="Например: 67", font=('Arial', 14, 'bold'), 
                bg='white', fg="#000000").pack(pady=10)
        
        tk.Button(auth_frame, text="АВТОРИЗАЦИЯ", command=self.check_auth,
                 font=('Arial', 14, 'bold'), bg='#00A36C', fg='white',
                 width=15, height=1, bd=0, cursor='hand2', relief=tk.FLAT).pack(pady=20)
        
        # Кнопка назад
        tk.Button(self.root, text="← Назад", command=self.show_start_window,
                 bg='#e74c3c', fg='white', font=('Arial', 11, 'bold'),
                 width=10, bd=0, cursor='hand2', relief=tk.FLAT).pack(pady=20)
    
    def check_auth(self):
        """Проверка авторизации"""
        operator_id = self.auth_id_entry.get().strip()
        
        if not operator_id:
            messagebox.showerror("Ошибка", "Введите ID оператора")
            return
        
        # ID должен быть числом (уже проверено валидацией, но на всякий случай)
        if not operator_id.isdigit():
            messagebox.showerror("Ошибка", "ID должен содержать только цифры")
            return
        
        if os.path.exists('operation_db.csv'):
            with open('operation_db.csv', 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    if row['id'] == operator_id:
                        self.operator_data = {
                            'id': row['id'],
                            'last_name': row['last_name'],
                            'first_name': row['first_name'],
                            'middle_name': row['middle_name'],
                            'age': row['age']
                        }
                        self.current_operator_id = int(operator_id)
                        
                        # ПОСЛЕ АВТОРИЗАЦИИ - показываем три колонки с данными
                        self.show_authorized_view()
                        return
            
            messagebox.showerror("Ошибка", f"Оператор с ID {operator_id} не найден")
    
    def show_authorized_view(self):
        """Показывает три колонки после авторизации"""
        for widget in self.root.winfo_children():
            widget.destroy()
        
        # Добавляем заголовок
        self.add_header(self.root)
        
        # Основной контейнер для трех колонок
        main_frame = tk.Frame(self.root, bg='#f0f0f0')
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        # === КОЛОНКА 1: ИНФОРМАЦИЯ ОПЕРАТОРА (СИНЯЯ) ===
        col1 = tk.Frame(main_frame, bg='white', bd=1, relief=tk.SOLID)
        col1.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5)
        
        tk.Label(col1, text="Информация оператора", 
                font=('Arial', 14, 'bold'), bg='#005BBB', fg='white',
                height=2).pack(fill=tk.X)
        
        content1 = tk.Frame(col1, bg='white', padx=20, pady=20)
        content1.pack(fill=tk.BOTH, expand=True)
        
        # Данные оператора в первой колонке
        info_text = f"Фамилия: {self.operator_data['last_name']}\n" \
                   f"Имя: {self.operator_data['first_name']}\n" \
                   f"Отчество: {self.operator_data['middle_name']}\n" \
                   f"Возраст: {self.operator_data['age']}"
        
        tk.Label(content1, text=info_text, 
                font=('Arial', 12), bg='white', fg='#2c3e50', justify='left').pack(anchor='w')
        
        # === КОЛОНКА 2: ИДЕНТИФИКАЦИЯ (ОРАНЖЕВАЯ) ===
        col2 = tk.Frame(main_frame, bg='white', bd=1, relief=tk.SOLID)
        col2.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5)
        
        tk.Label(col2, text="Идентификация", 
                font=('Arial', 14, 'bold'), bg='#FF6B00', fg='white',
                height=2).pack(fill=tk.X)
        
        content2 = tk.Frame(col2, bg='white', padx=20, pady=20)
        content2.pack(fill=tk.BOTH, expand=True)
        
        # ID
        tk.Label(content2, text=f"ID {self.operator_data['id']}", 
                font=('Arial', 16, 'bold'), bg='white', fg='#FF6B00').pack(pady=10)
        
        # Кнопка загрузки фото
        tk.Button(content2, text="Загрузить фото", command=self.upload_photo,
                 bg='#005BBB', fg='white', font=('Arial', 10),
                 width=15, bd=0, cursor='hand2', relief=tk.FLAT).pack(pady=5)
        
        # Рамка для фото
        photo_frame = tk.Frame(content2, bg='#ecf0f1', bd=1, relief=tk.SUNKEN,
                              width=200, height=150)
        photo_frame.pack(pady=10)
        photo_frame.pack_propagate(False)
        
        # Создаем photo_label для отображения фото
        self.photo_label = tk.Label(photo_frame, bg='#ecf0f1')
        self.photo_label.pack(expand=True, fill=tk.BOTH)
        
        # Проверяем, есть ли уже фото
        photo_path = f"operations/ID_{self.operator_data['id']}.jpg"
        if os.path.exists(photo_path):
            try:
                img = Image.open(photo_path)
                img.thumbnail((180, 130))
                photo = ImageTk.PhotoImage(img)
                self.photo_label.config(image=photo)
                self.photo_label.image = photo
            except:
                tk.Label(photo_frame, text="Фото отсутствует", 
                        font=('Arial', 10), bg='#ecf0f1', fg='#7f8c8d').pack(expand=True)
        else:
            tk.Label(photo_frame, text="Фото отсутствует", 
                    font=('Arial', 10), bg='#ecf0f1', fg='#7f8c8d').pack(expand=True)
        
        # === КОЛОНКА 3: ИНФОРМАЦИОННЫЙ БЛОК (ЗЕЛЕНАЯ) ===
        col3 = tk.Frame(main_frame, bg='white', bd=1, relief=tk.SOLID)
        col3.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5)
        
        tk.Label(col3, text="Информационный блок", 
                font=('Arial', 14, 'bold'), bg='#00A36C', fg='white',
                height=2).pack(fill=tk.X)
        
        self.content3 = tk.Frame(col3, bg='white', padx=20, pady=20)
        self.content3.pack(fill=tk.BOTH, expand=True)
        
        # Информация в третьей колонке
        now = datetime.now()
        info_text3 = f"{self.operator_data['last_name']} {self.operator_data['first_name']} {self.operator_data['middle_name']}\n" \
                    f"{self.operator_data['age']} лет\n\n" \
                    f"Дата/время: {now.strftime('%d.%m.%Y')} / {now.strftime('%H:%M:%S')}\n" \
                    f"Время запуска ПО: {now.strftime('%H:%M:%S')}\n" \
                    f"Время в дороге: 00:00:00\n" \
                    f"Оставшееся время: 09:00:00"
        
        tk.Label(self.content3, text=info_text3, 
                font=('Arial', 11), bg='white', fg='#2c3e50', justify='left').pack(anchor='w', pady=5)
        
        # Разделитель
        tk.Frame(self.content3, bg='#bdc3c7', height=1).pack(fill=tk.X, pady=10)
        
        # Статус
        tk.Label(self.content3, text="Оператор определен", 
                font=('Arial', 12, 'bold'), bg='white', fg='#00A36C').pack(anchor='w', pady=2)
        
        tk.Label(self.content3, text=f"ID {self.operator_data['id']}", 
                font=('Arial', 12, 'bold'), bg='white', fg='#2c3e50').pack(anchor='w', pady=2)
        
        tk.Label(self.content3, text="Для запуска программы нажмите \"Далее\"", 
                font=('Arial', 10), bg='white', fg='#34495e').pack(anchor='w', pady=(10, 15))
        
        # Кнопка Далее
        tk.Button(self.content3, text="Далее →", command=self.next_step,
                 bg='#005BBB', fg='white', font=('Arial', 10, 'bold'),
                 width=12, bd=0, cursor='hand2', relief=tk.FLAT).pack(anchor='w')
        
        # Кнопка назад
        tk.Button(self.root, text="← Назад", command=self.show_start_window,
                 bg='#e74c3c', fg='white', font=('Arial', 11, 'bold'),
                 width=10, bd=0, cursor='hand2', relief=tk.FLAT).pack(pady=10)
    
    def show_authorized_view_with_photo(self, img):
        """Показывает три колонки после авторизации с загруженным фото"""
        self.show_authorized_view()
        
        # Обновляем фото
        if hasattr(self, 'photo_label') and self.photo_label:
            img.thumbnail((180, 130))
            photo = ImageTk.PhotoImage(img)
            self.photo_label.config(image=photo)
            self.photo_label.image = photo

if __name__ == "__main__":
    root = tk.Tk()
    app = OperatorApp(root)
    root.mainloop()