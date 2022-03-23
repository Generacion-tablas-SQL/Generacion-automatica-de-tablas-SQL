from mo_sql_parsing import parse, normal_op
import clasificador as c
from constantes import NUM_FILAS


# def get_columnas(sentencia_parsed):
#     nombre_cols = list()
#     cols = sentencia_parsed.get("select")
#     if not isinstance(cols, list):
#         cols = [cols]
#     for col in cols:
#         nombre_cols.append(col.get("value").lower())
#
#     return nombre_cols


def poblador_tablas(sentencias_create, sentencia_select):
    """Dada una o varias tablas y una o varias sentencias select, ...

    :param sentencias_create: conjunto de sentencias create table
    :param sentencia_select: una sentencia select
    :return:
    """
    # tablas_restricciones = {tabla1: [
    #                    {col1: ["nullable", "unique", {min:0, max:10, eq: None, neq: 5, scale: 0, tipo: int}]},
    #                    {col2: ["primary key", {min: 5, max:10, eq: None, neq: None, like: '___-_%', tipo: varchar}]}
    #                    ]}
    tablas_restricciones = {}
    tablas_datos = {}
    tablas = sentencias_create.split(";")

    select_parsed = parse(sentencia_select, calls=normal_op)  # Parsea la consulta select
    where_restr = select_parsed.get("where")

    for tabla in tablas:
        tabla_parsed = parse(tabla, calls=normal_op)
        nombre_tabla = tabla_parsed.get("create table").get("name").lower()

        tablas_restricciones.update({nombre_tabla: {}})
        tablas_datos.update({nombre_tabla: {}})

        # datos: diccionario con un array de datos generados aleatoriamente asociado a cada columna
        # restricciones: diccionario con un array de restricciones asociado a cada columna
        datos, restricciones = c.clasificar_tipo(tabla_parsed.get("create table").get("columns"), where_restr)

        tablas_restricciones.get(nombre_tabla).update(restricciones)
        tablas_datos.get(nombre_tabla).update(datos)

    # nombre_cols = get_columnas(select_parsed)  # Agrega a una lista todas las columnas de la consulta
    nombre_tabla = select_parsed.get("from").lower()  # Identifica la tabla consultada

    value_list = list()
    insert_list = list()

    for i in range(0, NUM_FILAS):
        for data in tablas_datos.get(nombre_tabla).values():
            if len(data) > i:
                value_list.append(data[i])
            else:
                break
        if len(value_list) != 0:
            values = tuple(value_list)
            insert_list.append("INSERT INTO " + nombre_tabla + " VALUES " + str(values))
            value_list.clear()

    return insert_list
