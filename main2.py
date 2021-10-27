import constantes
import random
# from mo_sql_parsing import format


def number_of_digits(precision):  # precision 3 --> max_num = 999
    max_num = 9
    aux = 9
    if precision == 1:
        return 9
    while precision > 1:
        precision -= 1
        aux *= 10
        max_num = max_num + aux
    return max_num


def generate_int(column, constraint):
    data_type = column.get("type")
    key_list = list(data_type.keys())
    key = key_list[0].lower()
    restriction = list(data_type.values())

    if key not in constantes.ENTEROS:
        return "Este tipo de datos no es un entero"
    else:
        if key != "number" and str(restriction[0]) != "{}":  # Ej: {integer : 9}
            return "Este tipo de datos no soporta parámetros"
        if key == "number" and str(restriction[0]) == "{}":  # {number: {}}
            return "Este tipo de datos es un número real, no un entero"
        if key == "number" and isinstance(restriction[0], int):  # {number: 5}
            return random.randint(0, number_of_digits(restriction[0]))
        if key == "number" and len(restriction[0]) == 2 and restriction[0][1] != 0:  # Ej: {number : [4, 2]}
            return "Este tipo de datos es un número real, no un entero"
        if key == "number" and len(restriction[0]) == 2:  # Ej: {number: 4, 0}
            return random.randint(0, number_of_digits(restriction[0][0]))

        return random.randint(0, number_of_digits(38))  # int, integer y smallint tienen una precision de 38


print(generate_int({'name': 'id', 'type': {'NUMBER': [4, 0]}, 'option': {'check': {'gt': ['Id', 50]}}},
                   {'name': 'NombreLargo', 'check': {'gt': [{'length': 'Nombre'}, 5]}}))
