from mo_sql_parsing import parse
import constantes
import generador_datos as gd

# <----GENERAL---->
def restricciones_sql(parameters, column):
    """Comprueba las restricciones SQL.

    :param parameters: parámetros del tipo de dato.
    :param column: restricciones de la columna.
    :return: lista con las restricciones. El último elemento de la lista es un diccionario con las restricciones check.
    """

    restricciones_list = []
    check = column.get("check") if "check" in column else {}
    if ("nullable" in column and column.get("nullable")) or "nullable" not in column:  # No afecta
        restricciones_list.append("nullable")
    if "unique" in column:  # De momento no afecta
        restricciones_list.append("unique")
    if "primary key" in column:  # De momento no afecta
        restricciones_list.append("primary key")
    if "foreign key" in column:  # De momento no afecta
        restricciones_list.append("foreign key")
    if "default" in column:  # De momento no afecta
        restricciones_list.append({"default", column.get("default").get("literal")})

    restricciones_list.append({})
    if parameters[0] == "Number":
        restricciones_list[-1].update(comprobar_restricciones_check_num(parameters, check))
    elif parameters[0] == "String":
        # restricciones_list.append(comprobar_restricciones_check_str(parameters, check))
        pass
    else: # parameters[0] == "Fecha"
        # POR EL MOMENTO LAS FECHAS NO POSEEN RESTRICCIONES CHECK
        # restricciones_list.append(comprobar_restricciones_check_date(parameters, check))

        restricciones_list[-1].update({"sec_precision": parameters[1], "es_date": parameters[2]})
        pass


    return restricciones_list


def get_index(comparison, comparison_key, _not):
    return 1 if _not is None and isinstance(comparison.get(comparison_key)[1], int) else (
        1 if _not is not None and isinstance(comparison.get(comparison_key).get(_not)[1], int) else 0)


# <----NÚMEROS---->
def comprobar_restricciones_check_num(parameters, check):
    """Comprueba las restricciones CHECK

        :param parameters: precision(parameters[0]) y escala (parámetros[1])
        :param check: campo check de la sentencia parseada
        :return: diccionario con el número máximo, mínimo equal y not equal si se específica
        """

    _max = gd.max_number(parameters[1], parameters[2])
    _min = -_max
    _eq = None
    _neq = None
    _not = None

    if check == {}:
        return {"min": _min, "max": _max, "eq": _eq, "neq": _neq, "scale": parameters[1]}

    operator = list(check.keys())[0].lower()  # primer operador que aparece en el check

    # Crea una lista con la/las comparación/comparaciones
    if operator == "and" or operator == "or":
        comparisons = check.get(operator)
    else:
        comparisons = [check]

    for comparison in comparisons:

        comparison_key = list(comparison.keys())[0]
        if comparison_key == "not":
            _not = list(comparison.get("not").keys())[0]  # _not contiene: "lte", "gt"...

        if comparison_key == "eq":
            _eq = comparison.get("eq")[get_index(comparison, comparison_key, None)]
        elif comparison_key == "neq":
            _neq = comparison.get("neq")[get_index(comparison, comparison_key, None)]
        elif comparison_key == "gt" or _not == "gt":
            if _not == "gt":
                # mínimo entre _max y el contenido del comparador
                _max = min(_max, comparison.get("gt")[get_index(comparison, comparison_key, _not)] - 1)
            else:
                # máximo entre _min y el contenido del comparador
                _min = max(_min, comparison.get("gt")[get_index(comparison, comparison_key, None)] + 1)
        elif comparison_key == "gte" or _not == "gte":
            if _not == "gte":
                _max = min(_max, comparison.get("gte")[get_index(comparison, comparison_key, _not)])
            else:
                _min = max(_min, comparison.get("gte")[get_index(comparison, comparison_key, None)])
        elif comparison_key == "lt" or _not == "lt":
            if _not == "lt":
                _min = max(_min, comparison.get("not").get("lt")[get_index(comparison, comparison_key, _not)] + 1)
            else:
                _max = min(_max, comparison.get("lt")[get_index(comparison, comparison_key, None)] - 1)
        elif comparison_key == "lte" or _not == "lte":
            if _not == "lte":
                _min = max(_min, comparison.get("not").get("lte")[get_index(comparison, comparison_key, _not)] + 1)
            else:
                _max = min(_max, comparison.get("lte")[get_index(comparison, comparison_key, None)] - 1)
        _not = None

    return {"min": _min, "max": _max, "eq": _eq, "neq": _neq, "scale": parameters[1]}


# <----CADENAS DE CARACTERES---->

# <----FECHAS----> DE MOMENTO NO TIENEN RESTRICCIONES CHECK


# <----INICIO---->
def clasificar_tipo(columnas):
    """Detecta los tipo de datos de las columnas y delega la generación del tipo de dato detectado.

    :param columnas: columnas de una tabla
    :return: col_data: diccionario con los datos generados de cada columna
             col_restrictions: diccionario con las restricciones de cada columna.
    """

    col_data = {}
    col_restrictions = {}

    for column in columnas: #{'name': 'fec1', 'type': {'date': {}}, 'unique': True, 'nullable': False}
                            #{'name': 'fec2', 'type': {'timestamp': 2}, 'unique': True, 'nullable': True}

        col_name = column.get("name")
        data_type = list(column.get("type").keys())[0].lower()  # number
        parameters = list(column.get("type").values())  # [[5, 0]]

        if data_type in constantes.ENTEROS or data_type in constantes.REALES:
            data_type_param = []
            if data_type in constantes.ENTEROS:
                data_type_param.append(38) if parameters[0] == {} else data_type_param.append(parameters[0])
                data_type_param.append(0)
            else:
                data_type_param = [10, 4] if data_type == "float" or data_type == "real" else (
                    [38, 127] if parameters[0] == {} else (
                        [parameters[0], 0] if isinstance(parameters[0], int) else (
                            [parameters[0][0], parameters[0][1]]
                        )
                    )
                )
            data_type_param.insert(0, "Number")
            restricciones = restricciones_sql(data_type_param, column)
            restricciones[-1].update({"tipo": data_type})
            col_restrictions.update({col_name: restricciones})

            numbers = []
            for i in range(10):
                numbers.append(gd.generate_number(restricciones))
            col_data.update({col_name: numbers})

        elif data_type in constantes.STRINGS:
            # char y nchar tienen un tamaño por defecto de 1
            max_size = 1 if parameters[0] == {} else parameters[0]
            varying = False if data_type == "char" or data_type == "nchar" else True

            data_type_param = ["String", varying, max_size]
            restricciones = restricciones_sql(data_type_param, column)
            restricciones[-1].update({"tipo": data_type})
            col_restrictions.update({col_name: restricciones})

            data = []
            for i in range(10):
                # data.append(gd.generate_string(restricciones))
                pass
            col_data.update({col_name: data})
            # print(string_restrictions(key, parameters, column))

        elif data_type in constantes.FECHA:

            es_date = 1 if data_type[0] == "date" else 0
            sec_precision = 0 if parameters[0] == {} else parameters[0]

            data_type_param = ["Fecha", sec_precision, es_date]
            restricciones = restricciones_sql(data_type_param, column)
            restricciones[-1].update({"tipo": data_type})
            col_restrictions.update({col_name: restricciones})

            fechas = []
            for i in range(10):
                fechas.append(gd.gen_fecha(restricciones))   # restricciones[-1] = data_type , restricciones[0] = sec_precision ,restricciones[1]= es_date
            col_data.update({col_name: fechas})
        else:
            print("Ha habido un error en la clasificación de tipo de datos.")
    return col_data, col_restrictions

