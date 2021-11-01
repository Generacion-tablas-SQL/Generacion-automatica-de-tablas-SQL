# Tipos de datos soportados por Oracle

### Tipos de datos numéricos
####Built-in
- NUMBER [(p [,s])] → default s = 0. Si no se especifica ni _p_ ni _s_,
se almacena el valor tal y como se da. Rango de _p_: 1 a 38.
Rango de _s_: -84 a 127
- FLOAT [(p)] → Default p = 53. Precisión en bits. Rango de _p_: 1 a 126

####Ansi supported
- NUMERIC [(p [,s])] ≡ NUMBER [(p [,s])]
- DECIMAL [(p [,s])] ≡ NUMBER [(p [,s])]
- DEC [(p [,s])] ≡ NUMBER [(p [,s])]
- INTEGER ≡ NUMBER(38)
- INT ≡ NUMBER(38)
- SMALLINT ≡ NUMBER(38)
- FLOAT ≡ FLOAT(126)
- DOBLE PRECISION ≡ FLOAT(126)
- REAL ≡ FLOAT(63)

### Tipos de datos de caracteres

####Built-in
- CHAR[(size [BYTE | CHAR])] 
- VARCHAR2(size [BYTE | CHAR]) 
- NCHAR[(size)]
- NVARCHAR2(size)
- LONG

####Ansi supported
  - CHARACTER(size) ≡ CHAR(size)
  - CHARACTER VARYING(size) ≡ VARCHAR2(size)
  - CHAR VARYING(size) ≡ VARCHAR2(size)
  - NATIONAL CHARACTER(size) ≡ NCHAR(size)
  - NATIONAL CHAR(size) ≡ NCHAR(size)
  - NATIONAL CHARACTER VARYING(size) ≡ NVARCHAR2(size)
  - NATIONAL CHAR VARYING ≡ NVARCHAR2(size)
  - NCHAR VARYING(size) ≡ NVARCHAR2(size)

### Tipos de datos de fecha

- DATE 
- TIMESTAMP [(fractional_seconds_precision)]
- TIMESTAMP [(fractional_seconds_precision)] WITH TIME ZONE
- TIMESTAMP WITH LOCAL TIME ZONE
- INTERVAL YEAR [(year_precision)] TO MONTH
- INTERVAL [(day_precision)] DAY TO SECOND

[https://docs.oracle.com/cd/B19306_01/server.102/b14200/sql_elements001.htm](https://docs.oracle.com/cd/B19306_01/server.102/b14200/sql_elements001.htm)

[https://www.oracletutorial.com/oracle-basics/oracle-data-types/ ](https://www.oracletutorial.com/oracle-basics/oracle-data-types/)