import logging
import tkinter as tk
from tkinter import scrolledtext

from database import init_db, saugoti_skaiciavima, gauti_istorija

class Skaiciuotuvas:
    #susikuriu GUI su pavadinimu ir lango dydziu
    def __init__(self, langas, session):
        self.langas = langas
        self.session = session
        self.langas.title("Skaiciuotuvas")
        self.langas.geometry("320x300")
    #susikuriu lauka kur rasomi skaiciai ir eiluciu ir stulpeliu dydziai. Taip pat isjungiu galimybe rasyti skaicius klaviatura
        self.ivedimo_laukas = tk.Entry(self.langas, state='disabled')
        self.ivedimo_laukas.grid(row=1, column=0, columnspan=6)
        self.langas.grid_rowconfigure(1, minsize=50)
        self.langas.grid_columnconfigure(1, minsize=50)
    #apsirasau mygtukus, juos sudaro - mygtuko pavadinimas, eiles ir stulpelio vieta
        self.mygtukai = [
            ("%", 2, 0), ("+/-", 2, 1), ("CE", 2, 2), ("C", 2, 3),
            ("7", 3, 0), ("8", 3, 1), ("9", 3, 2), ("/", 3, 3),
            ("4", 4, 0), ("5", 4, 1), ("6", 4, 2), ("*", 4, 3),
            ("1", 5, 0), ("2", 5, 1), ("3", 5, 2), ("-", 5, 3),
            ("0", 6, 0), (".", 6, 1), ("=", 6, 2), ("+", 6, 3)
        ]
    # sukuriu mygtukus su ju parametrais.
        for tekstas, row, col in self.mygtukai:
            mygtukas = tk.Button(langas, text=tekstas, command=lambda t=tekstas: self.mygtuko_paspaudimas(t))
            mygtukas.grid(row=row, column=col, sticky="nsew")
            self.langas.grid_rowconfigure(row, weight=1, uniform="mygtukai")
            self.langas.grid_columnconfigure(col, weight=1, uniform="mygtukai")
    #sukuriu rezultato lauka kuriame matysis skaiciavimo rezultatas arba klaidos.
        self.rezultato_laukas = tk.Label(langas, text="")
        self.rezultato_laukas.grid(row=0, column=0, columnspan=4)
    #sukuriu tuscia lista kuriame laikomi ivesti skaiciai ir matematiniai veiksmai.
        self.skaiciu_seka = []
        self.rodyti_rezultata = False
    #sukuriam klaidu loggeri su jo parametrais
        self.logger = logging.getLogger("Skaiciuotuvo loggeris")
        self.logger.setLevel(logging.DEBUG)
        self.file_handler = logging.FileHandler("logger.log")
        self.file_handler.setLevel(logging.DEBUG)
        self.console_handler = logging.StreamHandler()
        self.console_handler.setLevel(logging.INFO)
        formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
        self.file_handler.setFormatter(formatter)
        self.console_handler.setFormatter(formatter)
        self.logger.addHandler(self.file_handler)
        self.logger.addHandler(self.console_handler)
        # self.logger.info("Skaiciuotuvas paleistas")
        self.istorijos_mygtukas = tk.Button(self.langas, text="Istorija", command=self.atidaryti_istorija)
        self.istorijos_mygtukas.grid(row=0, column=0, sticky="nw")


    #mygtuku paspaudimas, atliekami veiksmai su paduotu matematiniu veiksmu ir skaiciais.
    def mygtuko_paspaudimas(self, verte):
        current = self.ivedimo_laukas.get()
        if verte.isdigit():
            self.ivedimo_laukas.configure(state='normal')
            self.ivedimo_laukas.insert(tk.END, verte)
            self.ivedimo_laukas.configure(state='disabled')
        elif verte == "." and "." not in current:
            if self.rodyti_rezultata:
                self.ivedimo_laukas.delete(0, tk.END)
                self.rodyti_rezultata = False
            self.ivedimo_laukas.configure(state='normal')
            self.ivedimo_laukas.insert(tk.END, verte)
            self.ivedimo_laukas.configure(state='disabled')
        elif verte in "+-*/":
            self.skaiciu_seka.append(current)
            self.skaiciu_seka.append(verte)
            self.ivedimo_laukas.configure(state='normal')
            self.ivedimo_laukas.delete(0, tk.END)
            self.ivedimo_laukas.configure(state='disabled')
        elif verte == "=":
            self.skaiciu_seka.append(current)
            seka_string = ' '.join(self.skaiciu_seka)
            rezultatas = self.atlikti_veiksmus(self.skaiciu_seka)
            self.skaiciu_seka = [str(rezultatas)]
            self.ivedimo_laukas.configure(state='normal')
            self.ivedimo_laukas.delete(0, tk.END)
            self.ivedimo_laukas.configure(state='disabled')
            # print("Seka:", seka_string, "Rezultatas:", rezultatas)
            saugoti_skaiciavima(self.session, seka_string, rezultatas) #issaugojam duombazeje.
            if rezultatas.is_integer():
                self.rezultato_laukas.config(text=f"Rezultatas: {int(rezultatas)}")
            else:
                self.rezultato_laukas.config(text=f"Rezultatas: {rezultatas:.2f}")
            self.rodyti_rezultata = True
        elif verte == "C":
            self.rezultato_laukas.config(text="")
            self.ivedimo_laukas.configure(state='normal')
            self.ivedimo_laukas.delete(0, tk.END)
            self.ivedimo_laukas.configure(state='disabled')
            self.skaiciu_seka = []
        elif verte == "CE":
            self.ivedimo_laukas.configure(state='normal')
            self.ivedimo_laukas.delete(0, tk.END)
            self.ivedimo_laukas.configure(state='disabled')
            self.skaiciu_seka = []
        elif verte == "%":
            try:
                procentas = float(self.ivedimo_laukas.get()) / 100
                self.rezultato_laukas.config(text=f"Procentas: {procentas:.2f}")
            except:
                self.rezultato_laukas.config(text="Klaida")
        elif verte == "+/-":
            if current:
                if current[0] == "-":
                    self.ivedimo_laukas.configure(state='normal')
                    self.ivedimo_laukas.delete(0)
                else:
                    self.ivedimo_laukas.configure(state='normal')
                    self.ivedimo_laukas.insert(0, "-")
                self.ivedimo_laukas.configure(state='disabled')
            elif self.rodyti_rezultata:
                self.ivedimo_laukas.configure(state='normal')
                self.ivedimo_laukas.delete(0, tk.END)
                self.ivedimo_laukas.insert(0, "-")
                self.ivedimo_laukas.configure(state='disabled')
                self.rodyti_rezultata = False
            else:
                self.rezultato_laukas.config(text="Pirmiausiai iveskite skaiciu")

    #matematiniu veiksmu logika, kaip tvarkomas listas.
    def atlikti_veiksmus(self, seka):
        try:
            rezultatas = float(seka[0])
            for i in range(1, len(seka), 2):
                operacija = seka[i]
                skaicius = float(seka[i+1])
                if operacija == "+":
                    rezultatas += skaicius
                elif operacija == "-":
                    rezultatas -= skaicius
                elif operacija == "*":
                    rezultatas *= skaicius
                elif operacija == "/":
                    if skaicius == 0:
                        self.rezultato_laukas.config(text="Dalyba iš nulio negalima")
                        raise ZeroDivisionError("Dalyba iš nulio negalima")
                    rezultatas /= skaicius
            return rezultatas
        except ZeroDivisionError as zde:
            self.logger.error(f"Ivyko klaida: {str(zde)}")
            raise zde
        except Exception as e:
            self.rezultato_laukas.config(text="Klaida")
            self.logger.error(f"Ivyko klaida: {str(e)}")

    def atidaryti_istorija(self):
        istorija = gauti_istorija(self.session)
        IstorijosLangas(self.langas, istorija)
class IstorijosLangas:
    def __init__(self, parent, istorija):
        self.parent = parent
        self.istorija = istorija


        self.langas = tk.Toplevel(self.parent)
        self.langas.title("Skaiciavimo Istorija")
        self.langas.geometry('420x300')

        self.istorijos_laukas = scrolledtext.ScrolledText(self.langas, wrap=tk.WORD, width=40, height=15)
        self.istorijos_laukas.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)


        for skaiciavimas in self.istorija:
            self.istorijos_laukas.insert(tk.END, f"Seka: {skaiciavimas.skaiciu_seka}, Rezultatas: {skaiciavimas.rezultatas}\n")

        self.langas.mainloop()

if __name__ == "__main__":
    langas = tk.Tk()
    session = init_db()
    skaiciuotuvas = Skaiciuotuvas(langas, session)
    langas.mainloop()












