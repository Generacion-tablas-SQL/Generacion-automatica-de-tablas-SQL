from mo_sql_parsing import parse, normal_op
import clasificador as c
import constantes as cts

def poblador_tablas(sentencias_create, sentencia_select):
    """Dada una o varias tablas y una o varias sentencias select, ...

    :param sentencias_create: conjunto de sentencias create table
    :param sentencia_select: una sentencia select
    :return:
    """

    tablas_restricciones = {}  # Variable para almacenar en un diccionario las restricciones de cada tabla
    tablas_datos = {}  # Variable para almacenar en un diccionario los datos generados en cada columna de cada tabla

    # Parsear las sentencias CREATE TABLE
    tablas = sentencias_create.split(";")
    for tabla in tablas:
        tabla.strip()
        if tabla == "":
            tablas.remove(tabla)
    tablas_parsed = [parse(x, calls=normal_op) for x in tablas]

    # Parsear la sentencia SELECT
    select_parsed = parse(sentencia_select, calls=normal_op)  # Parsea la consulta select

    # Seleccionar las tablas que aparecen en la sentencia SELECT para luego iterar sobre ellas
    # Así evitamos analizar las tablas con las que no vamos a trabajar
    # tablas_select = list()
    _from = select_parsed.get("from")
    if not isinstance(_from, list):
        _from = [_from]
    # if len(_from) > 1:
    #     tablas_select = [x.get("join").lower() for x in _from[1:]]
    # tablas_select.insert(0, _from[0].lower())

    name_tablas = [tablas_parsed[x].get("create table").get("name").lower() for x in range(0, len(tablas_parsed))]

    # Analizar los joins
    joins = dict()
    if len(_from) > 1:
        num_elems = 2
        for join in _from[1:]:
            key = tuple([name_tablas[x] for x in range(0, num_elems)])
            joins.update({key: [join.get("on").get("op"), join.get("on")
                         .get("args")[0], join.get("on").get("args")[1]]})
            num_elems += 1

    for tabla_s in name_tablas:
        tablas_restricciones.update({tabla_s: {}})
        tablas_datos.update({tabla_s: {}})

        # Buscar las tabla en tablas_parsed cuyos nombres coincidan con tabla_s.
        # Así no iteramos sobre tablas no necesarias
        col_tablas = dict()
        for tabla_p in tablas_parsed:
            col_tablas = tabla_p.get("create table")
            if col_tablas.get("name").lower() == tabla_s:
                col_tablas.update({'name': tabla_s})  # Nos aseguramos de que se quede en minúsculas
                break

        if len(col_tablas) == 0:
            raise Exception("La tabla no existe")

        # datos: Diccionario con un array de datos generados aleatoriamente asociado a cada columna
        # restricciones: Diccionario con un array de restricciones asociado a cada columna
        datos, restricciones = c.clasificar_tipo(tabla_s, col_tablas.get("columns"), tablas_datos, joins, select_parsed.get("where"))

        tablas_restricciones.get(tabla_s).update(restricciones)
        tablas_datos.get(tabla_s).update(datos)

    insert_list = list()
    value_list = list()

    for tabla_s in name_tablas:
        num_filas = 500
        for data in tablas_datos.get(tabla_s).values():
            num_filas = min(num_filas, len(data))

        for i in range(0, num_filas):
            for data in tablas_datos.get(tabla_s).values():
                if len(data) > i:
                    value_list.append(data[i])
                else:
                    break
            if len(value_list) != 0:
                values = tuple(value_list)
                insert_list.append("INSERT INTO " + tabla_s + " VALUES " + str(values) + ";")
                value_list.clear()

    return insert_list


def set_null_probability(null_probability: int):
    if 0 <= null_probability <= 1:
        cts.NULL_PROBABILITY = null_probability
    else:
        raise Exception('Probabilidad fuera de rango. El valor debe estar entre 0 y 1')
