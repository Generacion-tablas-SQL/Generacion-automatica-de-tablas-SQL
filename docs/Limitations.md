# Limitaciones del proyecto

A continuación, se realizará una descripción de las limitaciones existentes en nuestro proyecto diferenciadas en los 
distintos ámbitos de implementación.
Muchas de estas limitaciones se pueden considerar para un trabajo futuro posterior a la finalización del proyecto.


### Generadores de datos:

- Se consideran los datos tipo **FLOAT** y **REAL** como números decimales de punto fijo.
- No se realiza la implementación del tipo de datos en coma (o punto) flotante de doble precisión (**DOUBLE PRECISION**), 
ya que la librería de parsing utilizada, mo-sql-parsing, no soporta este tipo de datos.
- No se realiza la implementación de los tipos de datos de más de una palabra (por ejemplo, **TIMESTAMP WITH TIME ZONE**),
ya que la librería de parsing utilizada, mo-sql-parsing, no lo soporta.

