from tkinter import messagebox


# Funkcja walidacji danych dla wydatków
def sprawdz_poprawnosc_danych(kategoria, kwota, data):
    if not kategoria or not kwota or not data:
        messagebox.showerror("Błąd", "Wszystkie wymagane pola muszą być wypełnione!")
        return False

    try:
        float(kwota)  # Sprawdza, czy kwota jest liczbą
    except ValueError:
        messagebox.showerror("Błąd", "Kwota musi być liczbą!")
        return False

    return True
