import constantes
from datetime import datetime, date
from decimal import Decimal
from mo_sql_parsing import parse
from mo_sql_parsing import format
import random
import datetime
import time


def max_number(es_float, precision, scale):  # Ej: precision 3 --> max_num = 999
    """Devuelve el número máximo que se puede generar con la precisión indicada.
        Ejemplo: si precision == 3, max_num = 999
                 si precision == 5 y precision == 2,  max_num = 999.99

    :param es_float: indica si se trata de un float
    :param precision: número de dígitos que contiene un número como máximo
    :param scale: número máximo de dígitos decimales
    :return: número máximo que se puede generar con la precisión indicada
    """

    max_num = 9
    aux = 9

    if es_float is False:  # NUMBER(p,s) con p(1,38) y s(-84,127)
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
    else:                                     # Float(n),  digits = (n / 3) + 1  ó  digits = ceil(bits / log(2,10)
        pass  # SIN IMPLEMENTAR TIPO FLOAT
    return max_num


def generate_number(es_float, _min, _max, _neq, scale):

    if random.random() < constantes.NULL_PROBABILITY:
        return None

    if not es_float and scale == 0:
        generated_number = random.randint(_min, _max)  # Genera un número entero
        if not _neq and generated_number == _neq:
            generated_number += 1
    else:
        generated_number = random.uniform(_min, _max)  # Genera un número real. No tiene en cuenta la escala
        generated_number = Decimal(str(generated_number)).quantize(Decimal(10) ** -scale)
        if not _neq and generated_number == _neq:

            if scale < 0:
                generated_number += 1
            else:
                generated_number += 1 / 10 ** scale  # Suma uno en el decimal menos significativo
    return generated_number

def option_check(check, es_float, not_null, precision, scale):
    """Comprueba las restricciones CHECK

        :param check: campo check de la sentencia parseada
        :param es_float: indica si el tipo de dato es un float
        :param not_null: indica si la sentencia contiene la opción NOT NULL
        :param precision: precisión de la parte entera del número
        :param scale: número de decimales
        :return: número aleatorio teniendo en cuenta las restricciones del campo option y del tipo de datos
        """
    _max = max_number(es_float, precision, scale)
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
                return comparison.get("eq")
            elif comparison_key[0] == "neq":
                _neq = comparison.get("neq")
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
            else:
                return "ERROR: Comparador no implementado"
            _not = None
    number = generate_number(es_float, _min, _max, _neq, scale)
    if not_null is True:
        while number is None:
            number = generate_number(es_float, _min, _max, False, scale)

    return number


def gen_fecha(es_date, inicio, final, formato, sec_precision):

    if es_date:  # Generar fecha de tipo DATE
        minimo = time.mktime(time.strptime(inicio, formato))  # Fecha mínima en formato DATE
        maximo = time.mktime(time.strptime(final, formato))  # Fecha máxima en formato DATE
        fecha = minimo + (maximo - minimo) * random.random()
        print(time.strftime("%d/%m/%Y", time.localtime(fecha)))

        return time.strftime("%d/%m/%Y", time.localtime(fecha))

    else:  # Generar fecha de tipo TIMESTAMP
        minimo = datetime.datetime.strptime(inicio, formato)  # Fecha mínima en formato TIMESTAMP 'YYYY-MM-DD HH24:MI:SS.FF'
        maximo = datetime.datetime.strptime(final, formato)  # Fecha máxima en formato TIMESTAMP
        fecha = minimo + (maximo - minimo) * random.random()
        if sec_precision == 6 or sec_precision == 0:
            print(fecha.strftime("%d/%m/%Y %H:%M:%S.%f"))
            return fecha.strftime("%d/%m/%Y %H:%M:%S.%f")
        else:
            sec_precision = 6 - sec_precision
            print(fecha.strftime("%d/%m/%Y %H:%M:%S.%f")[:-sec_precision])
            return fecha.strftime("%d/%m/%Y %H:%M:%S.%f")[:-sec_precision]


def check_fecha(check, es_date, not_null, sec_precision):
    """Comprueba las restricciones CHECK

            :param check: campo check de la sentencia parseada
            :param es_date: indica si el tipo de dato es DATE o TIMESTAMP
            :param not_null: indica si la sentencia contiene la opción NOT NULL
            :param sec_precision: precisión de la parte fraccional de los segundos (TIMESTAMP)
            :return: fecha aleatoria teniendo en cuenta las restricciones del campo option y del tipo de datos
            """
    """ POSIBLES RESTRICCIONES EN FECHAS: -OPERADORES: order_date >= TO_DATE('2014/02/01', 'yyyy/mm/dd') AND order_date <= TO_DATE('2014/02/28','yyyy/mm/dd');
        En oracle se pueden utilizar funciones para hacer una conversión de string a fecha y viceversa:
            - TO_CHAR(<date>, '<format>')
            - TO_DATE(<string>, '<format>')
    
    """
    # date [{}] {'name': 'fech1', 'type': {'date': {}}, 'unique': True, 'nullable': False,

    # 'check': {'and': [{'gte': ['fech1', {'to_date': [{'literal': '2014/02/01'}, {'literal': 'yyyy/mm/dd'}]}]},
    #                   {'lte': ['fech1', {'to_date': [{'literal': '2014/02/28'}, {'literal': 'yyyy/mm/dd'}]}]}]}}

    _neq = None
    _not = None
    if len(check) != 0:  # hay campo check
        operator = list(check.keys())[0].lower()  # primer operador que aparece en el check
        #print (list(check.keys()))
        if operator == "and" or operator == "or":
            comparisons = check.get(operator)  # lista de comparaciones
        else:
            comparisons = [check]  # Convierte el diccionario que contiene la comparación a una lista de un elemento
        lista = []
        for comparison in comparisons:
            comparison_key = list(comparison.keys())
            #print(list(comparison.keys()))
            f = comparison.get(comparison_key[0])                            # ['fech1', {'to_date': [{'literal': '01/02/2014'}, {'literal': 'yyyy/mm/dd'}]}]
            s1 = f[1]                                                        # {'to_date': [{'literal': '01/02/2014'}, {'literal': 'yyyy/mm/dd'}]}
            key = list(s1.keys())
            if key == ['to_date']:     #TIPO to_date

                s2 = list(s1.values())                                       # [[{'literal': '01/02/2014'}, {'literal': 'yyyy/mm/dd'}]]
                s3 = s2[0][0]                                                # {'literal': '01/02/2014'}
                s4 = str(list(s3.values())[0])                               # Cadena string con la fecha: 01/02/2014
                fecha = datetime.datetime.strptime(s4,'%d/%m/%Y').date()     # Objeto fecha 2014-02-01 para poder compararlas
                lista.append(fecha)  # Guarda las fechas
                #print(f)
                #print(key)
                #print(s2)
                #print(s3)
                #print(s4)
                #print(fecha)





            if key == ['to_char']:     #TIPO to_char
                pass                   #SIN IMPLEMENTAR AUN

        #print(lista)
        #if (lista[0] < lista[1]): print("Si")







def restrictions_fecha(esDate, secPrecision, column):
    """Comprueba las restricciones en el campo option.

        :param esDate: indica si el tipo de dato es DATE o TIMESTAMP
        :param secprecision: precisión de la parte fraccional de los segundos (TIMESTAMP)
        :param column: restricciones. Ej: {'name': 'fech2', 'type': {'timestamp': 2}, 'unique': True, 'nullable': True}
        :return: una fecha aleatoria o un string definiendo el error
        """
    # check = [d['check'] for d in column if 'check' in d]
    nullable = True
    # if not isinstance(options, list):  # Si solo hay una opción
    #    options = [options]
    #    print(options)

    if "nullable" in column:  # No afecta
        nullable = column.get("nullable")
    if "unique" in column:  # De momento no afecta
        pass
    if "primary key" in column:  # De momento no afecta
        pass
    if "check" not in column:
        return check_fecha([], esDate, nullable, secPrecision)
    else:
        return check_fecha(column.get("check"), esDate, nullable, secPrecision)


def option_restrictions(es_float, precision, scale, column):
    """Comprueba las restricciones en el campo option.

    :param es_float: indica si el tipo de dato es un float
    :param precision: precisión de la parte entera del número
    :param scale: número de decimales
    :param options: restricciones. Ej: {'check': {'gt': ['Id', 50]}} o
                                       {'check': {'and': [{'gte': ['Id', 50]}, {'lt': ['ID', 100]}]} o
                                      {'option': ['unique', 'not null', {'check': {'gte': ['Id', 50]}}}
    :return: un entero aleatorio o un string definiendo el error
    """

    # check = [d['check'] for d in column if 'check' in d]
    nullable = True
    # if not isinstance(options, list):  # Si solo hay una opción
    #    options = [options]
    #    print(options)
    if "nullable" in column:  # No afecta
        nullable = column.get("nullable")
    if "unique" in column:  # De momento no afecta
        pass
    if "primary key" in column:  # De momento no afecta
        pass
    if "check" not in column:
        return option_check([], es_float, nullable, precision, scale)
    else:
        return option_check(column.get("check"), es_float, nullable, precision, scale)


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


def generate_real(data_type, parameters, column, constraint):
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
    if data_type == "float":  # float-point
        precision = 126 if parameters[0][0] == "{}" else parameters[0]
        scale = None
        es_float = True
    elif data_type == "real":  # float-point
        precision = 63
        scale = None
        es_float = True
    else:  # fixed-point
        if parameters[0] == "{}":
            precision = 38
            scale = 127
        elif isinstance(parameters[0], int):
            precision = parameters[0]
            scale = 0
        else:
            precision = parameters[0][0]
            scale = parameters[0][1]
    return option_restrictions(es_float, precision, scale, column)

def generate_fecha(data_type, parameters, column, constraint):
    """Genera una fecha aleatoria que cumpla con las especificaciones de los parámetros y las opciones CHECK.

                :param data_type: tipo de dato de la columna (DATE O TIMESTAMP)
                :param parameters: parámetros del tipo de dato
                :param option: opciones adicionales definidas por el usuario (NULL, NOT NULL, UNIQUE, CHECK).
                                Ej: ['not null', {'check': {'gte': ['Id', 50]}}]
                                    'unique'
                                    {'check': {'gte': ['Id', 50]}}
                :param constraint: restricciones definidas después de las columnas **SIN IMPLEMENTAR**
                :return: una fecha aleatoria
                """
    sec_precision = 0
    es_date = False
    if data_type == "date":  # DATE 'YYYY-MM-DD'
        es_date = True
    else:                    #TIMESTAMP 'YYYY-MM-DD HH24:MI:SS.FF'  sec_precision = 2 (.FF)
        sec_precision = parameters[0]

    return restrictions_fecha(es_date, sec_precision, column)



def generate_string(data_type, parameters, option, constraint):
    """Genera una cadena de caracteres aleatoria que cumpla con las especificaciones de los parámetros
    y las opciones CHECK.

        :param data_type: tipo de dato de la columna
        :param parameters: parámetros del tipo de dato
        :param option: opciones adicionales definidas por el usuario (NULL, NOT NULL, UNIQUE, CHECK).
                        Ej: ['not null', {'check': {'gte': ['Id', 50]}}]
                            'unique'
                            {'check': {'gte': ['Id', 50]}}
        :param constraint: restricciones definidas después de las columnas **SIN IMPLEMENTAR**
        :return: un entero aleatorio
        """
    #print(data_type, parameters, option)


def clasificar_tipo(sentencia):
    """Detecta el tipo de datos y delega la generación del tipo de dato detectado.

    :param sentencia:
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

        if key in constantes.ENTEROS:
            print(generate_int(parameters, column, constraint))
        elif key in constantes.REALES:
            print(generate_real(key, parameters, column, constraint))
        elif key in constantes.STRINGS:
            # print("Datos de tipo cadena de caracteres aun sin implementar.")
            print(generate_string(key, parameters, column, constraint))
        elif key in constantes.FECHA:
            print(generate_fecha(key, parameters, column, constraint))
        else:
            print("Ha habido un error en la clasificación de tipo de datos.")


sentencia_tablas5 = """CREATE TABLE Persona (
    Id NUMBER(5) UNIQUE NOT NULL CHECK (NOT 0 <= ID AND ID < 100 AND ID != 80) ,
  real NUMBER(4,2) UNIQUE NULL CHECK (NOT id <= 0 AND id < 20 AND id != 0),
  string VARCHAR(15) UNIQUE NULL CHECK (LEN(ID) > 5),
  CONSTRAINT NombreLargo CHECK (LENGTH(Nombre) > 5), 
  fech1 DATE UNIQUE NOT NULL CHECK (fech1 >= TO_DATE('01/02/2014', 'yyyy/mm/dd') AND fech1 <= TO_DATE('28/02/2014','yyyy/mm/dd')),
  fech2 TIMESTAMP(2) UNIQUE NULL 
);"""

# print(parse(sentencia_tablas5))
clasificar_tipo(parse(sentencia_tablas5))

aux = {'create table': {
        'name': 'Persona',
        'columns': [
            {'name': 'id',
             'type': {'number': 5},
             'option': ['unique', 'not null',  # de -50 hasta 99
                        {'check': {'and': [{'gte': ['Id', -50]}, {'lt': ['ID', 100]}, {'neq': ['ID', 80]}]}}]},
            {'name': 'real',
             'type': {'number': [4, 2]},
             'option': ['unique', 'null',  # de -49.99 hasta 19.99
                        {'check': {'and': [{'not': {'lte': [0, 'id']}}, {'lt': ['ID', 20]}, {'neq': ['ID', 0]}]}}]},
            {'name': 'string',
             'type': {'char': 4},
             'option': ['unique', 'null',
                        {'check': {'and': [{'not': {'lte': [0, 'id']}}, {'lt': ['ID', 20]}, {'neq': ['ID', 0]}]}}]},

            {'name': 'fech1',
             'type': {'date': ''},
             'option': ['unique', 'null']
                        #,{'check': {'and': [{'not': {'lte': [0, 'id']}}, {'lt': ['ID', 20]}, {'neq': ['ID', 0]}]}
             },

            {'name': 'fech2',
             'type': {'timestap': 2},
             'option': ['unique', 'null']
                        #,{'check': {'and': [{'not': {'lte': [0, 'id']}}, {'lt': ['ID', 20]}, {'neq': ['ID', 0]}]}
             }
        ],
        'constraint': {'name': 'NombreLargo', 'check': {'gt': [{'length': 'Nombre'}, 5]}}}}

