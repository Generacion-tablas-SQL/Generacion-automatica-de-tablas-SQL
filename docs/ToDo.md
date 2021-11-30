###Ideas

###Por hacer
- Unit test
- Constraint
- Errores:
  - Los parámetros [38, 127] de NUMBER dan error en generate_number por la clase Decimal
  - Los decimales devuelven números en este formato "Decimal(14.32)", solo queremos el número.
- Restricciones WHERE en sentencias SELECT

###A medias
- eval en clasificador
- excepciones

###Hecho
Refactorización: 
- Función clasificar tipo: que devuelva variables con restricciones, así luego
se pueden mezclar con las restricciones del select. Antes llamabas a una función y 
te devolvía directamente el dato generado después de muchas llamadas sucesivas a 
otras funciones. Ahora queremos que se haga en dos partes: la función llama primero 
una función que devuelva las restricciones y luego llamar a otra que dadas una lista de
restricciones genere un dato aleatorio. La lista de condiciones tendrá siempre en la última
posición un diccionario con los valores min, max, eq, neq y la escala, en el caso de números.

Dada una sentencia select sencilla, devolver los datos de la tabla. SELECT ... FROM tabla

Check nombre LIKE '...' ⇾ con caracteres aleatorios y Faker mezclado

Fechas con to_date() y sin restricciones de momento. Devolver un TO_DATE('2012-006-05', 'YYYY-MM-DD')

###Cambios
- Se ha actualizado la versión de mo-sql-parsing y ya
no clasifica las restricciones dentro de un campo option.

###Preguntas
- Excepciones: ValueError devuelve todo el stack. Quiero que se siga ejecutando
