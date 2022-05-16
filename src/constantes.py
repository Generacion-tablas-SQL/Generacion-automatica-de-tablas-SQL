NULL_PROBABILITY = 0.2
NUM_FILAS = 10
UNIQUE_TRIES = 20

# Los tipos de datos de más de una palabra no son soportados por mo-sql-parsing
ENTEROS = ["int", "integer", "smallint"]  # NUMBER(p) y NUMBER(p,0) son enteros
COMPARADORES = ["eq", "neq", "gt", "gte", "lt", "lte"]
REALES = ["number", "float", "binary_float", "binary_double", "numeric", "decimal", "dec", "real"]
COMA_FLOTANTE = ["float", "binary_float", "binary_double", "real"]
STRINGS = ["char", "character", "varchar", "varchar2", "nchar", "nvarchar", "nvarchar2", "long"]
FECHA = ["date", "timestamp"]

