import argparse
import traceback
from poblador import poblador_tablas

def main():
    create_table = "CREATE TABLE Persona (" \
                   "real NUMBER(4,2) CHECK (REal >= 0.00 AND REAL <= 0.03)," \
                   "ent INT CHECK (INT > 25 AND INT < 45)," \
                   "string VARCHAR(15) NOT NULL CHECK (string LIKE 'C%' and LENGTH(string) > 5 and LENGTH(string) < 20)," \
                   "fec1 DATE NOT NULL, " \
                   "fec2 TIMESTAMP(2) NOT NULL)"

    select1 = "SELECT string FROM Persona WHERE LENGTH(string) < 4"
    select2 = "SELECT ent FROM Persona WHERE ent > 50 and real != 0.02"
    select3 = "SELECT string FROM Persona WHERE ent > 50 and string like 'Car'"
    select4 = "SELECT ent FROM Persona WHERE ent > 30 and ent < 32"
    select5 = "SELECT string FROM Persona WHERE string != 'Carmen' and string like 'Car%'"
    select6 = "SELECT fec1, ent FROM Persona WHERE fec1 > '30/08/2000' and ent > 35"
    select7 = "SELECT ent, real  FROM Persona WHERE ent > 30 and real > 0.00 and string != 'Carting'"
    select8 = "SELECT ent, real  FROM Persona WHERE ent > 30 and real > 0.00 and string != 'Carting' and fec1 > '30/08/2000'"

    try:
        print(*poblador_tablas(create_table, select8), sep='\n')
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
