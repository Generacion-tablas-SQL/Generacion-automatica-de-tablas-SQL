# Tipos de datos y Generadores
## Generación automática de tablas para probar consultas SQL
Dada una estructura de base de datos SQL y una consulta, generar filas de datos que rellenen las columnas
de forma que haya filas que encajen con la consulta y filas que no lo hagan.

Para llegar a conseguir la finalidad deseada, se ha dividido el proyecto en varias fases:
### Primera fase:
- Fase de investigación: consultar los tipos de datos soportados por Oracle.

### Segunda fase:
- Implementación de funciones generadoras de datos aleatorios. Uno para cada tipo de datos
  - Se tienen en cuenta las posibles restricciones, tanto del propio tipo de dato como las restricciones
  CHECK.   
  
### Tercera fase:
- Implementación de una función generadora de tablas que dada una o varias sentencias CREATE TABLE y 
una consulta, devuelva uno o varios strings de sentencias INSERT.
  - Empezamos por una consulta muy sencilla como "SELECT <columna> FROM <tabla>". 
