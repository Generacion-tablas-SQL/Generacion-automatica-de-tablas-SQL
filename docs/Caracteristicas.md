# Limitaciones del proyecto

A continuación, se realizará una descripción de las limitaciones existentes en nuestro proyecto diferenciadas en los 
distintos ámbitos de implementación.
Muchas de estas limitaciones se pueden considerar para un trabajo futuro posterior a la finalización del proyecto.

### Restricciones de columna:
- No implementado: orden alfabético (col > 'test')

### Generadores de datos:

- Se consideran los datos tipo **FLOAT**, **BINARY_FLOAT**, **BINARY_DOUBLE** y **REAL** como números decimales de 
coma fija con precisión 10 y escala 4.
- Los datos tipo **NUMBER** tendrán una precision y una escala de máximo 16, ya que float no soporta tantos dígitos sin 
cambiar su formato.
- No se realiza la implementación del tipo de datos en coma (o punto) flotante de doble precisión (**DOUBLE PRECISION**), 
ya que la librería de parsing utilizada, mo-sql-parsing, no soporta este tipo de datos.
- No se realiza la implementación de los tipos de datos de más de una palabra (por ejemplo, **TIMESTAMP WITH TIME ZONE**),
ya que la librería de parsing utilizada, mo-sql-parsing, no lo soporta.
- Se supone que los datos de tipo cadena de caracteres solo se podrá especificar el tamaño en número de caracteres y no
por tamaño en bytes debido a que mo-sql-parsing no lo soporta.
- De cara a la generación de los datos de tipo FECHA (DATE, TIMESTAMP), no se realiza la implementación de las restricciones de tipo CHECK.


- Comparaciones de strings: 
  - Función LENGTH
  - Restricción LIKE
    - No tiene en cuenta el parámetro ESCAPE


### Limitaciones parseador:

- El formateador de mo-sql-parsing no está tan desarrollado como el parseador por lo tanto, nos encontramos
con más errores. Cuando intentamos formatear una sentencia previamente parseada nos salta una excepción:
Exception: Operators should have only one key!
Esto nos impide tener un método de backup que genere datos aleatorios hasta que cumpla con la sentencia nuevamente 
formateada.

### Sentencias SELECT con WHERE:

- Se comprueba si el dato de la condición en el WHERE cumple con las restricciones de la columna
  - Si cumple con las restricciones de la columna devuelve una tupla con un valor booleano a True y el valor de la
condición.
  - Si no cumple con las restricciones de desigualdad, se adapta para que las cumpla devolviendo una tupla con un
valor booleano a True y el nuevo valor que se ajusta a los mínimos o máximos de la columnas.
  - Si no cumple alguna otra restricción, devuelve una tupla con un valor booleano a False y el valor de la condición.
  
- En las sentencias SELECT, si hay una restricción WHERE con LIKE, el literal debe contener al menos un caracter 
diferente a "_" o "%".