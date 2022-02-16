from poblador import poblador_tablas
import argparse

def parse_args():
    parser = argparse.ArgumentParser(description="Generación automática de tablas SQL")
    parser.add_argument("create_sentences", help="Lista con sentencias create")
    parser.add_argument("select_sentence", help="Sentencia select")
    args = parser.parse_args()
    return args

def main():
    create_table = "CREATE TABLE Persona (" \
                   "real NUMBER(4,2) UNIQUE NULL CHECK (NOT REal <= 0 AND REAL < 20 AND real != 10)," \
                   "ent INT CHECK (ent > 12 and ent < 50)," \
                   "string VARCHAR(15) UNIQUE NULL CHECK (string LIKE 'C%' and LENGTH(string) > 5 and LENGTH(string) < 10)," \
                   "fec1 DATE UNIQUE NOT NULL, " \
                   "fec2 TIMESTAMP(2) UNIQUE NOT NULL)"

    select1 = "SELECT ent FROM Persona"
    select2 = "SELECT ent, real FROM Persona"
    select3 = "SELECT string, fec1  FROM Persona WHERE ent > 50"

    inputs = parse_args()

    print(*poblador_tablas(inputs.create_sentences, inputs.select_sentence), sep='\n')


if __name__ == '__main__':
    main()
