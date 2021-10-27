import json
import constantes

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
    column_json = json.dumps(column)
    print(column_json)
    print(type(column_json))
   # tipo = column_json["type"]
    #print(tipo)
    #tipo = column_json[0]

    #if key not in constantes.ENTEROS:
     #   return -1
    #else:
     #   return random.randint()

generate_int2({'name': 'id', 'type': {'integer': {}}, 'option': {'check': {'gt': ['Id', 50]}}},
 "{'name': 'NombreLargo', 'check': {'gt': [{'length': 'Nombre'}, 5]}}}")