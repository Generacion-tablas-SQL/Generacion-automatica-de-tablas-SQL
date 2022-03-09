import itertools
from time import mktime, strptime, strftime, localtime
import re
import constantes
import generador_datos as gd

# <----GENERAL---->
def restricciones_sql(parameters, column):
    """Comprueba las restricciones SQL.

    :param parameters: lista con parámetros del tipo de dato.
    :param column: diccionario con restricciones de la columna.
    :return: lista con las restricciones. El último elemento de la lista es un diccionario con las restricciones check.
    """

    restricciones_list = list()
    restricciones_dict = dict()

    check = column.get("check", None)
    if ("nullable" in column and column.get("nullable")) or "nullable" not in column:
        restricciones_list.append("nullable")
    if "unique" in column and column.get("unique"):
        restricciones_dict.update({"unique": []})
    if "primary key" in column and column.get("primary key"):
        restricciones_dict.update({"primary key": []})
    if "foreign key" in column and column.get("foreign key"):
        restricciones_list.append("foreign key")
    if "default" in column:
        restricciones_list.append({"default", column.get("default").get("literal")})

    restricciones_list.append(restricciones_dict)
    if parameters[0] == "Number" or parameters[0] == "String":
        restricciones_list[-1].update(comprobar_restricciones_check(parameters, check))
    else:  # parameters[0] == "Fecha"
        # POR EL MOMENTO LAS FECHAS NO POSEEN RESTRICCIONES CHECK
        restricciones_list[-1].update({"sec_precision": parameters[2], "es_date": parameters[3]})

    return restricciones_list


def get_index(comparison, _not):
    """
    :param comparison: diccionario con la comparación
    :param _not: operación de la comparación asociada al not
    :return: indice que indica en que posición se sitúa el número a comparar
    """

    return 1 if _not is None and (
        isinstance(comparison.get("args")[1], int)
        or isinstance(comparison.get("args")[1], float)
        # or isinstance(comparison.get("args")[1], str)
    ) else (
        1 if _not is not None and (
            isinstance(comparison.get("args")[0].get("args")[1], int)
            or isinstance(comparison.get("args")[0].get("args")[1], float)
            # or isinstance(comparison.get("args")[0].get("args")[1], str)
            )
        else 0)


def generar_datos(col_name, restricciones, check, times):
    data = list()
    if restricciones[-1].get("tipo") == "Number":
        if restricciones[-1].get("other"):
            for i in range(0, times):
                data.append(gd.generate_random("Number", col_name, restricciones[-1], check))
        else:
            for i in range(0, times):
                gen_num, unique, primary = gd.generate_number(restricciones)
                if gen_num is not None:
                    data.append(gen_num)
                if unique is not None:
                    restricciones[-1].update({"unique": unique})
                if primary is not None:
                    restricciones[-1].update({"primary key": primary})

    elif restricciones[-1].get("tipo") == "String":
        if restricciones[-1].get("other"):
            for i in range(0, times):
                data.append(gd.generate_random("String", col_name, restricciones[-1], check))
        else:
            for i in range(0, times):
                data.append(gd.generate_string(restricciones[-1]))
    elif restricciones[-1].get("tipo") == "Date":
        for i in range(len(data), times):
            # restricciones[0] = sec_precision, restricciones[1]= es_date, restricciones[2] = data_type
            data.append(gd.gen_fecha(restricciones[-1]))
    else:
        raise Exception

    return data


# <----RESTRICCIONES WHERE---->
def cumple_restricciones(restricciones, data):
    new_data = data
    if restricciones.get("eq") is not None and restricciones.get("eq") != data:
        return False
    if restricciones.get("neq") is not None and restricciones.get("neq") == data:
        return False

    # No tenemos en cuenta el tipo Fecha ya que no tiene implementadas restricciones CHECK
    if restricciones.get("tipo") == "Number":
        if data < restricciones.get("min") or data > restricciones.get("max"):
            return False
    elif restricciones.get("tipo") == "String":
        if isinstance(data, int):
            if data < restricciones.get("min"):
                new_data = restricciones.get("min")
            elif data > restricciones.get("max"):
                new_data = restricciones.get("max")
        else:
            if (data.find("%") == -1 and len(data) < restricciones.get("min")) or len(data) > restricciones.get("max"):
                return False
            if restricciones.get("like") is not None:
                like_regex = restricciones.get("like").replace("%", "[a-zA-Z ]*").replace("_", "[a-zA-Z ]")
                data_regex = data.replace("%", "[a-zA-Z ]*").replace("_", "[a-zA-Z ]")
                if not re.match(like_regex, data_regex):
                    return False
    return new_data


def restricciones_where(col_name, restricciones_col, sentencia_where, gen_data):
    """Comprueba las restricciones where y modifica la lista de restricciones de forma que se puedan generar los
    datos consultados así como datos no consultados

    :param col_name: nombre de la columna
    :param restricciones_col: lista con restricciones de la columna consultada
    :param sentencia_where:
    :param gen_data: diccionario con datos previamente generados en esta función asociados a su columna. Si es la
    primera vez que accede, será un diccionario vacío
    :return: diccionario con datos generados, lista con valores unique usados, lista con valores primary key usados
    """

    op = sentencia_where.get("op")
    args = list()
    args.extend(sentencia_where.get("args"))

    _unique = restricciones_col.get("unique")
    _primary = restricciones_col.get("primary key")

    for arg in args:
        args_ = arg.get("args")
        arg_data, arg_col = (args_[1], args_[0]) if isinstance(args_[0], str) else (
            (args_[0], args_[1]) if isinstance(args_[1], str) else (
                # para WHERE con LENGTH()
                (args_[1], args_[0].get("args")[0]) if isinstance(args_[0], dict) else (args_[0], args_[1].get("args")[0])
            )
        )

        if arg_col != col_name:
            continue

        op_ = arg.get("op")
        col_data = list()  # Aquí se almacenan los datos generados para una columna del where

        # Para saber si existe una op length
        len_ex = str(args_[0]).find("length") if isinstance(args_[0], dict) else (
            str(args_[1]).find("length") if isinstance(args_[1], dict) else None
        )

        if isinstance(arg_data, dict):  # Para igualdades o desigualdades de cadenas o LIKE
            arg_data = arg_data.get("literal")

        ops = ["eq", "gt", "gte", "lt", "lte", "like", "length"]
        if op_ in ops:
            data = cumple_restricciones(restricciones_col, arg_data)
            if data != 0:
                if restricciones_col.get("tipo") == "Number":
                    scale = restricciones_col.get("scale")
                    for i in [-1 / 10 ** scale, 0, 1 / 10 ** scale]:
                        if scale == 0:
                            i = int(i)
                        if _unique is None and _primary is None:
                            col_data.append(arg_data + i)
                        elif _unique is not None and arg_data + i not in _unique:
                            col_data.append(arg_data + i)
                            _unique.append(arg_data + i)
                        elif _primary is not None and arg_data + i not in _primary:
                            col_data.append(arg_data + i)
                            _primary.append(arg_data + i)
                elif restricciones_col.get("tipo") == "String":
                    strings = list()
                    if op == "like":
                        old_like = restricciones_col.get("like")
                        restricciones_col.update({"like": arg_data})
                        strings.append(gd.generate_string(restricciones_col))
                        # FALTA VALOR INVÁLIDO
                        restricciones_col.update({"like": old_like})
                    elif len_ex != -1:  # Existe el campo length
                        old_min = restricciones_col.get("min")
                        old_max = restricciones_col.get("max")
                        for i in range(-1, 2):
                            if old_min <= data + i <= old_max:
                                restricciones_col.update({"min": data + i})
                                restricciones_col.update({"max": data + i})
                                strings.append(gd.generate_string(restricciones_col))
                        restricciones_col.update({"min": old_min})
                        restricciones_col.update({"max": old_max})

                        for i in strings:
                            if _unique is None and _primary is None:
                                col_data.append(i)
                            elif _unique is not None and arg_data + i not in _unique:
                                col_data.append(i)
                                _unique.append(i)
                            elif _primary is not None and arg_data + i not in _primary:
                                col_data.append(i)
                                _primary.append(i)
                    else:  # Operaciones con operadores
                        # Añadir siguiente caracter ascii al último caracter
                        # Cojo el ultimo caracter de la cadena y sumo un caracter ascii
                        char = chr(ord(arg_data[-1]) + 1)
                        strings.append(arg_data)
                        strings.append(arg_data[0:-1] + char)
                        char = chr(ord(arg_data[-1]) - 1)
                        strings.append(arg_data[0:-1] + char)

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

                    fecha = mktime(strptime(arg_data, "%d/%m/%Y"))
                    fechas = list()
                    fechas.append(strftime("%d/%m/%Y", localtime(fecha)))
                    fechas.append(strftime("%d/%m/%Y", localtime(fecha - 1)))
                    fechas.append(strftime("%d/%m/%Y", localtime(fecha + 86400)))  # Los días UTC duran 86400 s

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


# <----RESTRICCIONES CHECK---->
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
    _other = False

    if check is None:
        return {"min": _min, "max": _max, "eq": _eq, "neq": _neq, "like": _like, "scale": _scale, "other": _other}

    comparisons = check.get("args")

    for comparison in comparisons:

        comparison_op = comparison.get("op")
        if comparison_op == "not":
            _not = comparison.get("args")[0].get("op")  # _not contiene: "lte", "gt"...
        if comparison_op == "eq":
            _eq = comparison.get("args")[get_index(comparison, None)]
        elif comparison_op == "neq":
            _neq = comparison.get("args")[get_index(comparison, None)]
        elif comparison_op == "gt" or _not == "gt":
            if _not == "gt":
                # mínimo entre _max y el contenido del comparador
                _max = min(_max, comparison.get("args")[0].get("args")[get_index(comparison, _not)])
            else:
                # máximo entre _min y el contenido del comparador
                # Si es de tipo número decimal, se suma uno al decimal menos significativo
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
            _other = True
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

    return {"min": _min, "max": _max, "eq": _eq, "neq": _neq, "like": _like, "scale": _scale, "other": _other}


# <----INICIO---->
def clasificar_tipo(columnas, sentencia_where):
    """Detecta los tipo de datos de las columnas y delega la generación del tipo de dato detectado.

    :param columnas: array con las columnas de una tabla
    :param sentencia_where:
    :return: col_data: diccionario con los datos generados de cada columna
             col_restrictions: diccionario con las restricciones de cada columna.
    """

    col_data = {}
    col_restrictions = {}

    # op = sentencia_where.get("op")
    # and_or = op if op == "and" or op == "or" else None

    col_select = list()
    if sentencia_where is not None:
        args = list()
        args.extend(sentencia_where.get("args"))

        for arg in args:
            in_args = arg.get("args")
            col_select.append(in_args[0].lower()) if isinstance(in_args[0], str) else (
                col_select.append(in_args[1].lower()) if isinstance(in_args[1], str) else (
                    col_select.append(in_args[0].get("args")[0]) if isinstance(in_args[0], dict) else
                    col_select.append(in_args[1].get("args")[0])
                )
            )

    where_data = dict()
    # Evaluación de restricciones de las columnas
    for column in columnas:
        col_name = column.get("name").lower()
        data_type = column.get("type").get("op").lower()  # number
        parameters = column.get("type").get("args", None)  # [5, 0], [4]

        data = list()

        if data_type in constantes.ENTEROS or data_type in constantes.REALES:
            data_type_param = list()

            data_type_param.append("Number")
            data_type_param.append(col_name)

            if data_type in constantes.ENTEROS:
                data_type_param.append(38) if parameters is None else data_type_param.append(parameters)
                data_type_param.append(0)  # Escala = 0
            else:
                data_type_param.extend([10, 4]) if data_type == "float" or data_type == "real" else (
                    data_type_param.extend([38, 127]) if parameters is None else data_type_param.extend(parameters))

                if len(data_type_param) == 3:
                    data_type_param.append(0)

            restricciones = restricciones_sql(data_type_param, column)
            restricciones[-1].update({"tipo": "Number"})
            col_restrictions.update({col_name: restricciones})

            # Si el where contiene a la columna, comprobamos las restricciones
            if sentencia_where is not None and col_name in col_select:
                where_data, unique, primary = restricciones_where(col_name, restricciones[-1], sentencia_where,
                                                                  where_data)
                if unique is not None:
                    restricciones[-1].update({"unique": unique})
                if primary is not None:
                    restricciones[-1].update({"primary key": primary})

            col_data.update({col_name: data})

        elif data_type in constantes.STRINGS:
            # char y nchar tienen un tamaño por defecto de 1
            max_size = 1 if parameters is None else parameters[0]
            varying = False if data_type == "char" or data_type == "nchar" else True

            data_type_param = ["String", col_name, varying, max_size]
            restricciones = restricciones_sql(data_type_param, column)
            restricciones[-1].update({"tipo": "String"})
            col_restrictions.update({col_name: restricciones})

            # Si el where contiene a la columna, comprobamos las restricciones
            if col_name in col_select:
                where_data, unique, primary = restricciones_where(col_name, restricciones[-1], sentencia_where,
                                                                  where_data)
                if unique is not None:
                    restricciones[-1].update({"unique": unique})
                if primary is not None:
                    restricciones[-1].update({"primary key": primary})

            col_data.update({col_name: data})

        elif data_type in constantes.FECHA:

            es_date = 1 if data_type == "date" else 0
            sec_precision = 0 if parameters is None else parameters[0]

            data_type_param = ["Fecha", col_name, sec_precision, es_date]

            # restricciones = ['unique', {'sec_precision': 2, 'es_date': 0}]
            restricciones = restricciones_sql(data_type_param, column)

            # 'fec2': ['unique', {'sec_precision': 2, 'es_date': 0, 'tipo': 'Date'}]
            restricciones[-1].update({"tipo": "Date"})
            col_restrictions.update({col_name: restricciones})

            if col_name in col_select:

                where_data, unique, primary = restricciones_where(col_name, restricciones[-1], sentencia_where,
                                                                  where_data)
                if unique is not None:
                    restricciones[-1].update({"unique": unique})
                if primary is not None:
                    restricciones[-1].update({"primary key": primary})

            col_data.update({col_name: data})
        else:
            raise ValueError

    # Evaluación de permutaciones entre condiciones de una sentencia where doble
    values = list(where_data.values())
    keys = list(where_data.keys())
    if len(where_data) > 1:
        permutations = list(itertools.product(values[0], values[1]))

        unique1 = [] if col_restrictions.get(keys[0])[-1].get("unique") is not None else None
        unique2 = [] if col_restrictions.get(keys[1])[-1].get("unique") is not None else None
        primary1 = [] if col_restrictions.get(keys[0])[-1].get("primary key") is not None else None
        primary2 = [] if col_restrictions.get(keys[1])[-1].get("primary key") is not None else None

        for permutation in permutations:
            ok = True
            if cumple_restricciones(col_restrictions.get(keys[0])[-1], permutation[0]) and \
                    cumple_restricciones(col_restrictions.get(keys[1])[-1], permutation[1]):

                if unique1 is None and primary1 is None:
                    pass
                elif unique1 is not None and permutation[0] not in unique1:
                    unique1.append(permutation[0])
                elif primary1 is not None and permutation[0] not in primary1:
                    primary1.append(permutation[0])
                else:
                    ok = False

                if unique2 is None and primary2 is None:
                    pass
                elif unique2 is not None and permutation[1] not in unique2:
                    unique2.append(permutation[1])
                elif primary2 is not None and permutation[1] not in primary2:
                    primary2.append(permutation[1])
                else:
                    ok = False

                if ok:
                    col_data.get(keys[0]).append(permutation[0])
                    col_data.get(keys[1]).append(permutation[1])
            ok = True
    elif len(where_data) > 0:
        col_data.update({col_select[0]: where_data.get(col_select[0])})

    # Generación del resto de datos
    times = constantes.NUM_FILAS
    if sentencia_where is not None:
        times = min(len(col_data.get(keys[0])), len(col_data.get(keys[1]))) if len(keys) == 2 else len(col_data.get(keys[0]))
    for dato in col_data:
        if not col_data.get(dato):
            check = next((col for col in columnas if col['name'] == dato), None)
            col_data.update({dato: generar_datos(dato, col_restrictions.get(dato), check, times)})

    return col_data, col_restrictions
