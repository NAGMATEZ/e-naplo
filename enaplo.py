import sqlite3 as sqlite

# Connect to the SQLite database (it will create one if it doesn't exist)
connect = sqlite.connect('naplo.db')
c = connect.cursor()

c.execute("DROP TABLE IF EXISTS tanulok")
c.execute("DROP TABLE IF EXISTS tanarok")
c.execute("DROP TABLE IF EXISTS targyak")
c.execute("DROP TABLE IF EXISTS jegyek")

# Create tables
def tablak():
    c.execute("BEGIN IMMEDIATE TRANSACTION")
    # tanulok table
    c.execute(''' 
        CREATE TABLE IF NOT EXISTS tanulok (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        veznev TEXT,                     
        kernev TEXT,
        anyjaneve TEXT,
        kor INTEGER,
        osztaly TEXT
    )
    ''')
    
    # tanarok table
    c.execute(''' 
        CREATE TABLE IF NOT EXISTS tanarok (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        veznev TEXT,
        kernev TEXT
    )
    ''')

    # targyak table
    c.execute(''' 
        CREATE TABLE IF NOT EXISTS targyak (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nev TEXT,
        tanar_ID INTEGER
    )
    ''')

    # jegyek table
    c.execute(''' 
        CREATE TABLE IF NOT EXISTS jegyek (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        tanulo_id INTEGER,
        datum TEXT,
        targy_ID INTEGER, 
        jegy_tipus TEXT,
        jegy INTEGER
    )
    ''')
    connect.commit()

# Insert sample data into tables
def adatok():
    c.execute("BEGIN IMMEDIATE TRANSACTION")
    # Insert students
    c.executemany("INSERT INTO tanulok (veznev, kernev, anyjaneve, kor, osztaly) VALUES (?, ?, ?, ?, ?)", [
        ('Kovacs', 'Eszter', "Szabo Magdolna", 19, 'A'),
        ('Nagy', 'Zsigmond', "Nagy Agnes", 20, 'B'),
        ('Zold', 'Elemer', "Palocz Andrea", 17, 'D'),
        ('Karvalics', 'Janos', "Karacsony Panna", 22, 'C'),
        ('Elso', 'Diana', "Molnar Agota", 18, 'E'),
        ('Arva', 'Karoly', "Arva Barbara", 19, 'F'),
        ('Medve', 'Marton', "Palota Agnes", 20, 'C'),
        ('Lakatos', 'Benedek', "Kovacs Eszter", 17, 'G'),
        ('Pinczey', 'Andras', "Pinczey Karolina", 19, 'A'),
        ('Felho', 'Odett', "Nap Otilia", 20, 'B')
    ])

    # Insert teachers
    c.executemany("INSERT INTO tanarok (veznev, kernev) VALUES (?, ?)", [
        ('Molnar', 'Gergely'),
        ('Kiss', 'Eszter'),
        ('Horvath', 'Laszlo'),
        ('Farkas', 'Zsuzsanna'),
    ])

    # Insert subjects
    c.executemany("INSERT INTO targyak (nev, tanar_ID) VALUES (?, ?)", [
        ('Tortenelem', 1),
        ('Testneveles', 2),
        ('Matematika', 4),
        ('Digitalis Kultura', 2),
        ('Vizualis kultura', 3),
    ])

    # Insert grades
    c.executemany("INSERT INTO jegyek (tanulo_id, datum, targy_ID, jegy_tipus, jegy) VALUES (?, ?, ?, ?, ?)", [
        (4,'2024-09-03',1, "TZ", 4),
        (5,'2024-09-03',1, "TZ", 5),
        (2,'2023-09-04',2, "TZ", 4),
        (1,'2023-09-10',5, "TZ", 3),
        (6,'2023-09-15',3, "TZ", 4),
        (8,'2023-09-15',3, "TZ", 5),
        (9,'2023-09-17',4, "TZ", 2),
    ])
    connect.commit()

tablak()
adatok()

# Function to calculate weighted average grades
def felevijegy():
    c.execute("BEGIN IMMEDIATE TRANSACTION")
    veznev=input("Kérlek add meg a kívánt tanuló vezetéknevét: ")
    kernev=input("Kérlek add meg a kívánt tanuló keresztnevét: ")
    anyjaneve=input("Kérlek add meg a kívánt tanuló anyjának nevét: ")
    c.execute(''' 
        SELECT jegy, veznev, kernev, jegy_tipus
        FROM tanulok
        INNER JOIN jegyek ON tanulok.id=jegyek.tanulo_ID
        WHERE tanulok.veznev=? AND tanulok.kernev=? AND tanulok.anyjaneve=?
'''), (veznev, kernev, anyjaneve)
    
    jegyek_lista = c.fetchall()
    
    sum_jegyek = 0
    for jegy in jegyek_lista:
        if jegy[3] == 'HF':
            sum_jegyek += jegy[0] * 0.5
        elif jegy[3] == 'TZ':
            sum_jegyek += jegy[0] * 2
        else:
            sum_jegyek += jegy[0]
    
        if jegyek_lista:
            atlag = sum_jegyek / len(jegyek_lista)
            print(f"{jegy[1]} {jegy[2]} félévi jegy: {round(atlag)}")
        else:
            print("A tanulónak nincsnek érdemjegyei")
    connect.commit()

def tanuloatlag():
    c.execute("BEGIN IMMEDIATE TRANSACTION")
    veznev=input("Kérlek add meg a hozzáadni kívánt tanuló vezetéknevét: ")
    kernev=input("Kérlek add meg a hozzáadni kívánt tanuló keresztnevét: ")
    anyjaneve=input("Kérlek add meg a hozzáadni kívánt anyjának nevét: ")
    for i in range(1,11):
        c.execute(''' 
        SELECT jegy, veznev, kernev, jegy_tipus
        FROM tanulok
        INNER JOIN jegyek ON tanulok.id=jegyek.tanulo_ID
        WHERE tanulok.veznev=? AND tanulok.kernev=? AND tanulok.anyjaneve=?
        '''), (veznev, kernev, anyjaneve)
            
        jegyek_lista=c.fetchall
        connect.commit()
    sum=0
    for jegy in jegyek_lista:
        if jegy[3]=='HF':
            jegy[0]=jegy[0]*0.5
        elif jegy[3]=='TZ':
            jegy[0]=jegy[0]*2
        sum+=jegy[0]
    atlag=sum/len(jegyek_lista)
    print(jegy[1] + " " + jegy[2] +" felevi jegy : " + str(atlag))
    connect.commit()
      
def menu():
    while True:
        print("Üdvözöllek az E-Naplóban! Kérlek válassz az alábbi opciók közül:")
        print("1 - Tanulók statisztikái")
        print("2 - Tárgyak statisztikái")
        print("3 - Érdemjegy műveletek")
        print("4 - Tanuló hozzáadása, vagy szerkesztése")
        print("0 - Kilépés")
        szamok=[1,2,3,4,0]
        try:
            valasz = int(input("Válassz egy opciót (0-4): "))
            if valasz in szamok:
                break
            else:
                print("Érvénytelen választás, próbáld újra!")
        except ValueError:
            print("Csak számokat adj meg! Próbáld újra.")  # Error if input is not an integer
    if valasz==1:
        menu_tanulok()
    elif valasz==2:
        menu_targyak()
    elif valasz==3:
        menu_jegyek()
    elif valasz==4:
        menu_tan_hozz_szerk_torl()
    else:
        input("Sajnáljuk, hogy távozik, de visszavárjuk szoftverünkbe :), kilépni az enter billentyűvel tud     ")
def menu_tan_hozz_szerk_torl():
    while True:
        print("1 - Tanuló hozzáadása")
        print("2 - Tanuló szerkesztése")
        print("3 - Tanuló végleges törlése")
        print("0 - Vissza az előző szintre")
        szamok=[1,2,3,0]
        try:
            valasz = int(input("Válassz egy opciót (0-2): ")) 
            if valasz in szamok: 
                break
            else:
                print("Érvénytelen választás, próbáld újra!") 
        except ValueError:
            print("Csak számokat adj meg! Próbáld újra.")
    
    if valasz==1:
        tanhozz()
    elif valasz==2:
       tanszerk()
    elif valasz==3:
        tantorl()
    elif valasz==0:
        menu()

def tanhozz():
    c.execute("BEGIN IMMEDIATE TRANSACTION")
    veznev=input("Kérlek add meg a hozzáadni kívánt tanuló vezetéknevét: ")
    kernev=input("Kérlek add meg a hozzáadni kívánt tanuló keresztnevét: ")
    anyjaneve=input("Kérlek add meg a hozzáadni kívánt anyjának nevét: ")
    kor=input("Kérlek add meg a hozzáadni kívánt tanuló életkorát: ")
    osztaly=input("Kérlek add meg a hozzáadni kívánt tanuló osztályát (A-D): ")
    
    c.execute('''
        INSERT INTO tanulok
        VALUES(?,?,?,?,?)
        '''), (veznev,kernev,anyjaneve,kor,osztaly)
    connect.commit()
    
def tanszerk():
    c.execute("BEGIN IMMEDIATE TRANSACTION")
    veznev=input("Kérlek add meg a szerkeszteni kívánt tanuló vezetéknevét: ")
    kernev=input("Kérlek add meg a szerkeszteni kívánt tanuló keresztnevét: ")
    anyjaneve=input("Kérlek add meg a szerkeszteni kívánt anyjának nevét: ")
    val=input("A tanuló vezetéknevét, keresztnevét vagy osztályát szeretnéd módosítani? (V - vezetéknév, K - Keresztnév, O - osztály): ")
    kor=0
    while True:
        c.execute(''' 
        SELECT kor
        FROM tanulok
        WHERE tanulok.veznev=? AND tanulok.kernev=? AND tanulok.anyjaneve=?
        '''),(veznev, kernev, anyjaneve) 
        kor=c.fetchall()
        if kor!=False:
            break
        else:
            print("A tanuló nem található, próbáld újra")
    if val=='V':
        uj_veznev=input("Mire változtassuk a kiválasztott tanuló vezetéknevét?: ")
        c.execute('''
        UPDATE jegyek
        SET tanvezn=?
        WHERE jegyek.tanvezn? AND jegyek.tankern=? AND jegyek.anyjanev=?
        '''), (uj_veznev, veznev, kernev, anyjaneve)
        
        c.execute('''
        UPDATE tanulok
        SET veznev=?
        WHERE tanulok.veznev=? AND tanulok.kevnev=? AND tanulok.anyjaneve=?
        '''), (uj_veznev, veznev, kernev, anyjaneve)
        

    if val=='K':
        uj_kernev=input("Mire változtassuk a kiválasztott tanuló keresztnevét?: ")
        c.execute('''
        UPDATE jegyek
        SET tankern=?
        WHERE jegyek.tanvezn? AND jegyek.tankern=? AND jegyek.anyjanev=?
        '''), (uj_kernev, veznev, kernev, anyjaneve)
        
        c.execute('''
        UPDATE tanulok
        SET kernev=?
        WHERE tanulok.veznev=? AND tanulok.kevnev=? AND tanulok.anyjaneve=?
        '''), (uj_kernev, veznev, kernev, anyjaneve)
    
    if val=='O':
        uj_osztaly=input("Melyik osztályba írjuk át a kiválasztott tanulót?: ")
        c.execute('''
        UPDATE tanulok
        SET osztaly=?
        WHERE tanulok.veznev=? AND tanulok.kevnev=? AND tanulok.anyjaneve=?
        '''), (uj_osztaly, veznev, kernev, anyjaneve)
        connect.commit()

def tantorl():
    c.execute("BEGIN IMMEDIATE TRANSACTION")
    veznev=input("Kérlek add meg a törölni kívánt tanuló vezetéknevét: ")
    kernev=input("Kérlek add meg a törölni kívánt tanuló keresztnevét: ")
    anyjaneve=input("Kérlek add meg a törölni kívánt anyjának nevét: ")
    kor=0
    while True:
        c.execute(''' 
        SELECT kor
        FROM tanulok
        WHERE tanulok.veznev=? AND tanulok.kernev=? AND tanulok.anyjaneve=?
        '''),(veznev, kernev, anyjaneve) 
        kor=c.fetchall()
        if kor!=False:
            break
        else:
            print("A tanuló nem található, próbáld újra")
    while True:
        valasz=input("Biztosan törölni szeretnéd a taunlót?:  (I - igen, N - nem, vissza a menübe): ")
        if valasz=='N' or valasz=='I':
            break
        else:
            print(" Próbáld újra, egy betűt várok")
    if valasz=='N':
        menu_tan_hozz_szerk_torl()
    elif valasz=='I':
        c.execute(''' 
        DELETE FROM tanulok
        WHERE tanulok.veznev=? AND tanulok.kernev=? AND tanulok.anyjaneve=?
        '''), (veznev, kernev, anyjaneve)
        connect.commit()
    
def menu_tanulok():
    while True:
        print("1 - Félévi jegy lekérése a tanulóra adott tárgyból")
        print("2 - Tanuló tanulmányi átlaga")
        print("0 - Vissza az előző szintre")
        szamok=[1,2,0]
        try:
            valasz = int(input("Válassz egy opciót (0-2): ")) 
            if valasz in szamok: 
                break
            else:
                print("Érvénytelen választás, próbáld újra!") 
        except ValueError:
            print("Csak számokat adj meg! Próbáld újra.")
    
    if valasz==1:
        felevijegy()
    elif valasz==2:
        tanuloatlag()
    elif valasz==0:
        menu()

def menu_jegyek():
    while True:
        print("1 - Érdemjegy beírása")
        print("2 - Meglévő érdemjegy szerkesztése")
        print("3 - Meglévő érdemjegy törlése")
        print("0 - Vissza az előző szintre")
        szamok=[1,2,3,0]
        try:
            valasz = int(input("Válassz egy opciót (0-3): ")) 
            if valasz in szamok: 
                break
            else:
                print("Érvénytelen választás, próbáld újra!") 
        except ValueError:
            print("Csak számokat adj meg! Próbáld újra.")
        if valasz==1:
            jegy_beiras()
        elif valasz==2:
            jegy_szerk()
        elif valasz==3:
            jegy_torl()
        elif valasz==0:
            menu()

def jegy_beiras():
    c.execute("BEGIN IMMEDIATE TRANSACTION")
    kor=0
    while True:
        veznev=input("Kérlek add meg a tanuló vezetéknevét, akinek jegyet akarsz adni: ")
        kernev=input("Kérlek add meg a tanuló keresztnevét: ")
        c.execute(''' 
        SELECT kor
        FROM tanulok
        WHERE tanulok.veznev=? AND tanulok.kernev=? AND tanulok.anyjaneve=?
        '''),(veznev, kernev, anyjaneve) 
        kor=c.fetchall()
        if kor!=False:
            break
        else:
            print("A tanuló nem található, próbáld újra")
    anyjaneve=input("Kérlek add meg a tanuló anyjának nevét: ")
    datum=input("Kérlek add meg a dátumot kötőjelekkel (pl: 2013-02-13): ")
    targynev=input("Kérlek add meg, hogy melyik tárgyból adsz jegyet a diáknak: ")
    tipusok=["TZ", "F", "HF"]
    while True:
        jegy_tipus=input("Add meg, hogy milyen súlya van az érdemjegynek, amit adni készülsz (TZ - témazáró dolgozat, F - felelet, HF - házi feladat): ")
        if jegy_tipus in tipusok:
            break
        else:
            print("Kérlek válassz a fenti típusok közül!!")
    erdjegyek=[1,2,3,4,5]
    while True:
        try:
            jegy=int(input("Add meg, hogy hányas érdemjegyet szeretnél adni a tanulónak: "))
            if jegy in erdjegyek:
                break
            else:
                print("Nem érdemjegyet írtál be, kérlek 1 és 5 között értékeld a tanulót")
        except ValueError:
            print("Csak számokat adj meg! Próbáld újra.")
    c.execute('''SELECT veznev,kernev,anyjaneve
                 FROM tanulok
                 WHERE veznev=?,kernev=?,anyjaneve=?
              '''), (veznev, kernev, anyjaneve)
    c.execute('''
        INSERT INTO jegyek
        VALUES(?,?,?,?,?,?,?)
        '''), (datum,targynev,jegy_tipus,jegy)
    connect.commit()

def jegy_szerk():
    c.execute("BEGIN IMMEDIATE TRANSACTION")
    tanvezn=input("Add meg kérlek az érdemjegy tuladonosának vezetéknevét: ")
    tankern=input("Add meg kérlek az érdemjegy tuladonosának keresztnevét: ")
    anyjanev=input("Add meg kérlek az érdemjegy tuladonosa édesanyjának nevét: ")
    datum=input("Kérlek add meg a jegy adásának dátumát kötőjelekkel (pl.2013-01-01)")
    targynev=input("Add meg, hogy milyen tárgyból lett adva a jegy?")
    jegy_tipus=input("Add meg kérlek az érdemjegy típusát (TZ - témazáró dolgozat, F - felelet, HF - házi feladat): ")
    c.execute('''
        SELECT jegy
        FROM jegyek
        WHERE jegyek.tanvezn=? AND jegyek.tankern=? AND jegyek.anyjanev=? AND jegyek.datum=?  AND jegyek.targynev LIKE ? AND jegyek.jegy_tipus=?
    ''')(tanvezn,tankern,anyjanev,datum,targynev,jegy_tipus)
    check=c.fetchall
    if check!=False:
        erdjegyek=[1,2,3,4,5]
        while True:
            try:
                uj_jegy=int(input("Hányasra szeretnéd módosítani a jegyet?"))
                if uj_jegy in erdjegyek:
                    break
            except ValueError:
                print("Kérlek, számmal írd le")
        c.execute(''' 
            UPDATE jegyek
            SET jegy=?
            WHERE jegyek.tanvezn=? AND jegyek.tankern=? AND jegyek.anyjanev=? AND jegyek.datum=?  AND jegyek.targynev LIKE ? AND jegyek.jegy_tipus=?
        '''), (uj_jegy,tanvezn,tankern,anyjanev,datum,targynev,jegy_tipus)
    else:
        print("Az adott feltételekkel érdemjegy nem találhatő a naplóban")
    connect.commit()

def jegy_torl():
    c.execute("BEGIN IMMEDIATE TRANSACTION")
    tanvezn=input("Add meg kérlek az érdemjegy tuladonosának vezetéknevét: ")
    tankern=input("Add meg kérlek az érdemjegy tuladonosának keresztnevét: ")
    anyjanev=input("Add meg kérlek az érdemjegy tuladonosa édesanyjának nevét: ")
    datum=input("Kérlek add meg a jegy adásának dátumát kötőjelekkel (pl.2013-01-01)")
    targynev=input("Add meg, hogy milyen tárgyból lett adva a jegy?")
    jegy_tipus=input("Add meg kérlek az érdemjegy típusát (TZ - témazáró dolgozat, F - felelet, HF - házi feladat): ")
    c.execute('''
        SELECT jegy
        FROM jegyek
        WHERE jegyek.tanvezn=? AND jegyek.tankern=? AND jegyek.anyjanev=? AND jegyek.datum=?  AND jegyek.targynev LIKE ? AND jegyek.jegy_tipus=?
    ''')(tanvezn,tankern,anyjanev,datum,targynev,jegy_tipus)
    check=c.fetchall
    if check!=False:
        j=input("A rendszer talált egy jegyet ("+ check[0] + "), biztosan törölni szeretné? ( I - igen , N - nem, vissza az előző menübe)")
        if j=='I':
            c.execute(''' 
            DELETE
            FROM jegyek
            WHERE jegyek.tanvezn=? AND jegyek.tankern=? AND jegyek.anyjanev=? AND jegyek.datum=?  AND jegyek.targynev LIKE ? AND jegyek.jegy_tipus=?
            '''), (tanvezn,tankern,anyjanev,datum,targynev,jegy_tipus)
        elif j=='N':
            menu_jegyek()
    else:
        print("Az adott feltételekkel érdemjegy nem találhatő a naplóban")
    connect.commit()


def menu_targyak():
    print("1 - Egyes tárgyak átlagai")
    print("0 - Vissza az előző szintre")
    szamok=[0,1]
    while True:
        try:
            valasz = int(input("Válassz egy opciót (0-1): ")) 
            if valasz in szamok: 
                break
            else:
                print("Érvénytelen választás, próbáld újra!") 
        except ValueError:
            print("Csak számokat adj meg! Próbáld újra.")
    if valasz==0:
        menu()
    elif valasz==1:
        targyatlag()
    

def targyatlag():
    c.execute("BEGIN IMMEDIATE TRANSACTION")
    targynev=input("Add meg a tárgyat, aminek az átlagát tudni szeretnéd: ")
    oszt=input("Amennyiben szűrni szeretnéd a tárgy átlagát adott osztályra, írd be az osztály betűjelét: ")
    if oszt=="":
        c.execute(''' 
            SELECT jegy
            FROM jegyek
            WHERE jegyek.targynev=?
        '''), (targynev,)
        jegyek_lista=c.fetchall
        sum=0
        for jegy in jegyek_lista:
            if jegy[3]=='HF':
                jegy[0]=jegy[0]*0.5
            elif jegy[3]=='TZ':
                jegy[0]=jegy[0]*2
            sum+=jegy[0]
        atlag=sum/len(jegyek_lista)
        print("A(z) " + str(targynev) + " tárgy átlaga: " + str(round(atlag,2)))
    elif oszt!="":
        c.execute(''' 
        SELECT jegy
        FROM jegyek
        INNER JOIN tanulok
        ON jegyek.tanveznev=tanulok.veznev AND jegyek.tankernev=tanulok.kernev AND jegyek.anyjanev=tanulok.anyjaneve
        WHERE jegyek.targynev=? AND tanulok.osztaly=?
        '''), (targynev, oszt)
        jegyek_lista=c.fetchall
        sum=0
        for jegy in jegyek_lista:
            if jegy[3]=='HF':
                jegy[0]=jegy[0]*0.5
            elif jegy[3]=='TZ':
                jegy[0]=jegy[0]*2
            sum+=jegy[0]
        atlag=sum/len(jegyek_lista)
        print("A(z) " + str(targynev) + " tárgy átlaga: " + str(round(atlag,2)))
    connect.commit()         
menu()
connect.commit()
connect.close()