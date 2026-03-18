import requests, sqlite3, tkinter as tk
from datetime import datetime

API = "001ed8a039e6cb52a1591574e539b15b"
URL = f"https://api.openweathermap.org/data/2.5/weather?q=Wodzislaw Slaski&appid={API}&units=metric"

db = sqlite3.connect("pogoda.db")
c = db.cursor()
c.execute("CREATE TABLE IF NOT EXISTS dane (czas TEXT, temp REAL, cis REAL, wilg REAL)")

ok = tk.Tk()
ok.title("Pogoda - Wodzisław")

# Zmienna do śledzenia zakresu
zakres_aktywny = False

label = tk.Label(ok, text="Start...")
label.pack()

lista = tk.Listbox(ok, width=50, selectmode=tk.EXTENDED)
lista.pack()

def odswiez_liste():
    lista.delete(0, tk.END)
    for row in c.execute("SELECT * FROM dane ORDER BY czas DESC LIMIT 20"):
        lista.insert(tk.END, f"{row[0]} | {row[1]}°C | {row[2]} | {row[3]}")

def pobierz():
    try:
        d = requests.get(URL, verify=False).json()
        temp = d["main"]["temp"]
        cis = d["main"]["pressure"]
        wilg = d["main"]["humidity"]
        czas = datetime.now().strftime("%H:%M:%S")

        label.config(text=f"{czas}  {temp}°C  {cis}  {wilg}")

        c.execute("INSERT INTO dane VALUES (?,?,?,?)",(czas,temp,cis,wilg))
        db.commit()

        odswiez_liste()
    except:
        label.config(text="Błąd API")

    ok.after(60000, pobierz)

def pokaz_zakres():
    sel = lista.curselection()
    if len(sel) >= 2:
        start = lista.get(sel[-1]).split(" | ")[0]
        end = lista.get(sel[0]).split(" | ")[0]

        lista.delete(0, tk.END)
        for row in c.execute("SELECT * FROM dane WHERE czas BETWEEN ? AND ?", (start, end)):
            lista.insert(tk.END, f"{row[0]} | {row[1]}°C | {row[2]} | {row[3]}")

tk.Button(ok, text="Pokaż zaznaczony zakres", command=pokaz_zakres).pack()

pobierz()
ok.mainloop()