import argparse
import traceback
from poblador import poblador_tablas

def main():
    create_table1 = "CREATE TABLE Persona (" \
                   "real BINARY_FLOAT," \
                   "ent INT CHECK (INT > 25 AND INT <= 28)," \
                   "string VARCHAR(15) CHECK (string LIKE 'C%' and LENGTH(string) != 5 and LENGTH(string) <= 20)," \
                   "fec1 DATE NOT NULL CHECK(fec1 > '10/12/2000'), " \
                   "fec2 TIMESTAMP(2) NOT NULL)"

    select15 = "SELECT string FROM Persona WHERE LENGTH(string) <= 6 or LENGTH(string) > 2;"
    select16 = "SELECT ent FROM Persona WHERE real > 50 and real != 0.02;"
    select17 = "SELECT string FROM Persona WHERE ent > 30 and string like 'Carmen';"
    select4 = "SELECT ent FROM Persona WHERE ent > 30 and ent < 32"
    select5 = "SELECT string FROM Persona WHERE string != 'Carmen' and string like 'Car%';"
    select6 = "SELECT fec1, ent FROM Persona WHERE fec1 > '30/08/2000' and ent > 35;"
    select7 = "SELECT ent, real  FROM Persona WHERE ent > 30 and real > 0.00 and string != 'Carting';"
    select8 = "SELECT ent, real  FROM Persona WHERE ent > 30 and real > 0.00 and string != 'Carting' and fec1 > '30/08/2000';"
    select0 = "SELECT * FROM Persona;"

    create_table2 = "CREATE TABLE Club(" \
                        "CIF NUMBER(4) PRIMARY KEY NOT NULL ," \
                        "Nombre_Club VARCHAR(50) NOT NULL," \
                        "Sede VARCHAR(100)," \
                        "NumSocios NUMBER(5)," \
                        "NumAsientos NUMBER(5)" \
                    ");" \
                    "CREATE TABLE Jugador(" \
                        "NIF NUMBER(8) PRIMARY KEY NOT NULL," \
                        "Nombre VARCHAR(30) NOT NULL," \
                        "Altura NUMBER(3, 2)," \
                        "FechaNacimiento DATE," \
                        "CIF_Club NUMBER(4) REFERENCES Club(CIF)" \
                    ");" \
                    "CREATE TABLE Enfrenta(" \
                        "CIF_L NUMBER(4) REFERENCES Club(CIF) NOT NULL," \
                        "CIF_V NUMBER(4) REFERENCES Club(CIF) NOT NULL," \
                        "Goles_L NUMBER(2)," \
                        "Goles_V NUMBER(2)," \
                        "Fecha DATE," \
                        "CONSTRAINT PK_Enfrena PRIMARY KEY (CIF_L, CIF_V)" \
                    ");" \
                    "CREATE TABLE Jugador2(" \
                        "NIF2 NUMBER(8) PRIMARY KEY NOT NULL," \
                        "Nombre VARCHAR(30) NOT NULL," \
                        "Altura NUMBER(3, 2)," \
                        "CIF_Club2 NUMBER(4) REFERENCES Club(CIF)" \
                    ");"

    select9 = "SELECT * From Club JOIN Jugador ON CIF = CIF_CLUB;  "
    select10 = "SELECT * From Club JOIN Jugador ON CIF = CIF_CLUB JOIN Enfrenta ON CIF = CIF_L;"
    select11 = "SELECT * From Club JOIN Jugador ON CIF = CIF_CLUB WHERE Altura > 1.65;"
    select12 = "SELECT * From Club JOIN Jugador ON CIF = CIF_CLUB JOIN Enfrenta ON CIF = CIF_L WHERE Altura > 1.65;"
    select13 = "SELECT * From Club WHERE Nombre_Club = Sede;"
    select14 = "SELECT * From Enfrenta join  WHERE CIF_L = CIF AND Goles_V > 4 ;"










    create_table = "CREATE TABLE Club(" \
                        "CIF NUMBER(4) PRIMARY KEY NOT NULL CHECK (CIF > 0)," \
                        "Nombre_Club VARCHAR(10) NOT NULL," \
                        "Sede VARCHAR(17)," \
                        "NumSocios NUMBER(5) CHECK (NumSocios > 0) " \
                    ");" \
                    "CREATE TABLE Jugador(" \
                        "NIF NUMBER(8) PRIMARY KEY NOT NULL CHECK (NIF > 0)," \
                        "Nombre VARCHAR(30) NOT NULL," \
                        "Altura NUMBER(3, 2)," \
                        "FechaNacimiento DATE," \
                        "CIF_Club NUMBER(4) REFERENCES Club(CIF)" \
                    ");" \

    select3 = "SELECT * From Club JOIN Jugador ON CIF = CIF_CLUB " \
              "WHERE Altura > 1.65 or FechaNacimiento > '05/07/2000' ;"

    select1 = "SELECT * FROM Club WHERE CIF > 23;"
    select2 = "SELECT * FROM Club WHERE LENGTH(Nombre_Club) <= 5 and Nombre_Club like 'Equip%';"









    try:
        print(*poblador_tablas(create_table, select3), sep='\n')
    except Exception as msg:
        traceback.print_exc()
        print(msg)


if __name__ == '__main__':
    # parser = argparse.ArgumentParser(description='Create a ArcHydro schema')
    # parser.add_argument('--tables', metavar='path', required=True,
    #                    help='DB tables separated by semicolon.')
    # parser.add_argument('--select', metavar='path', required=True,
    #                     help='select statement')
    # args = parser.parse_args()
    # model_schema(workspace=args.workspace, schema=args.schema, dem=args.dem)
    # main(tables=args.tables, select=args.select)
    main()
