from raporty import *

if __name__ == "__main__":
    # Raport miesięczny
    print("\n=== Raport miesięczny ===")
    summary = raport_miesieczny()
    print(summary)

    # Trend wydatków
    print("\n=== Trend wydatków za ostatnie 6 miesięcy ===")
    trend = trend_wydatkow()
    print(trend)

    # Top 5 największych wydatków
    print("\n=== Top 5 największych wydatków ===")
    top = top_wydatki()
    print(top)

    # Statystyki kategorii
    print("\n=== Statystyki według kategorii ===")
    stats = statystyki_kategorii()
    print(stats)

    # Wykres dzienny z ostatniego tygodnia
    print("\n=== Wydatki w ostatnim tygodniu ===")
    daily = wykres_dzienny_tydzien()
    print(daily)