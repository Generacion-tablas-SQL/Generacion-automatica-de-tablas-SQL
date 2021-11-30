import clasificador as c
from mo_sql_parsing import parse


create_table = "CREATE TABLE Persona (real NUMBER(4,2) UNIQUE NULL CHECK (NOT REal <= 0 AND REAL < 20 AND real != 10)," \
               "string VARCHAR(15) UNIQUE NULL CHECK (string LIKE 'C%' and LENGTH(string) > 5 and LENGTH(string) < 10));"
select = "SELECT real FROM Persona"

def poblador_tablas(sentencias_create, sentencias_select):
    # tablas = {tabla1: [{col1: ["nullable", "unique", {min:0, max:10, eq: None, neq: 5, scale: 0, tipo: int}]},
    #                    {col2: ["primary key", {min: 5, max:10, eq: None, neq: None, like: '___-_%', tipo: varchar}]}]}
    tablas = {}

    create = sentencias_create.split(";")
    # select = sentencias_select.split(";")
    for sentencia in create:
        sentencia_p = parse(sentencia)
        nombre_tabla = sentencia_p.get("create table").get("name")
        tablas.update({nombre_tabla: []})

        datos, restricciones = c.clasificar_tipo1(sentencia_p.get("create table").get("columns"))

        tablas.get(nombre_tabla).append(restricciones)

        print(datos)


poblador_tablas(create_table, select)