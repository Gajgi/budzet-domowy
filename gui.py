from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from database import init_db, dodaj_wydatek, pobierz_wszystkie_wydatki
from helpers import sprawdz_poprawnosc_danych
import sqlite3
from datetime import datetime


def start_gui():
    try:
        # Połączenie z bazą danych
        conn = init_db()
        print("Połączenie z bazą danych nawiązane pomyślnie")
    except sqlite3.Error as e:
        messagebox.showerror("Błąd bazy danych", f"Nie można połączyć z bazą danych: {e}")
        return

    # Tworzenie okna aplikacji
    root = Tk()
    root.title("Budżet domowy - Wydatki")
    root.minsize(500, 600)  # Minimalna wielkość okna

    # Zmienne do przechowywania wartości
    kategoria_var = StringVar()
    kwota_var = StringVar()
    data_var = StringVar()
    uwagi_var = StringVar()

    # Ustawienie dzisiejszej daty jako domyślnej
    data_var.set(datetime.now().strftime('%Y-%m-%d'))

    def dodaj_do_bazy():
        try:
            kategoria = kategoria_var.get()
            kwota = kwota_var.get().replace(',', '.')  # Zamiana przecinka na kropkę
            data = data_var.get()
            uwagi = uwagi_var.get()

            if sprawdz_poprawnosc_danych(kategoria, kwota, data):
                dodaj_wydatek(conn, kategoria, float(kwota), data, uwagi)
                messagebox.showinfo("Sukces", "Wydatek dodany pomyślnie!")
                wyczysc_pola()
                odswiez_tabele()
        except Exception as e:
            messagebox.showerror("Błąd", f"Wystąpił błąd podczas dodawania wydatku: {str(e)}")
            print(f"Błąd podczas dodawania wydatku: {e}")

    def wyczysc_pola():
        kategoria_var.set("")
        kwota_var.set("")
        data_var.set(datetime.now().strftime('%Y-%m-%d'))
        uwagi_var.set("")
        kategoria_entry.focus()  # Przywrócenie fokusa na pierwsze pole

    def odswiez_tabele():
        try:
            for row in tabela.get_children():
                tabela.delete(row)
            dane = pobierz_wszystkie_wydatki(conn)
            for row in dane:
                tabela.insert("", END, values=row)
        except Exception as e:
            messagebox.showerror("Błąd", f"Błąd podczas odświeżania tabeli: {str(e)}")
            print(f"Błąd podczas odświeżania tabeli: {e}")

    # Frame dla formularza
    form_frame = ttk.LabelFrame(root, text="Dodaj nowy wydatek", padding="10")
    form_frame.pack(fill=X, padx=10, pady=5)

    # Pola formularza
    ttk.Label(form_frame, text="Kategoria:").grid(row=0, column=0, sticky=W, padx=5, pady=5)
    kategoria_entry = ttk.Combobox(form_frame, textvariable=kategoria_var,
                                   values=["Jedzenie", "Subskrypcje", "Chemia", "Leki", "Inne",
                                           "Kosmetyczka", "Pies", "Ubrania", "Auto"])
    kategoria_entry.grid(row=0, column=1, sticky=(W, E), padx=5, pady=5)

    ttk.Label(form_frame, text="Kwota:").grid(row=1, column=0, sticky=W, padx=5, pady=5)
    kwota_entry = ttk.Entry(form_frame, textvariable=kwota_var)
    kwota_entry.grid(row=1, column=1, sticky=(W, E), padx=5, pady=5)

    ttk.Label(form_frame, text="Data (YYYY-MM-DD):").grid(row=2, column=0, sticky=W, padx=5, pady=5)
    data_entry = ttk.Entry(form_frame, textvariable=data_var)
    data_entry.grid(row=2, column=1, sticky=(W, E), padx=5, pady=5)

    ttk.Label(form_frame, text="Uwagi:").grid(row=3, column=0, sticky=W, padx=5, pady=5)
    uwagi_entry = ttk.Entry(form_frame, textvariable=uwagi_var)
    uwagi_entry.grid(row=3, column=1, sticky=(W, E), padx=5, pady=5)

    # Przyciski
    button_frame = ttk.Frame(form_frame)
    button_frame.grid(row=4, column=0, columnspan=2, pady=10)

    ttk.Button(button_frame, text="Dodaj wydatek", command=dodaj_do_bazy).pack(side=LEFT, padx=5)
    ttk.Button(button_frame, text="Wyczyść", command=wyczysc_pola).pack(side=LEFT, padx=5)

    # Frame dla tabeli
    table_frame = ttk.LabelFrame(root, text="Lista wydatków", padding="10")
    table_frame.pack(fill=BOTH, expand=True, padx=10, pady=5)

    # Tabela wydatków
    tabela = ttk.Treeview(table_frame, columns=("Kategoria", "Kwota", "Data", "Uwagi"),
                          show="headings", selectmode="browse")

    # Konfiguracja kolumn
    tabela.heading("Kategoria", text="Kategoria")
    tabela.heading("Kwota", text="Kwota")
    tabela.heading("Data", text="Data")
    tabela.heading("Uwagi", text="Uwagi")

    tabela.column("Kategoria", width=100)
    tabela.column("Kwota", width=100)
    tabela.column("Data", width=100)
    tabela.column("Uwagi", width=200)

    # Dodanie scrollbara
    scrollbar = ttk.Scrollbar(table_frame, orient=VERTICAL, command=tabela.yview)
    tabela.configure(yscrollcommand=scrollbar.set)

    # Pakowanie tabeli i scrollbara
    tabela.pack(side=LEFT, fill=BOTH, expand=True)
    scrollbar.pack(side=RIGHT, fill=Y)

    # Pierwsze załadowanie danych
    odswiez_tabele()

    # Ustawienie fokusa na pierwsze pole
    kategoria_entry.focus()

    # Dodaj label na sumę wydatków
    suma_frame = ttk.Frame(root, padding="10")
    suma_frame.pack(fill=X, padx=10, pady=5)

    suma_label = ttk.Label(suma_frame, text="", font=("Arial", 10, "bold"))
    suma_label.pack(side=RIGHT)

    def aktualizuj_sume():
        try:
            suma = pobierz_sume_wydatkow(conn)
            suma_label.config(text=f"Suma wszystkich wydatków: {suma:.2f} zł")
        except Exception as e:
            messagebox.showerror("Błąd", f"Błąd podczas obliczania sumy: {str(e)}")

    # Modyfikacja funkcji odswiez_tabele
    def odswiez_tabele():
        try:
            for row in tabela.get_children():
                tabela.delete(row)
            dane = pobierz_wszystkie_wydatki(conn)
            for row in dane:
                tabela.insert("", END, values=row)
            aktualizuj_sume()  # Dodaj to wywołanie
        except Exception as e:
            messagebox.showerror("Błąd", f"Błąd podczas odświeżania tabeli: {str(e)}")
            print(f"Błąd podczas odświeżania tabeli: {e}")

    root.mainloop()