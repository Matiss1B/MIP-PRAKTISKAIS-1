import tkinter as tk  # Importējam Tkinter bibliotēku, kas ir Python standarta GUI framework
import os             # Os bibliotēka palīdz strādāt ar failu sistēmu un mapju ceļiem (paths)
import sys            # Sys ļauj noteikt, kāda operētājsistēma tiek izmantota (Windows, Mac, Linux)
import ctypes         # Ctypes ļauj izsaukt funkcijas no Windows API
import shutil         # Shutil ļauj ātri kopēt failus sistēmā (vajadzīgs Mac un Linux vidēm)

# =========================================================
# CROSS-PLATFORM FONTA IELĀDE
# Piezīme: Mēs pieņemam, ka fails "VT323-Regular.ttf" vienmēr atrodas "fonts" mapē.
# =========================================================
fonta_cels = os.path.join(os.path.dirname(__file__), "fonts", "VT323-Regular.ttf")

if sys.platform == "win32":
    # WINDOWS: Īslaicīgi ielādē fontu RAM atmiņā, izmantojot Windows OS API.
    ctypes.windll.gdi32.AddFontResourceExW(fonta_cels, 0x10, 0)

elif sys.platform == "darwin":
    # MAC (macOS): Iekopē fontu failu tieši Mac lietotāja 'Library/Fonts' mapē.
    mac_font_dir = os.path.expanduser("~/Library/Fonts")
    shutil.copy(fonta_cels, os.path.join(mac_font_dir, "VT323-Regular.ttf"))

else:
    # LINUX: Izveido slēpto '.fonts' mapi (ja tādas nav), iekopē tur fontu un atjaunina OS cache.
    linux_font_dir = os.path.expanduser("~/.fonts")
    os.makedirs(linux_font_dir, exist_ok=True)
    shutil.copy(fonta_cels, os.path.join(linux_font_dir, "VT323-Regular.ttf"))
    os.system("fc-cache -f") # Atjaunina Linux fontu kešatmiņu (cache)

# ---------------------------------------------------------
# 1. KLASIKA: GIF Animācijas Klase
# Šī klase manto (inherits) no tk.Label un ir paredzēta GIF failu atskaņošanai.
# Tkinter dabiski neatbalsta GIF animācijas, tas rāda tikai 1. kadru (frame).
# ---------------------------------------------------------
class AnimatedGif(tk.Label):
    def __init__(self, master, path, delay=150, shrink=1, **kwargs):
        # Inicializējam tk.Label (mātes klasi)
        super().__init__(master, **kwargs)
        self.frames = []  # Saraksts, kurā glabāsim visus GIF kadrus
        
        try:
            i = 0
            while True:
                # Ielādējam kadru pēc indeksa. Kad indekss vairs neeksistēs, metīs TclError.
                frame = tk.PhotoImage(file=path, format=f"gif -index {i}")
                
                # Ja nepieciešams samazināt bildi, izmantojam subsample (sadala pikseļu skaitu ar shrink vērtību)
                if shrink > 1:
                    frame = frame.subsample(shrink, shrink)
                
                self.frames.append(frame)
                i += 1
        except tk.TclError:
            pass  # Esam ielādējuši visus kadrus, pārtraucam ciklu
        
        self.delay = delay               # Ātrums milisekundēs starp kadriem
        self.current_frame = 0           # Pašreizējā kadra indekss
        
        if self.frames:
            # Uzstādām pirmo kadru un sākam animācijas loop
            self.config(image=self.frames[0])
            self.update_animation()

    def update_animation(self):
        """Šī funkcija izsauc pati sevi ik pēc 'delay' milisekundēm (recursive loop)."""
        if self.frames:
            # Pārslēdzam uz nākamo kadru. Izmantojam modulo (%), lai atgrieztos uz 0, kad sasniegts beigas.
            self.current_frame = (self.current_frame + 1) % len(self.frames)
            self.config(image=self.frames[self.current_frame])
            # Tkinter .after() komanda, kas ieplāno funkcijas izsaukumu nākotnē
            self.after(self.delay, self.update_animation)

# ---------------------------------------------------------
# 2. GALVENĀ KLASE: RetroGameGUI
# Šī klase satur VISU vizuālo loģiku (Views). Te nav spēles matemātikas!
# ---------------------------------------------------------
class RetroGameGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Skaitlu Cina")
        self.root.geometry("1100x900")
        self.root.configure(bg="black")

        # PIXEL FONT IESTATĪJUMI (izmēri dažādiem teksta tipiem)
        pixel_font = "VT323"
        self.font_title = (pixel_font, 36)
        self.font_normal = (pixel_font, 30)
        self.font_small = (pixel_font, 24)
        self.font_buttons = (pixel_font, 20)
        
        # Globālās krāsas tēmai
        self.bg_color = "black"
        self.fg_color = "#00FF00"  # Neona zaļā krāsa

        # Iestatījumu mainīgie (Tkinter specifiski mainīgie, kas seko līdzi UI izvēlēm)
        self.first_player = tk.StringVar(value="Cilveks")
        self.algorithm = tk.StringVar(value="Minimax")
        self.sequence_length = tk.IntVar(value=15)

        # CALLBACKS jeb "Āķi"
        self.on_start_game = None
        self.on_number_clicked = None
        
        # Vārdnīca (dictionary), kur glabāsim ģenerētās pogas
        self.pogas = {}
        self.aktivais_speletajs = None

        # Galvenais rāmis (Frame), kurā zīmēsim visu ekrānu saturu
        self.main_frame = tk.Frame(self.root, bg=self.bg_color)
        self.main_frame.pack(expand=True, fill="both")

        # Mainīgie Overlay (Noteikumu) pārvaldībai
        self.game_container = None
        self.rules_container = None

        # Sākam aplikāciju ar galveno izvēlni
        self.show_main_menu()

    def clear_screen(self):
        """Iztīra visu main_frame saturu, lai varētu zīmēt jaunu ekrānu."""
        for widget in self.main_frame.winfo_children():
            widget.destroy()

    # --- SKATS 1: GALVENĀ IZVĒLNE (Main Menu) ---
    def show_main_menu(self):
        self.clear_screen()
        # Virsraksts
        tk.Label(self.main_frame, text="Skaitļu Virkne", font=self.font_title, bg=self.bg_color, fg=self.fg_color).pack(pady=80)
        
        # Poga 'Spēlēt' ved uz Iestatījumu logu
        tk.Button(self.main_frame, text="Spēlēt", font=self.font_normal, bg=self.bg_color, fg=self.fg_color, activebackground=self.fg_color, activeforeground=self.bg_color, relief="flat", command=self.show_settings).pack(pady=15)
        # Poga, kas izslēdz spēli (destroy)
        tk.Button(self.main_frame, text="Iziet", font=self.font_normal, bg=self.bg_color, fg="red", activebackground="red", activeforeground=self.bg_color, relief="flat", command=self.root.destroy).pack(pady=15)

    # --- SKATS 2: IESTATĪJUMI (Pre-game Settings Lobby) ---
    def show_settings(self):
        self.clear_screen()
        tk.Label(self.main_frame, text="Pirms spēles sākuma", font=self.font_title, bg=self.bg_color, fg=self.fg_color).pack(pady=20)
        
        # RadioButtons ļauj izvēlēties vienu opciju no vairākām
        tk.Label(self.main_frame, text="\nKurš sāk spēli?", font=self.font_normal, bg=self.bg_color, fg="white").pack()
        tk.Radiobutton(self.main_frame, text="Cilvēks", variable=self.first_player, value="Cilveks", font=self.font_small, bg=self.bg_color, fg=self.fg_color, selectcolor="black").pack()
        tk.Radiobutton(self.main_frame, text="Dators", variable=self.first_player, value="Dators", font=self.font_small, bg=self.bg_color, fg=self.fg_color, selectcolor="black").pack()

        tk.Label(self.main_frame, text="\nDatora Algoritms:", font=self.font_normal, bg=self.bg_color, fg="white").pack()
        tk.Radiobutton(self.main_frame, text="Minimax", variable=self.algorithm, value="Minimax", font=self.font_small, bg=self.bg_color, fg=self.fg_color, selectcolor="black").pack()
        tk.Radiobutton(self.main_frame, text="Alpha-Beta", variable=self.algorithm, value="Alpha-Beta", font=self.font_small, bg=self.bg_color, fg=self.fg_color, selectcolor="black").pack()

        # Scale ir "slideris", kas ļauj izvēlēties garumu no 15 līdz 25
        tk.Label(self.main_frame, text="\nVirknes garums (15-25):", font=self.font_normal, bg=self.bg_color, fg="white").pack()
        scale = tk.Scale(self.main_frame, variable=self.sequence_length, from_=15, to=25, orient="horizontal", bg=self.bg_color, fg=self.fg_color, highlightthickness=0, font=self.font_small)
        scale.pack()

        # Šī poga iedarbina spēli, aizsūtot datus uz main.py
        tk.Button(self.main_frame, text="SĀKT SPĒLI", font=self.font_normal, bg=self.bg_color, fg=self.fg_color, activebackground=self.fg_color, activeforeground=self.bg_color, relief="flat", command=self._trigger_start_game).pack(pady=30)
        # Poga, kas atgriež atpakaļ uz galveno izvēlni
        tk.Button(self.main_frame, text="Atpakaļ uz izvēlni", font=self.font_small, bg=self.bg_color, fg="gray", activebackground="gray", activeforeground="black", relief="flat", command=self.show_main_menu).pack(pady=10)

    # --- Pārķērējs (Trigger) pirms signāla sūtīšanas uz main.py ---
    def _trigger_start_game(self):
        """Savāc iestatījumus un aizsūta uz main.py loģiku."""
        if self.on_start_game:
            iestatijumi = {
                "sacejs": self.first_player.get(),
                "algoritms": self.algorithm.get(),
                "garums": self.sequence_length.get()
            }
            self.on_start_game(iestatijumi)

    # =========================================================
    # TOGGLE FUNKCIJAS (Slēpt Spēli / Parādīt Noteikumus)
    # =========================================================
    def show_rules(self):
        """Paslēpj spēles laukumu un parāda noteikumu konteineri."""
        if self.game_container:
            self.game_container.pack_forget() # Paslēpj (bet neizdzēš!)
        if self.rules_container:
            self.rules_container.pack(expand=True, fill="both") # Parāda noteikumus

    def hide_rules(self):
        """Paslēpj noteikumu konteineri un atgriež spēles laukumu."""
        if self.rules_container:
            self.rules_container.pack_forget() # Paslēpj noteikumus
        if self.game_container:
            self.game_container.pack(expand=True, fill="both") # Parāda spēli atpakaļ


    # =========================================================
    # SKATS 3: SPĒLES LAUKUMA ZĪMĒŠANA (Tiek izsaukta no main.py)
    # =========================================================
    def build_game_board(self, sequence, sacejs, algo, garums):
        """Funkcija zīmē gan spēles laukumu, gan izveido paslēpto noteikumu laukumu."""
        self.clear_screen()
        self.aktivais_speletajs = sacejs
        self.pogas = {} 
        
        # -------------------------------------------------------------
        # KONTEINERIS 1: NOTEIKUMI (Sākumā izveidots, bet nav iepakots/parādīts)
        # -------------------------------------------------------------
        self.rules_container = tk.Frame(self.main_frame, bg=self.bg_color)
        
        # Izveidojam kastīti ar zaļu outline, kurā būs noteikumi
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
        
        # Poga "SKAIDRS", kas izsauc hide_rules()
        tk.Button(rules_box, text="SKAIDRS", font=self.font_normal, bg="black", fg=self.fg_color, 
                  activebackground=self.fg_color, activeforeground="black", relief="flat", 
                  command=self.hide_rules).pack(pady=(30, 0))

        # -------------------------------------------------------------
        # KONTEINERIS 2: SPĒLES LAUKUMS (Tiek izveidots un uzreiz parādīts)
        # -------------------------------------------------------------
        self.game_container = tk.Frame(self.main_frame, bg=self.bg_color)
        self.game_container.pack(expand=True, fill="both")

        # 1. Augšējā josla (Informācija un palīdzības poga)
        top_bar = tk.Frame(self.game_container, bg=self.bg_color)
        top_bar.pack(fill="x", padx=20, pady=10)
        
        info_text = f"Sāk: {sacejs}  |  Algo: {algo}  |  Garums: {garums}"
        self.lbl_status = tk.Label(top_bar, text=info_text, font=self.font_small, bg=self.bg_color, fg="gray")
        self.lbl_status.pack(expand=True, pady=5)
        
        # Jautājuma zīme uzzīmēta ar Canvas elementiem. Klikšķis izsauc show_rules()
        help_canvas = tk.Canvas(top_bar, width=40, height=40, bg=self.bg_color, highlightthickness=0, cursor="hand2")
        help_canvas.place(relx=1.0, rely=0.5, anchor="e")
        help_canvas.create_oval(2, 2, 38, 38, outline=self.fg_color, width=2)
        help_canvas.create_text(20, 20, text="?", font=("VT323", 24), fill=self.fg_color)
        help_canvas.bind("<Button-1>", lambda e: self.show_rules())

        # 2. Kaujas arēna (Avatari un rezultāts)
        arena_frame = tk.Frame(self.game_container, bg=self.bg_color)
        arena_frame.pack(pady=20)

        self.lbl_cilveka_punkti = tk.Label(arena_frame, text="CILVĒKS: 100", font=self.font_title, bg=self.bg_color, fg="yellow")
        self.lbl_cilveka_punkti.grid(row=0, column=0, padx=50)
        tk.Label(arena_frame, text=" VS ", font=self.font_title, bg=self.bg_color, fg="white").grid(row=0, column=1)
        self.lbl_datora_punkti = tk.Label(arena_frame, text="DATORS: 100", font=self.font_title, bg=self.bg_color, fg="yellow")
        self.lbl_datora_punkti.grid(row=0, column=2, padx=50)

        try:
            self.human_gif = AnimatedGif(arena_frame, "human.gif", shrink=2, bg=self.bg_color, highlightthickness=4, highlightbackground=self.bg_color)
            self.human_gif.grid(row=1, column=0, pady=20)
        except Exception:
            tk.Label(arena_frame, text="[Nav human.gif]", font=self.font_normal, bg=self.bg_color, fg="red").grid(row=1, column=0, pady=20)

        try:
            self.robot_gif = AnimatedGif(arena_frame, "robot.gif", shrink=2, bg=self.bg_color, highlightthickness=4, highlightbackground=self.bg_color)
            self.robot_gif.grid(row=1, column=2, pady=20)
        except Exception:
            tk.Label(arena_frame, text="[Nav robot.gif]", font=self.font_normal, bg=self.bg_color, fg="red").grid(row=1, column=2, pady=20)

        # Iestatām indikatoru tam, kurš sāk
        self.update_turn_indicator(sacejs)

        # 3. Apakšējais laukums ar ģenerētajiem skaitļiem
        bottom_container = tk.Frame(self.game_container, bg=self.bg_color, highlightbackground=self.fg_color, highlightthickness=2)
        bottom_container.pack(pady=20, ipadx=20, ipady=10)
        tk.Label(bottom_container, text="Skaitļu Virkne", font=self.font_normal, bg=self.bg_color, fg="white").pack(pady=10)
        
        btn_grid_frame = tk.Frame(bottom_container, bg=self.bg_color)
        btn_grid_frame.pack(pady=10)

        # Cikls iet cauri sarakstam 'sequence', ko atsūtīja main.py
        for i, val in enumerate(sequence):
            row = i // 10
            col = i % 10
            
            btn = tk.Button(btn_grid_frame, text=str(val), font=self.font_buttons, bg="black", fg=self.fg_color, 
                            activebackground=self.fg_color, activeforeground="black", relief="ridge", borderwidth=4, width=3)
            
            btn.config(command=lambda idx=i: self._trigger_button_click(idx))
            
            btn.grid(row=row, column=col, padx=8, pady=8)
            self.pogas[i] = btn

        # Poga ļauj iziet no spēles gan tās laikā, gan pēc beigām
        tk.Button(self.game_container, text="Atgriezties Izvēlnē", font=self.font_normal, bg=self.bg_color, fg=self.fg_color, activebackground=self.fg_color, activeforeground=self.bg_color, relief="flat", command=self.show_main_menu).pack(pady=20)

    # --- Pārķērējs skaitļu pogām ---
    def _trigger_button_click(self, index):
        """Padod nospiestās pogas indeksu uz main.py spēles loģiku"""
        if self.on_number_clicked:
            self.on_number_clicked(index)

    # =========================================================
    # GUI ATJAUNOŠANAS METODES (Tiek izsauktas no main.py)
    # =========================================================
    def update_scores(self, cilveks, dators):
        """Atjauno rezultātu text label ekrānā."""
        self.lbl_cilveka_punkti.config(text=f"CILVĒKS: {cilveks}")
        self.lbl_datora_punkti.config(text=f"DATORS: {dators}")

    def remove_button(self, index):
        """Iznīcina (destroy) pogu vizuāli no ekrāna, balstoties uz indeksu."""
        if index in self.pogas:
            self.pogas[index].destroy()
            del self.pogas[index] # Iztīra no dictionary

    def update_turn_indicator(self, player_name):
        """Pārslēdz zaļo outline (rāmi) apkārt tam GIFam, kura gājiens tas ir."""
        self.aktivais_speletajs = player_name
        if hasattr(self, 'human_gif') and hasattr(self, 'robot_gif'):
            if self.aktivais_speletajs == "Cilveks":
                self.human_gif.config(highlightbackground=self.fg_color)
                self.robot_gif.config(highlightbackground=self.bg_color)
            else:
                self.human_gif.config(highlightbackground=self.bg_color)
                self.robot_gif.config(highlightbackground=self.fg_color)

    def show_winner(self, message, color):
        """Paslēpj gājienu indikatorus un nomaina augšējo Info tekstu uz Uzvarētāja paziņojumu."""
        self.human_gif.config(highlightbackground=self.bg_color)
        self.robot_gif.config(highlightbackground=self.bg_color)
        self.lbl_status.config(text=message, fg=color, font=self.font_title)