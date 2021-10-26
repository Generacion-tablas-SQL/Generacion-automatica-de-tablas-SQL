import random
from random import randint

# Para estos generadores de los diferentes tipos de datos tenemos en cuenta las restricciones de tipo:
# *UNIQUE, PRIMARY KEY, REFERENCES, CONSTRAINT , *NOT NULL, CHECK Y LENGTH


# Generador de números enteros
# id = INT or INTEGER
# opt1 = null or nullable
# opt2 = unique

def generate_int(id, opt1, opt2):
    n = None;
    generados = []
    if (not eval("opt1.lower() == 'nullable' or opt1.lower() == 'null'")):  # No es nulo
        if(eval("id.lower() == 'integer' or id.lower() == 'int'")):  #Es un entero
                n = random.randint(0,10)
                generados.append(n)
                if(eval("id.lower() == 'unique'")): #Es valor unico
                    while n in generados:
                        n = random.randint(0, 10)
                    generados.append(n)
                print(n)
        else:
            print("No es un entero")
            exit()
    else:
        print(n)



generate_int("INT", "", "UNIQUE")
generate_int("INT", "", "UNIQUE")
generate_int("INT", "", "UNIQUE")
generate_int("INT", "", "UNIQUE")
generate_int("", "", "UNIQUE")
generate_int("INT", "NULL", "UNIQUE")
generate_int("INT", "nuLL", "UNIQUE")
generate_int("INT", "", "UNIQUE")
generate_int("INT", "", "UNIQUE")













