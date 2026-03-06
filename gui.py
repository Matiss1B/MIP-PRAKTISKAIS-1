import tkinter as tk  # GUI bibliotēka
import os             # Darbam ar failiem un mapēm
import sys            # Operētājsistēmas noteikšanai
import ctypes         # Windows specifikai
import shutil         # Failu kopēšanai

# Automātiska fonta ielāde (Windows, Mac, Linux)
fonta_cels = os.path.join(os.path.dirname(__file__), "fonts", "VT323-Regular.ttf")

if sys.platform == "win32":
    ctypes.windll.gdi32.AddFontResourceExW(fonta_cels, 0x10, 0)
elif sys.platform == "darwin":
    mac_font_dir = os.path.expanduser("~/Library/Fonts")
    shutil.copy(fonta_cels, os.path.join(mac_font_dir, "VT323-Regular.ttf"))
else:
    linux_font_dir = os.path.expanduser("~/.fonts")
    os.makedirs(linux_font_dir, exist_ok=True)
    shutil.copy(fonta_cels, os.path.join(linux_font_dir, "VT323-Regular.ttf"))
    os.system("fc-cache -f")

# Klase GIF animāciju
class AnimatedGif(tk.Label):
    def __init__(self, master, path, delay=150, shrink=1, **kwargs):
        super().__init__(master, **kwargs)
        self.frames = []
        
        # Ielādē visus GIF kadrus
        try:
            i = 0
            while True:
                frame = tk.PhotoImage(file=path, format=f"gif -index {i}")
                if shrink > 1:
                    frame = frame.subsample(shrink, shrink)
                self.frames.append(frame)
                i += 1
        except tk.TclError:
            pass 
        
        self.delay = delay
        self.current_frame = 0
        
        # Sāk animāciju, ja kadri eksistē
        if self.frames:
            self.config(image=self.frames[0])
            self.update_animation()

    # Pārslēdz uz nākamo kadru
    def update_animation(self):
        if self.frames:
            self.current_frame = (self.current_frame + 1) % len(self.frames)
            self.config(image=self.frames[self.current_frame])
            self.after(self.delay, self.update_animation)

# Galvenā GUI klase (Tikai vizuālā daļa)
class GameGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Skaitlu Cina")
        self.root.geometry("1100x900")
        self.root.configure(bg="black")

        # Fontu iestatījumi
        pixel_font = "VT323"
        self.font_title = (pixel_font, 36)
        self.font_normal = (pixel_font, 30)
        self.font_small = (pixel_font, 24)
        self.font_buttons = (pixel_font, 20)
        
        # Krāsas
        self.bg_color = "black"
        self.fg_color = "#00FF00" 

        # Iestatījumu mainīgie
        self.first_player = tk.StringVar(value="Cilveks")
        self.algorithm = tk.StringVar(value="Minimax")
        self.sequence_length = tk.IntVar(value=15)

        # Savienojumi ar main.py
        self.on_start_game = None
        self.on_number_clicked = None
        
        self.pogas = {}
        self.aktivais_speletajs = None

        # Galvenais rāmis
        self.main_frame = tk.Frame(self.root, bg=self.bg_color)
        self.main_frame.pack(expand=True, fill="both")

        self.game_container = None
        self.rules_container = None

        self.show_main_menu()

    # Notīra ekrānu
    def clear_screen(self):
        for widget in self.main_frame.winfo_children():
            widget.destroy()

    # Parāda galveno izvēlni
    def show_main_menu(self):
        self.clear_screen()
        tk.Label(self.main_frame, text="Skaitļu Virkne", font=self.font_title, bg=self.bg_color, fg=self.fg_color).pack(pady=80)
        tk.Button(self.main_frame, text="Spēlēt", font=self.font_normal, bg=self.bg_color, fg=self.fg_color, activebackground=self.fg_color, activeforeground=self.bg_color, relief="flat", command=self.show_settings).pack(pady=15)
        tk.Button(self.main_frame, text="Iziet", font=self.font_normal, bg=self.bg_color, fg="red", activebackground="red", activeforeground=self.bg_color, relief="flat", command=self.root.destroy).pack(pady=15)

    # Parāda iestatījumu logu
    def show_settings(self):
        self.clear_screen()
        tk.Label(self.main_frame, text="Pirms spēles sākuma", font=self.font_title, bg=self.bg_color, fg=self.fg_color).pack(pady=20)
        
        tk.Label(self.main_frame, text="\nKurš sāk spēli?", font=self.font_normal, bg=self.bg_color, fg="white").pack()
        tk.Radiobutton(self.main_frame, text="Cilvēks", variable=self.first_player, value="Cilveks", font=self.font_small, bg=self.bg_color, fg=self.fg_color, selectcolor="black").pack()
        tk.Radiobutton(self.main_frame, text="Dators", variable=self.first_player, value="Dators", font=self.font_small, bg=self.bg_color, fg=self.fg_color, selectcolor="black").pack()

        tk.Label(self.main_frame, text="\nDatora Algoritms:", font=self.font_normal, bg=self.bg_color, fg="white").pack()
        tk.Radiobutton(self.main_frame, text="Minimax", variable=self.algorithm, value="Minimax", font=self.font_small, bg=self.bg_color, fg=self.fg_color, selectcolor="black").pack()
        tk.Radiobutton(self.main_frame, text="Alpha-Beta", variable=self.algorithm, value="Alpha-Beta", font=self.font_small, bg=self.bg_color, fg=self.fg_color, selectcolor="black").pack()

        tk.Label(self.main_frame, text="\nVirknes garums (15-25):", font=self.font_normal, bg=self.bg_color, fg="white").pack()
        scale = tk.Scale(self.main_frame, variable=self.sequence_length, from_=15, to=25, orient="horizontal", bg=self.bg_color, fg=self.fg_color, highlightthickness=0, font=self.font_small)
        scale.pack()

        tk.Button(self.main_frame, text="SĀKT SPĒLI", font=self.font_normal, bg=self.bg_color, fg=self.fg_color, activebackground=self.fg_color, activeforeground=self.bg_color, relief="flat", command=self._trigger_start_game).pack(pady=30)
        tk.Button(self.main_frame, text="Atpakaļ uz izvēlni", font=self.font_small, bg=self.bg_color, fg="gray", activebackground="gray", activeforeground="black", relief="flat", command=self.show_main_menu).pack(pady=10)

    # Nolasa iestatījumus un paziņo main.py
    def _trigger_start_game(self):
        if self.on_start_game:
            iestatijumi = {
                "sacejs": self.first_player.get(),
                "algoritms": self.algorithm.get(),
                "garums": self.sequence_length.get()
            }
            self.on_start_game(iestatijumi)

    # Paslēpj spēli un parāda noteikumus
    def show_rules(self):
        if self.game_container:
            self.game_container.pack_forget() 
        if self.rules_container:
            self.rules_container.pack(expand=True, fill="both")

    # Paslēpj noteikumus un atgriež spēli
    def hide_rules(self):
        if self.rules_container:
            self.rules_container.pack_forget() 
        if self.game_container:
            self.game_container.pack(expand=True, fill="both") 

    # Uzzīmē spēles laukumu un noteikumus
    def build_game_board(self, sequence, sacejs, algo, garums):
        self.clear_screen()
        self.aktivais_speletajs = sacejs
        self.pogas = {} 
        
        # Noteikumu sadaļa (Sākumā paslēpta)
        self.rules_container = tk.Frame(self.main_frame, bg=self.bg_color)
        rules_box = tk.Frame(self.rules_container, bg=self.bg_color, highlightbackground=self.fg_color, highlightthickness=4)
        rules_box.pack(pady=50, padx=50, ipadx=40, ipady=40)

        tk.Label(rules_box, text="SPĒLES NOTEIKUMI", font=self.font_title, bg="black", fg="yellow").pack(pady=(0, 20))
        
        noteikumi_teksts = (
            "1. Abiem spēlētājiem sākumā ir 100 punkti.\n\n"
            "2. Spēlētāji pēc kārtas izvēlas vienu\n   skaitli no apakšējā laukuma.\n\n"
            "3. PĀRA skaitlis (2, 4):\n   No tava rezultāta atņem (skaitlis x 2).\n\n"
            "4. NEPĀRA skaitlis (1, 3):\n   Pretinieka rezultātam pieskaita\n   izvēlēto skaitli.\n\n"
            "MĒRĶIS:\nSpēles beigās iegūt MAZĀK punktu nekā pretiniekam!\n"
        )
        
        tk.Label(rules_box, text=noteikumi_teksts, font=self.font_small, bg="black", fg="white", justify="center").pack(pady=10)
        tk.Button(rules_box, text="SKAIDRS", font=self.font_normal, bg="black", fg=self.fg_color, activebackground=self.fg_color, activeforeground="black", relief="flat", command=self.hide_rules).pack(pady=(30, 0))

        # Spēles sadaļa
        self.game_container = tk.Frame(self.main_frame, bg=self.bg_color)
        self.game_container.pack(expand=True, fill="both")

        # Augšējā info josla un jautājuma zīme
        top_bar = tk.Frame(self.game_container, bg=self.bg_color)
        top_bar.pack(fill="x", padx=20, pady=10)
        
        info_text = f"Sāk: {sacejs}  |  Algo: {algo}  |  Garums: {garums}"
        self.lbl_status = tk.Label(top_bar, text=info_text, font=self.font_small, bg=self.bg_color, fg="gray")
        self.lbl_status.pack(expand=True, pady=5)
        
        help_canvas = tk.Canvas(top_bar, width=40, height=40, bg=self.bg_color, highlightthickness=0, cursor="hand2")
        help_canvas.place(relx=1.0, rely=0.5, anchor="e")
        help_canvas.create_oval(2, 2, 38, 38, outline=self.fg_color, width=2)
        help_canvas.create_text(20, 20, text="?", font=("VT323", 24), fill=self.fg_color)
        help_canvas.bind("<Button-1>", lambda e: self.show_rules())

        # Punkti un Avatari
        arena_frame = tk.Frame(self.game_container, bg=self.bg_color)
        arena_frame.pack(pady=20)

        self.lbl_cilveka_punkti = tk.Label(arena_frame, text="CILVĒKS: 100", font=self.font_title, bg=self.bg_color, fg="yellow")
        self.lbl_cilveka_punkti.grid(row=0, column=0, padx=50)
        tk.Label(arena_frame, text=" VS ", font=self.font_title, bg=self.bg_color, fg="white").grid(row=0, column=1)
        self.lbl_datora_punkti = tk.Label(arena_frame, text="DATORS: 100", font=self.font_title, bg=self.bg_color, fg="yellow")
        self.lbl_datora_punkti.grid(row=0, column=2, padx=50)

        # Avataru ielāde
        baze = os.path.dirname(__file__)
        human = os.path.join(baze, "Gifs", "human.gif")
        robot = os.path.join(baze, "Gifs", "robot.gif")

        try:
            self.human_gif = AnimatedGif(arena_frame, human, shrink=2, bg=self.bg_color, highlightthickness=4, highlightbackground=self.bg_color)
            self.human_gif.grid(row=1, column=0, pady=20)
        except Exception:
            tk.Label(arena_frame, text="[Nav human.gif]", font=self.font_normal, bg=self.bg_color, fg="red").grid(row=1, column=0, pady=20)

        try:
            self.robot_gif = AnimatedGif(arena_frame, robot, shrink=2, bg=self.bg_color, highlightthickness=4, highlightbackground=self.bg_color)
            self.robot_gif.grid(row=1, column=2, pady=20)
        except Exception:
            tk.Label(arena_frame, text="[Nav robot.gif]", font=self.font_normal, bg=self.bg_color, fg="red").grid(row=1, column=2, pady=20)

        self.update_turn_indicator(sacejs)

        # Skaitļu pogas
        bottom_container = tk.Frame(self.game_container, bg=self.bg_color, highlightbackground=self.fg_color, highlightthickness=2)
        bottom_container.pack(pady=20, ipadx=20, ipady=10)
        tk.Label(bottom_container, text="Skaitļu Virkne", font=self.font_normal, bg=self.bg_color, fg="white").pack(pady=10)
        
        btn_grid_frame = tk.Frame(bottom_container, bg=self.bg_color)
        btn_grid_frame.pack(pady=10)

        for i, val in enumerate(sequence):
            row = i // 10
            col = i % 10
            
            btn = tk.Button(btn_grid_frame, text=str(val), font=self.font_buttons, bg="black", fg=self.fg_color, activebackground=self.fg_color, activeforeground="black", relief="ridge", borderwidth=4, width=3)
            btn.config(command=lambda idx=i: self._trigger_button_click(idx))
            btn.grid(row=row, column=col, padx=8, pady=8)
            self.pogas[i] = btn

        tk.Button(self.game_container, text="Atgriezties Izvēlnē", font=self.font_normal, bg=self.bg_color, fg=self.fg_color, activebackground=self.fg_color, activeforeground=self.bg_color, relief="flat", command=self.show_main_menu).pack(pady=20)

    # Padod pogas klikšķi uz main.py
    def _trigger_button_click(self, index):
        if self.on_number_clicked:
            self.on_number_clicked(index)

    # Ieslēdz vai izslēdz skaitļu pogas
    def set_buttons_state(self, state):
        for btn in self.pogas.values():
            btn.config(state=state)

    # Atjauno rezultātu uz ekrāna
    def update_scores(self, cilveks, dators):
        self.lbl_cilveka_punkti.config(text=f"CILVĒKS: {cilveks}")
        self.lbl_datora_punkti.config(text=f"DATORS: {dators}")

    # Izdzēš pogu no ekrāna
    def remove_button(self, index):
        if index in self.pogas:
            self.pogas[index].destroy()
            del self.pogas[index]

    # Iezīmē aktīvo spēlētāju ar zaļu rāmi
    def update_turn_indicator(self, player_name):
        self.aktivais_speletajs = player_name
        if hasattr(self, 'human_gif') and hasattr(self, 'robot_gif'):
            if self.aktivais_speletajs == "Cilveks":
                self.human_gif.config(highlightbackground=self.fg_color)
                self.robot_gif.config(highlightbackground=self.bg_color)
            else:
                self.human_gif.config(highlightbackground=self.bg_color)
                self.robot_gif.config(highlightbackground=self.fg_color)

    # Paziņo uzvarētāju
    def show_winner(self, message, color):
        self.human_gif.config(highlightbackground=self.bg_color)
        self.robot_gif.config(highlightbackground=self.bg_color)
        self.lbl_status.config(text=message, fg=color, font=self.font_title)