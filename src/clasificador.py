from time import mktime, strptime, strftime, localtime
import random
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
    return 1 if _not is None and isinstance(comparison.get("args")[1], int) else (
        1 if _not is not None and isinstance(comparison.get("args")[0].get("args")[1], int) else 0)


# <----RESTRICCIONES WHERE---->
def cumple_restricciones(restricciones, data):
    if restricciones.get("eq") is not None and restricciones.get("eq") != data:
        return False
    if restricciones.get("neq") is not None and restricciones.get("neq") == data:
        return False

    # No tenemos en cuenta el tipo Fecha ya que no tiene implementadas restricciones CHECK
    if restricciones.get("tipo") == "Number":
        if data < restricciones.get("min") or data > restricciones.get("max"):
            return False
    elif restricciones.get("tipo") == "String":
        if (data.find("%") == 0 and len(data) < restricciones.get("min")) or len(data) > restricciones.get("max"):
            return False
        if restricciones.get("like") is not None:
            like_regex = restricciones.get("like").replace("%", "[a-zA-Z ]*").replace("_", "[a-zA-Z ]")
            data_regex = data.replace("%", "[a-zA-Z ]*").replace("_", "[a-zA-Z ]")
            if not re.match(like_regex, data_regex):
                return False
    return True

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

    if _eq is not None and (_eq < _min or _eq > _max):
        raise Exception("Restricciones de la columna no satisfactibles")

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


# <----RESTRICCIONES WHERE---->
def restricciones_where(restricciones_col, sentencia_where):
    """Comprueba las restricciones where y modifica la lista de restricciones de forma que se puedan generar los
    datos consultados así como datos no consultados

    :param restricciones_col: lista con restricciones de la columna consultada
    :param sentencia_where:
    :return: lista con datos generados
    """

    op = sentencia_where.get("op")
    args = sentencia_where.get("args")

    #Para saber si existe una op length
    s = str(args[0])
    lenEx = s.find("length")


    arg_data = args[1] if isinstance(args[0], str) else (
        args[0] if isinstance(args[1], str) else (
            args[1] if isinstance(args[0], dict) else args[0]  # para WHERE con función LENGTH()
        )
    )

    # arg_data = args[1] if isinstance(args[0], str) else args[0]
    if isinstance(arg_data, dict):  # Para igualdades o desigualdades de cadenas o LIKE
        arg_data = arg_data.get("literal")

    gen_data = list()

    ops = ["eq", "gt", "gte", "lt", "lte", "like", "length"]
    if op in ops:
        if cumple_restricciones(restricciones_col, arg_data):
            if restricciones_col.get("tipo") == "Number":
                scale = restricciones_col.get("scale")
                for i in [-1 / 10 ** scale, 0, 1 / 10 ** scale]:
                    gen_data.append(arg_data + i)
            elif restricciones_col.get("tipo") == "String":
                if op == "like":
                    restricciones_col.update({"like": arg_data})
                    gen_data.append(gd.generate_string(restricciones_col))
                if (lenEx != -1): #Existe el campo length
                    pass #FALTA

                #Operaciones con operadores
                b = len(arg_data) - 1
                gen_data.append(arg_data[:b])  # Quito el último caracter
                gen_data.append(arg_data)
                gen_data.append(arg_data + random.choice('abcdefghijklmnopqrstuvwxyz'))  # Añado un caracter

                #Añadir siguiente caracter ascii al último caracter
                cadena = arg_data
                b = len(cadena) - 1 #Cojo el ultimo caracter de la cadena
                ultima = cadena[b:]
                char = chr(ord(ultima) + 1) #Le sumo un caracter ascii
                b = len(cadena) - 1 #Quito el ultimo caracter de la cadena
                cadena = cadena[:b]
                cadena = cadena + char
                gen_data.append(cadena)
            else:  # tipo == "Fecha"
                fecha = mktime(strptime(arg_data, "%d/%m/%Y"))
                gen_data.append(strftime("%d/%m/%Y", localtime(fecha - 1)))
                gen_data.append(strftime("%d/%m/%Y", localtime(fecha)))
                # Los días UTC tienen una duración de 86 400 s
                gen_data.append(strftime("%d/%m/%Y", localtime(fecha + 86400)))

    return gen_data


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

    for column in columnas:
        col_name = column.get("name").lower()
        data_type = column.get("type").get("op").lower()  # number
        parameters = column.get("type").get("args", None)  # [5, 0], [4]

        args = sentencia_where.get("args")
        col_select = args[0].lower() if isinstance(args[0], str) else (
            args[1].lower() if isinstance(args[1], str) else (
                args[0].get("args")[0] if isinstance(args[0], dict) else args[1].get("args")[0]
            )
        )

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
            if col_name == col_select:
                data.extend(restricciones_where(restricciones[-1], sentencia_where))

            if restricciones[-1].get("other"):
                for i in range(len(data), 10):
                    data.append(gd.generate_random(data_type_param[0], data_type_param[1], restricciones[-1],
                                                   column.get("check")))
            else:
                a = len(data)
                for i in range(a, 10):
                    gen_num, unique, primary = gd.generate_number(restricciones[-1])
                    data.append(gen_num)
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
            if col_name == col_select:
                data.extend(restricciones_where(restricciones[-1], sentencia_where))

            if restricciones[-1].get("other"):
                for i in range(len(data), 10):
                    data.append(gd.generate_random(data_type_param[0], data_type_param[1], restricciones[-1],
                                                   column.get("check")))
            else:
                for i in range(len(data), 10):
                    data.append(gd.generate_string(restricciones[-1]))
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

            if col_name == col_select:
                data.extend(restricciones_where(restricciones[-1], sentencia_where))

            for i in range(len(data), 10):
                # restricciones[0] = sec_precision, restricciones[1]= es_date, restricciones[2] = data_type
                data.append(gd.gen_fecha(restricciones[-1]))
            col_data.update({col_name: data})
        else:
            raise ValueError
    return col_data, col_restrictions
