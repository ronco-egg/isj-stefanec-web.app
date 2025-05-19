# Je NUTNÉ nainštalovať alíček: do konzoly napíšte "pip install flask"
from flask import Flask, request, render_template
from flask_sqlalchemy import SQLAlchemy
import hashlib
import os
import sqlite3

app = Flask(__name__,instance_relative_config=True)
db_path = os.path.join(app.instance_path,"kurzy.db")

app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{db_path}".replace("//","/")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)
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

        <a href="/registracia_trenera"><button>Registruj trénera</button></a>
        <a href="/pridanie_kurzu"><button>Registruj kurz</button></a>
        <hr>
    '''

class Kurz(db.Model): 
    __tablename__= "Kurzy" 
    ID_kurzu             = db.column(db.Integer, primary_key=True) 
    Nazov_kurzu          = db.column(db.String, nullable=False) 
    Typ_sportu           = db.column(db.String) 
    Max_pocet_ucastnikov = db.column(db.Integer) 
    ID_trenera           = db.Column(db.Integer) 
    
    def __repr__(self):
        return f"<Kurz {self.Nazov_kurzu}>"


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

# PODSTRÁNKA NA ZOBRAZENIE KURZOV
@app.route('/miesta')  # API endpoint
def zobraz_miesta():
    conn = pripoj_db()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM Miesta")
    miesto = cursor.fetchall()

    conn.close()

   
    # for Nazov_miesta in miesto:
     #    vystup += f"<p>{Nazov_miesta}</p>"      # výpis kurzov do paragrafov <p>

    # vystup += '<a href="/">Späť</a>'    # k výstupu (+) pridáme odkaz s textom "Späť", ktorý odkazuje na stránku "/", teda homepage
    return render_template ("miesta.html", miesto = miesto)


@app.route('/kurzy')  # API endpoint
def zobraz_kurzy():
    """
    conn = pripoj_db()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM Kurzy")
    kurzy = cursor.fetchall()

    conn.close()

    # Jednoduchý textový výpis kurzov
    return render_template ("kurzy.html", kurzy = kurzy)   
"""
    kurzy = Kurz.query.all()
    return render_template("kurzy.html", kurzy = kurzy)


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
    #vystup = "<h2>Zoznam trénerov a kurzov:</h2>"
    #for trener in treneri:
    #    vystup += f"<p>{trener}</p>"

    # Odkaz na návrat
    #vystup += '<a href="/">Späť</a>'
    return render_template ("treneri.html", treneri = treneri)


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
    #vystup = "<h2>Súčet kapacity kurzov začínajúce na P:</h2>"
    #for Max_pocet_ucastnikov in Kapacita:
    #    vystup += f"<p>{Max_pocet_ucastnikov}</p>"
    #vystup += '<a href="/">Späť</a>'
    return render_template ("kapacita.html",Kapacita = Kapacita)

if __name__ == '__main__':
    app.run(debug=True)


# Aplikáciu spustíte, keď do konzoly napíšete "python app.py"