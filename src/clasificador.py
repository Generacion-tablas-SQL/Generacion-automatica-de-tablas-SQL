import itertools
import random
import string
from time import mktime, strptime, strftime, localtime
import re
import constantes
import generador_datos as gd

def restricciones_sql(parameters, column):
    """Comprueba las restricciones SQL.

    :param parameters: lista con parámetros del tipo de dato.
    :param column: diccionario con restricciones de la columna.
    :return: lista con las restricciones. El último elemento de la lista es un diccionario con las restricciones check.
    """

    restricciones_dict = dict()

    check = column.get("check", None)
    if ("nullable" in column and column.get("nullable")) or "nullable" not in column:
        restricciones_dict.update({"nullable": True})
    else:
        restricciones_dict.update({"nullable": False})
    if "unique" in column and column.get("unique"):
        restricciones_dict.update({"unique": []})
    if "primary_key" in column and column.get("primary_key"):
        restricciones_dict.update({"primary key": []})
    if "references" in column:
        restricciones_dict.update({"references": [x.lower() for x in column.get("references").values()]})

    if parameters[0] == "Number" or parameters[0] == "String":
        restricciones_dict.update(comprobar_restricciones_check(parameters, check))
    else:    # parameters[0] == "Fecha"
        # En esta versión de la biblioteca, las fechas no poseen restricciones check
        restricciones_dict.update({"sec_precision": parameters[2], "es_date": parameters[3]})

    return restricciones_dict


def get_index(comparison, _not):
    """
    :param comparison: diccionario con la comparación
    :param _not: operación de la comparación asociada al not
    :return: indice que indica en que posición se sitúa el número a comparar
    """

    return 1 if _not is None and (
        isinstance(comparison.get("args")[1], int)
        or isinstance(comparison.get("args")[1], float)
    ) else (
        1 if _not is not None and (
            isinstance(comparison.get("args")[0].get("args")[1], int)
            or isinstance(comparison.get("args")[0].get("args")[1], float)
            )
        else 0)


def generar_datos(restricciones, times):
    data = list()
    if restricciones.get("tipo") == "Number":
        for i in range(0, times):
            gen_num, unique, primary = gd.generate_number(restricciones)
            if gen_num is not None:
                data.append(gen_num)
            if unique is not None:
                restricciones.update({"unique": unique})
            if primary is not None:
                restricciones.update({"primary key": primary})

    elif restricciones.get("tipo") == "String":
        for i in range(0, times):
            gen_string, unique, primary = gd.generate_string(restricciones)
            if gen_string is not None:
                data.append(gen_string)
            if unique is not None:
                restricciones.update({"unique": unique})
            if primary is not None:
                restricciones.update({"primary key": primary})
    elif restricciones.get("tipo") == "Date":
        for i in range(len(data), times):
            data.append(gd.generate_fecha(restricciones))
    else:
        raise Exception

    return data


# <----RESTRICCIONES WHERE---->
def cumple_restricciones(restricciones, data):
    new_data = data
    valid = True
    if restricciones.get("eq") is not None and restricciones.get("eq") != data:
        valid = False
    if restricciones.get("neq") is not None and restricciones.get("neq") == data:
        valid = False

    if restricciones.get("tipo") == "Number":
        if data < restricciones.get("min"):
            new_data = restricciones.get("min")
        elif data > restricciones.get("max"):
            new_data = restricciones.get("max")
    elif restricciones.get("tipo") == "String":
        if isinstance(data, int) or isinstance(data, float):
            if data < restricciones.get("min"):
                new_data = restricciones.get("min")
            elif data > restricciones.get("max"):
                new_data = restricciones.get("max")
        else:
            if data.find("%") == -1:
                if len(data) < restricciones.get("min"):
                    for i in range(len(data), int(restricciones.get("min"))):
                        new_data += 'a'
                elif len(data) > restricciones.get("max"):
                    new_data = data[0:restricciones.get("max")]
            if restricciones.get("like") is not None:
                like_regex = restricciones.get("like").replace("%", "[a-zA-Z ]*").replace("_", "[a-zA-Z ]")
                data_regex = data.replace("%", "as").replace("_", "a")
                if not re.match(like_regex, data_regex):
                    valid = False
    return valid, new_data

# Para semiordenar el orden de las permutaciones más adelante.
def loop_list(op: str, scale: int):
    loop = list()
    if op in ["eq", "lte"]:
        loop = [0, -1 / 10 ** scale, 1 / 10 ** scale]
    elif op == "gte":
        loop = [0, 1 / 10 ** scale, -1 / 10 ** scale]
    elif op == "gt":
        loop = [1 / 10 ** scale, 0, -1 / 10 ** scale]
    elif op == "lt":
        loop = [-1 / 10 ** scale, 0, 1 / 10 ** scale]
    elif op == "neq":
        loop = [-1 / 10 ** scale, 1 / 10 ** scale, 0]
    return loop


def restricciones_where(col_name, restricciones_col, sentencia_where, gen_data, compara_cols):
    """Comprueba las condiciones del where y modifica el diccionario de restricciones de forma que se puedan generar los
    datos consultados así como datos no consultados.

    :param col_name: nombre de la columna
    :param restricciones_col: lista con restricciones de la columna consultada
    :param sentencia_where:
    :param gen_data: diccionario con datos previamente generados en esta función asociados a su columna. Si es la
    primera vez que accede, será un diccionario vacío
    :param compara_cols: valor que nos indica si se están comparando dos columnas de la misma tabla
    :return: diccionario con datos generados, lista con valores unique usados, lista con valores primary key usados
    """

    op = sentencia_where.get("op")
    args = list()
    if op == "and":
        args.extend(sentencia_where.get("args"))
    else:
        args.append(sentencia_where)

    _unique = restricciones_col.get("unique")
    _primary = restricciones_col.get("primary key")

    for arg in args:
        args_ = arg.get("args")
        arg_data, arg_col = (args_[1], args_[0]) if isinstance(args_[0], str) else (
            (args_[0], args_[1]) if isinstance(args_[1], str) else (
                (args_[1], args_[0].get("args")[0]) if isinstance(args_[0], dict) else (args_[0], args_[1].get("args")[0])
            )
        )

        if not compara_cols and arg_col.lower() != col_name:
            continue

        elif compara_cols and arg_col.lower() != col_name:
            data = gen_data.get(arg_data.lower())
            valid, data = cumple_restricciones(restricciones_col, data[0])
            gen_data[arg_data.lower()] = [data]
            break

        op_ = arg.get("op")
        col_data = list()  # Almacena los datos generados para una columna del where

        # Para saber si existe una operación length
        len_ex = str(args_[0]).find("length") if isinstance(args_[0], dict) else (
            str(args_[1]).find("length") if isinstance(args_[1], dict) else -1
        )

        # Para igualdades o desigualdades de cadenas o LIKE
        if isinstance(arg_data, dict):
            arg_data = arg_data.get("literal")

        ops = ["eq", "neq", "gt", "gte", "lt", "lte", "like", "length"]
        scale = restricciones_col.get("scale")
        if op_ in ops:
            if compara_cols:
                valid = True
            else:
                valid, data = cumple_restricciones(restricciones_col, arg_data)
            if valid:
                if restricciones_col.get("tipo") == "Number":
                    if compara_cols:
                        data = "NULL"
                        while data == "NULL":
                            data = gd.generate_number(restricciones_col)[0]

                    # Para semiordenar el orden de las permutaciones más adelante.
                    loop = loop_list(op_, scale)

                    for i in loop:
                        # Si hay restriccion unique o primary key y se repite un dato, se vuelve a generar hasta
                        # que se genera un dato no repetido, o hasta que de UNIQUE_TRIES vueltas
                        for j in range(0, constantes.UNIQUE_TRIES):
                            # Si se están comparando dos columnas de una tabla, generamos un valor aleatorio para la
                            # segunda columna y para la primera columna generamos valores frontera.
                            if compara_cols:
                                if gen_data.get(arg_data.lower()) is None:
                                    gen_data[arg_data.lower()] = [data]
                            if scale == 0:
                                i = int(i)
                                data = int(data)
                            else:
                                i = float(i)
                                data = float(data)

                            # Evita restas incorrectas como 0.03 - 0.01 = 0.19999..7
                            rounded_data = round(data + i, scale)

                            # Comprueba si el número generado cumple restricciones de su columna
                            valid2, data2 = cumple_restricciones(restricciones_col, rounded_data)
                            if scale == 0:
                                data2 = int(data2)

                            if _unique is None and _primary is None:
                                col_data.append(data2)
                                break
                            elif _unique is not None and data2 not in _unique:
                                col_data.append(data2)
                                _unique.append(data2)
                                break
                            elif _primary is not None and data2 not in _primary:
                                col_data.append(data2)
                                _primary.append(data2)
                                break
                            else:
                                if i == 0:
                                    break
                                else:
                                    # Suma o resta y vuelve a intentar insertarlo
                                    i += i
                elif restricciones_col.get("tipo") == "String":
                    if compara_cols:
                        data = "NULL"
                        while data == "NULL":
                            data = gd.generate_string(restricciones_col)[0]

                    strings = list()
                    if op_ == "like":
                        old_like = restricciones_col.get("like")
                        restricciones_col.update({"like": data})
                        strings.append(gd.generate_string(restricciones_col)[0])

                        # GENERAR VALOR INVÁLIDO
                        pos = 0
                        found = False
                        for i in data:
                            if i != "_" and i != "%" and i != old_like[pos]:
                                found = True
                                break
                            pos += 1

                        if found:
                            letr = random.choice(string.ascii_letters)
                            while letr == data[pos]:
                                letr = random.choice(string.ascii_letters)

                            invalid_data = data[0:pos] + letr + data[pos + 1:]
                            restricciones_col.update({"like": invalid_data})
                            strings.append(gd.generate_string(restricciones_col)[0])
                        else:
                            raise Exception("Restricción LIKE en sentencia SELECT no soportada. "
                                            "Debe contener al menos un caracter válido.")

                        restricciones_col.update({"like": old_like})

                    elif len_ex != -1:  # Existe el campo length

                        old_min = int(restricciones_col.get("min"))
                        old_max = int(restricciones_col.get("max"))

                        loop = loop_list(op_, 0)

                        data = int(data)
                        for i in loop:
                            i = int(i)
                            valid2, data2 = cumple_restricciones(restricciones_col, data + i)
                            if valid2 and data2 != data + i:
                                i = 0
                            restricciones_col.update({"min": data + i})
                            restricciones_col.update({"max": data + i})
                            strings.append(gd.generate_string(restricciones_col)[0])
                            restricciones_col.update({"min": old_min})
                            restricciones_col.update({"max": old_max})

                    else:  # Operaciones con operadores
                        loop = loop_list(op_, 0)
                        for i in loop:
                            if compara_cols:
                                if gen_data.get(arg_data.lower()) is None:
                                    gen_data[arg_data.lower()] = [data]
                            i = int(i)
                            char = chr(ord(data[-1]) + i)
                            strings.append(data[0:-1] + char)  # Añade el siguiente caracter ascii al último caracter

                    for i in strings:
                        if _unique is None and _primary is None:
                            col_data.append(i)
                        elif _unique is not None and arg_data + i not in _unique:
                            col_data.append(i)
                            _unique.append(i)
                        elif _primary is not None and arg_data + i not in _primary:
                            col_data.append(i)
                            _primary.append(i)

                else:  # tipo == "Fecha"
                    if compara_cols:
                        arg_data = "NULL"
                        while arg_data == "NULL":
                            arg_data = gd.generate_fecha(restricciones_col)

                    loop = list()
                    if op_ in ["eq", "lte"]:
                        loop = [0, -1, 86400]  # Los días UTC duran 86400 s
                    elif op_ == "gte":
                        loop = [0, 86400, -1]
                    elif op_ == "gt":
                        loop = [86400, 0, -1]
                    elif op_ == "lt":
                        loop = [-1, 0, 86400]
                    elif op_ == "neq":
                        loop = [-1, 86400, 0]

                    if restricciones_col.get("es_date"):
                        fecha = mktime(strptime(arg_data, "%d/%m/%Y"))
                    else:
                        fecha = mktime(strptime(arg_data, "%d/%m/%Y %H:%M:%S.%f"))

                    fechas = list()
                    for i in loop:
                        if compara_cols:
                            if gen_data.get(arg_data.lower()) is None:
                                gen_data[arg_data.lower()] = [data]

                        if restricciones_col.get("es_date"):
                            fechas.append(strftime("%d/%m/%Y", localtime(fecha + i)))
                        else:
                            fechas.append(strftime("%d/%m/%Y %H:%M:%S.%f", localtime(fecha + i)))

                    for i in fechas:
                        if _unique is None and _primary is None:
                            col_data.append(i)
                        elif _unique is not None and arg_data + i not in _unique:
                            col_data.append(i)
                            _unique.append(i)
                        elif _primary is not None and arg_data + i not in _primary:
                            col_data.append(i)
                            _primary.append(i)

                if gen_data.get(col_name) is None:
                    gen_data[col_name] = col_data[:]
                else:
                    gen_data[col_name].extend(col_data[:])
                col_data.clear()
        else:
            raise Exception("Operador en sentencia where no soportado")
    return gen_data, _unique, _primary


def comprobar_restricciones_check(parameters, check):
    """Comprueba las restricciones CHECK

        :param parameters: tipo de dato Number: ["Number", nombre_col, precision, escala]
                           tipo de dato String: ["String", nombre_col, varying, max_size]
        :param check: campo check de la sentencia parseada
        :return: diccionario con el número máximo, mínimo equal y not equal si se específica
        """

    _max = gd.max_number(parameters[2], parameters[3]) if parameters[0] == "Number" else parameters[3]
    _min = -_max if parameters[0] == "Number" else (1 if parameters[2] is True else parameters[3])
    _eq = None
    _neq = None
    _not = None
    _like = None
    _scale = 0 if parameters[0] == "String" else parameters[3]

    if check is None:
        return {"min": _min, "max": _max, "eq": _eq, "neq": _neq, "like": _like, "scale": _scale}

    comparisons = check.get("args")

    for comparison in comparisons:

        comparison_op = comparison.get("op")
        if comparison_op == "not":
            _not = comparison.get("args")[0].get("op")
        if comparison_op == "eq":
            _eq = comparison.get("args")[get_index(comparison, None)]
        elif comparison_op == "neq":
            _neq = comparison.get("args")[get_index(comparison, None)]
        elif comparison_op == "gt" or _not == "gt":
            if _not == "gt":
                # Calcula el mínimo entre _max y el contenido del comparador
                _max = min(_max, comparison.get("args")[0].get("args")[get_index(comparison, _not)])
            else:
                # Calcula el máximo entre _min y el contenido del comparador. Si es de tipo número decimal,
                # se suma uno al decimal menos significativo
                _min = max(_min, comparison.get("args")[get_index(comparison, None)] + 1 / 10 ** _scale)
        elif comparison_op == "gte" or _not == "gte":
            if _not == "gte":
                _max = min(_max, comparison.get("args")[0].get("args")[get_index(comparison, _not)] - 1 / 10 ** _scale)
            else:
                _min = max(_min, comparison.get("args")[get_index(comparison, None)])
        elif comparison_op == "lt" or _not == "lt":
            if _not == "lt":
                _min = max(_min, comparison.get("args")[0].get("args")[get_index(comparison, _not)])
            else:
                _max = min(_max, comparison.get("args")[get_index(comparison, None)] - 1 / 10 ** _scale)
        elif comparison_op == "lte" or _not == "lte":
            if _not == "lte":
                _min = max(_min, comparison.get("args")[0].get("args")[get_index(comparison, _not)] + 1 / 10 ** _scale)
            else:
                _max = min(_max, comparison.get("args")[get_index(comparison, None)])
        elif comparison_op == "like":
            _like = comparison.get("args")[1].get("literal")
        else:
            raise Exception("Operador en sentencia CREATE TABLE no soportado")
        _not = None

    if _min > _max or _max < _min:
        raise Exception("Restricciones de la columna no satisfactibles")
    if _eq is not None and (_eq < _min or _eq > _max):
        raise Exception("Restricciones de la columna no satisfactibles")
    if _like is not None:
        if len(_like) - _like.count('%') > _max:
            raise Exception("Restricciones de la columna no satisfactibles")
        if _like.count('%') == 0 and len(_like) < _min:
            raise Exception("Restricciones de la columna no satisfactibles")

    return {"min": _min, "max": _max, "eq": _eq, "neq": _neq, "like": _like, "scale": _scale}


def clasificar_tipo(nombre_tabla, columnas, tablas_datos, select_joins, condicion_where):

    """Detecta los tipo de datos de las columnas y delega la generación del tipo de dato detectado.

    :param nombre_tabla: nombre de la tabla que se se está clasificando
    :param columnas: lista con las columnas de la tabla necesaria parseada
    :param tablas_datos: diccionario con los datos de cada columna de cada tabla sobre la que se haya iterado.
    :param select_joins: diccionario con las columnas con las que dos tablas hacen join
    :param condicion_where:
    :return: col_data: diccionario con los datos generados de cada columna
             col_restrictions: diccionario con las restricciones de cada columna.
    """

    col_data = {}
    col_restrictions = {}

    # Analisis de condiciones en WHERE
    col_select = list()
    if condicion_where is not None:
        args = list()
        args.extend(condicion_where.get("args"))
        nombre_columnas = [x.get("name") for x in columnas]
        cont = 0  # Contamos el número de veces que aparece un nombre de columna en los argumentos
        compara_cols = False  # Si el contador es igual a 2 significa que se están comparando dos columnas de la tabla

        # Determinar el nombre de las columnas de las condiciones
        for arg in args:
            if isinstance(arg, dict):
                in_args = arg.get("args")

                # Para igualdades/desigualdades entre fechas.
                if in_args is None:
                    break
                col_select.append(in_args[0].lower()) if isinstance(in_args[0], str) else (
                    col_select.append(in_args[1].lower()) if isinstance(in_args[1], str) else (
                        col_select.append(in_args[0].get("args")[0]) if isinstance(in_args[0], dict) else
                        col_select.append(in_args[1].get("args")[0])
                    )
                )
            else:
                if isinstance(arg, str) and arg.lower() in nombre_columnas:
                    cont += 1
                    col_select.append(arg.lower())
                else:
                    in_args = args
                    if isinstance(in_args[0], str):
                        col_select.append(in_args[0].lower())
                    elif isinstance(in_args[1], str):
                        col_select.append(in_args[1].lower())
        if cont == 2:
            compara_cols = True

    where_data = dict()

    for column in columnas:
        col_name = column.get("name").lower()
        data_type = column.get("type").get("op").lower()
        parameters = column.get("type").get("args", None)

        data = list()

        if data_type in constantes.ENTEROS or data_type in constantes.REALES:
            data_type_param = list()

            data_type_param.append("Number")
            data_type_param.append(col_name)

            if data_type in constantes.ENTEROS:
                data_type_param.append(38) if parameters is None else data_type_param.append(parameters)
                data_type_param.append(0)
            else:
                # Si es un número con coma flotante lo convertimos a uno de coma fija
                data_type_param.extend([10, 4]) if data_type in constantes.COMA_FLOTANTE else (
                    data_type_param.extend([38, 127]) if parameters is None else data_type_param.extend(parameters))

                if len(data_type_param) == 3:
                    data_type_param.append(0)

            restricciones = restricciones_sql(data_type_param, column)
            restricciones.update({"tipo": "Number"})
            col_restrictions.update({col_name: restricciones})

            # Si el where contiene a la columna, comprobamos las restricciones
            if condicion_where is not None and col_name in col_select:
                where_data, unique, primary = restricciones_where(col_name, restricciones, condicion_where,
                                                                  where_data, compara_cols)
                if unique is not None:
                    restricciones.update({"unique": unique})
                if primary is not None:
                    restricciones.update({"primary key": primary})

            col_data.update({col_name: data})

        elif data_type in constantes.STRINGS:

            # char y nchar tienen un tamaño por defecto de 1
            max_size = 1 if parameters is None else parameters[0]
            varying = False if data_type == "char" or data_type == "nchar" else True

            data_type_param = ["String", col_name, varying, max_size]
            restricciones = restricciones_sql(data_type_param, column)
            restricciones.update({"tipo": "String"})
            col_restrictions.update({col_name: restricciones})

            # Si el where contiene a la columna, comprobamos las restricciones
            if col_name in col_select:
                where_data, unique, primary = restricciones_where(col_name, restricciones, condicion_where,
                                                                  where_data, compara_cols)
                if unique is not None:
                    restricciones.update({"unique": unique})
                if primary is not None:
                    restricciones.update({"primary key": primary})

            col_data.update({col_name: data})

        elif data_type in constantes.FECHA:

            es_date = 1 if data_type == "date" else 0
            sec_precision = 0 if parameters is None else parameters[0]

            data_type_param = ["Fecha", col_name, sec_precision, es_date]

            restricciones = restricciones_sql(data_type_param, column)

            restricciones.update({"tipo": "Date"})
            col_restrictions.update({col_name: restricciones})

            if col_name in col_select:

                where_data, unique, primary = restricciones_where(col_name, restricciones, condicion_where,
                                                                  where_data, compara_cols)
                if unique is not None:
                    restricciones.update({"unique": unique})
                if primary is not None:
                    restricciones.update({"primary key": primary})

            col_data.update({col_name: data})
        else:
            raise Exception("Tipo de dato no soportado.")

    # Evaluación de permutaciones entre condiciones de una sentencia where
    values = list(where_data.values())
    keys = list(where_data.keys())
    if len(where_data) > 1:
        permutations = list(itertools.product(*values))
        aux = permutations[0]
        permutations = random.sample(permutations[1:], len(permutations) - 1)
        permutations.insert(0, aux)

        uniques = list()
        primaries = list()
        for i in range(0, len(keys)):
            uniques.append([] if col_restrictions.get(keys[i]).get("unique") is not None else None)
            primaries.append([] if col_restrictions.get(keys[i]).get("primary key") is not None else None)

        for permutation in permutations:
            ok = True

            for i in range(0, len(keys)):
                if cumple_restricciones(col_restrictions.get(keys[i]), permutation[i]):
                    if uniques[i] is None and primaries[i] is None:
                        pass
                    elif uniques[i] is not None and permutation[i] not in uniques[i]:
                        uniques[i].append(permutation[i])
                    elif primaries[i] is not None and permutation[i] not in primaries[i]:
                        primaries[i].append(permutation[i])
                    else:
                        ok = False
                else:
                    ok = False
                    break
            if ok:
                for j in range(0, len(keys)):
                    col_data.get(keys[j]).append(permutation[j])

    elif len(where_data) > 0:
        col_data.update({col_select[0]: where_data.get(col_select[0])})

    times = 0
    if condicion_where is not None:
        for i in range(0, len(keys)):
            times = max(times, len(col_data.get(keys[i])))

    # Generación de datos por JOIN
    if len(select_joins) > 0:
        for join in select_joins:  # join es una tupla que contiene las tablas de un JOIN
            if nombre_tabla in join:
                # No se permite alias, asi que dos columnas de dos tablas diferentes tiene que llamarse
                # diferente, con lo cual no hay problema en comprobar las dos columnas.
                col = select_joins.get(join)[1].lower()
                # Compruebo si la columna es de la tabla sobre la que se está iterando o es de la otra
                if col_restrictions.get(col) is None:
                    col = select_joins.get(join)[2].lower()

                if col_restrictions.get(col) is not None:  # Puede ser que las col del JOIN no sean de la tabla actual
                    if col_restrictions.get(col).get('primary_key') is not None:
                        # Generar dos valores diferentes para la columna
                        check = next((columna for columna in columnas if columna['name'] == col), None)
                        datos_join = generar_datos(col_restrictions.get(col), 2)
                        while datos_join[0] == datos_join[1]:              # Comprobamos que los dos datos son distintos
                            datos_join[1] = generar_datos(col_restrictions.get(col), 1)
                        col_data.update({col: datos_join})
                    else:
                        # Generar un valor que coincida con alguno de los creados en el primary key de la otra tabla
                        datos_join = list()
                        # times es el número máximo de datos metidos en una columna por el where
                        aux_times = 1 if times == 0 else times
                        if len(col_data.get(col)) == 0:
                            tabla_primary = join[0]
                            col_primary = select_joins.get(join)[1].lower()
                            dato_primary = tablas_datos.get(tabla_primary).get(col_primary)[0]
                            if select_joins.get(join)[0] == "eq":
                                col_restrictions.get(col).update({"eq": dato_primary})
                            elif select_joins.get(join)[0] == "gt":
                                col_restrictions.get(col).update({"min": dato_primary + 1})
                            elif select_joins.get(join)[0] == "gte":
                                col_restrictions.get(col).update({"min": dato_primary})
                            elif select_joins.get(join)[0] == "lt":
                                col_restrictions.get(col).update({"max": dato_primary - 1})
                            elif select_joins.get(join)[0] == "lte":
                                col_restrictions.get(col).update({"max": dato_primary})
                            else:
                                raise Exception("Operador en join no soportado")

                            check = next((columna for columna in columnas if columna['name'] == col), None)
                            dato = generar_datos(col_restrictions.get(col), 1)

                            for i in range(0, aux_times):
                                datos_join.extend(dato)
                            col_data.update({col: datos_join})
                break

    # Generación de datos cuya columna referencia a otra tabla
    for columna in columnas:
        col_name = columna.get("name")
        references = col_restrictions.get(col_name).get("references")
        if len(col_data.get(col_name)) == 0 and references is not None:
            # Coger un dato aleatorio de la columna de la tabla a la que referencia

            # En la posición 0 siempre está el nombre de la tabla a la que referencia
            datos_references = tablas_datos.get(references[0]).get(references[1])

            datos_r = list()
            aux_times = 1 if times == 0 else times
            for i in range(0, aux_times):
                # Coger un valor de los generados en la col que tiene primary key
                datos_r.append(random.choice(datos_references))
            col_data.update({col_name: datos_r})

    # Generación del resto de datos
    if select_joins is not None:
        for key in col_data.keys():
            times = max(times, len(col_data.get(key)))

    if times == 0:
        times = constantes.NUM_FILAS

    for dato in col_data:
        if len(col_data.get(dato)) < times:
            times_aux = times - len(col_data.get(dato))
            check = next((col for col in columnas if col['name'] == dato), None)
            col_data.update({dato: generar_datos(col_restrictions.get(dato), times_aux)})

    return col_data, col_restrictions
