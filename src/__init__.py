import traceback

from poblador import poblador_tablas

def main():
    create_table = "CREATE TABLE Persona (" \
                   "real NUMBER(4,2) UNIQUE NULL CHECK (NOT REal < 0.00 AND REAL < 0.12)," \
                   "ent INT UNIQUE CHECK (ent >= 0 and ent <= 9)," \
                   "string VARCHAR(15) UNIQUE NULL CHECK (string LIKE 'C%' and LENGTH(string) > 5 and LENGTH(string) < 10)," \
                   "fec1 DATE UNIQUE NOT NULL, " \
                   "fec2 TIMESTAMP(2) UNIQUE NOT NULL)"

    select1 = "SELECT ent FROM Persona"
    select2 = "SELECT ent, real FROM Persona"
    select3 = "SELECT ent, ent  FROM Persona WHERE ent > -1"
    try:
        print(*poblador_tablas(create_table, select3), sep='\n')
    except Exception as msg:
        traceback.print_exc()
        print(msg)


if __name__ == '__main__':
    main()
