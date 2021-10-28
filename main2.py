import constantes
import random
# from mo_sql_parsing import format


def number_of_digits(precision):  # precision 3 --> max_num = 999
    """Devuelve el número máximo que se puede generar con la precisión indicada.

    :param precision: precisión del entero. Número de dígitos
    :return: número máximo que se puede generar con la precisión indicada
    """
    max_num = 9
    aux = 9
    if precision == 1:
        return 9
    while precision > 1:
        precision -= 1
        aux *= 10
        max_num = max_num + aux
    return max_num


def check_restrictions(name, generated_number, option):
    """Comprueba las restricciones en el campo option.

    :param name: nombre de la columna
    :param generated_number: numero generado sin tener en cuenta el campo option
    :param option: restricciones. Ej: {'check': {'gt': ['Id', 50]}}
    :return: un entero aleatorio o un string definiendo el error
    """
    pass


def generate_int(data_type, parameters, option, constraint):
    """Genera un entero aleatorio que cumpla con las especificaciones de los parámetros y las opciones CHECK.

        :param data_type: tipo de dato
        :param parameters: parámetros del tipo de dato
        :param option: opciones adicionales definidas por el usuario (NULL, NOT NULL, CHECK)
        :param constraint: restricciones definidas después de las columnas
        :return: un entero aleatorio
        """
    if data_type != "number":
        return random.randint(0, number_of_digits(38))  # int, integer y smallint tienen una precision de 38
    else:
        return random.randint(0, number_of_digits(parameters[0]))


def generate_real(data_type, parameters, option, constraint):
    pass


def main(sentencia):
    """Detecta el tipo de datos y delega la generación del tipo de dato detectado.

    :param sentencia:
    {'create table':
        {'name': 'Persona',
        'columns':
            [{'name': 'id', 'type': {'number': 5}, 'option': ['not null', {'check': {'gte': ['Id', 50]}}]},
            {'name': 'nombre', 'type': {'varchar': 30}}],
        'constraint': {'name': 'NombreLargo', 'check': {'gt': [{'length': 'Nombre'}, 5]}}}}
    :return:
    """
    constraint = sentencia.get("create table").get("constraint")  # constraint compartido por todas las columnas
    for column in sentencia.get("create table").get("columns"):
        data_type = column.get("type")  # {'NUmbEr': [5, 0]}
        key_list = list(data_type.keys())  # ['NUmbEr']
        key = key_list[0].lower()  # number
        parameters = list(data_type.values())  # [[5, 0]]
        option = ""

        if "option" in column:
            option = column.get("option")

        is_real = None
        if key == "number":
            if parameters[0] == "{}" or isinstance(parameters[0], list):
                is_real = True
        if is_real is not True and key in constantes.ENTEROS:
            print(generate_int(key, parameters, option, constraint))
        elif key in constantes.REALES:
            print(generate_real(key, parameters, option, constraint))


if __name__ == '__main__':
    main({'create table': {'name': 'Persona', 'columns': [{'name': 'id', 'type': {'number': 5},
          'option': ['not null', {'check': {'gte': ['Id', 50]}}]}, {'name': 'nombre', 'type': {'number': [4, 2]}}],
          'constraint': {'name': 'NombreLargo', 'check': {'gt': [{'length': 'Nombre'}, 5]}}}})
