###Ideas
- Por una parte, hacer funciones que devuelvan las restricciones tanto del create 
table como del select en variables a la función poblador_tablas.
- Luego llamar a la función generadora del tipo de dato pasándole las restricciones
como parámetros.

###A medias
Refactorizar: 
- Función clasificar tipo: que devuelva variables con restricciones, así luego
se pueden mezclar con las restricciones del select. Antes llamabas a una función y 
te devolvía directamente el dato generado después de muchas llamadas sucesivas a 
otras funciones. Ahora queremos que se haga en dos partes: la función llama primero 
una función que devuelva las restricciones y luego llamar a otra que dadas una lista de
restricciones genere un dato aleatorio. La lista de condiciones tendrá siempre en la última
posición un diccionario con los valores min, max, eq, neq y la escala, en el caso de números.
- Fusionar las funciones generate_<data_type> con función option_restrictions si 
esta última es específica para el tipo de dato que se va a generar

###Por hacer
- check nombre like '...' (genchar())  --> Hecho con caracteres aleatorios y Faker mezclado
- Meter Excepciones
- Fechas con to_date() y sin restricciones de momento. Devolver un TO_DATE('2012-006-05', 'YYYY-MM-DD')
- SELECT ... FROM tabla
- Unit test
- Probar tablas muy sencillas
- Refactorizar código:
  - Añadir clases
  - No repetir tanto código
  - Acortar If, else sencillos
  - Función generar_tablas
- Constraint

###Cambios
- Eliminar campo option. Se ha actualizado la versión de mo-sql-parsing y ya
no clasifica las restricciones dentro de un campo option.

###Preguntas
- Create table y select. ¿Mezclamos las restricciones?

