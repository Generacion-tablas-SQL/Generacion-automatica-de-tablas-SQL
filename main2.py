import json
import constantes
import random
from mo_sql_parsing import format

# sentencia_tablas4 = """CREATE TABLE Persona (
#   Id INTEGER CHECK (Id > 50) ,
#   Nombre VARCHAR(30) ,
#   CONSTRAINT NombreLargo CHECK (LENGTH(Nombre) > 5)
# );"""

# print(parse(sentencia_tablas4))

# salida: {'create table': {'name': 'Persona', 'columns': [
# {'name': 'id', 'type': {'integer': {}}, 'option': {'check': {'gt': ['Id', 50]}}},
# {'name': 'nombre', 'type': {'varchar': 30}}],
# 'constraint': {'name': 'NombreLargo', 'check': {'gt': [{'length': 'Nombre'}, 5]}}}}

# generate_int({'name': 'id', 'type': {'integer': {}}, 'option': {'check': {'gt': ['Id', 50]}}},
# "{'name': 'NombreLargo', 'check': {'gt': [{'length': 'Nombre'}, 5]}}}")
def generate_int2(column, constraint):
    data_type = column.get("type")
    key = list(data_type.keys())

    if key[0] not in constantes.ENTEROS:
        return -1
    else:
        return random.randint(0, 100)

print(generate_int2({'name': 'id', 'type': {'number': {}}, 'option': {'check': {'gt': ['Id', 50]}}},
              "{'name': 'NombreLargo', 'check': {'gt': [{'length': 'Nombre'}, 5]}}}"))