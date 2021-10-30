import constantes
import random
# from mo_sql_parsing import format


def max_number(precision):  # Ej: precision 3 --> max_num = 999
    """Devuelve el número máximo que se puede generar con la precisión indicada.
        Ejemplo: si precision == 3, max_num = 999
                 si precision == 5, max_num = 99999
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


def option_check(check, max_digits):
    """Comprueba las restricciones CHECK

    :param check: campo check de la sentencia parseada
    :param max_digits: número máximo de dígitos del número a generar
    :return: número aleatorio teniendo en cuenta las restricciones del campo option y del tipo de datos
    """

    _min = 0
    _max = max_number(max_digits)
    _neq = None
    operator = list(check.keys())[0].lower()
    if operator == "and" or operator == "or":
        comparisons = check.get(operator)
    else:
        comparisons = [check]
    for comparison in comparisons:
        comparison_key = list(comparison.keys())
        if comparison_key[0] == "eq":
            return comparison.get("eq")
        elif comparison_key[0] == "neq":
            _neq = comparison.get("neq")
        elif comparison_key[0] == "gt":
            _min = max(_min, comparison.get("gt")[1] + 1)
        elif comparison_key[0] == "gte":
            _min = max(_min, comparison.get("gte")[1])
        elif comparison_key[0] == "lt":
            _max = min(_max, comparison.get("lt")[1] - 1)
        elif comparison_key[0] == "lte":
            _max = min(_max, comparison.get("lte")[1])
    generated_number = random.randint(_min, _max)
    if _neq is not None and generated_number == _neq:
        generated_number = generated_number + 1
    return generated_number


def option_restrictions(max_digits, options):
    """Comprueba las restricciones en el campo option.

    :param max_digits: número máximo de dígitos del número a generar
    :param options: restricciones. Ej: {'check': {'gt': ['Id', 50]}} o
                                       {'check': {'and': [{'gte': ['Id', 50]}, {'lt': ['ID', 100]}]} o
                                      {'option': ['unique', 'not null', {'check': {'gte': ['Id', 50]}}}
    :return: un entero aleatorio o un string definiendo el error
    """

    check = [d['check'] for d in options if 'check' in d]

    if not isinstance(options, list):  # Si solo hay una opción
        options = [options]

    if "null" in options:
        return None
    if "not null" in options and len(options) == 1:
        return random.randint(0, max_number(max_digits))
    if "unique" in options:
        pass
    if check:
        return option_check(check[0], max_digits)
    return "Opciones no implementadas"


def generate_int(name, data_type, parameters, option, constraint):
    """Genera un entero aleatorio que cumpla con las especificaciones de los parámetros y las opciones CHECK.

        :param name: nombre de la columna
        :param data_type: tipo de dato
        :param parameters: parámetros del tipo de dato
        :param option: opciones adicionales definidas por el usuario (NULL, NOT NULL, UNIQUE, CHECK).
                        Ej: ['not null', {'check': {'gte': ['Id', 50]}}]
                            'unique'
                            {'check': {'gte': ['Id', 50]}}
        :param constraint: restricciones definidas después de las columnas **SIN IMPLEMENTAR**
        :return: un entero aleatorio
        """
    if data_type != "number":
        # int, integer y smallint tienen una precision de 38
        return option_restrictions(38, option)
    else:
        return option_restrictions(parameters[0], option)


def generate_real(name, data_type, parameters, option, constraint):
    pass


def main(sentencia):
    """Detecta el tipo de datos y delega la generación del tipo de dato detectado.

    :param sentencia:
    {'create table':
        {'name': 'Persona',
        'columns':
            [{'name': 'id', 'type': {'number': 5}, 'option': ['null', {'check': {'gte': ['Id', 50]}}]},
            {'name': 'nombre', 'type': {'varchar': 30}}],
        'constraint': {'name': 'NombreLargo', 'check': {'gt': [{'length': 'Nombre'}, 5]}}}}
    :return:
    """
    constraint = sentencia.get("create table").get("constraint")  # constraint compartido por todas las columnas
    for column in sentencia.get("create table").get("columns"):
        name = column.get("name")
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
            print(generate_int(name, key, parameters, option, constraint))
        elif key in constantes.REALES:
            print(generate_real(name, key, parameters, option, constraint))


if __name__ == '__main__':
    main({'create table': {
            'name': 'Persona',
            'columns': [
                {'name': 'id',
                 'type': {'number': 5},
                 'option': ['unique', 'not null',
                            {'check': {'and': [{'gte': ['Id', 50]}, {'lt': ['ID', 100]}, {'neq': ['ID', 80]}]}}]},
                {'name': 'nombre',
                 'type': {'number': [4, 2]}
                 }
            ],
            'constraint': {'name': 'NombreLargo', 'check': {'gt': [{'length': 'Nombre'}, 5]}}}})
