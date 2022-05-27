from datetime import datetime
from decimal import Decimal
from time import mktime, strftime, strptime, localtime
from faker import Faker
import random
import constantes

def max_number(precision, scale):
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
    if scale == 0:                           # Number sin decimales
        while precision > 1:
            precision -= 1
            aux *= 10
            max_num += aux
    else:                                    # Number con decimales, rango scale:[-84,0), (0,127]
        if scale in range(-84, 0):
            precision -= abs(scale)
            if precision <= 0:
                max_num = 9 * 10 ** abs(scale)
            else:
                while precision > 1:
                    precision -= 1
                    aux *= 10
                    max_num += aux
                max_num *= 10 ** abs(scale)

        elif scale in range(1, 128):
            num_nueves = precision if precision > scale else scale
            while num_nueves > 1:
                num_nueves -= 1
                aux *= 10
                max_num += aux
            max_num /= 10 ** scale

    return max_num


def generate_null_value():
    """Genera valores nulos con una probabilidad preestablecida
    :return: valor nulo
    """
    if random.random() < constantes.NULL_PROBABILITY:
        return "NULL"
    return ""


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
    _unique = restricciones.get("unique") if "unique" in restricciones else None
    _primary = restricciones.get("primary key") if "primary key" in restricciones else None
    _nullable = restricciones.get("nullable")

    fake = Faker(['en_US'])
    generated_string = None

    if _eq is not None:
        if _unique is not None and _eq != "NULL" and _eq not in _unique:
            _unique.append(_eq)
        if _primary is not None and _eq not in _primary:
            _primary.append(_eq)
        return _eq, _unique, _primary

    # Repetimos el proceso si genera un string generado previamente y existe una restricción
    # unique o primary key
    for i in range(0, constantes.UNIQUE_TRIES):
        if _nullable is True:
            generated_string = generate_null_value()

        if generated_string != "NULL":
            if _like is not None:
                generated_string = ""
                max_percentage_chars = _like.count('%') + _max - len(_like)
                for char in _like:
                    if char == '_':
                        generated_string += random.choice('abcdefghijklmnopqrstuvwxyz')
                    elif char == '%':
                        fin = random.randint(0, max_percentage_chars)
                        generated_string += fake.text()[0:fin]
                        max_percentage_chars -= fin
                    else:
                        generated_string += char
                if len(generated_string) < _min:
                    fin = _min - len(generated_string)
                    generated_string += fake.text()[0:int(fin)]
            else:
                fin = random.randint(_min, _max)
                generated_string = fake.text()[0:fin]
        if generated_string == "NULL" or (_unique is None and _primary is None):
            break
        if _unique is not None and generated_string not in _unique:
            _unique.append(generated_string)
            break
        if _primary is not None and generated_string not in _primary:
            _primary.append(generated_string)
            break
        generated_string = None
    return generated_string, _unique, _primary


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
    _unique = restricciones.get("unique") if "unique" in restricciones else None
    _primary = restricciones.get("primary key") if "primary key" in restricciones else None
    _nullable = restricciones.get("nullable")

    if _eq is not None:
        if _unique is not None and _eq != "NULL" and _eq not in _unique:
            _unique.append(_eq)
        if _primary is not None and _eq not in _primary:
            _primary.append(_eq)
        return _eq, _unique, _primary

    generated_number = None

    # Repetimos el proceso si genera un número generado previamente y existe una restricción
    # unique o primary key
    for i in range(0, constantes.UNIQUE_TRIES):
        if _nullable is True:
            generated_number = generate_null_value()

        if generated_number != "NULL":
            if scale == 0:
                # Genera un número entero
                generated_number = random.randint(_min, _max)
                if _neq is not None and generated_number == _neq:
                    generated_number += 1
            else:
                # Genera un número real
                generated_number = float(Decimal(str(random.uniform(_min, _max)))
                                         .quantize(Decimal(10) ** -scale))
                if _neq is not None and generated_number == _neq:
                    if scale < 0:
                        generated_number += 1
                    else:
                        generated_number += 1 / 10 ** scale
        if _unique is None and _primary is None:
            break
        if _unique is not None and generated_number == "NULL":
            break
        if _unique is not None and generated_number not in _unique:
            _unique.append(generated_number)
            break
        if _primary is not None and generated_number != "NULL" and generated_number not in _primary:
            _primary.append(generated_number)
            break
        generated_number = None
    return generated_number, _unique, _primary


def generate_fecha(restricciones):
    """Genera fechas aleatorias que cumplen una serie de restricciones
            :param restricciones: diccionario con los parámetros sec_precision, es_date, data_type
            :return: una fecha aleatoria del tipo específico(DATE o TIMESTAMP) en formato string

        Se establecen una fecha inicio y una fecha final como rango para generar la fecha aleatoria,
        además del formato específico en el que lo mostramos. DATE: 'YYYY-MM-DD ,
        TIMESTAMP: 'YYYY-MM-DD HH24:MI:SS.FF'
    """

    es_date = restricciones.get("es_date")
    sec_precision = restricciones.get("sec_precision")
    inicio = "01/01/1971"
    final = "12/12/2022"  # Se podria establecer como final la fecha actual del sistema
    formato = "%d/%m/%Y"  # Formato establecido por defecto
    _nullable = restricciones.get("nullable")
    generated_date = ""

    if _nullable:
        generated_date = generate_null_value()

    if generated_date != "NULL":
        if es_date:  # DATE
            minimo = mktime(strptime(inicio, formato))  # Fecha mínima en formato DATE
            maximo = mktime(strptime(final, formato))  # Fecha máxima en formato DATE
            fecha = minimo + (maximo - minimo) * random.random()
            generated_date = strftime(formato, localtime(fecha))

        else:  # TIMESTAMP
            # Fecha mínima en formato TIMESTAMP 'YYYY-MM-DD HH24:MI:SS.FF'
            minimo = datetime.strptime(inicio, formato)
            # Fecha máxima en formato TIMESTAMP
            maximo = datetime.strptime(final, formato)
            fecha = minimo + (maximo - minimo) * random.random()
            if sec_precision >= 6:
                generated_date = fecha.strftime("%d/%m/%Y %H:%M:%S.%f")
            elif sec_precision == 0:
                generated_date = fecha.strftime("%d/%m/%Y %H:%M:%S")
            else:
                sec_precision = 6 - sec_precision
                generated_date = fecha.strftime("%d/%m/%Y %H:%M:%S.%f")[:-sec_precision]
    return generated_date

