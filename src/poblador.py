import clasificador as c
import mo_parsing
from mo_sql_parsing import parse, normal_op
# import exceptionsDef


create_table = "CREATE TABLE Persona (" \
               "real NUMBER(4) UNIQUE NULL CHECK (NOT REal <= 0 AND REAL < 20 AND real != 10)," \
               "ent INT CHECK (ent > 12 and ent < 50)," \
               "string VARCHAR(15) UNIQUE NULL CHECK (string LIKE 'C%' and LENGTH(string) > 5 and LENGTH(string) < 10),"\
               "fec1 DATE UNIQUE NOT NULL, " \
               "fec2 TIMESTAMP(2) UNIQUE NOT NULL)"

select1 = "SELECT ent FROM Persona"  # WHERE ENT = 15
select2 = "SELECT ent, real FROM Persona"

def get_columnas(sentencia_parsed):
    nombre_cols = list()
    cols = sentencia_parsed.get("select")
    for col in cols:
        nombre_cols.append(col.get("value").lower())

    return nombre_cols


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

    try:
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

        sentencia_p = parse(sentencia_select)  # Parsea la consulta select
        nombre_cols = get_columnas(sentencia_p)  # Agrega a una lista todas las columnas de la consulta

        nombre_tabla = sentencia_p.get("from").lower()  # Identifica la tabla consultada

        for col in nombre_cols:
            print(col, ": ", tablas_datos.get(nombre_tabla).get(col), sep="")

        print(tablas_datos)
        print(tablas_restricciones)

    except IndentationError as err:
        print("Error, indexación incorrecta:\n", err)

    except mo_parsing.exceptions.ParseException as err:
        print("Error en el parse:\n", err)

    except AttributeError as err:
        print("Error, referencia al valor de atributo incorrecta:\n", err)

    except KeyError as err:
        print("Error en el acceso a diccionario, la clave no está definida:\n", err)

    except TypeError as err:
        print("Error, dato de tipo inapropiado:\n", err)

    except IndexError as err:
        print("Error, el índice no existe:\n", err)

    except NameError as err:
        print("Error, el nombre local o global no esta definido:\n", err)

    finally:
        pass
        #print("Fin de la ejecución.\n")


poblador_tablas(create_table, select2)
