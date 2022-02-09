from datetime import datetime
from decimal import Decimal
from time import mktime, strftime, strptime, localtime
from faker import Faker
from mo_sql_parsing import format
import random
import constantes

# <---- GENERADOR DE UN NUMERO MÁXIMO ---->
def max_number(precision, scale):  # Ej: precision 3 --> max_num = 999
    """Devuelve el número máximo que se puede generar con la precisión indicada.
        Ejemplo: si precision == 3, max_num = 999
                 si precision == 5 y precision == 2,  max_num = 999.99

    :param precision: número de dígitos que contiene un número como máximo
    :param scale: número máximo de dígitos decimales
    :return: número máximo que se puede generar con la precisión y escala indicada
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
                max_num = 9 * 10 ** abs(scale)
            else:
                while precision > 1:
                    precision -= 1
                    aux *= 10
                    max_num += aux
                max_num *= 10 ** abs(scale)  # Añade los dígitos redondeados a 0

        elif scale in range(1, 128):           # Se trata de un scale positivo
            num_nueves = precision if precision > scale else scale
            while num_nueves > 1:
                num_nueves -= 1
                aux *= 10
                max_num += aux
            max_num /= 10 ** scale

    return max_num


# <---- GENERADOR DE VALORES NULOS ---->
def generate_null_value():
    """Genera valores nulos con una probabilidad preestablecida
    :return: valor nulo
    """
    if random.random() < constantes.NULL_PROBABILITY:
        return "NULL"
    return ""

# <---- GENERADOR DE STRINGS ---->
def generate_string(restricciones):
    """Genera cadenas de caracteres aleatorias que cumplen una serie de restricciones

    :param restricciones: diccionario con restricciones
    :return: cadena de caracteres aleatoria
    """
    _min = restricciones.get("min")
    _max = restricciones.get("max")
    _neq = restricciones.get("neq")
    _eq = restricciones.get("eq")
    _like = restricciones.get("like")

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
        if len(generated_string) < _min:
            # Añade el resto de caracteres hasta el mínimo solicitado
            b = _min - len(generated_string)
            generated_string += fake.text()[0:int(b)]
    else:
        b = random.randint(_min, _max)
        generated_string = fake.text()[0:b]
    return generated_string


# <---- GENERADOR DE NÚMEROS ---->
def generate_number(restricciones):
    """Genera números aleatorios que cumplen una serie de restricciones

    :param restricciones: diccionario con restricciones
    :return: números aleatorios
    """
    scale = restricciones.get("scale")
    _min = restricciones.get("min")
    _max = restricciones.get("max")
    _eq = restricciones.get("eq")
    _neq = restricciones.get("neq")

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
        generated_number = float(Decimal(str(random.uniform(_min, _max))).quantize(Decimal(10) ** -scale))
        if _neq is not None and generated_number == _neq:
            if scale < 0:
                generated_number += 1
            else:
                generated_number += 1 / 10 ** scale  # Suma uno en el decimal menos significativo
    return generated_number


# <---- GENERADOR DE FECHAS ---->
def gen_fecha(restricciones):
    """Genera fechas aleatorias que cumplen una serie de restricciones
            :param restricciones: [sec_precision, es_date, data_type]
            :return: una una fecha aleatoria del tipo específico(DATE o TIMESTAMP) en formato string

        Se establecen una fecha inicio y una fecha final como rango para generar la fecha aleatoria, además
        del formato específico en el que lo mostramos. DATE: 'YYYY-MM-DD , TIMESTAMP: 'YYYY-MM-DD HH24:MI:SS.FF'
    """

    dict_restr = restricciones[-1]
    es_date = dict_restr.get("es_date")
    sec_precision = dict_restr.get("sec_precision")
    inicio = "01/01/1971"
    final = "12/12/2022"  # Se podria poner como final la fecha actual del sistema
    formato = "%d/%m/%Y"  # Formato establecido por defecto

    if es_date:  # DATE
        minimo = mktime(strptime(inicio, formato))  # Fecha mínima en formato DATE
        maximo = mktime(strptime(final, formato))  # Fecha máxima en formato DATE
        fecha = minimo + (maximo - minimo) * random.random()
        return strftime("%d/%m/%Y", localtime(fecha))

    else:  # TIMESTAMP
        minimo = datetime.strptime(inicio, formato)  # Fecha mínima en formato TIMESTAMP 'YYYY-MM-DD HH24:MI:SS.FF'
        maximo = datetime.strptime(final, formato)  # Fecha máxima en formato TIMESTAMP
        fecha = minimo + (maximo - minimo) * random.random()
        if sec_precision >= 6:
            return fecha.strftime("%d/%m/%Y %H:%M:%S.%f")
        elif sec_precision == 0:
            return fecha.strftime("%d/%m/%Y %H:%M:%S")
        else:
            sec_precision = 6 - sec_precision
            return fecha.strftime("%d/%m/%Y %H:%M:%S.%f")[:-sec_precision]


def generate_random(data_type, column_name, restricciones, check):
    tries = 20
    value = generate_string(restricciones) if data_type == "String" else generate_number(restricciones)
    check = format(check).lower()
    check = check.replace(column_name, str(value))
    check = check.replace("<>", "!=")

    while not eval(check) and tries > 0:
        new_value = generate_string(restricciones) if data_type == "String" else generate_number(restricciones)
        check = check.replace(str(value), str(new_value))
        value = new_value
        tries -= 1
        if tries > 0:
            return value
        else:
            # return "No se ha encontrado un dato que satisfaga las restricciones"
            raise ValueError
