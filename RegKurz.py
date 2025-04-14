from flask import Flask, request # type: ignore
import sqlite3
import hashlib

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
        <a href="/registracia_trenera"><button>Registruj trénera</button></a>
        <a href="/pridanie_kurzu"><button>Registruj kurz</button></a>
        <hr>
    '''


# STRÁNKA S FORMULÁROM NA REGISTRÁCIU TRÉNERA. Vráti HTML formulár s elementami
# Metóda je GET. (Predtým sme metódu nedefinovali. Ak žiadnu neuvedieme, automaticky je aj tak GET)
@app.route('/registracia_trenera', methods=['GET'])
def registracia_form():
    return '''
        <h2>Registrácia trénera</h2>
        <form action="/registracia" method="post">
            <label>Meno:</label><br>
            <input type="text" name="meno" required><br><br>

            <label>Priezvisko:</label><br>
            <input type="text" name="priezvisko" required><br><br>

            <label>Špecializácia:</label><br>
            <input type="text" name="specializacia" required><br><br>

            <label>Telefón:</label><br>
            <input type="text" name="telefon" required><br><br>

            <label>Heslo:</label><br>
            <input type="password" name="heslo" required><br><br>

            <button type="submit">Registrovať</button>
        </form>
        <hr>
        <a href="/">Späť</a>
    '''

@app.route('/pridanie_kurzu', methods=['GET'])
def pridanie_kurzu():
    return '''
        <h2>Registrácia kurzu</h2>
        <form action="/pridanie_kurzu" method="post">
            <label>Názov:</label><br>
            <input type="text" name="nazov" required><br><br>

            <label>sport:</label><br>
            <input type="text" name="sport" required><br><br>

            <label>Počet účastnikov:</label><br>
            <input type="text" name="pocet_ucastnikov" required><br><br>

            <label>ID_Trenera:</label><br>
            <input type="text" name="ID_Trenera" required><br><br>

            <button type="submit">Registrovať</button>
        </form>
        <hr>
        <a href="/">Späť</a>
    '''

# API ENDPOINT NA SPRACOVANIE REGISTRÁCIE. Mapuje sa na mená elementov z formulára z predošlého requestu (pomocou request.form[...])
# Pozor - metóda je POST
@app.route('/registracia_trenera', methods=['POST'])
def registracia_trenera():
    meno = request.form['meno']
    priezvisko = request.form['priezvisko']
    specializacia = request.form['specializacia']
    telefon = request.form['telefon']
    heslo = request.form['heslo']

    # Hashovanie hesla
    heslo_hash = hashlib.sha256(heslo.encode()).hexdigest()
    # Príklad:

    # Zápis do databázy
    conn = pripoj_db()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO Treneri (Meno, Priezvisko, Specializacia, Telefon, Heslo) VALUES (?, ?, ?, ?, ?)", 
                   (meno, priezvisko, specializacia, telefon, heslo_hash))
    conn.commit()
    conn.close()

    # Hlásenie o úspešnej registrácii
    return '''
        <h2>Tréner bol úspešne zaregistrovaný!</h2>
        <hr>
        <a href="/">Späť</a>
    '''

def sifrovanie(parametertext):
        A = 5
        B = 8

        result = ""

        for char in parametertext:     # V cykle pracujeme s každým znakom samostatne, výsledok pripisujeme do viet

            # Prevedieme znak na veľké písmeno - funkcia UPPER()
            char = char.upper()

            # číselné vyjadrenie písmena do premennej X (A=0, B=1, ..., Z=25) - funkcia ORD() (tu iba odčítame jeho ASCII reprezentáciu)
            cislopismena = ord(char) - ord('A')
            cislopismena = int(cislopismena)
            sifra = (A*(cislopismena)+B) % 26
            pismeno = chr(sifra+ ord('A'))
            result += pismeno
        return result

@app.route('/pridanie_kurzu', methods=['POST'])
def registracia_kurzu():
    nazov = request.form['nazov']
    sport = request.form['sport']
    pocet_ucastnikov = request.form['pocet_ucastnikov']
    ID_Trenera = request.form['ID_Trenera']

    sifrovany_nazov = sifrovanie(nazov)
    sifrovany_sport = sifrovanie(sport)
    
    conn = pripoj_db()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO Kurzy (Nazov_kurzu, Typ_sportu, Max_pocet_ucastnikov, ID_Trenera) VALUES (?, ?, ?, ?)", 
                   (sifrovany_nazov, sifrovany_sport, pocet_ucastnikov, ID_Trenera))
    conn.commit()
    conn.close()
    
    return '''
        <h2>Kurz bol úspešne zaregistrovaný!</h2>
        <hr>
        <a href="/">Späť</a>
    '''

if __name__ == '__main__':
    app.run(debug=True)