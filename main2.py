import constantes
import random
# from mo_sql_parsing import format


def max_number(es_float, precision, scale):  # Ej: precision 3 --> max_num = 999
    """Devuelve el número máximo que se puede generar con la precisión indicada.
        Ejemplo: si precision == 3, max_num = 999
                 si precision == 5 y precision == 2,  max_num = 999.99

    :param es_float: indica si se trata de un float
    :param precision: número de dígitos que contiene un número como máximo
    :param scale: número máximo de dígitos decimales
    :return: número máximo que se puede generar con la precisión indicada
    """
    if es_float is False:  # NUMBER(p,s) con p(1,38) y s(-84,127)
        max_num = 9
        aux = 9
        if scale == 0:  # Number sin decimales
            if precision == 1:
                return max_num
            while precision > 1:
                precision -= 1
                aux *= 10
                max_num = max_num + aux
        else:  # Number con decimales, rango s:(-84,127)
            max_num = 9.0
            if scale in range(-84, -1):  # Se trata de un scale negativo
                # FALTA ESTA PARTE DE SCALE NEGATIVO ----------------------
                if precision == 1:
                    pass
                while precision > 1:
                    precision -= 1
                    aux *= 10
                    max_num = max_num + aux

                    if precision > scale:
                        pass
                    elif precision == scale:
                        pass
                    else:                  # precision < scale
                        pass
                # ------------------------

            if scale in range(1, 127):  # Se trata de un scale positivo
                # max_num = 9.0
                # aux = 9.0

                if precision == 1:
                    if scale == precision:   # 0.9
                        max_num = max_num / 10.0
                    else:  # scale > precision
                        max_num /= 10.0 ** scale
                else:
                    n = precision
                    while n > 1:
                        aux *= 10.0
                        max_num += aux
                        n -= 1
                    if precision != scale:
                        max_num /= (10.0**float(scale))

    else:  # Float(n),  digits = (n / 3) + 1  ó  digits = ceil(bits / log(2,10)
        pass
        # SIN IMPLEMENTAR TIPO FLOAT

    return max_num


def option_check(check, es_float, precision, scale):
    """Comprueba las restricciones CHECK

    :param check: campo check de la sentencia parseada
    :param es_float: indica si el tipo de dato es un float
    :param precision: precisión de la parte entera del número
    :param scale: número de decimales
    :return: número aleatorio teniendo en cuenta las restricciones del campo option y del tipo de datos
    """

    _max = max_number(es_float, precision, scale)
    _min = -_max
    _neq = None
    operator = list(check.keys())[0].lower()  # primer operador que aparece en el check
    if operator == "and" or operator == "or":
        comparisons = check.get(operator)
    else:
        comparisons = [check]  # Convierte el diccionario que contiene la comparación a una lista de un elemento
    for comparison in comparisons:
        comparison_key = list(comparison.keys())
        if comparison_key[0] == "eq":
            return comparison.get("eq")
        elif comparison_key[0] == "neq":
            _neq = comparison.get("neq")
        elif comparison_key[0] == "gt":
            _min = max(_min, comparison.get("gt")[1] + 1)  # (id > 38) and (id > 36) --> _min = 39;
        elif comparison_key[0] == "gte":
            _min = max(_min, comparison.get("gte")[1])  # (id >= 38) and (id >= 36) --> _min = 38;
        elif comparison_key[0] == "lt":
            _max = min(_max, comparison.get("lt")[1] - 1)  # (id < 36) and (id < 38) --> _min = 35;
        elif comparison_key[0] == "lte":
            _max = min(_max, comparison.get("lte")[1])  # (id <= 36) and (id <= 38) --> _min = 36;
        else:
            return "ERROR: Comparador no implementado"

    generated_number = random.randint(_min, _max)
    if _neq is not None and generated_number == _neq:
        generated_number = generated_number + 1
    return generated_number


def option_restrictions(es_float, precision, scale, options):
    """Comprueba las restricciones en el campo option.

    :param es_float: indica si el tipo de dato es un float
    :param precision: precisión de la parte entera del número
    :param scale: número de decimales
    :param options: restricciones. Ej: {'check': {'gt': ['Id', 50]}} o
                                       {'check': {'and': [{'gte': ['Id', 50]}, {'lt': ['ID', 100]}]} o
                                      {'option': ['unique', 'not null', {'check': {'gte': ['Id', 50]}}}
    :return: un entero aleatorio o un string definiendo el error
    """

    check = [d['check'] for d in options if 'check' in d]

    if len(check) == 0:
        _max = max_number(es_float, precision, scale)
        _min = -_max
        return random.randint(_min, _max)

    if not isinstance(options, list):  # Si solo hay una opción
        options = [options]

    if "null" in options:
        return None
    if "not null" in options and len(options) == 1:
        return random.randint(0, max_number(es_float, precision, scale))
    if "unique" in options:
        pass
    if "primary key" in options:
        pass
    if check:
        return option_check(check[0], es_float, precision, scale)
    return "Opciones no implementadas"


def generate_int(parameters, option, constraint):
    """Genera un número entero aleatorio que cumpla con las especificaciones de los parámetros y las opciones CHECK.

        :param parameters: parámetros del tipo de dato
        :param option: opciones adicionales definidas por el usuario (NULL, NOT NULL, UNIQUE, CHECK).
                        Ej: ['not null', {'check': {'gte': ['Id', 50]}}]
                            'unique'
                            {'check': {'gte': ['Id', 50]}}
        :param constraint: restricciones definidas después de las columnas **SIN IMPLEMENTAR**
        :return: un entero aleatorio
        """
    if parameters[0] == {}:
        # int, integer y smallint tienen una precision de 38
        return option_restrictions(False, 38, 0, option)
    else:
        return option_restrictions(False, parameters[0], 0, option)


def generate_real(data_type, parameters, option, constraint):
    """Genera un número real aleatorio que cumpla con las especificaciones de los parámetros y las opciones CHECK.

            :param data_type: tipo de dato de la columna
            :param parameters: parámetros del tipo de dato
            :param option: opciones adicionales definidas por el usuario (NULL, NOT NULL, UNIQUE, CHECK).
                            Ej: ['not null', {'check': {'gte': ['Id', 50]}}]
                                'unique'
                                {'check': {'gte': ['Id', 50]}}
            :param constraint: restricciones definidas después de las columnas **SIN IMPLEMENTAR**
            :return: un entero aleatorio
            """
    es_float = False
    if data_type == "float":
        precision = 126 if parameters[0] == "{}" else parameters[0]
        scale = None
        es_float = True
    else:  # data_type == "number"
        if parameters[0] == "{}":
            precision = 38
            scale = 127
        else:
            precision = parameters[0][0]
            scale = parameters[0][1]
    option_restrictions(es_float, precision, scale, option)


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
            print(generate_int(parameters, option, constraint))
        elif key in constantes.REALES:
            print(generate_real(key, parameters, option, constraint))
        elif key in constantes.STRINGS:
            print("Datos de tipo cadena de caracteres sin implementar.")
        elif key in constantes.FECHA:
            print("Datos de tipo fecha")
        else:
            print("Ha habido un error en la clasificación de tipo de datos.")


if __name__ == '__main__':
    main({'create table': {
            'name': 'Persona',
            'columns': [
                {'name': 'id',
                 'type': {'number': {}},
                 'option': ['unique', 'not null',
                            {'check': {'and': [{'gte': ['Id', -50]}, {'lt': ['ID', 100]}, {'neq': ['ID', 80]}]}}]},
                {'name': 'nombre',
                 'type': {'number': [4, 2]}
                 }
            ],
            'constraint': {'name': 'NombreLargo', 'check': {'gt': [{'length': 'Nombre'}, 5]}}}})
