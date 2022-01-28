# Limitaciones del proyecto

A continuación, se realizará una descripción de las limitaciones existentes en nuestro proyecto diferenciadas en los 
distintos ámbitos de implementación.
Muchas de estas limitaciones se pueden considerar para un trabajo futuro posterior a la finalización del proyecto.


### Generadores de datos:

- Se consideran los datos tipo **FLOAT** y **REAL** como números decimales de punto fijo con precisión 10 y escala 4.
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
  - Función LEN
  - Restricción LIKE
    - No tiene en cuenta el parámetro ESCAPE

