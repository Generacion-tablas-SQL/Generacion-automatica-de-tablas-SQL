NULL_PROBABILITY = 0.1
ENTEROS = ["int", "integer", "smallint"]  # NUMBER(p) y NUMBER(p, 0) son enteros
COMPARADORES = ["eq", "neq", "gt", "gte", "lt", "lte"]
REALES = ["number", "float", "numeric", "decimal", "dec", "real"]  # double precision no soportado por mo-sql-parsing
STRINGS = ["char", "character", "varchar", "varchar2", "nchar", "nvarchar", "nvarchar2", "long"]
FECHA = ["date", "timestamp"]  # Los tipos de datos de más de una palabra no son soportados por mo-sql-parsing

