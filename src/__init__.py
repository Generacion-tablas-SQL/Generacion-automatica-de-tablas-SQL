import traceback

from poblador import poblador_tablas

def main():
    create_table = "CREATE TABLE Persona (" \
                   "real NUMBER(4,2) UNIQUE NULL CHECK (REal >= 0.00 AND REAL <= 0.03)," \
                   "ent INT ," \
                   "string VARCHAR(15) NOT NULL CHECK (string LIKE 'C%' and LENGTH(string) > 5 and LENGTH(string) < 20)," \
                   "fec1 DATE NOT NULL, " \
                   "fec2 TIMESTAMP(2) NOT NULL)"

    select1 = "SELECT string FROM Persona WHERE fec1 > '01/02/2000'"
    select2 = "SELECT ent, real FROM Persona WHERE ent > 3 and ent < 6"
    select3 = "SELECT ent, real  FROM Persona WHERE ent > 30 and real > 0.00"
    select4 = "SELECT ent FROM Persona WHERE ent > 40 and ent < 30"
    select5 = "SELECT fec1, ent FROM Persona WHERE fec1 > '30/08/2000' and ent > 35"

    try:
        print(*poblador_tablas(create_table, select3), sep='\n')
    except Exception as msg:
        traceback.print_exc()
        print(msg)


if __name__ == '__main__':
    main()
