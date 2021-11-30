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
- check nombre like '...' (genchar())  --> HECHO con caracteres aleatorios y Faker mezclado
- Meter Excepciones
- Fechas con to_date() y sin restricciones de momento. Devolver un TO_DATE('2012-006-05', 'YYYY-MM-DD')
- SELECT ... FROM tabla ⇾ HECHO
- Unit test
- Refactorizar código:
  - Añadir clases ⇾ HECHO
  - No repetir tanto código ⇾ HECHO
  - Acortar If, else sencillos ⇾ HECHO
  - Función generar_tablas ⇾ HECHO sencillo
- Constraint
- Errores:
  -  Los parámetros [38, 127] de NUMBER dan error en generate_number por la clase Decimal
- eval en clasificador

###Cambios
- Se ha actualizado la versión de mo-sql-parsing y ya
no clasifica las restricciones dentro de un campo option.

###Preguntas

