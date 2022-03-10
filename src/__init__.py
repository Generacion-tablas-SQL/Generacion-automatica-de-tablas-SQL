import traceback

from poblador import poblador_tablas

def main():
    create_table = "CREATE TABLE Persona (" \
                   "real NUMBER(4,2) NULL CHECK (NOT REal < 0.00 AND REAL <= 0.03)," \
                   "ent INT UNIQUE CHECK (ent > 3 and ent < 50)," \
                   "string VARCHAR(15) NOT NULL CHECK (string LIKE 'C%' and LENGTH(string) > 5 and LENGTH(string) < 20)," \
                   "fec1 DATE NOT NULL, " \
                   "fec2 TIMESTAMP(2) NOT NULL)"

    select1 = "SELECT string FROM Persona WHERE string like 'S%'"
    select2 = "SELECT ent, real FROM Persona WHERE ent > 30 and ent < 40"
    select3 = "SELECT ent, real  FROM Persona WHERE ent > 30 and real > 0.00 and string != 'Carting'"
    select4 = "SELECT ent FROM Persona WHERE ent > 40 and ent < 30"
    select5 = "SELECT fec1, ent FROM Persona WHERE fec1 > '30/08/2000' and ent > 35"

    try:
        print(*poblador_tablas(create_table, select1), sep='\n')
    except Exception as msg:
        traceback.print_exc()
        print(msg)


if __name__ == '__main__':
    main()
