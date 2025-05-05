# Je NUTNÉ nainštalovať alíček: do konzoly napíšte "pip install flask"
from flask import Flask, request, render_template
import sqlite3

app = Flask(__name__)


# rýchly úvod do HTML elementov:
# <h1> ...text... </h1>, alebo <h2>             - heading - nadpisy
# <p> ...text... </p>                           - paragraf (normálny text)
# <a href="www.---.com"> ...text...></a>        - odkaz (v rámci textu)
# <button> ...text... </button>                 - tlačidlo s textom


# Pripojenie k databáze
def pripoj_db():
    conn = sqlite3.connect("kurzy.db")
    return conn


@app.route('/')  # API endpoint
def index():
    # Úvodná homepage s dvoma tlačidami ako ODKAZMI na svoje stránky - volanie API nedpointu
    return '''
        <h1>Výber z databázy</h1>
        <a href="/miesta"><button>Zobraz všetky miesta</button></a>
        <a href="/kurzy"><button>Zobraz všetky kurzy</button></a>
        <a href="/treneri"><button>Zobraz všetkých trénerov a kurzov</button></a>
        <a href="/sucetkapacity"><button>Výpis súčtu maximálnej kapacity všetkých kurzov, ktoré začínajú na písmeno P</button></a>
        <hr>
    '''


# PODSTRÁNKA NA ZOBRAZENIE KURZOV
@app.route('/miesta')  # API endpoint
def zobraz_miesta():
    conn = pripoj_db()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM Miesta")
    miesto = cursor.fetchall()

    conn.close()

    # Jednoduchý textový výpis kurzov
    vystup = "<h2>Zoznam Miest:</h2>"  # nadpis <h2>
    for Nazov_miesta in miesto:
        vystup += f"<p>{Nazov_miesta}</p>"      # výpis kurzov do paragrafov <p>

    # Odkaz na návrat
    vystup += '<a href="/">Späť</a>'    # k výstupu (+) pridáme odkaz s textom "Späť", ktorý odkazuje na stránku "/", teda homepage
    return vystup


@app.route('/kurzy')  # API endpoint
def zobraz_kurzy():
    conn = pripoj_db()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM Kurzy")
    kurzy = cursor.fetchall()

    conn.close()

    # Jednoduchý textový výpis kurzov
    return render_template ("kurzy.html", kurzy = kurzy)


# PODSTRÁNKA NA ZOBRAZENIE TRÉNEROV
@app.route('/treneri')  # API endpoint
def zobraz_trenerov():
    conn = pripoj_db()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT T.ID_trenera, T.Meno || ' ' || T.Priezvisko as Trener, Nazov_kurzu
        FROM Treneri T LEFT JOIN Kurzy K ON T.ID_trenera = K.ID_trenera
    """)
    treneri = cursor.fetchall()

    conn.close()

    # Jednoduchý textový výpis trénerov a ich kurzov
    vystup = "<h2>Zoznam trénerov a kurzov:</h2>"
    for trener in treneri:
        vystup += f"<p>{trener}</p>"

    # Odkaz na návrat
    vystup += '<a href="/">Späť</a>'
    return vystup

@app.route('/sucetkapacity')
def zobraz_kapacitu():
    conn = pripoj_db()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT SUM(Max_pocet_ucastnikov) 
        FROM Kurzy WHERE Nazov_kurzu LIKE 'P%'
    """)
    Kapacita = cursor.fetchall()

    conn.close()
    vystup = "<h2>Súčet kapacity kurzov začínajúce na P:</h2>"
    for Max_pocet_ucastnikov in Kapacita:
        vystup += f"<p>{Max_pocet_ucastnikov}</p>"
    vystup += '<a href="/">Späť</a>'
    return vystup

if __name__ == '__main__':
    app.run(debug=True)


# Aplikáciu spustíte, keď do konzoly napíšete "python app.py"