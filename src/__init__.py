import traceback

from poblador import poblador_tablas

def main():
    create_table = "CREATE TABLE Persona (" \
                   "real NUMBER(4,2) NULL CHECK (NOT REal < 0.00 AND REAL < 0.02)," \
                   "ent INT UNIQUE CHECK (ent > 12 and ent < 50)," \
                   "string VARCHAR(15) UNIQUE NULL CHECK (string LIKE 'C%' and LENGTH(string) > 5 and LENGTH(string) < 10)," \
                   "fec1 DATE UNIQUE NOT NULL, " \
                   "fec2 TIMESTAMP(2) UNIQUE NOT NULL)"

    select1 = "SELECT ent FROM Persona"
    select2 = "SELECT ent, real FROM Persona"
    select3 = "SELECT ent, real  FROM Persona WHERE ent > 30 and real = 0.01"
    try:
        print(*poblador_tablas(create_table, select3), sep='\n')
    except Exception as msg:
        traceback.print_exc()
        print(msg)


if __name__ == '__main__':
    main()
