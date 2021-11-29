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
    if "check" in column:
        restricciones_list.append(comprobar_restricciones_check_num(parameters, column.get("check")))
    else:
        restricciones_list.append({"scale": parameters[1]})
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

    _max = gd.max_number(parameters[0], parameters[1])
    _min = -_max
    _eq = None
    _neq = None
    _not = None

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

    return {"min": _min, "max": _max, "eq": _eq, "neq": _neq, "scale": parameters[1]}


# <----ENTEROS---->

# <----DECIMALES---->

# <----CADENAS DE CARACTERES---->

# <----FECHAS---->


def clasificar_tipo1(sentencias):
    """Detecta el tipo de datos y delega la generación del tipo de dato detectado.

    :param sentencias:
    :return:
    """

    # tablas = {tabla1: [col1: {tipo: int, restricciones: [{min:0, max:10, 'primary key': true, neq: 5}]},
    #                    col2: {tipo: varchar, restricciones: [{min: 5, max:10, like: '___-_%'}]}]}
    tablas = {}

    # columnas_tabla = {[{nombre: "", tipo:  "", restricciones: []}]}

    # nombre_tablas = []
    # columnas_tabla = []
    sentencias_list = sentencias.split(';')
    for sentencia in sentencias_list:
        print(sentencia)
        sentencia_d = parse(sentencia)
        nombre_tabla = sentencia_d.get("create table").get("name")
        tablas.update({nombre_tabla: []})
        for column in sentencia_d.get("create table").get("columns"):
            nombre_col = column.get("name")
            data_type = list(column.get("type").keys())[0].lower()  # number
            parameters = list(column.get("type").values())  # [[5, 0]]
            if data_type in constantes.ENTEROS:
                data_type_param = []
                data_type_param.append(38) if parameters[0] == {} else data_type_param.append(parameters[0])
                data_type_param.append(0)
                restricciones = restricciones_sql(data_type_param, column)
                print(gd.generate_number1(restricciones))
                print(restricciones)
                # col_dict = {}
                # col_dict.update({nombre_col: comprobar_restricciones_ent(parameters, column)})
            elif data_type in constantes.REALES:
                # print(gd.generate_real(data_type, parameters, column))
                # es_float, _min, _max, _neq, scale = generate_real(key, parameters, column, constraint)
                # print(generate_number(es_float, _min, _max, _neq, scale))
                pass
            elif data_type in constantes.STRINGS:
                # print(gd.string_restrictions(data_type, parameters, column))
                pass
            elif data_type in constantes.FECHA:
                # print(gd.generate_fecha(data_type, parameters, column))
                pass
            else:
                print("Ha habido un error en la clasificación de tipo de datos.")


create_table = "CREATE TABLE Persona (ent INT(4) UNIQUE NULL CHECK (NOT enT <= 0 AND ENT < 20 AND ent != 10)," \
               "string VARCHAR(15) UNIQUE NULL CHECK (string LIKE 'C%' and LENGTH(string) > 5 and LENGTH(string) < 10));"

clasificar_tipo1(create_table)
