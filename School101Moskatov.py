import tkinter as tk
from tkinter import ttk, messagebox
import pyodbc
import random
from PIL import Image, ImageTk
import customtkinter as ctk
import os
from pathlib import Path
from datetime import datetime

# =====================================================
# КОНФИГУРАЦИЯ ДЛЯ ШКОЛЫ №101
# =====================================================
SCHOOL_INFO = {
    'full_name': 'ГОСУДАРСТВЕННОЕ БЮДЖЕТНОЕ ОБЩЕОБРАЗОВАТЕЛЬНОЕ УЧРЕЖДЕНИЕ "ОСНОВНАЯ ШКОЛА №101 ГОРОДСКОГО ОКРУГА МАКЕЕВКА" ДОНЕЦКОЙ НАРОДНОЙ РЕСПУБЛИКИ',
    'short_name': 'Школа №101 г. Макеевка',
    'address': '286111, Донецкая Народная Республика, Макеевка г.о., пгт. Свердлово, ул. Горького, д. 1/1',
    'postal_address': '286111, Донецкая Народная Республика, Макеевка г.о., пгт. Свердлово, ул. Горького, д. 1/1',
    'email': 'mak_school_101@mail.ru',
    'phone': '+7(949) 5587101',
    'mobile': '+7(949) 5587101',
    'inn': '9311021296',
    'kpp': '931101001',
    'ogrn': '1222905001000000052',
    'okved': '85.13',
    'treasury_account': '40102810745370000095',
    'treasury_subaccount': '03234643217190008200',
    'bank': 'ОКЦ №5 ЮГУ Банка России//УФК по Донецкой Народной Республике, г. Донецк',
    'bic': '042157901',
    'personal_account': '21826LZ7280',
    'director': 'Павлова А.В.'
}

# Конфигурация базы данных для SQL Server
DB_CONFIG = {
    'driver': '{ODBC Driver 17 for SQL Server}',
    'server': '(localdb)\\MSSQLLocalDB',
    'database': 'school_101_db',
    'trusted_connection': 'yes'
}

# Настройка темы
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("green")

# ЦВЕТОВАЯ ПАЛИТРА
COLORS = {
    'primary': '#2ecc71',
    'secondary': '#27ae60',
    'accent': '#e67e22',
    'success': '#3498db',
    'warning': '#f39c12',
    'error': '#e74c3c',
    'info': '#1abc9c',
    'light': '#ecf0f1',
    'dark': '#2c3e50',
    'gray': '#7f8c8d',
    'card_bg': '#34495e',
    'sidebar': '#2c3e50',
    'hover': '#3d566e',
    'border': '#e67e22',
    'text_light': '#ecf0f1',
    'text_dark': '#2c3e50',
    'gradient_start': '#2c3e50',
    'gradient_end': '#3498db'
}

# Стили для виджетов
FONTS = {
    'title': ("Segoe UI", 24, "bold"),
    'subtitle': ("Segoe UI", 16, "bold"),
    'heading': ("Segoe UI", 13, "bold"),
    'body': ("Segoe UI", 11),
    'small': ("Segoe UI", 9),
    'button': ("Segoe UI", 11, "bold")
}

class CenterWindowMixin:
    """Миксин для центрирования окон"""
    def center_window(self, width, height):
        """Центрирует окно на экране"""
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        x = (screen_width - width) // 2
        y = (screen_height - height) // 2
        self.geometry(f'{width}x{height}+{x}+{y}')

class Database:
    @staticmethod
    def get_connection():
        try:
            conn_str = (
                f"DRIVER={DB_CONFIG['driver']};"
                f"SERVER={DB_CONFIG['server']};"
                f"DATABASE={DB_CONFIG['database']};"
                f"Trusted_Connection={DB_CONFIG['trusted_connection']};"
            )
            connection = pyodbc.connect(conn_str)
            return connection
        except pyodbc.Error as e:
            messagebox.showerror("Ошибка подключения", 
                f"Не удалось подключиться к базе данных школы №101.\nОшибка: {str(e)}\n\n"
                f"Убедитесь, что:\n"
                f"1. SQL Server LocalDB установлен\n"
                f"2. База данных school_101_db создана\n"
                f"3. Драйвер ODBC установлен")
            return None
    
    @staticmethod
    def dict_fetchall(cursor):
        """Преобразует результат запроса в список словарей"""
        columns = [column[0] for column in cursor.description]
        return [dict(zip(columns, row)) for row in cursor.fetchall()]
    
    @staticmethod
    def dict_fetchone(cursor):
        """Преобразует одну строку результата в словарь"""
        columns = [column[0] for column in cursor.description]
        row = cursor.fetchone()
        if row:
            return dict(zip(columns, row))
        return None

class ModernButton(ctk.CTkButton):
    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)
        self.configure(
            font=FONTS['button'],
            corner_radius=10,
            border_width=0,
            height=38,
            border_spacing=3
        )

class ModernEntry(ctk.CTkEntry):
    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)
        self.configure(
            font=FONTS['body'],
            corner_radius=8,
            border_width=1,
            border_color=COLORS['border'],
            height=38,
            fg_color=COLORS['card_bg']
        )

class ModernLabel(ctk.CTkLabel):
    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)
        self.configure(font=FONTS['body'])

class CardFrame(ctk.CTkFrame):
    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)
        self.configure(
            fg_color=COLORS['card_bg'],
            corner_radius=15,
            border_width=1,
            border_color=COLORS['border']
        )

class SchoolInfoFrame(CardFrame):
    """Фрейм с информацией о школе для отображения в приложении"""
    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)
        self.setup_ui()
    
    def setup_ui(self):
        # Иконка школы
        icon_label = ctk.CTkLabel(
            self,
            text="🏫",
            font=("Segoe UI", 32),
            text_color=COLORS['accent']
        )
        icon_label.pack(pady=(8, 2))
        
        # Заголовок
        ctk.CTkLabel(
            self,
            text=SCHOOL_INFO['short_name'],
            font=FONTS['subtitle'],
            text_color=COLORS['accent']
        ).pack(pady=(0, 2))
        
        ctk.CTkLabel(
            self,
            text=SCHOOL_INFO['full_name'][:50] + "...",
            font=FONTS['small'],
            text_color=COLORS['gray'],
            wraplength=250
        ).pack(pady=(0, 5))
        
        # Разделитель
        separator = ctk.CTkFrame(self, height=1, fg_color=COLORS['border'])
        separator.pack(fill="x", padx=10, pady=5)
        
        # Контакты
        contacts_frame = ctk.CTkFrame(self, fg_color="transparent")
        contacts_frame.pack(fill="x", padx=10, pady=2)
        
        ctk.CTkLabel(
            contacts_frame,
            text=f"📞 {SCHOOL_INFO['phone']}",
            font=FONTS['small'],
            text_color=COLORS['text_light']
        ).pack(anchor="w", pady=1)
        
        ctk.CTkLabel(
            contacts_frame,
            text=f"✉️ {SCHOOL_INFO['email']}",
            font=FONTS['small'],
            text_color=COLORS['text_light']
        ).pack(anchor="w", pady=1)
        
        ctk.CTkLabel(
            contacts_frame,
            text=f"📍 {SCHOOL_INFO['address'][:30]}...",
            font=FONTS['small'],
            text_color=COLORS['text_light']
        ).pack(anchor="w", pady=1)

class CaptchaPuzzle:
    def __init__(self):
        self.pieces = []
        self.correct_order = []
        self.current_order = []
        self.images = []
        self.load_real_images()
        
    def load_real_images(self):
        """Загрузка РЕАЛЬНЫХ изображений пользователя"""
        # ПРОБУЕМ РАЗНЫЕ ВАРИАНТЫ СТРУКТУРЫ ПАПОК
        base_path = r"C:\Users\Eduard\Downloads\Эд"
        
        # Вариант 1: Эд\Эд1, Эд\Эд2, Эд\Эд3, Эд\Эд4
        image_paths_v1 = [
            fr"{base_path}\Эд1\1.png",
            fr"{base_path}\Эд2\2.png", 
            fr"{base_path}\Эд3\3.png",
            fr"{base_path}\Эд4\4.png"
        ]
        
        # Вариант 2: Эд\Эддд\Эд1 и т.д.
        image_paths_v2 = [
            fr"{base_path}\Эддд\Эд1\1.png",
            fr"{base_path}\Эддд\Эд2\2.png",
            fr"{base_path}\Эддд\Эд3\3.png",
            fr"{base_path}\Эддд\Эд4\4.png"
        ]
        
        # Вариант 3: файлы напрямую в папке Эд
        image_paths_v3 = [
            fr"{base_path}\1.png",
            fr"{base_path}\2.png",
            fr"{base_path}\3.png", 
            fr"{base_path}\4.png"
        ]
        
        print("=" * 60)
        print("ПОИСК ВАШИХ ИЗОБРАЖЕНИЙ")
        print("=" * 60)
        
        # Сначала проверим, что существует базовая папка
        if not os.path.exists(base_path):
            print(f"❌ Базовая папка не найдена: {base_path}")
            self.create_fallback_images()
            return
        
        print(f"✅ Базовая папка существует: {base_path}")
        
        # Покажем что есть в папке Эд
        try:
            print(f"\nСодержимое папки {base_path}:")
            for item in os.listdir(base_path):
                item_path = os.path.join(base_path, item)
                if os.path.isdir(item_path):
                    print(f"📁 {item}/")
                    # Покажем что внутри вложенных папок
                    try:
                        for subitem in os.listdir(item_path):
                            subitem_path = os.path.join(item_path, subitem)
                            if os.path.isfile(subitem_path):
                                print(f"    📄 {subitem}")
                    except:
                        pass
                else:
                    print(f"📄 {item}")
        except Exception as e:
            print(f"Ошибка при чтении папки: {e}")
        
        print("\n" + "-" * 60)
        
        # Пробуем найти изображения
        all_path_variants = [
            ("Вариант 1 (Эд1, Эд2...)", image_paths_v1),
            ("Вариант 2 (Эддд\\Эд1...)", image_paths_v2),
            ("Вариант 3 (image1.png...)", image_paths_v3)
        ]
        
        found_paths = []
        
        for variant_name, paths in all_path_variants:
            print(f"\nПробуем {variant_name}:")
            found_in_variant = 0
            
            for i, path in enumerate(paths, 1):
                if os.path.exists(path):
                    print(f"  ✅ Изображение {i}: {path}")
                    found_paths.append(path)
                    found_in_variant += 1
                else:
                    print(f"  ❌ Не найдено: {path}")
            
            if found_in_variant == 4:
                print(f"✅ Найдены ВСЕ 4 изображения!")
                break
            elif found_in_variant > 0:
                print(f"Найдено {found_in_variant}/4 изображений")
        
        print("\n" + "-" * 60)
        
        # Если нашли какие-то пути, загружаем их
        if found_paths:
            print(f"Загружаем {len(found_paths)} найденных изображений...")
            for i, path in enumerate(found_paths[:4]):  # берем максимум 4
                try:
                    img = Image.open(path)
                    
                    # Конвертируем если нужно
                    if img.mode != 'RGB':
                        img = img.convert('RGB')
                    
                    # Масштабируем
                    img = img.resize((150, 150), Image.Resampling.LANCZOS)
                    self.images.append(img)
                    print(f"✅ Загружено изображение {i+1}: {os.path.basename(path)}")
                    
                except Exception as e:
                    print(f"❌ Ошибка загрузки {path}: {e}")
                    # Добавляем черный квадрат
                    self.images.append(Image.new('RGB', (150, 150), color=(50, 50, 50)))
        else:
            print("❌ Не найдено ни одного изображения!")
            
        # Если изображений меньше 4, добавляем недостающие
        while len(self.images) < 4:
            missing_num = len(self.images) + 1
            img = Image.new('RGB', (150, 150), color=(100, 100, 100))
            
            # Добавим текст на черный квадрат
            from PIL import ImageDraw, ImageFont
            draw = ImageDraw.Draw(img)
            try:
                font = ImageFont.truetype("arial.ttf", 40)
                draw.text((40, 50), f"?", fill=(255, 255, 0), font=font)
            except:
                pass
                
            self.images.append(img)
            print(f"➕ Добавлено изображение-заглушка {missing_num}")
        
        print("=" * 60)
        print(f"ИТОГО: {len(self.images)} изображений готово к использованию")
        print("=" * 60)
    
    def create_fallback_images(self):
        """Создает изображения если ничего не найдено"""
        from PIL import ImageDraw, ImageFont
        
        print("Создаю изображения...")
        
        # Создаем 4 разных изображения
        for i in range(4):
            # Разные цвета для разных частей
            colors = [
                (255, 100, 100),  # Красный
                (100, 255, 100),  # Зеленый
                (100, 100, 255),  # Синий
                (255, 255, 100)   # Желтый
            ]
            
            img = Image.new('RGB', (150, 150), color=colors[i])
            draw = ImageDraw.Draw(img)
            
            try:
                font = ImageFont.truetype("arial.ttf", 60)
                draw.text((50, 40), f"{i+1}", fill=(0, 0, 0), font=font)
            except:
                pass
            
            self.images.append(img)
            print(f"Создано изображение {i+1}")
    
    def create_puzzle(self):
        """Создает пазл из загруженных изображений"""
        self.pieces = self.images[:4]
        self.correct_order = [0, 1, 2, 3]
        
        # Создаем перемешанный порядок
        self.current_order = self.correct_order.copy()
        
        # Перемешиваем до тех пор, пока порядок не изменится
        while self.current_order == self.correct_order:
            self.current_order = random.sample(range(4), 4)
        
        print(f"\n🧩 СОЗДАН ПАЗЛ")
        print(f"Правильный порядок: {[i+1 for i in self.correct_order]}")
        print(f"Перемешанный порядок: {[i+1 for i in self.current_order]}")
        
        return self.pieces, self.current_order
    
    def check_solution(self, user_order):
        """Проверяет правильность решения"""
        is_correct = user_order == self.correct_order
        
        print(f"\n🔍 ПРОВЕРКА")
        print(f"Вы собрали: {[i+1 for i in user_order]}")
        print(f"Нужно было: {[i+1 for i in self.correct_order]}")
        print(f"Результат: {'✅ ВЕРНО' if is_correct else '❌ НЕВЕРНО'}")
        
        return is_correct

class LoginWindow(ctk.CTk, CenterWindowMixin):
    def __init__(self):
        super().__init__()
        self.title(f"🎓 {SCHOOL_INFO['short_name']} - Система управления")
        
        # Устанавливаем правильные размеры для окна входа
        window_width = 1000
        window_height = 600
        
        self.geometry(f"{window_width}x{window_height}")
        self.resizable(False, False)
        self.center_window(window_width, window_height)
        
        self.captcha = CaptchaPuzzle()
        self.failed_attempts = 0
        self.current_user = None
        self.selected_piece = None
        self.puzzle_buttons = []
        self.piece_images = []
        
        self.setup_ui()
        
    def setup_ui(self):
        # Основной контейнер
        main_container = ctk.CTkFrame(self, fg_color=COLORS['dark'])
        main_container.pack(fill="both", expand=True)
        
        # Левая панель (информация о школе) - фиксированная ширина
        left_panel = ctk.CTkFrame(
            main_container, 
            width=380,
            fg_color=COLORS['gradient_start']
        )
        left_panel.pack(side="left", fill="y")
        left_panel.pack_propagate(False)
        
        # Контент левой панели с прокруткой
        left_canvas = tk.Canvas(left_panel, bg=COLORS['gradient_start'], highlightthickness=0)
        left_scrollbar = ctk.CTkScrollbar(left_panel, orientation="vertical", command=left_canvas.yview)
        left_scrollable = ctk.CTkFrame(left_canvas, fg_color="transparent")
        
        left_scrollable.bind(
            "<Configure>",
            lambda e: left_canvas.configure(scrollregion=left_canvas.bbox("all"))
        )
        
        left_canvas.create_window((0, 0), window=left_scrollable, anchor="nw", width=360)
        left_canvas.configure(yscrollcommand=left_scrollbar.set)
        
        left_canvas.pack(side="left", fill="both", expand=True)
        left_scrollbar.pack(side="right", fill="y")
        
        # Логотип
        logo_frame = CardFrame(left_scrollable, fg_color=COLORS['accent'])
        logo_frame.pack(pady=(20, 10), ipadx=10, ipady=10)
        
        logo_label = ctk.CTkLabel(
            logo_frame, 
            text="🏫", 
            font=("Segoe UI", 60),
            text_color="white"
        )
        logo_label.pack()
        
        # Название школы
        ctk.CTkLabel(
            left_scrollable, 
            text="Школа №101", 
            font=("Segoe UI", 28, "bold"),
            text_color=COLORS['accent']
        ).pack(pady=(0, 2))
        
        ctk.CTkLabel(
            left_scrollable, 
            text="г. Макеевка, пгт. Свердлово", 
            font=FONTS['subtitle'],
            text_color=COLORS['text_light']
        ).pack(pady=(0, 10))
        
        # Информация о школе
        info_frame = SchoolInfoFrame(left_scrollable)
        info_frame.pack(fill="x", padx=15, pady=5)
        
        # Правая панель с формой входа
        right_panel = ctk.CTkFrame(
            main_container, 
            width=620,
            fg_color=COLORS['card_bg']
        )
        right_panel.pack(side="right", fill="both", expand=True)
        right_panel.pack_propagate(False)
        
        # Контент правой панели с прокруткой
        right_canvas = tk.Canvas(right_panel, bg=COLORS['card_bg'], highlightthickness=0)
        right_scrollbar = ctk.CTkScrollbar(right_panel, orientation="vertical", command=right_canvas.yview)
        right_scrollable = ctk.CTkFrame(right_canvas, fg_color="transparent")
        
        right_scrollable.bind(
            "<Configure>",
            lambda e: right_canvas.configure(scrollregion=right_canvas.bbox("all"))
        )
        
        right_canvas.create_window((0, 0), window=right_scrollable, anchor="nw", width=600)
        right_canvas.configure(yscrollcommand=right_scrollbar.set)
        
        right_canvas.pack(side="left", fill="both", expand=True)
        right_scrollbar.pack(side="right", fill="y")
        
        # Заголовок формы
        ctk.CTkLabel(
            right_scrollable, 
            text="Добро пожаловать!", 
            font=("Segoe UI", 28, "bold"),
            text_color=COLORS['accent']
        ).pack(pady=(20, 5))
        
        ctk.CTkLabel(
            right_scrollable, 
            text="Войдите в систему", 
            font=FONTS['subtitle'],
            text_color=COLORS['gray']
        ).pack(pady=(0, 20))
        
        # Поля ввода
        form_frame = ctk.CTkFrame(right_scrollable, fg_color="transparent")
        form_frame.pack(fill="x", padx=40, pady=5)
        
        # Логин
        ctk.CTkLabel(
            form_frame, 
            text="Логин", 
            font=FONTS['heading'],
            text_color=COLORS['text_light']
        ).pack(anchor="w", pady=(5, 2))
        
        self.username_entry = ModernEntry(
            form_frame, 
            placeholder_text="Введите ваш логин"
        )
        self.username_entry.pack(fill="x", pady=(0, 10))
        
        # Пароль
        ctk.CTkLabel(
            form_frame, 
            text="Пароль", 
            font=FONTS['heading'],
            text_color=COLORS['text_light']
        ).pack(anchor="w", pady=(5, 2))
        
        self.password_entry = ModernEntry(
            form_frame, 
            placeholder_text="Введите ваш пароль", 
            show="•"
        )
        self.password_entry.pack(fill="x", pady=(0, 15))
        
        # Капча
        ctk.CTkLabel(
            form_frame, 
            text="Соберите пазл для подтверждения", 
            font=FONTS['heading'],
            text_color=COLORS['text_light']
        ).pack(pady=(5, 5))
        
        self.puzzle_frame = CardFrame(form_frame, height=180)
        self.puzzle_frame.pack(fill="x", pady=5)
        self.puzzle_frame.pack_propagate(False)
        
        self.generate_new_captcha()
        
        # Кнопки
        button_row = ctk.CTkFrame(form_frame, fg_color="transparent")
        button_row.pack(fill="x", pady=10)
        
        ModernButton(
            button_row, 
            text="🔄 Перемешать", 
            command=self.shuffle_puzzle,
            fg_color=COLORS['accent'],
            hover_color=COLORS['secondary'],
            width=130
        ).pack(side="left", padx=(0, 5))
        
        ModernButton(
            button_row, 
            text="📝 Регистрация", 
            command=self.open_registration,
            fg_color=COLORS['gray'],
            hover_color=COLORS['hover'],
            width=130
        ).pack(side="left")
        
        # Кнопка входа
        self.login_btn = ModernButton(
            form_frame,
            text="🚪 Войти в систему",
            command=self.login,
            fg_color=COLORS['primary'],
            hover_color=COLORS['secondary'],
            height=45
        )
        self.login_btn.pack(fill="x", pady=(10, 15))
        
        # Нижняя информация
        bottom_frame = ctk.CTkFrame(form_frame, fg_color="transparent")
        bottom_frame.pack(fill="x", pady=(5, 15))
        
        ctk.CTkLabel(
            bottom_frame,
            text="🔒 Безопасный вход | v2.0",
            font=FONTS['small'],
            text_color=COLORS['gray']
        ).pack(side="left")
        
        ctk.CTkLabel(
            bottom_frame,
            text=f"© 2026 {SCHOOL_INFO['short_name']}",
            font=FONTS['small'],
            text_color=COLORS['gray']
        ).pack(side="right")
    
    def generate_new_captcha(self):
        for widget in self.puzzle_frame.winfo_children():
            widget.destroy()
        
        pieces, order = self.captcha.create_puzzle()
        self.puzzle_buttons = []
        self.piece_images = []
        self.selected_piece = None
        
        # Сетка для пазла
        grid_frame = ctk.CTkFrame(self.puzzle_frame, fg_color="transparent")
        grid_frame.pack(expand=True)
        
        for i, piece_idx in enumerate(order):
            piece = pieces[piece_idx]
            piece_img = ctk.CTkImage(light_image=piece, dark_image=piece, size=(70, 70))
            self.piece_images.append(piece_img)
            
            piece_btn = ctk.CTkButton(
                grid_frame,
                image=piece_img,
                text="",
                width=80,
                height=80,
                command=lambda idx=i: self.select_piece(idx),
                fg_color="transparent",
                border_width=2,
                border_color=COLORS['border'],
                corner_radius=8,
                hover_color=COLORS['hover']
            )
            row = i // 2
            col = i % 2
            piece_btn.grid(row=row, column=col, padx=3, pady=3)
            self.puzzle_buttons.append(piece_btn)
    
    def select_piece(self, idx):
        if self.selected_piece is None:
            self.selected_piece = idx
            self.puzzle_buttons[idx].configure(border_color=COLORS['primary'])
        else:
            if idx != self.selected_piece:
                self.captcha.current_order[self.selected_piece], self.captcha.current_order[idx] = \
                    self.captcha.current_order[idx], self.captcha.current_order[self.selected_piece]
                self.update_puzzle_display()
                self.puzzle_buttons[self.selected_piece].configure(border_color=COLORS['border'])
                self.selected_piece = None
            else:
                self.puzzle_buttons[idx].configure(border_color=COLORS['border'])
                self.selected_piece = None
    
    def shuffle_puzzle(self):
        if self.selected_piece is not None:
            self.puzzle_buttons[self.selected_piece].configure(border_color=COLORS['border'])
            self.selected_piece = None
        
        random.shuffle(self.captcha.current_order)
        self.update_puzzle_display()
    
    def update_puzzle_display(self):
        for i, piece_idx in enumerate(self.captcha.current_order):
            piece = self.captcha.pieces[piece_idx]
            piece_img = ctk.CTkImage(light_image=piece, dark_image=piece, size=(70, 70))
            self.puzzle_buttons[i].configure(image=piece_img)
    
    def login(self):
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()
        
        if not username or not password:
            messagebox.showwarning("Ошибка", "Заполните все поля")
            return
        
        if not self.captcha.check_solution(self.captcha.current_order):
            self.failed_attempts += 1
            messagebox.showerror("Ошибка", "Пазл собран неправильно!")
            self.generate_new_captcha()
            
            if self.failed_attempts >= 3:
                messagebox.showerror("Блокировка", "Слишком много попыток")
                return
            return
        
        connection = Database.get_connection()
        if connection is None:
            return
            
        try:
            cursor = connection.cursor()
            cursor.execute(
                "SELECT * FROM users WHERE username = ?",
                (username,)
            )
            user = Database.dict_fetchone(cursor)
            
            if user:
                if user['is_blocked']:
                    messagebox.showerror("Блокировка", "Аккаунт заблокирован")
                    return
                
                if password == user['password']:
                    cursor.execute(
                        "UPDATE users SET failed_attempts = 0 WHERE user_id = ?",
                        (user['user_id'],)
                    )
                    connection.commit()
                    
                    self.current_user = user
                    self.open_main_app()
                else:
                    self.handle_failed_attempt(user, connection)
            else:
                messagebox.showerror("Ошибка", "Неверный логин или пароль")
                
        except Exception as e:
            messagebox.showerror("Ошибка", f"Ошибка: {str(e)}")
        finally:
            connection.close()
    
    def handle_failed_attempt(self, user, connection):
        try:
            cursor = connection.cursor()
            new_attempts = user['failed_attempts'] + 1
            cursor.execute(
                "UPDATE users SET failed_attempts = ? WHERE user_id = ?",
                (new_attempts, user['user_id'])
            )
            
            if new_attempts >= 3:
                cursor.execute(
                    "UPDATE users SET is_blocked = 1 WHERE user_id = ?",
                    (user['user_id'],)
                )
                messagebox.showerror("Блокировка", "3 неудачные попытки. Аккаунт заблокирован.")
            else:
                messagebox.showerror("Ошибка", f"Неверный пароль. Осталось попыток: {3 - new_attempts}")
            
            connection.commit()
            self.generate_new_captcha()
                
        except Exception as e:
            messagebox.showerror("Ошибка", f"Ошибка базы данных: {str(e)}")
    
    def open_registration(self):
        RegistrationWindow(self)
    
    def open_main_app(self):
        self.withdraw()
        if self.current_user['role'] == 'admin':
            AdminApp(self, self.current_user)
        elif self.current_user['role'] == 'teacher':
            TeacherApp(self, self.current_user)
        else:
            StudentApp(self, self.current_user)

class RegistrationWindow(ctk.CTkToplevel, CenterWindowMixin):
    def __init__(self, parent):
        super().__init__(parent)
        self.title(f"📝 Регистрация - {SCHOOL_INFO['short_name']}")
        
        # Устанавливаем правильные размеры для окна регистрации
        window_width = 650
        window_height = 750
        
        self.geometry(f"{window_width}x{window_height}")
        self.resizable(False, False)
        self.center_window(window_width, window_height)
        self.transient(parent)
        self.grab_set()
        
        self.setup_ui()
        
    def setup_ui(self):
        # Основной фрейм с прокруткой
        main_container = ctk.CTkFrame(self, fg_color=COLORS['dark'])
        main_container.pack(fill="both", expand=True)
        
        canvas = tk.Canvas(main_container, bg=COLORS['dark'], highlightthickness=0)
        scrollbar = ctk.CTkScrollbar(main_container, orientation="vertical", command=canvas.yview)
        scrollable_frame = ctk.CTkFrame(canvas, fg_color=COLORS['dark'])
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw", width=610)
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Основной фрейм с карточкой
        main_frame = CardFrame(scrollable_frame)
        main_frame.pack(fill="both", expand=True, padx=15, pady=15)
        
        # Заголовок
        ctk.CTkLabel(
            main_frame, 
            text="📝 Регистрация в системе", 
            font=("Segoe UI", 28, "bold"),
            text_color=COLORS['accent']
        ).pack(pady=(20, 5))
        
        ctk.CTkLabel(
            main_frame, 
            text="Заполните форму для создания учетной записи", 
            font=FONTS['body'],
            text_color=COLORS['gray']
        ).pack(pady=(0, 15))
        
        # Поля формы
        form_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        form_frame.pack(fill="both", expand=True, padx=25, pady=5)
        
        # Роль
        ctk.CTkLabel(
            form_frame, 
            text="Выберите роль", 
            font=FONTS['heading'],
            text_color=COLORS['text_light']
        ).pack(anchor="w", pady=(5, 2))
        
        role_frame = CardFrame(form_frame)
        role_frame.pack(fill="x", pady=(0, 10))
        
        self.role_var = tk.StringVar(value="student")
        
        roles_frame = ctk.CTkFrame(role_frame, fg_color="transparent")
        roles_frame.pack(pady=8)
        
        ctk.CTkRadioButton(
            roles_frame, 
            text="🎒 Ученик", 
            variable=self.role_var, 
            value="student",
            font=FONTS['body'],
            fg_color=COLORS['primary']
        ).pack(side="left", padx=15)
        
        ctk.CTkRadioButton(
            roles_frame, 
            text="👨‍🏫 Учитель", 
            variable=self.role_var, 
            value="teacher",
            font=FONTS['body'],
            fg_color=COLORS['primary']
        ).pack(side="left", padx=15)
        
        # ФИО
        ctk.CTkLabel(
            form_frame, 
            text="ФИО", 
            font=FONTS['heading'],
            text_color=COLORS['text_light']
        ).pack(anchor="w", pady=(5, 2))
        self.fullname_entry = ModernEntry(form_frame, placeholder_text="Иванов Иван Иванович")
        self.fullname_entry.pack(fill="x", pady=(0, 8))
        
        # Логин и пароль
        credentials_frame = ctk.CTkFrame(form_frame, fg_color="transparent")
        credentials_frame.pack(fill="x", pady=(0, 8))
        
        # Логин
        login_frame = ctk.CTkFrame(credentials_frame, fg_color="transparent")
        login_frame.pack(side="left", fill="both", expand=True, padx=(0, 5))
        
        ctk.CTkLabel(
            login_frame, 
            text="Логин", 
            font=FONTS['heading'],
            text_color=COLORS['text_light']
        ).pack(anchor="w")
        self.username_entry = ModernEntry(login_frame, placeholder_text="Придумайте логин")
        self.username_entry.pack(fill="x", pady=(2, 0))
        
        # Пароль
        password_frame = ctk.CTkFrame(credentials_frame, fg_color="transparent")
        password_frame.pack(side="right", fill="both", expand=True, padx=(5, 0))
        
        ctk.CTkLabel(
            password_frame, 
            text="Пароль", 
            font=FONTS['heading'],
            text_color=COLORS['text_light']
        ).pack(anchor="w")
        self.password_entry = ModernEntry(password_frame, placeholder_text="Придумайте пароль", show="•")
        self.password_entry.pack(fill="x", pady=(2, 0))
        
        # Подтверждение пароля и телефон
        second_row = ctk.CTkFrame(form_frame, fg_color="transparent")
        second_row.pack(fill="x", pady=(0, 8))
        
        # Подтверждение пароля
        confirm_frame = ctk.CTkFrame(second_row, fg_color="transparent")
        confirm_frame.pack(side="left", fill="both", expand=True, padx=(0, 5))
        
        ctk.CTkLabel(
            confirm_frame, 
            text="Подтвердите пароль", 
            font=FONTS['heading'],
            text_color=COLORS['text_light']
        ).pack(anchor="w")
        self.confirm_password_entry = ModernEntry(confirm_frame, placeholder_text="Повторите пароль", show="•")
        self.confirm_password_entry.pack(fill="x", pady=(2, 0))
        
        # Телефон
        phone_frame = ctk.CTkFrame(second_row, fg_color="transparent")
        phone_frame.pack(side="right", fill="both", expand=True, padx=(5, 0))
        
        ctk.CTkLabel(
            phone_frame, 
            text="Телефон", 
            font=FONTS['heading'],
            text_color=COLORS['text_light']
        ).pack(anchor="w")
        self.phone_entry = ModernEntry(phone_frame, placeholder_text="+7 (___) ___-__-__")
        self.phone_entry.pack(fill="x", pady=(2, 0))
        
        # Устанавливаем начальное значение с маской
        self.phone_entry.insert(0, "+7 (___) ___-__-__")
        
        # Привязываем обработчики для форматирования
        self.phone_entry.bind('<KeyRelease>', self.format_phone)
        self.phone_entry.bind('<FocusIn>', self.on_phone_focus_in)
        self.phone_entry.bind('<FocusOut>', self.on_phone_focus_out)
        
        # Email
        ctk.CTkLabel(
            form_frame, 
            text="Email", 
            font=FONTS['heading'],
            text_color=COLORS['text_light']
        ).pack(anchor="w", pady=(5, 2))
        self.email_entry = ModernEntry(form_frame, placeholder_text="example@email.com")
        self.email_entry.pack(fill="x", pady=(0, 15))
        
        # Кнопки
        button_frame = ctk.CTkFrame(form_frame, fg_color="transparent")
        button_frame.pack(fill="x", pady=10)
        
        ModernButton(
            button_frame,
            text="✅ Зарегистрироваться",
            command=self.register,
            fg_color=COLORS['primary'],
            hover_color=COLORS['secondary'],
            width=180
        ).pack(side="left", padx=(0, 5))
        
        ModernButton(
            button_frame,
            text="❌ Отмена",
            command=self.destroy,
            fg_color=COLORS['error'],
            hover_color=COLORS['warning'],
            width=130
        ).pack(side="left")
    
    def on_phone_focus_in(self, event):
        """При фокусе на поле телефона - устанавливаем курсор на первую цифру"""
        widget = event.widget
        current_text = widget.get()
        
        # Ищем первую подчеркивание для установки курсора
        try:
            cursor_pos = current_text.index('_')
            widget.icursor(cursor_pos)
        except ValueError:
            # Если подчеркиваний нет, ставим курсор в конец цифр
            digits_only = ''.join([c for c in current_text if c.isdigit()])
            if digits_only:
                # Ищем позицию после последней цифры
                for i, char in enumerate(current_text):
                    if char.isdigit():
                        last_digit_pos = i
                widget.icursor(last_digit_pos + 1)
            else:
                widget.icursor(2)  # после "+7"
    
    def on_phone_focus_out(self, event):
        """При потере фокуса - если номер пустой, восстанавливаем маску"""
        widget = event.widget
        current_text = widget.get()
        
        # Удаляем все нецифры кроме + и подчеркивания
        clean_text = ''.join([c for c in current_text if c in ['+', '(', ')', ' ', '-', '_'] or c.isdigit()])
        
        # Если номер пустой (только маска), восстанавливаем полную маску
        digits = ''.join([c for c in clean_text if c.isdigit()])
        if len(digits) == 0:
            widget.delete(0, tk.END)
            widget.insert(0, "+7 (___) ___-__-__")
    
    def format_phone(self, event):
        """Форматирование номера телефона по маске +7 (xxx) xxx-xx-xx"""
        widget = event.widget
        current_text = widget.get()
        
        # Сохраняем позицию курсора
        cursor_pos = widget.index(tk.INSERT)
        
        # Удаляем все нецифры кроме +, (, ), -, пробелов и подчеркиваний
        allowed_chars = ['+', '(', ')', ' ', '-', '_']
        filtered_chars = []
        for char in current_text:
            if char.isdigit() or char in allowed_chars:
                filtered_chars.append(char)
        filtered_text = ''.join(filtered_chars)
        
        # Извлекаем только цифры
        digits = ''.join([c for c in filtered_text if c.isdigit()])
        
        # Ограничиваем длину (максимум 11 цифр: 1 код страны + 10 номера)
        if len(digits) > 11:
            digits = digits[:11]
        
        # Если есть код страны, оставляем его, иначе ставим 7 по умолчанию
        if digits:
            if len(digits) >= 1:
                country_code = digits[0]
                number_digits = digits[1:]
            else:
                country_code = '7'
                number_digits = ''
        else:
            country_code = '7'
            number_digits = ''
        
        # Формируем номер по маске
        formatted = f"+{country_code}"
        
        if number_digits or '_' in current_text:
            formatted += " ("
            
            # Первые 3 цифры номера или подчеркивания
            if len(number_digits) >= 1:
                formatted += number_digits[:3]
                remaining = number_digits[3:]
            else:
                formatted += "___"
                remaining = ""
            
            formatted += ")"
            
            # Если есть еще цифры или мы редактируем
            if remaining or cursor_pos > len(formatted):
                formatted += " "
                
                # Следующие 3 цифры
                if len(remaining) >= 1:
                    formatted += remaining[:3]
                    remaining = remaining[3:]
                else:
                    formatted += "___"
                
                formatted += "-"
                
                # Следующие 2 цифры
                if len(remaining) >= 1:
                    formatted += remaining[:2]
                    remaining = remaining[2:]
                else:
                    formatted += "__"
                
                formatted += "-"
                
                # Последние 2 цифры
                if len(remaining) >= 1:
                    formatted += remaining[:2]
                else:
                    formatted += "__"
            else:
                # Дополняем оставшуюся часть маской
                formatted += " ___-__-__"
        
        # Обновляем поле ввода, если текст изменился
        if formatted != current_text:
            widget.delete(0, tk.END)
            widget.insert(0, formatted)
            
            # Восстанавливаем позицию курсора
            try:
                # Пытаемся найти ту же относительную позицию
                if cursor_pos < len(formatted):
                    # Если курсор был на цифре, стараемся поставить его на цифру
                    if cursor_pos < len(current_text) and current_text[cursor_pos-1:cursor_pos].isdigit():
                        # Ищем следующую цифру в новой строке
                        new_pos = cursor_pos
                        while new_pos < len(formatted) and not formatted[new_pos].isdigit():
                            new_pos += 1
                        if new_pos < len(formatted):
                            widget.icursor(new_pos + 1)
                        else:
                            widget.icursor(len(formatted))
                    else:
                        widget.icursor(cursor_pos)
                else:
                    widget.icursor(len(formatted))
            except:
                widget.icursor(len(formatted))
    
    def register(self):
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()
        confirm_password = self.confirm_password_entry.get().strip()
        fullname = self.fullname_entry.get().strip()
        
        # Получаем телефон в формате маски и очищаем его
        phone_text = self.phone_entry.get().strip()
        
        # Если телефон - это просто маска (без цифр), устанавливаем пустое значение
        if phone_text == "+7 (___) ___-__-__":
            phone = ""
        else:
            # Извлекаем только цифры из телефона
            phone_digits = ''.join(filter(str.isdigit, phone_text))
            
            # Если введен только код страны (7), тоже считаем пустым
            if len(phone_digits) <= 1:
                phone = ""
            else:
                phone = phone_digits
        
        email = self.email_entry.get().strip()
        role = self.role_var.get()
        
        if not username or not password or not fullname:
            messagebox.showwarning("Ошибка", "Заполните обязательные поля")
            return
        
        if password != confirm_password:
            messagebox.showwarning("Ошибка", "Пароли не совпадают")
            return
        
        # Валидация телефона (если введен)
        if phone:
            if len(phone) < 10:
                messagebox.showwarning("Ошибка", "Номер телефона должен содержать 10 цифр (без кода страны)")
                return
            if len(phone) > 15:
                messagebox.showwarning("Ошибка", "Слишком длинный номер телефона")
                return
        
        connection = Database.get_connection()
        if connection is None:
            return
            
        try:
            cursor = connection.cursor()
            cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
            if Database.dict_fetchone(cursor):
                messagebox.showwarning("Ошибка", "Логин уже занят")
                return
            
            cursor.execute("""
                INSERT INTO users (username, password, full_name, phone, email, role)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (username, password, fullname, phone or None, email or None, role))
            
            connection.commit()
            messagebox.showinfo("Успех", "✅ Регистрация успешна! ✅")
            self.destroy()
                
        except Exception as e:
            messagebox.showerror("Ошибка", f"Ошибка регистрации: {str(e)}")
        finally:
            connection.close()

# НОВЫЙ СТИЛЬ для Treeview
def configure_treeview_style():
    style = ttk.Style()
    style.theme_use('clam')
    
    # Общий стиль для Treeview
    style.configure("Treeview",
        background=COLORS['card_bg'],
        foreground=COLORS['text_light'],
        fieldbackground=COLORS['card_bg'],
        borderwidth=0,
        font=FONTS['body'],
        rowheight=28
    )
    
    style.configure("Treeview.Heading",
        background=COLORS['accent'],
        foreground="white",
        font=FONTS['heading'],
        borderwidth=0,
        relief="flat"
    )
    
    style.map("Treeview.Heading",
        background=[('active', COLORS['secondary'])],
        foreground=[('active', 'white')]
    )
    
    style.map("Treeview",
        background=[('selected', COLORS['primary'])],
        foreground=[('selected', 'white')]
    )

class MainApp(ctk.CTkToplevel, CenterWindowMixin):
    def __init__(self, parent, user):
        super().__init__(parent)
        self.user = user
        self.protocol("WM_DELETE_WINDOW", self.on_closing)
        
    def on_closing(self):
        self.master.deiconify()
        self.destroy()

class StudentApp(MainApp):
    def __init__(self, parent, user):
        super().__init__(parent, user)
        self.title(f"🎒 {SCHOOL_INFO['short_name']} - Ученик: {user['full_name']}")
        
        # Устанавливаем правильные размеры для окна ученика
        window_width = 1300
        window_height = 750
        
        self.geometry(f"{window_width}x{window_height}")
        self.center_window(window_width, window_height)
        
        # Настройка стилей
        configure_treeview_style()
        
        self.setup_ui()
        
    def setup_ui(self):
        # Боковая панель - фиксированная ширина
        sidebar = ctk.CTkFrame(self, width=260, fg_color=COLORS['sidebar'], corner_radius=0)
        sidebar.pack(side="left", fill="y")
        sidebar.pack_propagate(False)
        
        # Боковая панель с прокруткой
        sidebar_canvas = tk.Canvas(sidebar, bg=COLORS['sidebar'], highlightthickness=0)
        sidebar_scrollbar = ctk.CTkScrollbar(sidebar, orientation="vertical", command=sidebar_canvas.yview)
        sidebar_scrollable = ctk.CTkFrame(sidebar_canvas, fg_color="transparent")
        
        sidebar_scrollable.bind(
            "<Configure>",
            lambda e: sidebar_canvas.configure(scrollregion=sidebar_canvas.bbox("all"))
        )
        
        sidebar_canvas.create_window((0, 0), window=sidebar_scrollable, anchor="nw", width=240)
        sidebar_canvas.configure(yscrollcommand=sidebar_scrollbar.set)
        
        sidebar_canvas.pack(side="left", fill="both", expand=True)
        sidebar_scrollbar.pack(side="right", fill="y")
        
        # Верхняя часть боковой панели
        header_frame = ctk.CTkFrame(sidebar_scrollable, height=120, fg_color=COLORS['accent'], corner_radius=0)
        header_frame.pack(fill="x")
        header_frame.pack_propagate(False)
        
        ctk.CTkLabel(
            header_frame,
            text="🎒",
            font=("Segoe UI", 40),
            text_color="white"
        ).pack(pady=(15, 2))
        
        ctk.CTkLabel(
            header_frame,
            text="Ученик",
            font=FONTS['subtitle'],
            text_color="white"
        ).pack()
        
        # Информация о пользователе
        user_info_frame = CardFrame(sidebar_scrollable)
        user_info_frame.pack(fill="x", padx=10, pady=10)
        
        ctk.CTkLabel(
            user_info_frame,
            text=self.user['full_name'],
            font=FONTS['heading'],
            text_color=COLORS['text_light'],
            wraplength=220
        ).pack(pady=8)
        
        # Информация о школе
        school_info = SchoolInfoFrame(sidebar_scrollable)
        school_info.pack(fill="x", padx=10, pady=5)
        
        # Меню
        menu_frame = CardFrame(sidebar_scrollable)
        menu_frame.pack(fill="x", padx=10, pady=5)
        
        ctk.CTkLabel(
            menu_frame,
            text="📋 Меню",
            font=FONTS['heading'],
            text_color=COLORS['accent']
        ).pack(pady=5)
        
        menu_items = [
            ("📅 Расписание", "Расписание"),
            ("📊 Оценки", "Оценки"),
            ("📚 Домашние задания", "Домашние задания"),
            ("👥 Посещаемость", "Посещаемость")
        ]
        
        for icon_text, tab_name in menu_items:
            btn = ModernButton(
                menu_frame,
                text=icon_text,
                command=lambda tn=tab_name: self.tabview.set(tn),
                fg_color="transparent",
                hover_color=COLORS['hover'],
                anchor="w",
                height=35
            )
            btn.pack(fill="x", padx=5, pady=1)
        
        # Статистика
        stats_frame = CardFrame(sidebar_scrollable)
        stats_frame.pack(fill="x", padx=10, pady=5)
        
        ctk.CTkLabel(
            stats_frame,
            text="📈 Статистика",
            font=FONTS['heading'],
            text_color=COLORS['accent']
        ).pack(pady=5)
        
        self.stats_label = ctk.CTkLabel(
            stats_frame,
            text="Загрузка...",
            font=FONTS['small'],
            text_color=COLORS['gray']
        )
        self.stats_label.pack(pady=(0, 8))
        
        # Кнопка выхода
        ModernButton(
            sidebar_scrollable,
            text="🚪 Выйти",
            command=self.on_closing,
            fg_color=COLORS['error'],
            hover_color=COLORS['warning'],
            height=40
        ).pack(fill="x", padx=10, pady=10)
        
        # Основная область
        main_area = ctk.CTkFrame(self, fg_color=COLORS['dark'], corner_radius=0)
        main_area.pack(side="right", fill="both", expand=True)
        
        # Заголовок
        header_frame = CardFrame(main_area)
        header_frame.pack(fill="x", padx=15, pady=15)
        
        self.current_tab_label = ctk.CTkLabel(
            header_frame,
            text="Расписание",
            font=("Segoe UI", 20, "bold"),
            text_color=COLORS['accent']
        )
        self.current_tab_label.pack(pady=10)
        
        # Вкладки
        self.tabview = ctk.CTkTabview(main_area, fg_color=COLORS['card_bg'])
        self.tabview.pack(fill="both", expand=True, padx=15, pady=(0, 15))
        
        for tab_name in ["Расписание", "Оценки", "Домашние задания", "Посещаемость"]:
            self.tabview.add(tab_name)
            self.tabview.tab(tab_name).configure(fg_color=COLORS['card_bg'])
        
        self.tabview.configure(
            segmented_button_fg_color=COLORS['sidebar'],
            segmented_button_selected_color=COLORS['accent'],
            segmented_button_selected_hover_color=COLORS['secondary'],
            text_color=COLORS['text_light']
        )
        
        self.tabview._segmented_button.configure(font=FONTS['button'])
        
        self.setup_schedule_tab()
        self.setup_grades_tab()
        self.setup_homework_tab()
        self.setup_attendance_tab()
        
        # Связываем переключение вкладок с обновлением заголовка
        self.tabview.configure(command=self.on_tab_changed)
        
        # Загрузка данных
        self.load_schedule()
        self.load_grades()
        self.load_homework()
        self.load_attendance()
        self.load_stats()
    
    def on_tab_changed(self, tab_name):
        self.current_tab_label.configure(text=tab_name)
    
    def setup_schedule_tab(self):
        tab = self.tabview.tab("Расписание")
        
        # Контейнер с прокруткой
        container = ctk.CTkFrame(tab, fg_color="transparent")
        container.pack(fill="both", expand=True, padx=5, pady=5)
        
        # Таблица расписания
        columns = ("День недели", "Урок", "Предмет", "Учитель", "Кабинет")
        self.schedule_tree = ttk.Treeview(container, columns=columns, show="headings", style="Treeview", height=18)
        
        for col in columns:
            self.schedule_tree.heading(col, text=col)
            self.schedule_tree.column(col, width=130)
        
        scrollbar_y = ttk.Scrollbar(container, orient="vertical", command=self.schedule_tree.yview)
        scrollbar_x = ttk.Scrollbar(container, orient="horizontal", command=self.schedule_tree.xview)
        self.schedule_tree.configure(yscrollcommand=scrollbar_y.set, xscrollcommand=scrollbar_x.set)
        
        self.schedule_tree.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
        scrollbar_y.grid(row=0, column=1, sticky="ns", pady=5)
        scrollbar_x.grid(row=1, column=0, sticky="ew", padx=5)
        
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        
        # Кнопка обновить
        ModernButton(
            tab,
            text="🔄 Обновить расписание",
            command=self.load_schedule,
            fg_color=COLORS['primary'],
            hover_color=COLORS['secondary'],
            height=35
        ).pack(pady=8)
    
    def load_schedule(self):
        connection = Database.get_connection()
        if connection is None:
            return
            
        try:
            cursor = connection.cursor()
            cursor.execute("""
                SELECT s.day_of_week, s.lesson_number, 
                       sub.subject_name, u.full_name, s.room
                FROM schedule s
                JOIN subjects sub ON s.subject_id = sub.subject_id
                JOIN users u ON s.teacher_id = u.user_id
                WHERE s.class_id IN (
                    SELECT class_id FROM users WHERE user_id = ?
                )
                ORDER BY 
                    CASE s.day_of_week
                        WHEN 'Понедельник' THEN 1
                        WHEN 'Вторник' THEN 2
                        WHEN 'Среда' THEN 3
                        WHEN 'Четверг' THEN 4
                        WHEN 'Пятница' THEN 5
                        WHEN 'Суббота' THEN 6
                        ELSE 7
                    END,
                    s.lesson_number
            """, (self.user['user_id'],))
            
            schedule = Database.dict_fetchall(cursor)
            
            for item in self.schedule_tree.get_children():
                self.schedule_tree.delete(item)
            
            for item in schedule:
                self.schedule_tree.insert("", "end", values=(
                    item['day_of_week'],
                    item['lesson_number'],
                    item['subject_name'],
                    item['full_name'],
                    item['room'] or "---"
                ))
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось загрузить расписание: {str(e)}")
        finally:
            connection.close()
    
    def setup_grades_tab(self):
        tab = self.tabview.tab("Оценки")
        
        container = ctk.CTkFrame(tab, fg_color="transparent")
        container.pack(fill="both", expand=True, padx=5, pady=5)
        
        columns = ("Дата", "Предмет", "Оценка", "Тип урока", "Учитель", "Комментарий")
        self.grades_tree = ttk.Treeview(container, columns=columns, show="headings", style="Treeview", height=18)
        
        for col in columns:
            self.grades_tree.heading(col, text=col)
            self.grades_tree.column(col, width=120)
        
        scrollbar_y = ttk.Scrollbar(container, orient="vertical", command=self.grades_tree.yview)
        scrollbar_x = ttk.Scrollbar(container, orient="horizontal", command=self.grades_tree.xview)
        self.grades_tree.configure(yscrollcommand=scrollbar_y.set, xscrollcommand=scrollbar_x.set)
        
        self.grades_tree.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
        scrollbar_y.grid(row=0, column=1, sticky="ns", pady=5)
        scrollbar_x.grid(row=1, column=0, sticky="ew", padx=5)
        
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        
        ModernButton(
            tab,
            text="🔄 Обновить оценки",
            command=self.load_grades,
            fg_color=COLORS['primary'],
            hover_color=COLORS['secondary'],
            height=35
        ).pack(pady=8)
    
    def load_grades(self):
        connection = Database.get_connection()
        if connection is None:
            return
            
        try:
            cursor = connection.cursor()
            cursor.execute("""
                SELECT g.grade_date, sub.subject_name, g.grade, 
                       g.lesson_type, u.full_name, g.comment
                FROM grades g
                JOIN subjects sub ON g.subject_id = sub.subject_id
                JOIN users u ON g.teacher_id = u.user_id
                WHERE g.student_id = ?
                ORDER BY g.grade_date DESC
            """, (self.user['user_id'],))
            
            grades = Database.dict_fetchall(cursor)
            
            for item in self.grades_tree.get_children():
                self.grades_tree.delete(item)
            
            for grade in grades:
                comment = grade['comment'] or "---"
                lesson_type = grade['lesson_type'] or "урок"
                self.grades_tree.insert("", "end", values=(
                    grade['grade_date'].strftime("%d.%m.%Y"),
                    grade['subject_name'],
                    grade['grade'],
                    lesson_type,
                    grade['full_name'],
                    comment
                ))
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось загрузить оценки: {str(e)}")
        finally:
            connection.close()
    
    def setup_homework_tab(self):
        tab = self.tabview.tab("Домашние задания")
        
        container = ctk.CTkFrame(tab, fg_color="transparent")
        container.pack(fill="both", expand=True, padx=5, pady=5)
        
        columns = ("Предмет", "Дата задания", "Срок сдачи", "Задание", "Учитель")
        self.homework_tree = ttk.Treeview(container, columns=columns, show="headings", style="Treeview", height=18)
        
        for col in columns:
            self.homework_tree.heading(col, text=col)
            self.homework_tree.column(col, width=150)
        
        scrollbar_y = ttk.Scrollbar(container, orient="vertical", command=self.homework_tree.yview)
        scrollbar_x = ttk.Scrollbar(container, orient="horizontal", command=self.homework_tree.xview)
        self.homework_tree.configure(yscrollcommand=scrollbar_y.set, xscrollcommand=scrollbar_x.set)
        
        self.homework_tree.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
        scrollbar_y.grid(row=0, column=1, sticky="ns", pady=5)
        scrollbar_x.grid(row=1, column=0, sticky="ew", padx=5)
        
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        
        ModernButton(
            tab,
            text="🔄 Обновить задания",
            command=self.load_homework,
            fg_color=COLORS['primary'],
            hover_color=COLORS['secondary'],
            height=35
        ).pack(pady=8)
    
    def load_homework(self):
        connection = Database.get_connection()
        if connection is None:
            return
            
        try:
            cursor = connection.cursor()
            cursor.execute("""
                SELECT h.homework_date, h.due_date, h.description,
                       sub.subject_name, u.full_name
                FROM homework h
                JOIN subjects sub ON h.subject_id = sub.subject_id
                JOIN users u ON h.teacher_id = u.user_id
                WHERE h.class_id IN (
                    SELECT class_id FROM users WHERE user_id = ?
                ) AND h.due_date >= GETDATE()
                ORDER BY h.due_date
            """, (self.user['user_id'],))
            
            homework = Database.dict_fetchall(cursor)
            
            for item in self.homework_tree.get_children():
                self.homework_tree.delete(item)
            
            for hw in homework:
                desc = hw['description'][:50] + "..." if len(hw['description']) > 50 else hw['description']
                self.homework_tree.insert("", "end", values=(
                    hw['subject_name'],
                    hw['homework_date'].strftime("%d.%m.%Y"),
                    hw['due_date'].strftime("%d.%m.%Y"),
                    desc,
                    hw['full_name']
                ))
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось загрузить задания: {str(e)}")
        finally:
            connection.close()
    
    def setup_attendance_tab(self):
        tab = self.tabview.tab("Посещаемость")
        
        container = ctk.CTkFrame(tab, fg_color="transparent")
        container.pack(fill="both", expand=True, padx=5, pady=5)
        
        columns = ("Дата", "Статус", "Причина")
        self.attendance_tree = ttk.Treeview(container, columns=columns, show="headings", style="Treeview", height=18)
        
        for col in columns:
            self.attendance_tree.heading(col, text=col)
            self.attendance_tree.column(col, width=200)
        
        scrollbar_y = ttk.Scrollbar(container, orient="vertical", command=self.attendance_tree.yview)
        scrollbar_x = ttk.Scrollbar(container, orient="horizontal", command=self.attendance_tree.xview)
        self.attendance_tree.configure(yscrollcommand=scrollbar_y.set, xscrollcommand=scrollbar_x.set)
        
        self.attendance_tree.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
        scrollbar_y.grid(row=0, column=1, sticky="ns", pady=5)
        scrollbar_x.grid(row=1, column=0, sticky="ew", padx=5)
        
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        
        ModernButton(
            tab,
            text="🔄 Обновить посещаемость",
            command=self.load_attendance,
            fg_color=COLORS['primary'],
            hover_color=COLORS['secondary'],
            height=35
        ).pack(pady=8)
    
    def load_attendance(self):
        connection = Database.get_connection()
        if connection is None:
            return
            
        try:
            cursor = connection.cursor()
            cursor.execute("""
                SELECT attendance_date, status, reason
                FROM attendance
                WHERE student_id = ?
                ORDER BY attendance_date DESC
            """, (self.user['user_id'],))
            
            attendance = Database.dict_fetchall(cursor)
            
            for item in self.attendance_tree.get_children():
                self.attendance_tree.delete(item)
            
            for att in attendance:
                reason = att['reason'] or "---"
                self.attendance_tree.insert("", "end", values=(
                    att['attendance_date'].strftime("%d.%m.%Y"),
                    att['status'],
                    reason
                ))
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось загрузить посещаемость: {str(e)}")
        finally:
            connection.close()
    
    def load_stats(self):
        connection = Database.get_connection()
        if connection is None:
            return
            
        try:
            cursor = connection.cursor()
            cursor.execute("""
                SELECT 
                    COUNT(*) as total_grades,
                    AVG(CAST(grade AS FLOAT)) as avg_grade,
                    COUNT(DISTINCT subject_id) as subjects_count
                FROM grades 
                WHERE student_id = ?
            """, (self.user['user_id'],))
            
            stats = Database.dict_fetchone(cursor)
            
            if stats and stats['total_grades'] > 0:
                text = f"📊 Оценок: {stats['total_grades']}\n"
                text += f"⭐ Средний балл: {stats['avg_grade']:.1f}\n"
                text += f"📚 Предметов: {stats['subjects_count']}"
                self.stats_label.configure(text=text)
            else:
                self.stats_label.configure(text="📊 Нет оценок\n⭐ Средний балл: -\n📚 Предметов: 0")
                    
        except Exception:
            self.stats_label.configure(text="Ошибка загрузки\nстатистики")
        finally:
            connection.close()

class TeacherApp(MainApp):
    def __init__(self, parent, user):
        super().__init__(parent, user)
        self.title(f"👨‍🏫 {SCHOOL_INFO['short_name']} - Учитель: {user['full_name']}")
        
        window_width = 1400
        window_height = 800
        
        self.geometry(f"{window_width}x{window_height}")
        self.center_window(window_width, window_height)
        
        configure_treeview_style()
        self.setup_ui()
        
    def setup_ui(self):
        # Боковая панель - фиксированная ширина
        sidebar = ctk.CTkFrame(self, width=260, fg_color=COLORS['sidebar'], corner_radius=0)
        sidebar.pack(side="left", fill="y")
        sidebar.pack_propagate(False)
        
        # Боковая панель с прокруткой
        sidebar_canvas = tk.Canvas(sidebar, bg=COLORS['sidebar'], highlightthickness=0)
        sidebar_scrollbar = ctk.CTkScrollbar(sidebar, orientation="vertical", command=sidebar_canvas.yview)
        sidebar_scrollable = ctk.CTkFrame(sidebar_canvas, fg_color="transparent")
        
        sidebar_scrollable.bind(
            "<Configure>",
            lambda e: sidebar_canvas.configure(scrollregion=sidebar_canvas.bbox("all"))
        )
        
        sidebar_canvas.create_window((0, 0), window=sidebar_scrollable, anchor="nw", width=240)
        sidebar_canvas.configure(yscrollcommand=sidebar_scrollbar.set)
        
        sidebar_canvas.pack(side="left", fill="both", expand=True)
        sidebar_scrollbar.pack(side="right", fill="y")
        
        # Верхняя часть
        header_frame = ctk.CTkFrame(sidebar_scrollable, height=120, fg_color=COLORS['accent'], corner_radius=0)
        header_frame.pack(fill="x")
        header_frame.pack_propagate(False)
        
        ctk.CTkLabel(
            header_frame,
            text="👨‍🏫",
            font=("Segoe UI", 40),
            text_color="white"
        ).pack(pady=(15, 2))
        
        ctk.CTkLabel(
            header_frame,
            text="Учитель",
            font=FONTS['subtitle'],
            text_color="white"
        ).pack()
        
        # Информация о пользователе
        user_info_frame = CardFrame(sidebar_scrollable)
        user_info_frame.pack(fill="x", padx=10, pady=10)
        
        ctk.CTkLabel(
            user_info_frame,
            text=self.user['full_name'],
            font=FONTS['heading'],
            text_color=COLORS['text_light'],
            wraplength=220
        ).pack(pady=8)
        
        # Информация о школе
        school_info = SchoolInfoFrame(sidebar_scrollable)
        school_info.pack(fill="x", padx=10, pady=5)
        
        # Меню
        menu_frame = CardFrame(sidebar_scrollable)
        menu_frame.pack(fill="x", padx=10, pady=5)
        
        ctk.CTkLabel(
            menu_frame,
            text="📋 Меню",
            font=FONTS['heading'],
            text_color=COLORS['accent']
        ).pack(pady=5)
        
        menu_items = [
            ("🏫 Мои классы", "Мои классы"),
            ("📝 Выставить оценку", "Выставить оценку"),
            ("📚 Домашние задания", "Домашние задания"),
            ("👥 Посещаемость", "Посещаемость")
        ]
        
        for icon_text, tab_name in menu_items:
            ModernButton(
                menu_frame,
                text=icon_text,
                command=lambda tn=tab_name: self.tabview.set(tn),
                fg_color="transparent",
                hover_color=COLORS['hover'],
                anchor="w",
                height=35
            ).pack(fill="x", padx=5, pady=1)
        
        # Статистика
        stats_frame = CardFrame(sidebar_scrollable)
        stats_frame.pack(fill="x", padx=10, pady=5)
        
        ctk.CTkLabel(
            stats_frame,
            text="📊 Статистика",
            font=FONTS['heading'],
            text_color=COLORS['accent']
        ).pack(pady=5)
        
        self.teacher_stats_label = ctk.CTkLabel(
            stats_frame,
            text="Загрузка...",
            font=FONTS['small'],
            text_color=COLORS['gray']
        )
        self.teacher_stats_label.pack(pady=(0, 8))
        
        # Кнопка выхода
        ModernButton(
            sidebar_scrollable,
            text="🚪 Выйти",
            command=self.on_closing,
            fg_color=COLORS['error'],
            hover_color=COLORS['warning'],
            height=40
        ).pack(fill="x", padx=10, pady=10)
        
        # Основная область
        main_area = ctk.CTkFrame(self, fg_color=COLORS['dark'], corner_radius=0)
        main_area.pack(side="right", fill="both", expand=True)
        
        # Вкладки
        self.tabview = ctk.CTkTabview(main_area)
        self.tabview.pack(fill="both", expand=True, padx=15, pady=15)
        
        for tab_name in ["Мои классы", "Выставить оценку", "Домашние задания", "Посещаемость"]:
            self.tabview.add(tab_name)
            self.tabview.tab(tab_name).configure(fg_color=COLORS['card_bg'])
        
        self.tabview.configure(
            segmented_button_fg_color=COLORS['sidebar'],
            segmented_button_selected_color=COLORS['accent'],
            segmented_button_selected_hover_color=COLORS['secondary'],
            text_color=COLORS['text_light']
        )
        
        self.tabview._segmented_button.configure(font=FONTS['button'])
        
        self.setup_classes_tab()
        self.setup_give_grade_tab()
        self.setup_teacher_homework_tab()
        self.setup_teacher_attendance_tab()
        
        # Загрузка статистики
        self.load_teacher_stats()
    
    def setup_classes_tab(self):
        tab = self.tabview.tab("Мои классы")
        
        container = ctk.CTkFrame(tab, fg_color="transparent")
        container.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Таблица классов
        columns = ("Класс", "Учебный год", "Количество учеников")
        self.classes_tree = ttk.Treeview(container, columns=columns, show="headings", style="Treeview", height=20)
        
        for col in columns:
            self.classes_tree.heading(col, text=col)
            self.classes_tree.column(col, width=200)
        
        scrollbar = ttk.Scrollbar(container, orient="vertical", command=self.classes_tree.yview)
        self.classes_tree.configure(yscrollcommand=scrollbar.set)
        
        self.classes_tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Кнопка обновить
        ModernButton(
            tab,
            text="🔄 Обновить список классов",
            command=self.load_classes,
            fg_color=COLORS['primary'],
            hover_color=COLORS['secondary'],
            height=35
        ).pack(pady=10)
        
        self.load_classes()
    
    def load_classes(self):
        connection = Database.get_connection()
        if connection is None:
            return
            
        try:
            cursor = connection.cursor()
            cursor.execute("""
                SELECT c.class_name, c.academic_year, 
                       COUNT(u.user_id) as student_count
                FROM classes c
                LEFT JOIN users u ON c.class_id = u.class_id AND u.role = 'student'
                WHERE c.class_teacher_id = ?
                GROUP BY c.class_id, c.class_name, c.academic_year
            """, (self.user['user_id'],))
            
            classes = Database.dict_fetchall(cursor)
            
            for item in self.classes_tree.get_children():
                self.classes_tree.delete(item)
            
            for cls in classes:
                self.classes_tree.insert("", "end", values=(
                    cls['class_name'],
                    cls['academic_year'] or "---",
                    cls['student_count']
                ))
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось загрузить классы: {str(e)}")
        finally:
            connection.close()
    
    def setup_give_grade_tab(self):
        tab = self.tabview.tab("Выставить оценку")
        
        # Контейнер с прокруткой
        canvas = tk.Canvas(tab, bg=COLORS['card_bg'], highlightthickness=0)
        scrollbar = ctk.CTkScrollbar(tab, orientation="vertical", command=canvas.yview)
        scrollable = ctk.CTkFrame(canvas, fg_color=COLORS['card_bg'])
        
        scrollable.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        form_frame = CardFrame(scrollable)
        form_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        ctk.CTkLabel(
            form_frame,
            text="📝 Выставить оценку",
            font=("Segoe UI", 20, "bold"),
            text_color=COLORS['accent']
        ).pack(pady=(15, 15))
        
        # Сетка полей
        grid_frame = ctk.CTkFrame(form_frame, fg_color="transparent")
        grid_frame.pack(fill="both", expand=True, padx=30, pady=5)
        
        # Выбор класса
        ctk.CTkLabel(
            grid_frame, 
            text="Класс:", 
            font=FONTS['heading'],
            text_color=COLORS['text_light']
        ).grid(row=0, column=0, sticky="w", pady=(5, 2))
        self.class_combo = ttk.Combobox(grid_frame, font=FONTS['body'], width=28)
        self.class_combo.grid(row=0, column=1, pady=(5, 2), padx=(5, 0))
        self.class_combo.bind('<<ComboboxSelected>>', self.on_class_selected)
        
        # Выбор ученика
        ctk.CTkLabel(
            grid_frame, 
            text="Ученик:", 
            font=FONTS['heading'],
            text_color=COLORS['text_light']
        ).grid(row=1, column=0, sticky="w", pady=(5, 2))
        self.student_combo = ttk.Combobox(grid_frame, font=FONTS['body'], width=28)
        self.student_combo.grid(row=1, column=1, pady=(5, 2), padx=(5, 0))
        
        # Выбор предмета
        ctk.CTkLabel(
            grid_frame, 
            text="Предмет:", 
            font=FONTS['heading'],
            text_color=COLORS['text_light']
        ).grid(row=2, column=0, sticky="w", pady=(5, 2))
        self.subject_combo = ttk.Combobox(grid_frame, font=FONTS['body'], width=28)
        self.subject_combo.grid(row=2, column=1, pady=(5, 2), padx=(5, 0))
        
        # Оценка
        ctk.CTkLabel(
            grid_frame, 
            text="Оценка:", 
            font=FONTS['heading'],
            text_color=COLORS['text_light']
        ).grid(row=3, column=0, sticky="w", pady=(5, 2))
        
        grade_frame = ctk.CTkFrame(grid_frame, fg_color="transparent")
        grade_frame.grid(row=3, column=1, sticky="w", pady=(5, 2), padx=(5, 0))
        
        self.grade_var = tk.IntVar(value=5)
        for i in range(1, 6):
            ctk.CTkRadioButton(
                grade_frame, 
                text=str(i), 
                variable=self.grade_var, 
                value=i,
                font=FONTS['body'],
                fg_color=COLORS['primary']
            ).pack(side="left", padx=3)
        
        # Тип урока
        ctk.CTkLabel(
            grid_frame, 
            text="Тип урока:", 
            font=FONTS['heading'],
            text_color=COLORS['text_light']
        ).grid(row=4, column=0, sticky="w", pady=(5, 2))
        self.lesson_type_combo = ttk.Combobox(
            grid_frame, 
            values=['урок', 'контрольная', 'самостоятельная', 'проект'], 
            font=FONTS['body'],
            width=28
        )
        self.lesson_type_combo.set('урок')
        self.lesson_type_combo.grid(row=4, column=1, pady=(5, 2), padx=(5, 0))
        
        # Комментарий
        ctk.CTkLabel(
            grid_frame, 
            text="Комментарий:", 
            font=FONTS['heading'],
            text_color=COLORS['text_light']
        ).grid(row=5, column=0, sticky="nw", pady=(5, 2))
        self.comment_text = ctk.CTkTextbox(grid_frame, width=250, height=80, font=FONTS['body'])
        self.comment_text.grid(row=5, column=1, pady=(5, 2), padx=(5, 0))
        
        # Кнопка
        button_frame = ctk.CTkFrame(form_frame, fg_color="transparent")
        button_frame.pack(pady=15)
        
        ModernButton(
            button_frame, 
            text="✅ Выставить оценку", 
            command=self.add_grade, 
            fg_color=COLORS['primary'],
            hover_color=COLORS['secondary'],
            width=180
        ).pack()
        
        self.load_classes_for_teacher()
        self.load_subjects()
    
    def load_classes_for_teacher(self):
        connection = Database.get_connection()
        if connection is None:
            return
            
        try:
            cursor = connection.cursor()
            cursor.execute("""
                SELECT DISTINCT c.class_name
                FROM schedule s
                JOIN classes c ON s.class_id = c.class_id
                WHERE s.teacher_id = ?
            """, (self.user['user_id'],))
            
            classes = Database.dict_fetchall(cursor)
            class_names = [cls['class_name'] for cls in classes]
            self.class_combo['values'] = class_names
                
        except Exception as e:
            messagebox.showerror("Ошибка", f"Ошибка загрузки классов: {str(e)}")
        finally:
            connection.close()
    
    def load_subjects(self):
        connection = Database.get_connection()
        if connection is None:
            return
            
        try:
            cursor = connection.cursor()
            cursor.execute("""
                SELECT DISTINCT s.subject_name
                FROM schedule sch
                JOIN subjects s ON sch.subject_id = s.subject_id
                WHERE sch.teacher_id = ?
            """, (self.user['user_id'],))
            
            subjects = Database.dict_fetchall(cursor)
            subject_names = [sub['subject_name'] for sub in subjects]
            self.subject_combo['values'] = subject_names
                
        except Exception as e:
            messagebox.showerror("Ошибка", f"Ошибка загрузки предметов: {str(e)}")
        finally:
            connection.close()
    
    def on_class_selected(self, event):
        class_name = self.class_combo.get()
        if not class_name:
            return
        
        connection = Database.get_connection()
        if connection is None:
            return
            
        try:
            cursor = connection.cursor()
            cursor.execute("""
                SELECT u.user_id, u.full_name
                FROM users u
                JOIN classes c ON u.class_id = c.class_id
                WHERE c.class_name = ? AND u.role = 'student'
                ORDER BY u.full_name
            """, (class_name,))
            
            students = Database.dict_fetchall(cursor)
            student_names = [f"{stud['full_name']} (ID: {stud['user_id']})" for stud in students]
            self.student_combo['values'] = student_names
                
        except Exception as e:
            messagebox.showerror("Ошибка", f"Ошибка загрузки учеников: {str(e)}")
        finally:
            connection.close()
    
    def add_grade(self):
        student_text = self.student_combo.get()
        subject_name = self.subject_combo.get()
        grade = self.grade_var.get()
        lesson_type = self.lesson_type_combo.get()
        comment = self.comment_text.get("1.0", "end-1c").strip()
        
        if not student_text or not subject_name:
            messagebox.showwarning("Ошибка", "Выберите ученика и предмет")
            return
        
        try:
            student_id = int(student_text.split('ID: ')[1].rstrip(')'))
        except:
            messagebox.showerror("Ошибка", "Некорректный формат ученика")
            return
        
        connection = Database.get_connection()
        if connection is None:
            return
            
        try:
            cursor = connection.cursor()
            cursor.execute("SELECT subject_id FROM subjects WHERE subject_name = ?", (subject_name,))
            subject = Database.dict_fetchone(cursor)
            
            if not subject:
                messagebox.showerror("Ошибка", "Предмет не найден")
                return
            
            cursor.execute("""
                INSERT INTO grades (student_id, subject_id, teacher_id, grade, 
                                   grade_date, lesson_type, comment)
                VALUES (?, ?, ?, ?, GETDATE(), ?, ?)
            """, (student_id, subject['subject_id'], self.user['user_id'], 
                  grade, lesson_type, comment or None))
            
            connection.commit()
            messagebox.showinfo("Успех", f"✅ Оценка {grade} выставлена ученику!")
            
            self.comment_text.delete("1.0", "end")
            self.grade_var.set(5)
                
        except Exception as e:
            messagebox.showerror("Ошибка", f"Ошибка при выставлении оценки: {str(e)}")
        finally:
            connection.close()
    
    def setup_teacher_homework_tab(self):
        tab = self.tabview.tab("Домашние задания")
        
        canvas = tk.Canvas(tab, bg=COLORS['card_bg'], highlightthickness=0)
        scrollbar = ctk.CTkScrollbar(tab, orientation="vertical", command=canvas.yview)
        scrollable = ctk.CTkFrame(canvas, fg_color=COLORS['card_bg'])
        
        scrollable.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        form_frame = CardFrame(scrollable)
        form_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        ctk.CTkLabel(
            form_frame,
            text="📚 Добавить домашнее задание",
            font=("Segoe UI", 20, "bold"),
            text_color=COLORS['accent']
        ).pack(pady=(15, 15))
        
        # Сетка полей
        grid_frame = ctk.CTkFrame(form_frame, fg_color="transparent")
        grid_frame.pack(fill="both", expand=True, padx=30, pady=5)
        
        # Выбор класса
        ctk.CTkLabel(
            grid_frame, 
            text="Класс:", 
            font=FONTS['heading'],
            text_color=COLORS['text_light']
        ).grid(row=0, column=0, sticky="w", pady=(5, 2))
        self.hw_class_combo = ttk.Combobox(grid_frame, font=FONTS['body'], width=28)
        self.hw_class_combo.grid(row=0, column=1, pady=(5, 2), padx=(5, 0))
        
        # Выбор предмета
        ctk.CTkLabel(
            grid_frame, 
            text="Предмет:", 
            font=FONTS['heading'],
            text_color=COLORS['text_light']
        ).grid(row=1, column=0, sticky="w", pady=(5, 2))
        self.hw_subject_combo = ttk.Combobox(grid_frame, font=FONTS['body'], width=28)
        self.hw_subject_combo.grid(row=1, column=1, pady=(5, 2), padx=(5, 0))
        
        # Описание задания
        ctk.CTkLabel(
            grid_frame, 
            text="Задание:", 
            font=FONTS['heading'],
            text_color=COLORS['text_light']
        ).grid(row=2, column=0, sticky="nw", pady=(5, 2))
        self.hw_description_text = ctk.CTkTextbox(grid_frame, width=250, height=80, font=FONTS['body'])
        self.hw_description_text.grid(row=2, column=1, pady=(5, 2), padx=(5, 0))
        
        # Срок сдачи
        ctk.CTkLabel(
            grid_frame, 
            text="Срок сдачи:", 
            font=FONTS['heading'],
            text_color=COLORS['text_light']
        ).grid(row=3, column=0, sticky="w", pady=(5, 2))
        self.hw_due_date_entry = ModernEntry(grid_frame, placeholder_text="2026-12-31", width=250)
        self.hw_due_date_entry.grid(row=3, column=1, pady=(5, 2), padx=(5, 0))
        
        # Кнопка
        button_frame = ctk.CTkFrame(form_frame, fg_color="transparent")
        button_frame.pack(pady=15)
        
        ModernButton(
            button_frame, 
            text="✅ Добавить задание", 
            command=self.add_homework, 
            fg_color=COLORS['primary'],
            hover_color=COLORS['secondary'],
            width=180
        ).pack()
        
        self.load_hw_classes()
        self.load_hw_subjects()
    
    def load_hw_classes(self):
        connection = Database.get_connection()
        if connection is None:
            return
            
        try:
            cursor = connection.cursor()
            cursor.execute("""
                SELECT DISTINCT c.class_name
                FROM schedule s
                JOIN classes c ON s.class_id = c.class_id
                WHERE s.teacher_id = ?
            """, (self.user['user_id'],))
            
            classes = Database.dict_fetchall(cursor)
            class_names = [cls['class_name'] for cls in classes]
            self.hw_class_combo['values'] = class_names
                
        except Exception as e:
            messagebox.showerror("Ошибка", f"Ошибка загрузки классов: {str(e)}")
        finally:
            connection.close()
    
    def load_hw_subjects(self):
        connection = Database.get_connection()
        if connection is None:
            return
            
        try:
            cursor = connection.cursor()
            cursor.execute("SELECT subject_name FROM subjects")
            subjects = Database.dict_fetchall(cursor)
            subject_names = [sub['subject_name'] for sub in subjects]
            self.hw_subject_combo['values'] = subject_names
                
        except Exception as e:
            messagebox.showerror("Ошибка", f"Ошибка загрузки предметов: {str(e)}")
        finally:
            connection.close()
    
    def add_homework(self):
        class_name = self.hw_class_combo.get()
        subject_name = self.hw_subject_combo.get()
        description = self.hw_description_text.get("1.0", "end-1c").strip()
        due_date = self.hw_due_date_entry.get().strip()
        
        if not class_name or not subject_name or not description or not due_date:
            messagebox.showwarning("Ошибка", "Заполните все поля")
            return
        
        try:
            datetime.strptime(due_date, "%Y-%m-%d")
        except ValueError:
            messagebox.showerror("Ошибка", "Некорректный формат даты. Используйте ГГГГ-ММ-ДД")
            return
        
        connection = Database.get_connection()
        if connection is None:
            return
            
        try:
            cursor = connection.cursor()
            cursor.execute("SELECT class_id FROM classes WHERE class_name = ?", (class_name,))
            class_data = Database.dict_fetchone(cursor)
            
            cursor.execute("SELECT subject_id FROM subjects WHERE subject_name = ?", (subject_name,))
            subject_data = Database.dict_fetchone(cursor)
            
            if not class_data or not subject_data:
                messagebox.showerror("Ошибка", "Класс или предмет не найдены")
                return
            
            cursor.execute("""
                INSERT INTO homework (teacher_id, class_id, subject_id, 
                                    homework_date, due_date, description)
                VALUES (?, ?, ?, GETDATE(), ?, ?)
            """, (self.user['user_id'], class_data['class_id'], 
                  subject_data['subject_id'], due_date, description))
            
            connection.commit()
            messagebox.showinfo("Успех", "✅ Домашнее задание добавлено!")
            
            self.hw_description_text.delete("1.0", "end")
            self.hw_due_date_entry.delete(0, "end")
                
        except Exception as e:
            messagebox.showerror("Ошибка", f"Ошибка при добавлении задания: {str(e)}")
        finally:
            connection.close()
    
    def setup_teacher_attendance_tab(self):
        tab = self.tabview.tab("Посещаемость")
        
        canvas = tk.Canvas(tab, bg=COLORS['card_bg'], highlightthickness=0)
        scrollbar = ctk.CTkScrollbar(tab, orientation="vertical", command=canvas.yview)
        scrollable = ctk.CTkFrame(canvas, fg_color=COLORS['card_bg'])
        
        scrollable.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        main_frame = ctk.CTkFrame(scrollable, fg_color=COLORS['card_bg'])
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Форма сверху
        form_frame = CardFrame(main_frame)
        form_frame.pack(fill="x", padx=15, pady=15)
        
        form_grid = ctk.CTkFrame(form_frame, fg_color="transparent")
        form_grid.pack(fill="x", padx=20, pady=15)
        
        # Выбор класса
        ctk.CTkLabel(
            form_grid, 
            text="Класс:", 
            font=FONTS['heading'],
            text_color=COLORS['text_light']
        ).grid(row=0, column=0, sticky="w", pady=(0, 8))
        self.att_class_combo = ttk.Combobox(form_grid, font=FONTS['body'], width=22)
        self.att_class_combo.grid(row=0, column=1, pady=(0, 8), padx=(8, 15))
        self.att_class_combo.bind('<<ComboboxSelected>>', self.on_att_class_selected)
        
        # Дата
        ctk.CTkLabel(
            form_grid, 
            text="Дата:", 
            font=FONTS['heading'],
            text_color=COLORS['text_light']
        ).grid(row=0, column=2, sticky="w", pady=(0, 8))
        self.att_date_entry = ModernEntry(form_grid, placeholder_text="2026-10-10", width=150)
        self.att_date_entry.insert(0, datetime.now().strftime("%Y-%m-%d"))
        self.att_date_entry.grid(row=0, column=3, pady=(0, 8), padx=(8, 0))
        
        # Кнопки управления
        button_frame = ctk.CTkFrame(form_frame, fg_color="transparent")
        button_frame.pack(fill="x", padx=20, pady=(0, 15))
        
        ModernButton(
            button_frame,
            text="✅ Отметить всех присутствующими",
            command=lambda: self.mark_all_attendance('присутствовал'),
            fg_color=COLORS['success'],
            hover_color=COLORS['info'],
            height=35
        ).pack(side="left", padx=(0, 5))
        
        ModernButton(
            button_frame,
            text="🚫 Отметить всех отсутствующими",
            command=lambda: self.mark_all_attendance('отсутствовал'),
            fg_color=COLORS['warning'],
            hover_color=COLORS['error'],
            height=35
        ).pack(side="left", padx=(0, 5))
        
        ModernButton(
            button_frame,
            text="💾 Сохранить",
            command=self.save_attendance,
            fg_color=COLORS['primary'],
            hover_color=COLORS['secondary'],
            height=35
        ).pack(side="left")
        
        # Таблица учеников
        table_frame = CardFrame(main_frame)
        table_frame.pack(fill="both", expand=True, padx=15, pady=(0, 15))
        
        container = ctk.CTkFrame(table_frame, fg_color="transparent")
        container.pack(fill="both", expand=True, padx=5, pady=5)
        
        columns = ("Ученик", "Статус", "Причина")
        self.attendance_mark_tree = ttk.Treeview(
            container, 
            columns=columns, 
            show="headings", 
            style="Treeview",
            height=15
        )
        
        for col in columns:
            self.attendance_mark_tree.heading(col, text=col)
            self.attendance_mark_tree.column(col, width=200)
        
        scrollbar_y = ttk.Scrollbar(container, orient="vertical", command=self.attendance_mark_tree.yview)
        scrollbar_x = ttk.Scrollbar(container, orient="horizontal", command=self.attendance_mark_tree.xview)
        self.attendance_mark_tree.configure(yscrollcommand=scrollbar_y.set, xscrollcommand=scrollbar_x.set)
        
        self.attendance_mark_tree.grid(row=0, column=0, sticky="nsew")
        scrollbar_y.grid(row=0, column=1, sticky="ns")
        scrollbar_x.grid(row=1, column=0, sticky="ew")
        
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        
        self.load_att_classes()
    
    def load_att_classes(self):
        connection = Database.get_connection()
        if connection is None:
            return
            
        try:
            cursor = connection.cursor()
            cursor.execute("""
                SELECT DISTINCT c.class_name
                FROM schedule s
                JOIN classes c ON s.class_id = c.class_id
                WHERE s.teacher_id = ?
            """, (self.user['user_id'],))
            
            classes = Database.dict_fetchall(cursor)
            class_names = [cls['class_name'] for cls in classes]
            self.att_class_combo['values'] = class_names
                
        except Exception as e:
            messagebox.showerror("Ошибка", f"Ошибка загрузки классов: {str(e)}")
        finally:
            connection.close()
    
    def on_att_class_selected(self, event):
        class_name = self.att_class_combo.get()
        if not class_name:
            return
        
        connection = Database.get_connection()
        if connection is None:
            return
            
        try:
            cursor = connection.cursor()
            cursor.execute("""
                SELECT u.user_id, u.full_name
                FROM users u
                JOIN classes c ON u.class_id = c.class_id
                WHERE c.class_name = ? AND u.role = 'student'
                ORDER BY u.full_name
            """, (class_name,))
            
            students = Database.dict_fetchall(cursor)
            
            for item in self.attendance_mark_tree.get_children():
                self.attendance_mark_tree.delete(item)
            
            for student in students:
                self.attendance_mark_tree.insert("", "end", 
                    values=(student['full_name'], "присутствовал", ""),
                    tags=(student['user_id'],))
                
        except Exception as e:
            messagebox.showerror("Ошибка", f"Ошибка загрузки учеников: {str(e)}")
        finally:
            connection.close()
    
    def mark_all_attendance(self, status):
        for item in self.attendance_mark_tree.get_children():
            current_values = self.attendance_mark_tree.item(item)['values']
            self.attendance_mark_tree.item(item, values=(
                current_values[0],
                status,
                current_values[2]
            ))
    
    def save_attendance(self):
        class_name = self.att_class_combo.get()
        date_str = self.att_date_entry.get().strip()
        
        if not class_name or not date_str:
            messagebox.showwarning("Ошибка", "Выберите класс и дату")
            return
        
        try:
            attendance_date = datetime.strptime(date_str, "%Y-%m-%d")
        except ValueError:
            messagebox.showerror("Ошибка", "Некорректный формат даты. Используйте ГГГГ-ММ-ДД")
            return
        
        connection = Database.get_connection()
        if connection is None:
            return
            
        try:
            cursor = connection.cursor()
            cursor.execute("SELECT class_id FROM classes WHERE class_name = ?", (class_name,))
            class_data = Database.dict_fetchone(cursor)
            
            if not class_data:
                messagebox.showerror("Ошибка", "Класс не найден")
                return
            
            for item in self.attendance_mark_tree.get_children():
                values = self.attendance_mark_tree.item(item)['values']
                tags = self.attendance_mark_tree.item(item)['tags']
                
                if len(tags) > 0:
                    student_id = tags[0]
                    status = values[1]
                    reason = values[2] or None
                    
                    cursor.execute("""
                        SELECT * FROM attendance 
                        WHERE student_id = ? AND attendance_date = ?
                    """, (student_id, attendance_date.date()))
                    
                    existing = Database.dict_fetchone(cursor)
                    
                    if existing:
                        cursor.execute("""
                            UPDATE attendance 
                            SET status = ?, reason = ?
                            WHERE attendance_id = ?
                        """, (status, reason, existing['attendance_id']))
                    else:
                        cursor.execute("""
                            INSERT INTO attendance (student_id, class_id, 
                                                  attendance_date, status, reason)
                            VALUES (?, ?, ?, ?, ?)
                        """, (student_id, class_data['class_id'], 
                              attendance_date.date(), status, reason))
            
            connection.commit()
            messagebox.showinfo("Успех", "✅ Посещаемость сохранена!")
                
        except Exception as e:
            messagebox.showerror("Ошибка", f"Ошибка при сохранении посещаемости: {str(e)}")
        finally:
            connection.close()
    
    def load_teacher_stats(self):
        connection = Database.get_connection()
        if connection is None:
            return
            
        try:
            cursor = connection.cursor()
            cursor.execute("""
                SELECT 
                    COUNT(DISTINCT c.class_id) as classes_count,
                    COUNT(DISTINCT s.subject_id) as subjects_count
                FROM schedule s
                JOIN classes c ON s.class_id = c.class_id
                JOIN subjects sub ON s.subject_id = sub.subject_id
                WHERE s.teacher_id = ?
            """, (self.user['user_id'],))
            
            stats = Database.dict_fetchone(cursor)
            
            if stats:
                text = f"🏫 Классов: {stats['classes_count']}\n"
                text += f"📚 Предметов: {stats['subjects_count']}"
                self.teacher_stats_label.configure(text=text)
            else:
                self.teacher_stats_label.configure(text="Нет данных")
                    
        except Exception:
            self.teacher_stats_label.configure(text="Ошибка загрузки")
        finally:
            connection.close()

class AdminApp(MainApp):
    def __init__(self, parent, user):
        super().__init__(parent, user)
        self.title(f"⚙️ {SCHOOL_INFO['short_name']} - Администратор: {user['full_name']}")
        
        window_width = 1500
        window_height = 850
        
        self.geometry(f"{window_width}x{window_height}")
        self.center_window(window_width, window_height)
        
        configure_treeview_style()
        self.setup_ui()
        
    def setup_ui(self):
        # Боковая панель - фиксированная ширина
        sidebar = ctk.CTkFrame(self, width=260, fg_color=COLORS['sidebar'], corner_radius=0)
        sidebar.pack(side="left", fill="y")
        sidebar.pack_propagate(False)
        
        # Боковая панель с прокруткой
        sidebar_canvas = tk.Canvas(sidebar, bg=COLORS['sidebar'], highlightthickness=0)
        sidebar_scrollbar = ctk.CTkScrollbar(sidebar, orientation="vertical", command=sidebar_canvas.yview)
        sidebar_scrollable = ctk.CTkFrame(sidebar_canvas, fg_color="transparent")
        
        sidebar_scrollable.bind(
            "<Configure>",
            lambda e: sidebar_canvas.configure(scrollregion=sidebar_canvas.bbox("all"))
        )
        
        sidebar_canvas.create_window((0, 0), window=sidebar_scrollable, anchor="nw", width=240)
        sidebar_canvas.configure(yscrollcommand=sidebar_scrollbar.set)
        
        sidebar_canvas.pack(side="left", fill="both", expand=True)
        sidebar_scrollbar.pack(side="right", fill="y")
        
        # Верхняя часть
        header_frame = ctk.CTkFrame(sidebar_scrollable, height=120, fg_color=COLORS['accent'], corner_radius=0)
        header_frame.pack(fill="x")
        header_frame.pack_propagate(False)
        
        ctk.CTkLabel(
            header_frame,
            text="⚙️",
            font=("Segoe UI", 40),
            text_color="white"
        ).pack(pady=(15, 2))
        
        ctk.CTkLabel(
            header_frame,
            text="Администратор",
            font=FONTS['subtitle'],
            text_color="white"
        ).pack()
        
        # Информация о пользователе
        user_info_frame = CardFrame(sidebar_scrollable)
        user_info_frame.pack(fill="x", padx=10, pady=10)
        
        ctk.CTkLabel(
            user_info_frame,
            text=self.user['full_name'],
            font=FONTS['heading'],
            text_color=COLORS['text_light'],
            wraplength=220
        ).pack(pady=8)
        
        # Информация о школе
        school_info = SchoolInfoFrame(sidebar_scrollable)
        school_info.pack(fill="x", padx=10, pady=5)
        
        # Меню
        menu_frame = CardFrame(sidebar_scrollable)
        menu_frame.pack(fill="x", padx=10, pady=5)
        
        ctk.CTkLabel(
            menu_frame,
            text="📋 Меню",
            font=FONTS['heading'],
            text_color=COLORS['accent']
        ).pack(pady=5)
        
        menu_items = [
            ("👥 Пользователи", "Пользователи"),
            ("🏫 Классы", "Классы"),
            ("📚 Предметы", "Предметы"),
            ("📅 Расписание", "Расписание"),
            ("📊 Статистика", "Статистика")
        ]
        
        for icon_text, tab_name in menu_items:
            ModernButton(
                menu_frame,
                text=icon_text,
                command=lambda tn=tab_name: self.tabview.set(tn),
                fg_color="transparent",
                hover_color=COLORS['hover'],
                anchor="w",
                height=35
            ).pack(fill="x", padx=5, pady=1)
        
        # Системная информация
        info_frame = CardFrame(sidebar_scrollable)
        info_frame.pack(fill="x", padx=10, pady=5)
        
        ctk.CTkLabel(
            info_frame,
            text="📋 Система",
            font=FONTS['heading'],
            text_color=COLORS['accent']
        ).pack(pady=5)
        
        ctk.CTkLabel(
            info_frame,
            text=f"ИНН: {SCHOOL_INFO['inn']}\nОГРН: {SCHOOL_INFO['ogrn']}\nСтатус: 🟢 Активна",
            font=FONTS['small'],
            text_color=COLORS['gray']
        ).pack(pady=(0, 8))
        
        # Кнопка выхода
        ModernButton(
            sidebar_scrollable,
            text="🚪 Выйти",
            command=self.on_closing,
            fg_color=COLORS['error'],
            hover_color=COLORS['warning'],
            height=40
        ).pack(fill="x", padx=10, pady=10)
        
        # Основная область
        main_area = ctk.CTkFrame(self, fg_color=COLORS['dark'], corner_radius=0)
        main_area.pack(side="right", fill="both", expand=True)
        
        # Вкладки
        self.tabview = ctk.CTkTabview(main_area)
        self.tabview.pack(fill="both", expand=True, padx=15, pady=15)
        
        for tab_name in ["Пользователи", "Классы", "Предметы", "Расписание", "Статистика"]:
            self.tabview.add(tab_name)
            self.tabview.tab(tab_name).configure(fg_color=COLORS['card_bg'])
        
        self.tabview.configure(
            segmented_button_fg_color=COLORS['sidebar'],
            segmented_button_selected_color=COLORS['accent'],
            segmented_button_selected_hover_color=COLORS['secondary'],
            text_color=COLORS['text_light']
        )
        
        self.tabview._segmented_button.configure(font=FONTS['button'])
        
        self.setup_users_tab()
        self.setup_classes_tab()
        self.setup_subjects_tab()
        self.setup_schedule_tab()
        self.setup_stats_tab()
    
    def setup_users_tab(self):
        tab = self.tabview.tab("Пользователи")
        
        # Кнопки управления
        button_frame = ctk.CTkFrame(tab, fg_color="transparent")
        button_frame.pack(pady=8)
        
        buttons = [
            ("➕ Добавить", self.add_user, COLORS['primary']),
            ("✏️ Редактировать", self.edit_user, COLORS['info']),
            ("🔒 Блокировать", self.block_user, COLORS['warning']),
            ("🔓 Разблокировать", self.unblock_user, COLORS['accent']),
            ("🗑️ Удалить", self.delete_user, COLORS['error']),
            ("🔄 Обновить", self.load_users, COLORS['success'])
        ]
        
        for text, command, color in buttons:
            ModernButton(
                button_frame,
                text=text,
                command=command,
                fg_color=color,
                hover_color=COLORS['hover'],
                width=110
            ).pack(side="left", padx=1)
        
        # Таблица пользователей с прокруткой
        container = ctk.CTkFrame(tab, fg_color="transparent")
        container.pack(fill="both", expand=True, padx=8, pady=8)
        
        columns = ("ID", "Логин", "ФИО", "Роль", "Телефон", "Email", "Статус")
        self.users_tree = ttk.Treeview(container, columns=columns, show="headings", style="Treeview", height=20)
        
        column_widths = [50, 100, 200, 80, 120, 150, 100]
        for i, col in enumerate(columns):
            self.users_tree.heading(col, text=col)
            self.users_tree.column(col, width=column_widths[i])
        
        scrollbar_y = ttk.Scrollbar(container, orient="vertical", command=self.users_tree.yview)
        scrollbar_x = ttk.Scrollbar(container, orient="horizontal", command=self.users_tree.xview)
        self.users_tree.configure(yscrollcommand=scrollbar_y.set, xscrollcommand=scrollbar_x.set)
        
        self.users_tree.grid(row=0, column=0, sticky="nsew")
        scrollbar_y.grid(row=0, column=1, sticky="ns")
        scrollbar_x.grid(row=1, column=0, sticky="ew")
        
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        
        self.load_users()
    
    def load_users(self):
        connection = Database.get_connection()
        if connection is None:
            return
            
        try:
            cursor = connection.cursor()
            cursor.execute("""
                SELECT * FROM users 
                ORDER BY 
                    CASE role
                        WHEN 'admin' THEN 1
                        WHEN 'teacher' THEN 2
                        WHEN 'student' THEN 3
                        ELSE 4
                    END,
                    full_name
            """)
            users = Database.dict_fetchall(cursor)
            
            for item in self.users_tree.get_children():
                self.users_tree.delete(item)
            
            for user in users:
                status = "🔒 Заблокирован" if user['is_blocked'] else "✅ Активен"
                role_rus = {
                    'admin': 'Админ',
                    'teacher': 'Учитель',
                    'student': 'Ученик'
                }.get(user['role'], user['role'])
                
                self.users_tree.insert("", "end", values=(
                    user['user_id'],
                    user['username'],
                    user['full_name'],
                    role_rus,
                    user['phone'] or "---",
                    user['email'] or "---",
                    status
                ))
        except Exception as e:
            messagebox.showerror("Ошибка", f"Ошибка загрузки: {str(e)}")
        finally:
            connection.close()
    
    def add_user(self):
        RegistrationWindow(self)
    
    def edit_user(self):
        selected = self.users_tree.selection()
        if not selected:
            messagebox.showwarning("Внимание", "Выберите пользователя для редактирования")
            return
        
        user_data = self.users_tree.item(selected[0])['values']
        
        # Получаем оригинальные данные из базы для правильного отображения роли
        connection = Database.get_connection()
        if connection is None:
            return
            
        try:
            cursor = connection.cursor()
            cursor.execute("SELECT * FROM users WHERE user_id = ?", (user_data[0],))
            original_user = Database.dict_fetchone(cursor)
            
            if not original_user:
                messagebox.showerror("Ошибка", "Пользователь не найден")
                return
                
        except Exception as e:
            messagebox.showerror("Ошибка", f"Ошибка загрузки данных: {str(e)}")
            return
        finally:
            connection.close()
        
        dialog = ctk.CTkToplevel(self)
        dialog.title("✏️ Редактирование пользователя")
        
        window_width = 500
        window_height = 600
        
        dialog.geometry(f"{window_width}x{window_height}")
        dialog.resizable(False, False)
        dialog.transient(self)
        dialog.grab_set()
        dialog.after(10, lambda: self.center_window(dialog, window_width, window_height))
        
        main_frame = CardFrame(dialog)
        main_frame.pack(fill="both", expand=True, padx=15, pady=15)
        
        # Заголовок
        title_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        title_frame.pack(fill="x", padx=15, pady=10)
        
        ctk.CTkLabel(
            title_frame, 
            text="✏️ Редактирование пользователя", 
            font=FONTS['subtitle'],
            text_color=COLORS['text_light']
        ).pack(pady=(0, 8))
        
        # Контейнер с прокруткой
        canvas = tk.Canvas(main_frame, bg=COLORS['card_bg'], highlightthickness=0)
        scrollbar = ctk.CTkScrollbar(main_frame, orientation="vertical", command=canvas.yview)
        scrollable = ctk.CTkFrame(canvas, fg_color=COLORS['card_bg'])
        
        scrollable.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable, anchor="nw", width=440)
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Логин
        ctk.CTkLabel(
            scrollable, 
            text="Логин:", 
            font=FONTS['heading'],
            text_color=COLORS['text_light']
        ).pack(anchor="w", pady=(5, 2), padx=15)
        username_entry = ModernEntry(scrollable, width=300)
        username_entry.insert(0, user_data[1])
        username_entry.pack(fill="x", padx=15, pady=(0, 8))
        
        # Пароль
        ctk.CTkLabel(
            scrollable, 
            text="Новый пароль (оставьте пустым, чтобы не менять):", 
            font=FONTS['heading'],
            text_color=COLORS['text_light']
        ).pack(anchor="w", pady=(5, 2), padx=15)
        password_entry = ModernEntry(scrollable, width=300, show="•")
        password_entry.pack(fill="x", padx=15, pady=(0, 8))
        
        # ФИО
        ctk.CTkLabel(
            scrollable, 
            text="ФИО:", 
            font=FONTS['heading'],
            text_color=COLORS['text_light']
        ).pack(anchor="w", pady=(5, 2), padx=15)
        fullname_entry = ModernEntry(scrollable, width=300)
        fullname_entry.insert(0, user_data[2])
        fullname_entry.pack(fill="x", padx=15, pady=(0, 8))
        
        # Роль
        ctk.CTkLabel(
            scrollable, 
            text="Роль:", 
            font=FONTS['heading'],
            text_color=COLORS['text_light']
        ).pack(anchor="w", pady=(5, 2), padx=15)
        
        role_frame = CardFrame(scrollable)
        role_frame.pack(fill="x", padx=15, pady=(0, 8))
        
        current_role = original_user['role']
        self.role_var = tk.StringVar(value=current_role)
        
        roles = [
            ("admin", "Админ"),
            ("teacher", "Учитель"),
            ("student", "Ученик")
        ]
        
        for i, (role_value, role_text) in enumerate(roles):
            radio = ctk.CTkRadioButton(
                role_frame, 
                text=role_text, 
                variable=self.role_var, 
                value=role_value,
                font=FONTS['body'],
                fg_color=COLORS['primary'],
                hover_color=COLORS['secondary']
            )
            radio.pack(anchor="w", padx=15, pady=5 if i == 0 else 2)
        
        # Телефон с маской
        ctk.CTkLabel(
            scrollable, 
            text="Телефон:", 
            font=FONTS['heading'],
            text_color=COLORS['text_light']
        ).pack(anchor="w", pady=(5, 2), padx=15)
        
        phone_entry = ModernEntry(scrollable, width=300)
        
        # Получаем телефон из базы данных
        phone_text = original_user.get('phone', '')
        
        # Если есть телефон в базе, форматируем его
        if phone_text and phone_text.strip():
            # Извлекаем цифры из телефона
            digits = ''.join(filter(str.isdigit, str(phone_text)))
            
            # Форматируем в маску +7 (xxx) xxx-xx-xx
            if len(digits) == 11 and digits[0] == '7':  # Российский формат
                formatted = f"+7 ({digits[1:4]}) {digits[4:7]}-{digits[7:9]}-{digits[9:11]}"
                phone_entry.insert(0, formatted)
            elif len(digits) >= 10:
                # Если есть код страны, предполагаем что это 7
                if len(digits) == 10:
                    formatted = f"+7 ({digits[:3]}) {digits[3:6]}-{digits[6:8]}-{digits[8:10]}"
                else:
                    # Для других форматов просто показываем цифры
                    phone_entry.insert(0, phone_text)
            else:
                # Пустой телефон - ставим маску
                phone_entry.insert(0, "+7 (___) ___-__-__")
        else:
            # Пустой телефон - ставим маску
            phone_entry.insert(0, "+7 (___) ___-__-__")
        
        # Привязываем обработчики для форматирования
        phone_entry.bind('<KeyRelease>', self.format_phone)
        phone_entry.bind('<FocusIn>', self.on_phone_focus_in)
        phone_entry.bind('<FocusOut>', self.on_phone_focus_out)
        
        phone_entry.pack(fill="x", padx=15, pady=(0, 8))
        
        # Email
        ctk.CTkLabel(
            scrollable, 
            text="Email:", 
            font=FONTS['heading'],
            text_color=COLORS['text_light']
        ).pack(anchor="w", pady=(5, 2), padx=15)
        email_entry = ModernEntry(scrollable, width=300)
        email_text = original_user.get('email', '')
        if email_text:
            email_entry.insert(0, email_text)
        email_entry.pack(fill="x", padx=15, pady=(0, 8))
        
        # Кнопки
        button_frame = ctk.CTkFrame(scrollable, fg_color="transparent")
        button_frame.pack(pady=15)
        
        def save_changes():
            username = username_entry.get().strip()
            password = password_entry.get().strip()
            fullname = fullname_entry.get().strip()
            role = self.role_var.get()
            
            # Получаем телефон в формате маски и очищаем его
            phone_text = phone_entry.get().strip()
            
            # Если телефон - это просто маска (без цифр), устанавливаем пустое значение
            if phone_text == "+7 (___) ___-__-__":
                phone = ""
            else:
                # Извлекаем только цифры из телефона
                phone_digits = ''.join(filter(str.isdigit, phone_text))
                
                # Если введен только код страны (7), тоже считаем пустым
                if len(phone_digits) <= 1:
                    phone = ""
                else:
                    phone = phone_digits
            
            email = email_entry.get().strip()
            
            if not username or not fullname:
                messagebox.showwarning("Ошибка", "Заполните обязательные поля")
                return
            
            # Валидация телефона (если введен)
            if phone:
                if len(phone) < 10:
                    messagebox.showwarning("Ошибка", "Номер телефона должен содержать 10 цифр (без кода страны)")
                    return
                if len(phone) > 15:
                    messagebox.showwarning("Ошибка", "Слишком длинный номер телефона")
                    return
            
            connection = Database.get_connection()
            if connection is None:
                return
                
            try:
                cursor = connection.cursor()
                if password:
                    cursor.execute("""
                        UPDATE users 
                        SET username = ?, password = ?, full_name = ?, 
                            role = ?, phone = ?, email = ?
                        WHERE user_id = ?
                    """, (username, password, fullname, role, phone or None, email or None, user_data[0]))
                else:
                    cursor.execute("""
                        UPDATE users 
                        SET username = ?, full_name = ?, 
                            role = ?, phone = ?, email = ?
                        WHERE user_id = ?
                    """, (username, fullname, role, phone or None, email or None, user_data[0]))
                
                connection.commit()
                messagebox.showinfo("Успех", "✅ Данные пользователя обновлены!")
                self.load_users()
                dialog.destroy()
                    
            except Exception as e:
                messagebox.showerror("Ошибка", f"Ошибка обновления: {str(e)}")
            finally:
                connection.close()
        
        ModernButton(
            button_frame,
            text="💾 Сохранить",
            command=save_changes,
            fg_color=COLORS['success'],
            hover_color=COLORS['info'],
            width=110
        ).pack(side="left", padx=3)
        
        ModernButton(
            button_frame,
            text="❌ Отмена",
            command=dialog.destroy,
            fg_color=COLORS['error'],
            hover_color=COLORS['warning'],
            width=110
        ).pack(side="left", padx=3)
    
    def on_phone_focus_in(self, event):
        """При фокусе на поле телефона - устанавливаем курсор на первую цифру"""
        widget = event.widget
        current_text = widget.get()
        
        # Ищем первую подчеркивание для установки курсора
        try:
            cursor_pos = current_text.index('_')
            widget.icursor(cursor_pos)
        except ValueError:
            # Если подчеркиваний нет, ставим курсор в конец цифр
            digits_only = ''.join([c for c in current_text if c.isdigit()])
            if digits_only:
                # Ищем позицию после последней цифры
                for i, char in enumerate(current_text):
                    if char.isdigit():
                        last_digit_pos = i
                widget.icursor(last_digit_pos + 1)
            else:
                widget.icursor(2)  # после "+7"
    
    def on_phone_focus_out(self, event):
        """При потере фокуса - если номер пустой, восстанавливаем маску"""
        widget = event.widget
        current_text = widget.get()
        
        # Если номер пустой (только маска), восстанавливаем полную маску
        digits = ''.join([c for c in current_text if c.isdigit()])
        if len(digits) == 0:
            widget.delete(0, tk.END)
            widget.insert(0, "+7 (___) ___-__-__")
    
    def format_phone(self, event):
        """Форматирование номера телефона по маске +7 (xxx) xxx-xx-xx"""
        widget = event.widget
        current_text = widget.get()
        
        # Сохраняем позицию курсора
        cursor_pos = widget.index(tk.INSERT)
        
        # Удаляем все нецифры кроме +, (, ), -, пробелов и подчеркиваний
        allowed_chars = ['+', '(', ')', ' ', '-', '_']
        filtered_chars = []
        for char in current_text:
            if char.isdigit() or char in allowed_chars:
                filtered_chars.append(char)
        filtered_text = ''.join(filtered_chars)
        
        # Извлекаем только цифры
        digits = ''.join([c for c in filtered_text if c.isdigit()])
        
        # Ограничиваем длину (максимум 11 цифр: 1 код страны + 10 номера)
        if len(digits) > 11:
            digits = digits[:11]
        
        # Если есть код страны, оставляем его, иначе ставим 7 по умолчанию
        if digits:
            if len(digits) >= 1:
                country_code = digits[0]
                number_digits = digits[1:]
            else:
                country_code = '7'
                number_digits = ''
        else:
            country_code = '7'
            number_digits = ''
        
        # Формируем номер по маске
        formatted = f"+{country_code}"
        
        if number_digits or '_' in current_text:
            formatted += " ("
            
            # Первые 3 цифры номера или подчеркивания
            if len(number_digits) >= 1:
                formatted += number_digits[:3]
                remaining = number_digits[3:]
            else:
                formatted += "___"
                remaining = ""
            
            formatted += ")"
            
            # Если есть еще цифры или мы редактируем
            if remaining or cursor_pos > len(formatted):
                formatted += " "
                
                # Следующие 3 цифры
                if len(remaining) >= 1:
                    formatted += remaining[:3]
                    remaining = remaining[3:]
                else:
                    formatted += "___"
                
                formatted += "-"
                
                # Следующие 2 цифры
                if len(remaining) >= 1:
                    formatted += remaining[:2]
                    remaining = remaining[2:]
                else:
                    formatted += "__"
                
                formatted += "-"
                
                # Последние 2 цифры
                if len(remaining) >= 1:
                    formatted += remaining[:2]
                else:
                    formatted += "__"
            else:
                # Дополняем оставшуюся часть маской
                formatted += " ___-__-__"
        
        # Обновляем поле ввода, если текст изменился
        if formatted != current_text:
            widget.delete(0, tk.END)
            widget.insert(0, formatted)
            
            # Восстанавливаем позицию курсора
            try:
                # Пытаемся найти ту же относительную позицию
                if cursor_pos < len(formatted):
                    # Если курсор был на цифре, стараемся поставить его на цифру
                    if cursor_pos < len(current_text) and current_text[cursor_pos-1:cursor_pos].isdigit():
                        # Ищем следующую цифру в новой строке
                        new_pos = cursor_pos
                        while new_pos < len(formatted) and not formatted[new_pos].isdigit():
                            new_pos += 1
                        if new_pos < len(formatted):
                            widget.icursor(new_pos + 1)
                        else:
                            widget.icursor(len(formatted))
                    else:
                        widget.icursor(cursor_pos)
                else:
                    widget.icursor(len(formatted))
            except:
                widget.icursor(len(formatted))
    
    def block_user(self):
        selected = self.users_tree.selection()
        if not selected:
            messagebox.showwarning("Внимание", "Выберите пользователя для блокировки")
            return
        
        user_data = self.users_tree.item(selected[0])['values']
        
        if "Заблокирован" in user_data[6]:
            messagebox.showwarning("Внимание", "Пользователь уже заблокирован")
            return
        
        if messagebox.askyesno("Подтверждение", f"Заблокировать пользователя {user_data[2]}?"):
            connection = Database.get_connection()
            if connection is None:
                return
                
            try:
                cursor = connection.cursor()
                cursor.execute("""
                    UPDATE users 
                    SET is_blocked = 1 
                    WHERE user_id = ?
                """, (user_data[0],))
                
                connection.commit()
                messagebox.showinfo("Успех", "✅ Пользователь заблокирован!")
                self.load_users()
                    
            except Exception as e:
                messagebox.showerror("Ошибка", f"Ошибка блокировки: {str(e)}")
            finally:
                connection.close()
    
    def unblock_user(self):
        selected = self.users_tree.selection()
        if not selected:
            messagebox.showwarning("Внимание", "Выберите пользователя для разблокировки")
            return
        
        user_data = self.users_tree.item(selected[0])['values']
        
        if "Активен" in user_data[6]:
            messagebox.showwarning("Внимание", "Пользователь уже активен")
            return
        
        if messagebox.askyesno("Подтверждение", f"Разблокировать пользователя {user_data[2]}?"):
            connection = Database.get_connection()
            if connection is None:
                return
                
            try:
                cursor = connection.cursor()
                cursor.execute("""
                    UPDATE users 
                    SET is_blocked = 0, failed_attempts = 0 
                    WHERE user_id = ?
                """, (user_data[0],))
                
                connection.commit()
                messagebox.showinfo("Успех", "✅ Пользователь разблокирован!")
                self.load_users()
                    
            except Exception as e:
                messagebox.showerror("Ошибка", f"Ошибка: {str(e)}")
            finally:
                connection.close()
    
    # ИСПРАВЛЕННЫЙ МЕТОД delete_user
    def delete_user(self):
        selected = self.users_tree.selection()
        if not selected:
            messagebox.showwarning("Внимание", "Выберите пользователя для удаления")
            return
        
        user_data = self.users_tree.item(selected[0])['values']
        user_id = user_data[0]  # ID пользователя (строка, но в SQL передадим как есть)
        user_name = user_data[2]
        
        # Предупреждение о каскадном удалении
        if not messagebox.askyesno("Подтверждение", 
                                  f"Вы действительно хотите удалить пользователя {user_name}?\n\n"
                                  "Будут также удалены:\n"
                                  "- Все оценки (как ученика, так и выставленные им как учителем)\n"
                                  "- Все записи посещаемости\n"
                                  "- Все домашние задания, созданные им\n"
                                  "- Все записи в расписании, где он указан как учитель\n"
                                  "- Классное руководство (будет снято)\n"
                                  "Это действие необратимо!"):
            return
        
        connection = Database.get_connection()
        if connection is None:
            return
        
        try:
            cursor = connection.cursor()
            # Начинаем транзакцию (автоматически, так как autocommit = False по умолчанию)
            
            # 1. Удаление из attendance (где студент)
            cursor.execute("DELETE FROM attendance WHERE student_id = ?", (user_id,))
            
            # 2. Удаление из grades (где студент)
            cursor.execute("DELETE FROM grades WHERE student_id = ?", (user_id,))
            
            # 3. Удаление из grades (где учитель)
            cursor.execute("DELETE FROM grades WHERE teacher_id = ?", (user_id,))
            
            # 4. Удаление из homework (где учитель)
            cursor.execute("DELETE FROM homework WHERE teacher_id = ?", (user_id,))
            
            # 5. Удаление из schedule (где учитель)
            cursor.execute("DELETE FROM schedule WHERE teacher_id = ?", (user_id,))
            
            # 6. Обновление классов, где он был классным руководителем (установить NULL)
            cursor.execute("UPDATE classes SET class_teacher_id = NULL WHERE class_teacher_id = ?", (user_id,))
            
            # 7. Наконец, удаление самого пользователя
            cursor.execute("DELETE FROM users WHERE user_id = ?", (user_id,))
            
            # Подтверждаем транзакцию
            connection.commit()
            
            messagebox.showinfo("Успех", f"✅ Пользователь {user_name} и все связанные данные удалены!")
            self.load_users()  # обновляем список
            
        except Exception as e:
            # Если ошибка, откат произойдет автоматически при закрытии соединения без commit
            messagebox.showerror("Ошибка", f"Не удалось удалить пользователя: {str(e)}")
        finally:
            connection.close()
    
    def setup_classes_tab(self):
        tab = self.tabview.tab("Классы")
        
        # Кнопки управления
        button_frame = ctk.CTkFrame(tab, fg_color="transparent")
        button_frame.pack(pady=8)
        
        buttons = [
            ("➕ Добавить", self.add_class, COLORS['primary']),
            ("✏️ Редактировать", self.edit_class, COLORS['info']),
            ("🗑️ Удалить", self.delete_class, COLORS['error']),
            ("🔄 Обновить", self.load_classes_admin, COLORS['success'])
        ]
        
        for text, command, color in buttons:
            ModernButton(
                button_frame,
                text=text,
                command=command,
                fg_color=color,
                hover_color=COLORS['hover'],
                width=110
            ).pack(side="left", padx=1)
        
        # Таблица классов с прокруткой
        container = ctk.CTkFrame(tab, fg_color="transparent")
        container.pack(fill="both", expand=True, padx=8, pady=8)
        
        columns = ("ID", "Класс", "Год обучения", "Учебный год", "Классный руководитель", "Учеников")
        self.classes_tree = ttk.Treeview(container, columns=columns, show="headings", style="Treeview", height=20)
        
        column_widths = [50, 80, 100, 100, 200, 80]
        for i, col in enumerate(columns):
            self.classes_tree.heading(col, text=col)
            self.classes_tree.column(col, width=column_widths[i])
        
        scrollbar_y = ttk.Scrollbar(container, orient="vertical", command=self.classes_tree.yview)
        scrollbar_x = ttk.Scrollbar(container, orient="horizontal", command=self.classes_tree.xview)
        self.classes_tree.configure(yscrollcommand=scrollbar_y.set, xscrollcommand=scrollbar_x.set)
        
        self.classes_tree.grid(row=0, column=0, sticky="nsew")
        scrollbar_y.grid(row=0, column=1, sticky="ns")
        scrollbar_x.grid(row=1, column=0, sticky="ew")
        
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        
        self.load_classes_admin()
    
    def load_classes_admin(self):
        connection = Database.get_connection()
        if connection is None:
            return
            
        try:
            cursor = connection.cursor()
            cursor.execute("""
                SELECT c.*, u.full_name as teacher_name,
                       COUNT(st.user_id) as student_count
                FROM classes c
                LEFT JOIN users u ON c.class_teacher_id = u.user_id
                LEFT JOIN users st ON c.class_id = st.class_id AND st.role = 'student'
                GROUP BY c.class_id, c.class_name, c.grade, c.academic_year, 
                         c.class_teacher_id, u.full_name
                ORDER BY c.grade, c.class_name
            """)
            classes = Database.dict_fetchall(cursor)
            
            for item in self.classes_tree.get_children():
                self.classes_tree.delete(item)
            
            for cls in classes:
                self.classes_tree.insert("", "end", values=(
                    cls['class_id'],
                    cls['class_name'],
                    cls['grade'],
                    cls['academic_year'] or "---",
                    cls['teacher_name'] or "---",
                    cls['student_count']
                ))
        except Exception as e:
            messagebox.showerror("Ошибка", f"Ошибка загрузки: {str(e)}")
        finally:
            connection.close()
    
    def add_class(self):
        dialog = ctk.CTkToplevel(self)
        dialog.title("➕ Добавить класс")
        
        window_width = 400
        window_height = 350
        
        dialog.geometry(f"{window_width}x{window_height}")
        dialog.transient(self)
        dialog.grab_set()
        dialog.after(10, lambda: self.center_window(dialog, window_width, window_height))
        
        main_frame = CardFrame(dialog)
        main_frame.pack(fill="both", expand=True, padx=15, pady=15)
        
        ctk.CTkLabel(
            main_frame, 
            text="➕ Новый класс", 
            font=FONTS['subtitle'],
            text_color=COLORS['text_light']
        ).pack(pady=(15, 15))
        
        # Название класса
        ctk.CTkLabel(
            main_frame, 
            text="Название класса (например, 10А):", 
            font=FONTS['heading'],
            text_color=COLORS['text_light']
        ).pack(anchor="w", pady=(5, 2), padx=15)
        name_entry = ModernEntry(main_frame)
        name_entry.pack(fill="x", padx=15, pady=(0, 8))
        
        # Год обучения
        ctk.CTkLabel(
            main_frame, 
            text="Год обучения (1-11):", 
            font=FONTS['heading'],
            text_color=COLORS['text_light']
        ).pack(anchor="w", pady=(5, 2), padx=15)
        grade_entry = ModernEntry(main_frame)
        grade_entry.pack(fill="x", padx=15, pady=(0, 8))
        
        # Учебный год
        ctk.CTkLabel(
            main_frame, 
            text="Учебный год (например, 2026-2027):",
            font=FONTS['heading'],
            text_color=COLORS['text_light']
        ).pack(anchor="w", pady=(5, 2), padx=15)
        year_entry = ModernEntry(main_frame)
        year_entry.pack(fill="x", padx=15, pady=(0, 8))
        
        def save_class():
            name = name_entry.get().strip()
            grade = grade_entry.get().strip()
            year = year_entry.get().strip()
            
            if not name or not grade:
                messagebox.showwarning("Ошибка", "Заполните обязательные поля")
                return
            
            try:
                grade_int = int(grade)
                if grade_int < 1 or grade_int > 11:
                    raise ValueError
            except ValueError:
                messagebox.showerror("Ошибка", "Год обучения должен быть числом от 1 до 11")
                return
            
            connection = Database.get_connection()
            if connection is None:
                return
                
            try:
                cursor = connection.cursor()
                cursor.execute("""
                    INSERT INTO classes (class_name, grade, academic_year)
                    VALUES (?, ?, ?)
                """, (name, grade_int, year or None))
                
                connection.commit()
                messagebox.showinfo("Успех", "✅ Класс добавлен!")
                self.load_classes_admin()
                dialog.destroy()
                    
            except Exception as e:
                messagebox.showerror("Ошибка", f"Ошибка добавления: {str(e)}")
            finally:
                connection.close()
        
        # Кнопки
        button_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        button_frame.pack(pady=15)
        
        ModernButton(
            button_frame,
            text="💾 Сохранить",
            command=save_class,
            fg_color=COLORS['success'],
            hover_color=COLORS['info'],
            width=110
        ).pack(side="left", padx=3)
        
        ModernButton(
            button_frame,
            text="❌ Отмена",
            command=dialog.destroy,
            fg_color=COLORS['error'],
            hover_color=COLORS['warning'],
            width=110
        ).pack(side="left", padx=3)
    
    def edit_class(self):
        selected = self.classes_tree.selection()
        if not selected:
            messagebox.showwarning("Внимание", "Выберите класс для редактирования")
            return
        
        class_data = self.classes_tree.item(selected[0])['values']
        
        dialog = ctk.CTkToplevel(self)
        dialog.title("✏️ Редактирование класса")
        
        window_width = 400
        window_height = 350
        
        dialog.geometry(f"{window_width}x{window_height}")
        dialog.transient(self)
        dialog.grab_set()
        dialog.after(10, lambda: self.center_window(dialog, window_width, window_height))
        
        main_frame = CardFrame(dialog)
        main_frame.pack(fill="both", expand=True, padx=15, pady=15)
        
        ctk.CTkLabel(
            main_frame, 
            text="✏️ Редактирование класса", 
            font=FONTS['subtitle'],
            text_color=COLORS['text_light']
        ).pack(pady=(15, 15))
        
        # Название класса
        ctk.CTkLabel(
            main_frame, 
            text="Название класса:", 
            font=FONTS['heading'],
            text_color=COLORS['text_light']
        ).pack(anchor="w", pady=(5, 2), padx=15)
        name_entry = ModernEntry(main_frame)
        name_entry.insert(0, class_data[1])
        name_entry.pack(fill="x", padx=15, pady=(0, 8))
        
        # Год обучения
        ctk.CTkLabel(
            main_frame, 
            text="Год обучения:", 
            font=FONTS['heading'],
            text_color=COLORS['text_light']
        ).pack(anchor="w", pady=(5, 2), padx=15)
        grade_entry = ModernEntry(main_frame)
        grade_entry.insert(0, class_data[2])
        grade_entry.pack(fill="x", padx=15, pady=(0, 8))
        
        # Учебный год
        ctk.CTkLabel(
            main_frame, 
            text="Учебный год:", 
            font=FONTS['heading'],
            text_color=COLORS['text_light']
        ).pack(anchor="w", pady=(5, 2), padx=15)
        year_entry = ModernEntry(main_frame)
        year_entry.insert(0, class_data[3] if class_data[3] != "---" else "")
        year_entry.pack(fill="x", padx=15, pady=(0, 8))
        
        def save_changes():
            name = name_entry.get().strip()
            grade = grade_entry.get().strip()
            year = year_entry.get().strip()
            
            if not name or not grade:
                messagebox.showwarning("Ошибка", "Заполните обязательные поля")
                return
            
            try:
                grade_int = int(grade)
                if grade_int < 1 or grade_int > 11:
                    raise ValueError
            except ValueError:
                messagebox.showerror("Ошибка", "Год обучения должен быть числом от 1 до 11")
                return
            
            connection = Database.get_connection()
            if connection is None:
                return
                
            try:
                cursor = connection.cursor()
                cursor.execute("""
                    UPDATE classes 
                    SET class_name = ?, grade = ?, academic_year = ?
                    WHERE class_id = ?
                """, (name, grade_int, year or None, class_data[0]))
                
                connection.commit()
                messagebox.showinfo("Успех", "✅ Класс обновлен!")
                self.load_classes_admin()
                dialog.destroy()
                    
            except Exception as e:
                messagebox.showerror("Ошибка", f"Ошибка обновления: {str(e)}")
            finally:
                connection.close()
        
        # Кнопки
        button_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        button_frame.pack(pady=15)
        
        ModernButton(
            button_frame,
            text="💾 Сохранить",
            command=save_changes,
            fg_color=COLORS['success'],
            hover_color=COLORS['info'],
            width=110
        ).pack(side="left", padx=3)
        
        ModernButton(
            button_frame,
            text="❌ Отмена",
            command=dialog.destroy,
            fg_color=COLORS['error'],
            hover_color=COLORS['warning'],
            width=110
        ).pack(side="left", padx=3)
    
    def delete_class(self):
        selected = self.classes_tree.selection()
        if not selected:
            messagebox.showwarning("Внимание", "Выберите класс")
            return
        
        class_data = self.classes_tree.item(selected[0])['values']
        
        if messagebox.askyesno("Подтверждение", f"Удалить класс {class_data[1]}?\nВсе связанные данные будут удалены!"):
            connection = Database.get_connection()
            if connection is None:
                return
                
            try:
                cursor = connection.cursor()
                cursor.execute("DELETE FROM classes WHERE class_id = ?", (class_data[0],))
                
                connection.commit()
                messagebox.showinfo("Успех", "✅ Класс удален!")
                self.load_classes_admin()
                    
            except Exception as e:
                messagebox.showerror("Ошибка", f"Ошибка удаления: {str(e)}")
            finally:
                connection.close()
    
    def setup_subjects_tab(self):
        tab = self.tabview.tab("Предметы")
        
        # Кнопки управления
        button_frame = ctk.CTkFrame(tab, fg_color="transparent")
        button_frame.pack(pady=8)
        
        buttons = [
            ("➕ Добавить", self.add_subject, COLORS['primary']),
            ("✏️ Редактировать", self.edit_subject, COLORS['info']),
            ("🗑️ Удалить", self.delete_subject, COLORS['error']),
            ("🔄 Обновить", self.load_subjects_admin, COLORS['success'])
        ]
        
        for text, command, color in buttons:
            ModernButton(
                button_frame,
                text=text,
                command=command,
                fg_color=color,
                hover_color=COLORS['hover'],
                width=110
            ).pack(side="left", padx=1)
        
        # Таблица предметов с прокруткой
        container = ctk.CTkFrame(tab, fg_color="transparent")
        container.pack(fill="both", expand=True, padx=8, pady=8)
        
        columns = ("ID", "Название", "Описание")
        self.subjects_tree = ttk.Treeview(container, columns=columns, show="headings", style="Treeview", height=20)
        
        column_widths = [50, 150, 500]
        for i, col in enumerate(columns):
            self.subjects_tree.heading(col, text=col)
            self.subjects_tree.column(col, width=column_widths[i])
        
        scrollbar_y = ttk.Scrollbar(container, orient="vertical", command=self.subjects_tree.yview)
        scrollbar_x = ttk.Scrollbar(container, orient="horizontal", command=self.subjects_tree.xview)
        self.subjects_tree.configure(yscrollcommand=scrollbar_y.set, xscrollcommand=scrollbar_x.set)
        
        self.subjects_tree.grid(row=0, column=0, sticky="nsew")
        scrollbar_y.grid(row=0, column=1, sticky="ns")
        scrollbar_x.grid(row=1, column=0, sticky="ew")
        
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        
        self.load_subjects_admin()
    
    def load_subjects_admin(self):
        connection = Database.get_connection()
        if connection is None:
            return
            
        try:
            cursor = connection.cursor()
            cursor.execute("SELECT * FROM subjects ORDER BY subject_name")
            subjects = Database.dict_fetchall(cursor)
            
            for item in self.subjects_tree.get_children():
                self.subjects_tree.delete(item)
            
            for subject in subjects:
                desc = subject['description'] or "---"
                self.subjects_tree.insert("", "end", values=(
                    subject['subject_id'],
                    subject['subject_name'],
                    desc
                ))
        except Exception as e:
            messagebox.showerror("Ошибка", f"Ошибка загрузки: {str(e)}")
        finally:
            connection.close()
    
    def add_subject(self):
        dialog = ctk.CTkToplevel(self)
        dialog.title("➕ Добавить предмет")
        
        window_width = 400
        window_height = 300
        
        dialog.geometry(f"{window_width}x{window_height}")
        dialog.transient(self)
        dialog.grab_set()
        dialog.after(10, lambda: self.center_window(dialog, window_width, window_height))
        
        main_frame = CardFrame(dialog)
        main_frame.pack(fill="both", expand=True, padx=15, pady=15)
        
        ctk.CTkLabel(
            main_frame, 
            text="➕ Новый предмет", 
            font=FONTS['subtitle'],
            text_color=COLORS['text_light']
        ).pack(pady=(15, 15))
        
        # Название предмета
        ctk.CTkLabel(
            main_frame, 
            text="Название предмета:", 
            font=FONTS['heading'],
            text_color=COLORS['text_light']
        ).pack(anchor="w", pady=(5, 2), padx=15)
        name_entry = ModernEntry(main_frame)
        name_entry.pack(fill="x", padx=15, pady=(0, 8))
        
        # Описание
        ctk.CTkLabel(
            main_frame, 
            text="Описание:", 
            font=FONTS['heading'],
            text_color=COLORS['text_light']
        ).pack(anchor="w", pady=(5, 2), padx=15)
        desc_entry = ctk.CTkTextbox(main_frame, height=80, font=FONTS['body'])
        desc_entry.pack(fill="x", padx=15, pady=(0, 8))
        
        def save_subject():
            name = name_entry.get().strip()
            desc = desc_entry.get("1.0", "end-1c").strip()
            
            if not name:
                messagebox.showwarning("Ошибка", "Введите название предмета")
                return
            
            connection = Database.get_connection()
            if connection is None:
                return
                
            try:
                cursor = connection.cursor()
                cursor.execute("""
                    INSERT INTO subjects (subject_name, description)
                    VALUES (?, ?)
                """, (name, desc or None))
                
                connection.commit()
                messagebox.showinfo("Успех", "✅ Предмет добавлен!")
                self.load_subjects_admin()
                dialog.destroy()
                    
            except Exception as e:
                messagebox.showerror("Ошибка", f"Ошибка добавления: {str(e)}")
            finally:
                connection.close()
        
        # Кнопки
        button_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        button_frame.pack(pady=15)
        
        ModernButton(
            button_frame,
            text="💾 Сохранить",
            command=save_subject,
            fg_color=COLORS['success'],
            hover_color=COLORS['info'],
            width=110
        ).pack(side="left", padx=3)
        
        ModernButton(
            button_frame,
            text="❌ Отмена",
            command=dialog.destroy,
            fg_color=COLORS['error'],
            hover_color=COLORS['warning'],
            width=110
        ).pack(side="left", padx=3)
    
    def edit_subject(self):
        selected = self.subjects_tree.selection()
        if not selected:
            messagebox.showwarning("Внимание", "Выберите предмет для редактирования")
            return
        
        subject_data = self.subjects_tree.item(selected[0])['values']
        
        dialog = ctk.CTkToplevel(self)
        dialog.title("✏️ Редактирование предмета")
        
        window_width = 400
        window_height = 300
        
        dialog.geometry(f"{window_width}x{window_height}")
        dialog.transient(self)
        dialog.grab_set()
        dialog.after(10, lambda: self.center_window(dialog, window_width, window_height))
        
        main_frame = CardFrame(dialog)
        main_frame.pack(fill="both", expand=True, padx=15, pady=15)
        
        ctk.CTkLabel(
            main_frame, 
            text="✏️ Редактирование предмета", 
            font=FONTS['subtitle'],
            text_color=COLORS['text_light']
        ).pack(pady=(15, 15))
        
        # Название предмета
        ctk.CTkLabel(
            main_frame, 
            text="Название предмета:", 
            font=FONTS['heading'],
            text_color=COLORS['text_light']
        ).pack(anchor="w", pady=(5, 2), padx=15)
        name_entry = ModernEntry(main_frame)
        name_entry.insert(0, subject_data[1])
        name_entry.pack(fill="x", padx=15, pady=(0, 8))
        
        # Описание
        ctk.CTkLabel(
            main_frame, 
            text="Описание:", 
            font=FONTS['heading'],
            text_color=COLORS['text_light']
        ).pack(anchor="w", pady=(5, 2), padx=15)
        desc_entry = ctk.CTkTextbox(main_frame, height=80, font=FONTS['body'])
        desc_entry.insert("1.0", subject_data[2] if subject_data[2] != "---" else "")
        desc_entry.pack(fill="x", padx=15, pady=(0, 8))
        
        def save_changes():
            name = name_entry.get().strip()
            desc = desc_entry.get("1.0", "end-1c").strip()
            
            if not name:
                messagebox.showwarning("Ошибка", "Введите название предмета")
                return
            
            connection = Database.get_connection()
            if connection is None:
                return
                
            try:
                cursor = connection.cursor()
                cursor.execute("""
                    UPDATE subjects 
                    SET subject_name = ?, description = ?
                    WHERE subject_id = ?
                """, (name, desc or None, subject_data[0]))
                
                connection.commit()
                messagebox.showinfo("Успех", "✅ Предмет обновлен!")
                self.load_subjects_admin()
                dialog.destroy()
                    
            except Exception as e:
                messagebox.showerror("Ошибка", f"Ошибка обновления: {str(e)}")
            finally:
                connection.close()
        
        # Кнопки
        button_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        button_frame.pack(pady=15)
        
        ModernButton(
            button_frame,
            text="💾 Сохранить",
            command=save_changes,
            fg_color=COLORS['success'],
            hover_color=COLORS['info'],
            width=110
        ).pack(side="left", padx=3)
        
        ModernButton(
            button_frame,
            text="❌ Отмена",
            command=dialog.destroy,
            fg_color=COLORS['error'],
            hover_color=COLORS['warning'],
            width=110
        ).pack(side="left", padx=3)
    
    def delete_subject(self):
        selected = self.subjects_tree.selection()
        if not selected:
            messagebox.showwarning("Внимание", "Выберите предмет")
            return
        
        subject_data = self.subjects_tree.item(selected[0])['values']
        
        if messagebox.askyesno("Подтверждение", f"Удалить предмет '{subject_data[1]}'?"):
            connection = Database.get_connection()
            if connection is None:
                return
                
            try:
                cursor = connection.cursor()
                cursor.execute("DELETE FROM subjects WHERE subject_id = ?", (subject_data[0],))
                
                connection.commit()
                messagebox.showinfo("Успех", "✅ Предмет удален!")
                self.load_subjects_admin()
                    
            except Exception as e:
                messagebox.showerror("Ошибка", f"Ошибка удаления: {str(e)}")
            finally:
                connection.close()
    
    def setup_schedule_tab(self):
        tab = self.tabview.tab("Расписание")
        
        # Кнопки управления
        button_frame = ctk.CTkFrame(tab, fg_color="transparent")
        button_frame.pack(pady=8)
        
        buttons = [
            ("➕ Добавить", self.add_schedule, COLORS['primary']),
            ("✏️ Редактировать", self.edit_schedule, COLORS['info']),
            ("🗑️ Удалить", self.delete_schedule, COLORS['error']),
            ("🔄 Обновить", self.load_schedule_admin, COLORS['success'])
        ]
        
        for text, command, color in buttons:
            ModernButton(
                button_frame,
                text=text,
                command=command,
                fg_color=color,
                hover_color=COLORS['hover'],
                width=110
            ).pack(side="left", padx=1)
        
        # Таблица расписания с прокруткой
        container = ctk.CTkFrame(tab, fg_color="transparent")
        container.pack(fill="both", expand=True, padx=8, pady=8)
        
        columns = ("ID", "Класс", "День", "Урок", "Предмет", "Учитель", "Кабинет")
        self.schedule_tree = ttk.Treeview(container, columns=columns, show="headings", style="Treeview", height=20)
        
        column_widths = [50, 80, 100, 50, 150, 150, 80]
        for i, col in enumerate(columns):
            self.schedule_tree.heading(col, text=col)
            self.schedule_tree.column(col, width=column_widths[i])
        
        scrollbar_y = ttk.Scrollbar(container, orient="vertical", command=self.schedule_tree.yview)
        scrollbar_x = ttk.Scrollbar(container, orient="horizontal", command=self.schedule_tree.xview)
        self.schedule_tree.configure(yscrollcommand=scrollbar_y.set, xscrollcommand=scrollbar_x.set)
        
        self.schedule_tree.grid(row=0, column=0, sticky="nsew")
        scrollbar_y.grid(row=0, column=1, sticky="ns")
        scrollbar_x.grid(row=1, column=0, sticky="ew")
        
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        
        self.load_schedule_admin()
    
    def load_schedule_admin(self):
        connection = Database.get_connection()
        if connection is None:
            return
            
        try:
            cursor = connection.cursor()
            cursor.execute("""
                SELECT s.*, c.class_name, sub.subject_name, u.full_name as teacher_name
                FROM schedule s
                JOIN classes c ON s.class_id = c.class_id
                JOIN subjects sub ON s.subject_id = sub.subject_id
                JOIN users u ON s.teacher_id = u.user_id
                ORDER BY 
                    CASE s.day_of_week
                        WHEN 'Понедельник' THEN 1
                        WHEN 'Вторник' THEN 2
                        WHEN 'Среда' THEN 3
                        WHEN 'Четверг' THEN 4
                        WHEN 'Пятница' THEN 5
                        WHEN 'Суббота' THEN 6
                        ELSE 7
                    END,
                    s.lesson_number
            """)
            schedule = Database.dict_fetchall(cursor)
            
            for item in self.schedule_tree.get_children():
                self.schedule_tree.delete(item)
            
            for item in schedule:
                self.schedule_tree.insert("", "end", values=(
                    item['schedule_id'],
                    item['class_name'],
                    item['day_of_week'],
                    item['lesson_number'],
                    item['subject_name'],
                    item['teacher_name'],
                    item['room'] or "---"
                ))
        except Exception as e:
            messagebox.showerror("Ошибка", f"Ошибка загрузки: {str(e)}")
        finally:
            connection.close()
    
    def add_schedule(self):
        dialog = ctk.CTkToplevel(self)
        dialog.title("➕ Добавить урок в расписание")
        
        window_width = 400
        window_height = 500
        
        dialog.geometry(f"{window_width}x{window_height}")
        dialog.transient(self)
        dialog.grab_set()
        dialog.after(10, lambda: self.center_window(dialog, window_width, window_height))
        
        main_frame = CardFrame(dialog)
        main_frame.pack(fill="both", expand=True, padx=15, pady=15)
        
        # Контейнер с прокруткой
        canvas = tk.Canvas(main_frame, bg=COLORS['card_bg'], highlightthickness=0)
        scrollbar = ctk.CTkScrollbar(main_frame, orientation="vertical", command=canvas.yview)
        scrollable = ctk.CTkFrame(canvas, fg_color=COLORS['card_bg'])
        
        scrollable.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable, anchor="nw", width=340)
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        ctk.CTkLabel(
            scrollable, 
            text="➕ Новый урок", 
            font=FONTS['subtitle'],
            text_color=COLORS['text_light']
        ).pack(pady=(10, 10))
        
        # Класс
        ctk.CTkLabel(
            scrollable, 
            text="Класс:", 
            font=FONTS['heading'],
            text_color=COLORS['text_light']
        ).pack(anchor="w", pady=(5, 2), padx=15)
        class_combo = ttk.Combobox(scrollable, font=FONTS['body'], width=25)
        class_combo.pack(fill="x", padx=15, pady=(0, 8))
        
        # День недели
        ctk.CTkLabel(
            scrollable, 
            text="День недели:", 
            font=FONTS['heading'],
            text_color=COLORS['text_light']
        ).pack(anchor="w", pady=(5, 2), padx=15)
        day_combo = ttk.Combobox(
            scrollable, 
            values=['Понедельник', 'Вторник', 'Среда', 'Четверг', 'Пятница', 'Суббота'], 
            font=FONTS['body'],
            width=25
        )
        day_combo.pack(fill="x", padx=15, pady=(0, 8))
        
        # Номер урока
        ctk.CTkLabel(
            scrollable, 
            text="Номер урока:", 
            font=FONTS['heading'],
            text_color=COLORS['text_light']
        ).pack(anchor="w", pady=(5, 2), padx=15)
        lesson_entry = ModernEntry(scrollable)
        lesson_entry.pack(fill="x", padx=15, pady=(0, 8))
        
        # Предмет
        ctk.CTkLabel(
            scrollable, 
            text="Предмет:", 
            font=FONTS['heading'],
            text_color=COLORS['text_light']
        ).pack(anchor="w", pady=(5, 2), padx=15)
        subject_combo = ttk.Combobox(scrollable, font=FONTS['body'], width=25)
        subject_combo.pack(fill="x", padx=15, pady=(0, 8))
        
        # Учитель
        ctk.CTkLabel(
            scrollable, 
            text="Учитель:", 
            font=FONTS['heading'],
            text_color=COLORS['text_light']
        ).pack(anchor="w", pady=(5, 2), padx=15)
        teacher_combo = ttk.Combobox(scrollable, font=FONTS['body'], width=25)
        teacher_combo.pack(fill="x", padx=15, pady=(0, 8))
        
        # Кабинет
        ctk.CTkLabel(
            scrollable, 
            text="Кабинет:", 
            font=FONTS['heading'],
            text_color=COLORS['text_light']
        ).pack(anchor="w", pady=(5, 2), padx=15)
        room_entry = ModernEntry(scrollable, placeholder_text="Необязательно")
        room_entry.pack(fill="x", padx=15, pady=(0, 8))
        
        # Загружаем данные для комбобоксов
        self.load_schedule_combos(class_combo, subject_combo, teacher_combo)
        
        def save_schedule():
            class_name = class_combo.get()
            day = day_combo.get()
            lesson_num = lesson_entry.get().strip()
            subject_name = subject_combo.get()
            teacher_name = teacher_combo.get()
            room = room_entry.get().strip()
            
            if not all([class_name, day, lesson_num, subject_name, teacher_name]):
                messagebox.showwarning("Ошибка", "Заполните все обязательные поля")
                return
            
            try:
                lesson_int = int(lesson_num)
                if lesson_int < 1 or lesson_int > 8:
                    raise ValueError
            except ValueError:
                messagebox.showerror("Ошибка", "Номер урока должен быть числом от 1 до 8")
                return
            
            connection = Database.get_connection()
            if connection is None:
                return
                
            try:
                cursor = connection.cursor()
                cursor.execute("SELECT class_id FROM classes WHERE class_name = ?", (class_name,))
                class_data = Database.dict_fetchone(cursor)
                
                cursor.execute("SELECT subject_id FROM subjects WHERE subject_name = ?", (subject_name,))
                subject_data = Database.dict_fetchone(cursor)
                
                cursor.execute("SELECT user_id FROM users WHERE full_name = ? AND role = 'teacher'", (teacher_name,))
                teacher_data = Database.dict_fetchone(cursor)
                
                if not class_data or not subject_data or not teacher_data:
                    messagebox.showerror("Ошибка", "Не найдены данные для вставки")
                    return
                
                cursor.execute("""
                    INSERT INTO schedule (class_id, subject_id, teacher_id, 
                                        day_of_week, lesson_number, room)
                    VALUES (?, ?, ?, ?, ?, ?)
                """, (class_data['class_id'], subject_data['subject_id'], 
                      teacher_data['user_id'], day, lesson_int, room or None))
                
                connection.commit()
                messagebox.showinfo("Успех", "✅ Урок добавлен в расписание!")
                self.load_schedule_admin()
                dialog.destroy()
                    
            except Exception as e:
                messagebox.showerror("Ошибка", f"Ошибка добавления: {str(e)}")
            finally:
                connection.close()
        
        # Кнопки
        button_frame = ctk.CTkFrame(scrollable, fg_color="transparent")
        button_frame.pack(pady=15)
        
        ModernButton(
            button_frame,
            text="💾 Сохранить",
            command=save_schedule,
            fg_color=COLORS['success'],
            hover_color=COLORS['info'],
            width=110
        ).pack(side="left", padx=3)
        
        ModernButton(
            button_frame,
            text="❌ Отмена",
            command=dialog.destroy,
            fg_color=COLORS['error'],
            hover_color=COLORS['warning'],
            width=110
        ).pack(side="left", padx=3)
    
    def load_schedule_combos(self, class_combo, subject_combo, teacher_combo):
        connection = Database.get_connection()
        if connection is None:
            return
            
        try:
            cursor = connection.cursor()
            cursor.execute("SELECT class_name FROM classes ORDER BY class_name")
            classes = Database.dict_fetchall(cursor)
            class_combo['values'] = [cls['class_name'] for cls in classes]
            
            cursor.execute("SELECT subject_name FROM subjects ORDER BY subject_name")
            subjects = Database.dict_fetchall(cursor)
            subject_combo['values'] = [sub['subject_name'] for sub in subjects]
            
            cursor.execute("SELECT full_name FROM users WHERE role = 'teacher' ORDER BY full_name")
            teachers = Database.dict_fetchall(cursor)
            teacher_combo['values'] = [tch['full_name'] for tch in teachers]
                
        except Exception as e:
            messagebox.showerror("Ошибка", f"Ошибка загрузки данных: {str(e)}")
        finally:
            connection.close()
    
    def edit_schedule(self):
        selected = self.schedule_tree.selection()
        if not selected:
            messagebox.showwarning("Внимание", "Выберите урок для редактирования")
            return
        
        schedule_data = self.schedule_tree.item(selected[0])['values']
        
        dialog = ctk.CTkToplevel(self)
        dialog.title("✏️ Редактирование урока")
        
        window_width = 400
        window_height = 500
        
        dialog.geometry(f"{window_width}x{window_height}")
        dialog.transient(self)
        dialog.grab_set()
        dialog.after(10, lambda: self.center_window(dialog, window_width, window_height))
        
        main_frame = CardFrame(dialog)
        main_frame.pack(fill="both", expand=True, padx=15, pady=15)
        
        # Контейнер с прокруткой
        canvas = tk.Canvas(main_frame, bg=COLORS['card_bg'], highlightthickness=0)
        scrollbar = ctk.CTkScrollbar(main_frame, orientation="vertical", command=canvas.yview)
        scrollable = ctk.CTkFrame(canvas, fg_color=COLORS['card_bg'])
        
        scrollable.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable, anchor="nw", width=340)
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        ctk.CTkLabel(
            scrollable, 
            text="✏️ Редактирование урока", 
            font=FONTS['subtitle'],
            text_color=COLORS['text_light']
        ).pack(pady=(10, 10))
        
        # Класс
        ctk.CTkLabel(
            scrollable, 
            text="Класс:", 
            font=FONTS['heading'],
            text_color=COLORS['text_light']
        ).pack(anchor="w", pady=(5, 2), padx=15)
        class_combo = ttk.Combobox(scrollable, font=FONTS['body'], width=25)
        class_combo.insert(0, schedule_data[1])
        class_combo.pack(fill="x", padx=15, pady=(0, 8))
        
        # День недели
        ctk.CTkLabel(
            scrollable, 
            text="День недели:", 
            font=FONTS['heading'],
            text_color=COLORS['text_light']
        ).pack(anchor="w", pady=(5, 2), padx=15)
        day_combo = ttk.Combobox(
            scrollable, 
            values=['Понедельник', 'Вторник', 'Среда', 'Четверг', 'Пятница', 'Суббота'], 
            font=FONTS['body'],
            width=25
        )
        day_combo.set(schedule_data[2])
        day_combo.pack(fill="x", padx=15, pady=(0, 8))
        
        # Номер урока
        ctk.CTkLabel(
            scrollable, 
            text="Номер урока:", 
            font=FONTS['heading'],
            text_color=COLORS['text_light']
        ).pack(anchor="w", pady=(5, 2), padx=15)
        lesson_entry = ModernEntry(scrollable)
        lesson_entry.insert(0, schedule_data[3])
        lesson_entry.pack(fill="x", padx=15, pady=(0, 8))
        
        # Предмет
        ctk.CTkLabel(
            scrollable, 
            text="Предмет:", 
            font=FONTS['heading'],
            text_color=COLORS['text_light']
        ).pack(anchor="w", pady=(5, 2), padx=15)
        subject_combo = ttk.Combobox(scrollable, font=FONTS['body'], width=25)
        subject_combo.insert(0, schedule_data[4])
        subject_combo.pack(fill="x", padx=15, pady=(0, 8))
        
        # Учитель
        ctk.CTkLabel(
            scrollable, 
            text="Учитель:", 
            font=FONTS['heading'],
            text_color=COLORS['text_light']
        ).pack(anchor="w", pady=(5, 2), padx=15)
        teacher_combo = ttk.Combobox(scrollable, font=FONTS['body'], width=25)
        teacher_combo.insert(0, schedule_data[5])
        teacher_combo.pack(fill="x", padx=15, pady=(0, 8))
        
        # Кабинет
        ctk.CTkLabel(
            scrollable, 
            text="Кабинет:", 
            font=FONTS['heading'],
            text_color=COLORS['text_light']
        ).pack(anchor="w", pady=(5, 2), padx=15)
        room_entry = ModernEntry(scrollable, placeholder_text="Необязательно")
        room_entry.insert(0, schedule_data[6] if schedule_data[6] != "---" else "")
        room_entry.pack(fill="x", padx=15, pady=(0, 8))
        
        self.load_schedule_combos(class_combo, subject_combo, teacher_combo)
        
        def save_changes():
            class_name = class_combo.get()
            day = day_combo.get()
            lesson_num = lesson_entry.get().strip()
            subject_name = subject_combo.get()
            teacher_name = teacher_combo.get()
            room = room_entry.get().strip()
            
            if not all([class_name, day, lesson_num, subject_name, teacher_name]):
                messagebox.showwarning("Ошибка", "Заполните все обязательные поля")
                return
            
            try:
                lesson_int = int(lesson_num)
                if lesson_int < 1 or lesson_int > 8:
                    raise ValueError
            except ValueError:
                messagebox.showerror("Ошибка", "Номер урока должен быть числом от 1 до 8")
                return
            
            connection = Database.get_connection()
            if connection is None:
                return
                
            try:
                cursor = connection.cursor()
                cursor.execute("SELECT class_id FROM classes WHERE class_name = ?", (class_name,))
                class_data = Database.dict_fetchone(cursor)
                
                cursor.execute("SELECT subject_id FROM subjects WHERE subject_name = ?", (subject_name,))
                subject_data = Database.dict_fetchone(cursor)
                
                cursor.execute("SELECT user_id FROM users WHERE full_name = ? AND role = 'teacher'", (teacher_name,))
                teacher_data = Database.dict_fetchone(cursor)
                
                if not class_data or not subject_data or not teacher_data:
                    messagebox.showerror("Ошибка", "Не найдены данные для обновления")
                    return
                
                cursor.execute("""
                    UPDATE schedule 
                    SET class_id = ?, subject_id = ?, teacher_id = ?,
                        day_of_week = ?, lesson_number = ?, room = ?
                    WHERE schedule_id = ?
                """, (class_data['class_id'], subject_data['subject_id'], 
                      teacher_data['user_id'], day, lesson_int, room or None, schedule_data[0]))
                
                connection.commit()
                messagebox.showinfo("Успех", "✅ Урок обновлен!")
                self.load_schedule_admin()
                dialog.destroy()
                    
            except Exception as e:
                messagebox.showerror("Ошибка", f"Ошибка обновления: {str(e)}")
            finally:
                connection.close()
        
        # Кнопки
        button_frame = ctk.CTkFrame(scrollable, fg_color="transparent")
        button_frame.pack(pady=15)
        
        ModernButton(
            button_frame,
            text="💾 Сохранить",
            command=save_changes,
            fg_color=COLORS['success'],
            hover_color=COLORS['info'],
            width=110
        ).pack(side="left", padx=3)
        
        ModernButton(
            button_frame,
            text="❌ Отмена",
            command=dialog.destroy,
            fg_color=COLORS['error'],
            hover_color=COLORS['warning'],
            width=110
        ).pack(side="left", padx=3)
    
    def delete_schedule(self):
        selected = self.schedule_tree.selection()
        if not selected:
            messagebox.showwarning("Внимание", "Выберите урок")
            return
        
        schedule_data = self.schedule_tree.item(selected[0])['values']
        
        if messagebox.askyesno("Подтверждение", f"Удалить урок {schedule_data[4]} для {schedule_data[1]}?"):
            connection = Database.get_connection()
            if connection is None:
                return
                
            try:
                cursor = connection.cursor()
                cursor.execute("DELETE FROM schedule WHERE schedule_id = ?", (schedule_data[0],))
                
                connection.commit()
                messagebox.showinfo("Успех", "✅ Урок удален из расписания!")
                self.load_schedule_admin()
                    
            except Exception as e:
                messagebox.showerror("Ошибка", f"Ошибка удаления: {str(e)}")
            finally:
                connection.close()
    
    def setup_stats_tab(self):
        tab = self.tabview.tab("Статистика")
        
        main_frame = CardFrame(tab)
        main_frame.pack(fill="both", expand=True, padx=15, pady=15)
        
        ctk.CTkLabel(
            main_frame,
            text=f"📊 Статистика {SCHOOL_INFO['short_name']}",
            font=("Segoe UI", 22, "bold"),
            text_color=COLORS['accent']
        ).pack(pady=(15, 15))
        
        # Таблица статистики с прокруткой
        container = ctk.CTkFrame(main_frame, fg_color="transparent")
        container.pack(fill="both", expand=True, padx=10, pady=5)
        
        columns = ("Показатель", "Значение")
        self.stats_tree = ttk.Treeview(
            container, 
            columns=columns, 
            show="headings", 
            style="Treeview",
            height=18
        )
        
        for col in columns:
            self.stats_tree.heading(col, text=col)
            self.stats_tree.column(col, width=300)
        
        scrollbar_y = ttk.Scrollbar(container, orient="vertical", command=self.stats_tree.yview)
        scrollbar_x = ttk.Scrollbar(container, orient="horizontal", command=self.stats_tree.xview)
        self.stats_tree.configure(yscrollcommand=scrollbar_y.set, xscrollcommand=scrollbar_x.set)
        
        self.stats_tree.grid(row=0, column=0, sticky="nsew")
        scrollbar_y.grid(row=0, column=1, sticky="ns")
        scrollbar_x.grid(row=1, column=0, sticky="ew")
        
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        
        # Кнопка обновить
        button_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        button_frame.pack(pady=10)
        
        ModernButton(
            button_frame,
            text="🔄 Обновить статистику",
            command=self.load_stats,
            fg_color=COLORS['primary'],
            hover_color=COLORS['secondary'],
            height=35
        ).pack()
        
        self.load_stats()
    
    def load_stats(self):
        connection = Database.get_connection()
        if connection is None:
            return
            
        try:
            cursor = connection.cursor()
            stats = []
            
            # Количество пользователей по ролям
            cursor.execute("""
                SELECT role, COUNT(*) as count 
                FROM users 
                GROUP BY role
            """)
            role_stats = Database.dict_fetchall(cursor)
            for stat in role_stats:
                role_rus = {
                    'admin': 'Администраторы',
                    'teacher': 'Учителя',
                    'student': 'Ученики'
                }.get(stat['role'], stat['role'])
                stats.append((f"Количество {role_rus}", stat['count']))
            
            # Количество классов
            cursor.execute("SELECT COUNT(*) as count FROM classes")
            class_count = Database.dict_fetchone(cursor)['count']
            stats.append(("Количество классов", class_count))
            
            # Количество предметов
            cursor.execute("SELECT COUNT(*) as count FROM subjects")
            subject_count = Database.dict_fetchone(cursor)['count']
            stats.append(("Количество предметов", subject_count))
            
            # Средняя оценка
            cursor.execute("SELECT AVG(CAST(grade AS FLOAT)) as avg_grade FROM grades")
            avg_grade = Database.dict_fetchone(cursor)['avg_grade']
            stats.append(("Средний балл по школе", f"{avg_grade:.2f}" if avg_grade else "Нет данных"))
            
            # Посещаемость за последнюю неделю
            cursor.execute("""
                SELECT 
                    SUM(CASE WHEN status = 'присутствовал' THEN 1 ELSE 0 END) as present,
                    COUNT(*) as total,
                    ROUND(SUM(CASE WHEN status = 'присутствовал' THEN 1 ELSE 0 END) * 100.0 / NULLIF(COUNT(*), 0), 2) as percentage
                FROM attendance 
                WHERE attendance_date >= DATEADD(DAY, -7, GETDATE())
            """)
            attendance = Database.dict_fetchone(cursor)
            if attendance and attendance['total'] > 0:
                stats.append(("Посещаемость за неделю", f"{attendance['percentage']}%"))
            else:
                stats.append(("Посещаемость за неделю", "Нет данных"))
            
            # Количество домашних заданий на этой неделе
            cursor.execute("""
                SELECT COUNT(*) as count 
                FROM homework 
                WHERE due_date >= GETDATE() 
                AND due_date < DATEADD(DAY, 7, GETDATE())
            """)
            hw_count = Database.dict_fetchone(cursor)['count']
            stats.append(("Домашних заданий на этой неделе", hw_count))
            
            # Количество заблокированных пользователей
            cursor.execute("SELECT COUNT(*) as count FROM users WHERE is_blocked = 1")
            blocked_count = Database.dict_fetchone(cursor)['count']
            stats.append(("Заблокированных пользователей", blocked_count))
            
            # Информация о школе
            stats.append(("", ""))
            stats.append(("--- РЕКВИЗИТЫ ШКОЛЫ ---", ""))
            stats.append(("ИНН", SCHOOL_INFO['inn']))
            stats.append(("КПП", SCHOOL_INFO['kpp']))
            stats.append(("ОГРН", SCHOOL_INFO['ogrn']))
            stats.append(("ОКВЭД", SCHOOL_INFO['okved']))
            stats.append(("БИК", SCHOOL_INFO['bic']))
            stats.append(("Лицевой счет", SCHOOL_INFO['personal_account']))
            stats.append(("Казначейский счет", SCHOOL_INFO['treasury_subaccount']))
            
            # Очищаем и заполняем таблицу
            for item in self.stats_tree.get_children():
                self.stats_tree.delete(item)
            
            for stat_name, stat_value in stats:
                self.stats_tree.insert("", "end", values=(stat_name, stat_value))
                
        except Exception as e:
            messagebox.showerror("Ошибка", f"Ошибка загрузки статистики: {str(e)}")
        finally:
            connection.close()

def main():
    # Создаем папку для изображений капчи, если её нет
    captcha_folder = r"C:\School101\Captcha"
    os.makedirs(captcha_folder, exist_ok=True)
    print(f"✅ Папка для изображений капчи: {captcha_folder}")
    
    app = LoginWindow()
    app.mainloop()

if __name__ == "__main__":
    main()