import tkinter as tk
import random
# Importējam mūsu uzrakstīto RetroGameGUI klasi no faila gui.py
from gui import RetroGameGUI 

# =========================================================
# SPĒLES DZINIS (Game Engine / Controller)
# Šī klase satur VISU spēles loģiku un matemātiku.
# Šis ir tas fails, kurā komanda rakstīs savu Minimax algoritmu.
# =========================================================
class GameEngine:
    def __init__(self):
        # 1. Izveidojam pašu Tkinter logu (root)
        self.root = tk.Tk()
        # 2. Padodam root logu mūsu GUI klasei, lai tā to varētu "izzīmēt"
        self.gui = RetroGameGUI(self.root)
        
        # 3. Pievienojam GUI callbacks (Event Listeners)
        # Kad GUI izsauks 'on_start_game', dzinis izpildīs funkciju 'sakt_jaunu_speli'
        self.gui.on_start_game = self.sakt_jaunu_speli
        # Kad GUI nospiedīs uz skaitļa, dzinis izpildīs 'apstradat_gajienu'
        self.gui.on_number_clicked = self.apstradat_gajienu
        
        # 4. Spēles Stāvokļa mainīgie (State)
        # Šie dati veidos pamatu Spēles Kokam (Game Tree), kad komanda rakstīs algoritmu.
        self.cilveka_punkti = 100
        self.datora_punkti = 100
        self.virkne = [] # Saraksts, kas saturēs ģenerētos skaitļus (piem. [1, 4, 2, 3])
        self.aktivais_speletajs = None
        self.iestatijumi = {}
        self.spele_beigusies = False

    def sakt_jaunu_speli(self, iestatijumi):
        """
        Izsaukta no GUI, kad lietotājs nospiež pogu 'Spēlēt'.
        Sagatavo datus un inicializē cīņas lauku.
        """
        # Saglabājam iestatījumus un atiestatām punktus
        self.iestatijumi = iestatijumi
        self.cilveka_punkti = 100
        self.datora_punkti = 100
        self.spele_beigusies = False
        self.aktivais_speletajs = iestatijumi["sacejs"]
        
        # Ģenerējam datu struktūru - masīvu (list) ar nejaušiem skaitļiem 1-4
        garums = iestatijumi["garums"]
        self.virkne = [random.randint(1, 4) for _ in range(garums)]
        
        # Sūtam komandu uz GUI klasi, lai uzzīmē laukumu, balstoties uz ģenerēto sarakstu
        self.gui.build_game_board(self.virkne, self.aktivais_speletajs, iestatijumi["algoritms"], garums)

        # Loģika: Ja datori sāk pirmais, iedarbinām datora gājienu ar 1 sekundes (1000ms) aizkavi
        if self.aktivais_speletajs == "Dators":
            self.root.after(1000, self.veikt_datora_gajienu)

    def apstradat_gajienu(self, index):
        """
        Galvenā spēles loģika. Šī funkcija tiek izsaukta gan tad, kad klikšķina cilvēks,
        gan tad, kad AI izvēlas savu gājienu.
        'index' ir skaitļa atrašanās vieta masīvā (piem., nospieda 3. pogu).
        """
        # Aizsargmehānisms: Ja spēle beigusies vai šī vieta jau ir tukša (None), nedarām neko.
        if self.spele_beigusies or self.virkne[index] is None:
            return 
            
        skaitlis = self.virkne[index] # Paņemam skaitļa vērtību
        
        # 1. NOTEIKUMU MATEMĀTIKA (Modulo operators % pārbauda dalāmību ar 2)
        if skaitlis % 2 == 0: 
            # Ja dalās bez atlikuma (Pāra skaitlis): Atņem savus punktus (skaitlis * 2)
            atnem = skaitlis * 2
            if self.aktivais_speletajs == "Cilveks":
                self.cilveka_punkti -= atnem
            else:
                self.datora_punkti -= atnem
        else: 
            # Ja nedalās (Nepāra skaitlis): Pieskaita punktus pretiniekam
            if self.aktivais_speletajs == "Cilveks":
                self.datora_punkti += skaitlis
            else:
                self.cilveka_punkti += skaitlis

        # 2. STĀVOKĻA (STATE) ATJAUNOŠANA
        # Nomainām izlietoto skaitli sarakstā uz None (tā nav 'null', lai nesabojātu saraksta indeksus)
        self.virkne[index] = None 
        # Pavēlam GUI atjaunot vizuālos rezultātus ekrānā
        self.gui.update_scores(self.cilveka_punkti, self.datora_punkti)
        # Pavēlam GUI nodzēst attiecīgo pogu no ekrāna
        self.gui.remove_button(index)

        # 3. SPĒLES BEIGU PĀRBAUDE
        # Funkcija 'all' atgriezīs True tikai tad, ja visi elementi sarakstā ir None.
        if all(x is None for x in self.virkne):
            self.spele_beigusies = True
            self.pazinot_uzvaretaju()
            return # Pārtraucam šīs funkcijas tālāku izpildi

        # 4. GĀJIENU MAIŅA
        # Izmantojam 'Ternary operator' priekš īsākas 'if/else' sintakses
        self.aktivais_speletajs = "Dators" if self.aktivais_speletajs == "Cilveks" else "Cilveks"
        # Pavēlam GUI pārslēgt neona rāmi ap avatariem
        self.gui.update_turn_indicator(self.aktivais_speletajs)

        # 5. DATORA GĀJIENA IZSAUKŠANA
        # Ja pēc gājiena maiņas tagad ir Datora kārta, liekam tam "padomāt" 800 milisekundes.
        # (after tiek izmantots, lai neiesaldētu visu GUI kamēr notiek gaidīšana).
        if self.aktivais_speletajs == "Dators":
            self.root.after(800, self.veikt_datora_gajienu)

    def veikt_datora_gajienu(self):
        """
        ====================================================================
        KOMANDAS UZDEVUMS ŠEIT: 
        Šī ir vieta, kur jums jāievieto Heuristic funkcija un Spēles koks 
        (Minimax / Alpha-Beta algoritms). 
        ====================================================================
        Šobrīd AI ir izveidots kā "Random Picker" (Izvēlas uz labu laimi),
        lai varētu vizuāli notestēt UI funkcionalitāti.
        """
        if self.spele_beigusies: return # AI nevar spēlēt pēc spēles beigām
        
        # Enumerate iet cauri sarakstam un atdod (indekss, vērtība).
        # Mēs saglabājam tikai tos indeksus, kuru vērtība nav izlietota (nav None)
        pieejamie_indeksi = [i for i, x in enumerate(self.virkne) if x is not None]
        
        if pieejamie_indeksi:
            # Izvēlamies nejaušu indeksu no pieejamajiem
            izveletais_indekss = random.choice(pieejamie_indeksi)
            # Dators simulē pogas nospiešanu, nosūtot savu izvēli atpakaļ uz 'apstradat_gajienu'
            self.apstradat_gajienu(izveletais_indekss)

    def pazinot_uzvaretaju(self):
        """Spēles beigu loģika. Pārbauda un paziņo to, kuram ir mazāk punktu."""
        if self.cilveka_punkti < self.datora_punkti:
            self.gui.show_winner("UZVARA! Cilvēkam mazāk punktu!", "cyan")
        elif self.datora_punkti < self.cilveka_punkti:
            self.gui.show_winner("ZAAUDĒJUMS! Datoram mazāk punktu!", "red")
        else:
            self.gui.show_winner("NEIZŠĶIRTS!", "yellow")

    def run(self):
        """Iedarbina galveno Tkinter ciklu (event loop), kas uztur logu atvērtu."""
        self.root.mainloop()

# Aizsardzība: Šis bloks izpildās tikai tad, ja mēs palaižam šo failu pa tiešo, 
# nevis importējam to citā failā.
if __name__ == "__main__":
    speles_dzinis = GameEngine()
    speles_dzinis.run()