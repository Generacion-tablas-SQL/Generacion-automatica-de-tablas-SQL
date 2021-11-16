###Preguntas
- Create table y select. ¿Mezclamos las restricciones?
- Formato fechas
- En strings: LIKE, AS, TRIM() es solo en las sentencias select?

###Cambios
- Eliminar campo option. Se ha actualizado la versión de mo-sql-parsing y ya
no clasifica las restricciones dentro de un campo option.

###Ideas
- Por una parte, hacer funciones que devuelvan las restricciones tanto del create 
table como del select en variables a la función poblador_tablas.
- Luego llamar a la función generadora del tipo de dato pasándole las restricciones
como parámetros.

###A medias
Refactorizar: 
- Función clasificar tipo: que devuelva variables con restricciones, así luego
se pueden mezclar con las restricciones del select.
- Fusionar las funciones generate_<data_type> con función option_restrictions si 
esta última es específica para el tipo de dato que se va a generar

###Por hacer
- Refactorizar código:
  - Añadir clases
  - No repetir tanto código
  - Acortar If, else sencillos
  - Función generar_tablas
- Constraint