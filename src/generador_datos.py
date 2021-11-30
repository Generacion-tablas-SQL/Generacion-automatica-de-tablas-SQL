import constantes
from datetime import datetime
from decimal import Decimal
from mo_sql_parsing import parse
from mo_sql_parsing import format
from faker import Faker
import random
import datetime
import time

# <---- GENERADOR DE UN NUMERO MÁXIMO ---->
def max_number(precision, scale):  # Ej: precision 3 --> max_num = 999
    """Devuelve el número máximo que se puede generar con la precisión indicada.
        Ejemplo: si precision == 3, max_num = 999
                 si precision == 5 y precision == 2,  max_num = 999.99

    :param precision: número de dígitos que contiene un número como máximo
    :param scale: número máximo de dígitos decimales
    :return: número máximo que se puede generar con la precisión indicada
    """

    max_num = 9
    aux = 9

    # NUMBER(p,s) con p(1,38) y s(-84,127)
    if scale == 0:                      # Number sin decimales
        while precision > 1:            # Más de 1 dígito
            precision -= 1
            aux *= 10
            max_num += aux
    else:                               # Number con decimales, rango scale:[-84,0), (0,127]
        if scale in range(-84, 0):      # Se trata de un scale negativo
            precision -= abs(scale)  # Dígitos no redondeados
            if precision <= 0:
                max_num = 0.0
            else:
                while precision > 1:
                    precision -= 1
                    aux *= 10.0
                    max_num += aux
                max_num *= 10.0 ** abs(scale)  # Añade los dígitos redondeados a 0

        elif scale in range(1, 128):       # Se trata de un scale positivo
            while precision > 1:
                precision -= 1
                aux *= 10
                max_num += aux
            max_num /= 10 ** scale
    return max_num


# <---- GENERADOR DE VALORES NULOS ---->
def generate_null_value():
    if random.random() < constantes.NULL_PROBABILITY:
        return "NULL"
    return ""

# <---- GENERADOR DE STRINGS ---->
def generate_string(_min, _max, _neq, _like):
    fake = Faker(['en_US'])
    generated_string = ""
    if _like is not None:
        max_percentage_chars = _like.count('%') + _max - len(_like)
        for char in _like:
            if char == '_':
                generated_string += random.choice('abcdefghijklmnopqrstuvwxyz')
            elif char == '%':
                b = random.randint(0, max_percentage_chars)  # El % puede no ser ningún caracter
                generated_string += fake.text()[0:b]
                max_percentage_chars -= b
            else:
                generated_string += char
    else:
        b = random.randint(_min, _max)
        generated_string = fake.text()[0:b]
    return generated_string


# <---- GENERADOR DE NÚMEROS ---->
def generate_number(restricciones):
    dict_restr = restricciones[-1]
    scale = dict_restr.get("scale")
    _min = dict_restr.get("min")
    _max = dict_restr.get("max")
    _eq = dict_restr.get("eq")
    _neq = dict_restr.get("neq")

    if "nullable" in restricciones:
        if generate_null_value() == "NULL":
            return None

    if _eq is not None:
        return _eq

    if scale == 0:
        generated_number = random.randint(_min, _max)  # Genera un número entero
        if _neq is not None and generated_number == _neq:
            generated_number += 1
    else:
        # Genera un número real
        generated_number = Decimal(str(random.uniform(_min, _max))).quantize(Decimal(10) ** -scale)
        if _neq is not None and generated_number == _neq:
            if scale < 0:
                generated_number += 1
            else:
                generated_number += 1 / 10 ** scale  # Suma uno en el decimal menos significativo
    return generated_number


# <---- GENERADOR DE FECHAS ---->
def gen_fecha(es_date, sec_precision):
    """Comprueba las restricciones en el campo option.
            :param es_date: indica si el tipo de dato es DATE o TIMESTAMP
            :param sec_precision: precisión de la parte fraccional de los segundos (TIMESTAMP)
            :return: una una fecha aleatoria del tipo específico(DATE o TIMESTAMP) en formato string
            """
    # Se establecen una fecha inicio y una fecha final como rango para generar la fecha aleatoria, además
    # del formato específico en el que lo mostramos. DATE: 'YYYY-MM-DD , TIMESTAMP: 'YYYY-MM-DD HH24:MI:SS.FF'

    inicio = "01/01/1971"
    final = "12/12/2021"  # Se podria poner como final la fecha actual del sistema
    formato = "%d/%m/%Y"  # Formato establecido por defecto

    if es_date:  # Generar fecha de tipo DATE
        minimo = time.mktime(time.strptime(inicio, formato))  # Fecha mínima en formato DATE
        maximo = time.mktime(time.strptime(final, formato))  # Fecha máxima en formato DATE
        fecha = minimo + (maximo - minimo) * random.random()
        # print(time.strftime("%d/%m/%Y", time.localtime(fecha)))
        return time.strftime("%d/%m/%Y", time.localtime(fecha))

    else:  # Generar fecha de tipo TIMESTAMP
        minimo = datetime.datetime.strptime(inicio,
                                            formato)  # Fecha mínima en formato TIMESTAMP 'YYYY-MM-DD HH24:MI:SS.FF'
        maximo = datetime.datetime.strptime(final, formato)  # Fecha máxima en formato TIMESTAMP
        fecha = minimo + (maximo - minimo) * random.random()
        if sec_precision == 6 or sec_precision == 0:
            # print(fecha.strftime("%d/%m/%Y %H:%M:%S.%f"))
            return fecha.strftime("%d/%m/%Y %H:%M:%S.%f")
        else:
            sec_precision = 6 - sec_precision
            # print(fecha.strftime("%d/%m/%Y %H:%M:%S.%f")[:-sec_precision])
            return fecha.strftime("%d/%m/%Y %H:%M:%S.%f")[:-sec_precision]


# ______________________________________________________________________________________________________________________


def option_check_string(column_name, check, varying, size):
    _min = 1 if varying is True else size
    _max = size
    _like = None
    _not = None
    _neq = None
    if len(check) != 0:
        operator = list(check.keys())[0].lower()  # primer operador que aparece en el check
        if operator == "and" or operator == "or":
            comparisons = check.get(operator)  # lista de comparaciones
        else:
            comparisons = [check]  # Convierte el diccionario que contiene la comparación a una lista de un elemento
        for comparison in comparisons:
            comparison_key = list(comparison.keys())
            if comparison_key[0] == "not":
                _not = list(comparison.get("not").keys())[0]
            if comparison_key[0] == "eq":
                _max = comparison.get("eq")
                _min = _max
            elif comparison_key[0] == "neq":
                _neq = comparison.get("neq")
            elif comparison_key[0] == "gt" or _not == "gt":
                if _not == "gt":
                    index = 1 if isinstance(comparison.get("not").get("gt")[1], int) else 0
                    _max = min(_max, comparison.get("gt")[index] - 1)
                else:
                    index = 1 if isinstance(comparison.get("gt")[1], int) else 0
                    _min = max(_min, comparison.get("gt")[index] + 1)
            elif comparison_key[0] == "gte" or _not == "gte":
                if _not == "gte":
                    index = 1 if isinstance(comparison.get("not").get("gte")[1], int) else 0
                    _max = min(_max, comparison.get("gte")[index])
                else:
                    index = 1 if isinstance(comparison.get("gte")[1], int) else 0
                    _min = max(_min, comparison.get("gte")[index])
            elif comparison_key[0] == "lt" or _not == "lt":
                if _not == "lt":
                    index = 1 if isinstance(comparison.get("not").get("lt")[1], int) else 0
                    _min = max(_min, comparison.get("not").get("lt")[index] + 1)
                else:
                    index = 1 if isinstance(comparison.get("lt")[1], int) else 0
                    _max = min(_max, comparison.get("lt")[index] - 1)
            elif comparison_key[0] == "lte" or _not == "lte":
                if _not == "lte":
                    index = 1 if isinstance(comparison.get("not").get("lte")[1], int) else 0
                    _min = max(_min, comparison.get("not").get("lte")[index] + 1)
                else:
                    index = 1 if isinstance(comparison.get("lte")[1], int) else 0
                    _max = min(_max, comparison.get("lte")[index] - 1)
            elif comparison_key[0] == "like":
                _like = comparison.get("like")[1].get("literal")
            else:
                tries = 20
                string = generate_string(_min, _max, _neq, _like)
                check = format(check).lower()
                check = check.replace(column_name, string)
                check = check.replace("<>", "!=")
                while not eval(check) and tries > 0:
                    new_string = generate_string(_min, _max, _neq, _like)
                    check = check.replace(string, new_string)
                    string = new_string
                    tries -= 1
                if tries > 0:
                    return string
                else:
                    return "No se ha encontrado un dato que satisfaga las restricciones"
            _not = None
    return generate_string(_min, _max, _neq, _like)


def option_check(column_name, check, precision, scale):
    """Comprueba las restricciones CHECK

    :param column_name: nombre de la columna
    :param check: campo check de la sentencia parseada
    :param precision: precisión de la parte entera del número
    :param scale: número de decimales
    :return: número aleatorio teniendo en cuenta las restricciones del campo option y del tipo de datos
    """

    _max = max_number(precision, scale)
    _min = -_max
    _neq = None
    _not = None
    if len(check) != 0:  # hay campo check
        operator = list(check.keys())[0].lower()  # primer operador que aparece en el check
        if operator == "and" or operator == "or":
            comparisons = check.get(operator)  # lista de comparaciones
        else:
            comparisons = [check]  # Convierte el diccionario que contiene la comparación a una lista de un elemento
        for comparison in comparisons:
            comparison_key = list(comparison.keys())
            if comparison_key[0] == "not":
                _not = list(comparison.get("not").keys())[0]
            if comparison_key[0] == "eq":
                index = 1 if isinstance(comparison.get("eq")[1], int) else 0
                return comparison.get("eq")[index]
            elif comparison_key[0] == "neq":
                index = 1 if isinstance(comparison.get("neq")[1], int) else 0
                _neq = comparison.get("neq")[index]
            elif comparison_key[0] == "gt" or _not == "gt":
                if _not == "gt":
                    index = 1 if isinstance(comparison.get("not").get("gt")[1], int) else 0
                    _max = min(_max, comparison.get("gt")[index] - 1)
                else:
                    index = 1 if isinstance(comparison.get("gt")[1], int) else 0
                    _min = max(_min, comparison.get("gt")[index] + 1)  # (id > 38) and (id > 36) --> _min = 39;
            elif comparison_key[0] == "gte" or _not == "gte":
                if _not == "gte":
                    index = 1 if isinstance(comparison.get("not").get("gte")[1], int) else 0
                    _max = min(_max, comparison.get("gte")[index])
                else:
                    index = 1 if isinstance(comparison.get("gte")[1], int) else 0
                    _min = max(_min, comparison.get("gte")[index])  # (id >= 38) and (id >= 36) --> _min = 38;
            elif comparison_key[0] == "lt" or _not == "lt":
                if _not == "lt":
                    index = 1 if isinstance(comparison.get("not").get("lt")[1], int) else 0
                    _min = max(_min, comparison.get("not").get("lt")[index] + 1)
                else:
                    index = 1 if isinstance(comparison.get("lt")[1], int) else 0
                    _max = min(_max, comparison.get("lt")[index] - 1)  # (id < 36) and (id < 38) --> _min = 35;
            elif comparison_key[0] == "lte" or _not == "lte":
                if _not == "lte":
                    index = 1 if isinstance(comparison.get("not").get("lte")[1], int) else 0
                    _min = max(_min, comparison.get("not").get("lte")[index] + 1)
                else:
                    index = 1 if isinstance(comparison.get("lte")[1], int) else 0
                    _max = min(_max, comparison.get("lte")[index] - 1)  # (id <= 36) and (id <= 38) --> _min = 36;
            # else:
            #     tries = 20
            #     number = generate_number(_min, _max, _neq, scale)
            #     check = format(check).lower()
            #     check = check.replace(column_name, str(number))
            #     check = check.replace("<>", "!=")
            #     while not eval(check) and tries > 0:
            #         new_number = generate_number(_min, _max, _neq, scale)
            #         check = check.replace(str(number), str(new_number))
            #         number = new_number
            #         tries -= 1
            #     if tries > 0:
            #         return number
            #     else:
            #         return "No se ha encontrado un dato que satisfaga las restricciones"
            _not = None
    # number = generate_number(_min, _max, _neq, scale)
    number = ""
    return number


"""No se realiza la implementación de restricciones de tipo check en las fechas, únicamente se 
generan valores del tipo especificado: DATE o TIMESTAMP(scale)"""
def restrictions_fecha(es_date, sec_precision, column):
    """Comprueba las restricciones en el campo option.

        :param es_date: indica si el tipo de dato es DATE o TIMESTAMP
        :param sec_precision: precisión de la parte fraccional de los segundos (TIMESTAMP)
        :param column: restricciones. Ej: {'name': 'fech2', 'type': {'timestamp': 2}, 'unique': True, 'nullable': True}
        :return: una fecha aleatoria
        """

    if ("nullable" in column and column.get("nullable")) or "nullable" not in column:  # No afecta
        if random.random() < constantes.NULL_PROBABILITY:
            return None
    if "unique" in column:  # De momento no afecta
        pass
    if "primary key" in column:  # De momento no afecta
        pass
    if "check" not in column:  # No hay restricciones CHECK
        return gen_fecha(es_date, sec_precision)
    else:
        pass
        # return check_fecha(column.get("check"), es_date, sec_precision)


def generate_fecha(data_type, parameters, column):
    """Genera una fecha aleatoria que cumpla con las especificaciones de los parámetros y las opciones CHECK.

        :param data_type: tipo de dato de la columna (DATE O TIMESTAMP)
        :param parameters: parámetros del tipo de dato
        :param column: opciones adicionales definidas por el usuario (NULL, NOT NULL, UNIQUE, CHECK) contenidas en
                    el campo column de la sentencia.
        :return: una fecha aleatoria
        """
    sec_precision = 0
    es_date = False
    if data_type == "date":  # DATE 'YYYY-MM-DD'
        es_date = True
    else:                    # TIMESTAMP 'YYYY-MM-DD HH24:MI:SS.FF'  sec_precision = 2 (.FF)
        sec_precision = parameters[0]

    return restrictions_fecha(es_date, sec_precision, column)

