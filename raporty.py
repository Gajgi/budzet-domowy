import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
import seaborn as sns
import sqlite3

plt.style.use('default')



def wczytaj_dane():
    """Wczytuje dane z bazy SQLite do DataFrame"""
    conn = sqlite3.connect('wydatki.db')
    df = pd.read_sql_query("""
                           SELECT kategoria, kwota, date(data) as data, uwagi
                           FROM wydatki
                           """, conn)
    df['data'] = pd.to_datetime(df['data'])
    return df


def raport_miesieczny(rok=None, miesiac=None):
    """Generuje raport miesięczny wydatków"""
    df = wczytaj_dane()
    if rok is None:
        rok = datetime.now().year
    if miesiac is None:
        miesiac = datetime.now().month

    mask = (df['data'].dt.year == rok) & (df['data'].dt.month == miesiac)
    monthly_df = df[mask]

    # Podsumowanie według kategorii
    summary = monthly_df.groupby('kategoria')['kwota'].agg(['sum', 'count']).round(2)
    summary.columns = ['Suma wydatków', 'Liczba transakcji']

    # Wykres kołowy
    plt.figure(figsize=(12, 6))
    plt.subplot(1, 2, 1)
    monthly_df.groupby('kategoria')['kwota'].sum().plot(kind='pie', autopct='%1.1f%%')
    plt.title(f'Wydatki w {miesiac}/{rok}')

    # Wykres słupkowy
    plt.subplot(1, 2, 2)
    monthly_df.groupby('kategoria')['kwota'].sum().plot(kind='bar')
    plt.title('Suma wydatków według kategorii')
    plt.xticks(rotation=45)

    plt.tight_layout()
    plt.show()

    return summary


def trend_wydatkow(ostatnie_miesiace=6):
    """Pokazuje trend wydatków w czasie"""
    df = wczytaj_dane()
    trend = df.groupby([df['data'].dt.to_period('M')])['kwota'].sum()
    trend = trend.tail(ostatnie_miesiace)

    plt.figure(figsize=(12, 6))
    trend.plot(kind='line', marker='o')
    plt.title('Trend wydatków w czasie')
    plt.grid(True)
    plt.xticks(rotation=45)
    plt.show()

    return trend


def top_wydatki(n=5):
    """Pokazuje top N największych wydatków"""
    df = wczytaj_dane()
    return df.nlargest(n, 'kwota')[['data', 'kategoria', 'kwota', 'uwagi']]


def statystyki_kategorii():
    """Generuje szczegółowe statystyki dla każdej kategorii"""
    df = wczytaj_dane()
    stats = df.groupby('kategoria').agg({
        'kwota': ['count', 'sum', 'mean', 'min', 'max']
    }).round(2)
    stats.columns = ['Liczba', 'Suma', 'Średnia', 'Minimum', 'Maksimum']
    return stats


def wykres_dzienny_tydzien():
    """Pokazuje wydatki dzienne w ostatnim tygodniu"""
    df = wczytaj_dane()
    last_week = df[df['data'] > pd.Timestamp.now() - pd.Timedelta(days=7)]
    daily = last_week.groupby('data')['kwota'].sum()

    plt.figure(figsize=(12, 6))
    daily.plot(kind='bar')
    plt.title('Wydatki w ostatnim tygodniu')
    plt.xticks(rotation=45)
    plt.grid(True)
    plt.show()

    return daily