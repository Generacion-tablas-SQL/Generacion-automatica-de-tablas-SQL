

import random
from random import randint

# Para estos generadores de los diferentes tipos de datos tenemos en cuenta las restricciones de tipo:
# UNIQUE, PRIMARY KEY, REFERENCES , *NOT NULL, *CHECK Y LENGTH


# Generador de numeros enteros
# INT = INTEGER

def generate_int(id, valor):

    if(eval("id.lower() == 'integer' or id.lower() == 'int'")):
        if(not eval("id.lower() == 'null'")):
            n = random.randint(0,500)
            print(n)


generate_int("INT")
#generate_int("INTEGER")
#generate_int("inTeGer")
#generate_int("integer")
















