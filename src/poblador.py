import clasificador as c
from mo_sql_parsing import parse, normal_op


create_table = "CREATE TABLE Persona (" \
               "real NUMBER(4) UNIQUE NULL CHECK (NOT REal <= 0 AND REAL < 20 AND real != 10)," \
               "ent INT CHECK (ent > 12 and ent < 50)," \
              "string VARCHAR(15) UNIQUE NULL CHECK (string LIKE 'C%' and LENGTH(string) > 5 and LENGTH(string) < 10),"\
               " fec1 DATE UNIQUE NOT NULL, " \
               "fec2 TIMESTAMP(7) UNIQUE NOT NULL)"

select = "SELECT ent FROM Persona"


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
    create_s = sentencias_create.split(";")

    for sentencia in create_s:
        sentencia_p = parse(sentencia, calls=normal_op)
        nombre_tabla = sentencia_p.get("create table").get("name").lower()
        tablas_restricciones.update({nombre_tabla: {}})
        tablas_datos.update({nombre_tabla: {}})

        # datos: diccionario con un array de datos generados aleatoriamente asociado a cada columna
        # restricciones: diccionario con un array de restricciones asociado a cada columna
        datos, restricciones = c.clasificar_tipo(sentencia_p.get("create table").get("columns"))

        tablas_restricciones.get(nombre_tabla).update(restricciones)
        tablas_datos.get(nombre_tabla).update(datos)

    sentencia_p = parse(sentencia_select)
    nombre_col = sentencia_p.get("select").get("value").lower()
    nombre_tabla = sentencia_p.get("from").lower()
    print(tablas_datos.get(nombre_tabla).get(nombre_col))

    print(tablas_datos)
    print(tablas_restricciones)


poblador_tablas(create_table, select)
