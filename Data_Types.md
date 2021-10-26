# Tipos de datos soportados por Oracle

### Tipos de datos numéricos
####Built-in
- NUMBER [(p [,s])]
- NUMBER (p,s)
- NUMBER (p, 0)
- FLOAT [(p)]
- LONG

####Ansi supported
- NUMERIC [(p [,s])]
- DECIMAL [(p [,s])]
- DEC [(p [,s])]
- INTEGER
- INT
- SMALLINT
- FLOAT [(p)]
- DOBLE PRECISION
- REAL

### Tipos de datos de caracteres

####Built-in
- CHAR [(size [BYTE | CHAR])] 
- VARCHAR2(size [BYTE | CHAR]) 
- NCHAR[(size)]
- NVARCHAR2(size)
- 
####Ansi supported
- CHARACTER [VARYING] (size)
- CHAR VARYING (size)
- NCHAR VARYING (size)
- VARCHAR (size)
- NATIONAL CHARACTER [VARYING] (size)
- NATIONAL CHAR [VARYING] (size)

### Tipos de datos de fecha

- DATE 
- TIMESTAMP [(fractional_seconds_precision)]
- TIMESTAMP [(fractional_seconds_precision)] WITH TIME ZONE
- TIMESTAMP WITH LOCAL TIME ZONE
- INTERVAL YEAR [(year_precision)] TO MONTH
- INTERVAL [(day_precision)] DAY TO SECOND

[https://docs.oracle.com/cd/B19306_01/server.102/b14200/sql_elements001.htm](https://docs.oracle.com/cd/B19306_01/server.102/b14200/sql_elements001.htm)