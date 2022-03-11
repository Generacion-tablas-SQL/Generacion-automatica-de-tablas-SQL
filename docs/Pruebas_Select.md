## PRUEBAS SELECT
- Select sin where:

"SELECT ent FROM Persona". --> Genera 10 sentencias INSERT INTO

- Una restricción:

"SELECT ent FROM Persona where ent > 30". --> Genera 3 sentencias INSERT INTO, una con ent = 31,
otra ent = 30 y otra con ent = 29

"SELECT string FROM Persona WHERE real > 0" --> Genera 3 sentencias INSERT INTO con 0.01, 0 y 0.
--> REVISAR::::Generar 0.00 no 0.

"SELECT string FROM Persona WHERE real > 0.03" --> Genera 3 sentencias INSERT INTO con 0.03, 0.03
y 0.019999999999999997 --> REVISAR::::Problema en cumple_restricciones

"SELECT string FROM Persona WHERE string like '%'" --> REVISAR

"SELECT string FROM Persona WHERE string like 'Carmen'" --> Carmen, jarmen --> OK

"SELECT string FROM Persona WHERE LENGTH(string) > 7"  --> CNPopula (8), CArrive (7) y CSourc (6) --> OK

"SELECT string FROM Persona WHERE REAL = NULL" --> REVISAR::::restricciones_where en búsqueda de
nombre de arg_data y arg_col

"SELECT string FROM Persona WHERE fec1 = '01/02/2000'"  --> Genera mismo dia, dia anterior y dia
siguiente. --> OK

- Una restriccion que no cumple restriccion de columna:

"SELECT string FROM Persona WHERE ent > 50" (ent < 50 en columna) --> Genera 3 INSERT INTO con 
ent = 49 y 48 --> Si no tuviera restricción unique en la columna se generaría un 2º valor 49.

"SELECT string FROM Persona WHERE ent = 50" (ent < 50 en columna) --> Genera 2 INSERT INTO con 
ent = 49, 48. Si no tuviera restricción unique en la columna se generaría un 2º valor 49.

"SELECT string FROM Persona WHERE string like 'Car'" --> Genera 10 INSERT INTO. Al no cumplir
las restricciones de columna(LENGTH(string) > 5) no se generan valores "personalizados"

"SELECT string FROM Persona WHERE LENGTH(string) > 4" --> Genera 3 INSERT INTO. Restriccion de 
columna: lenght(string) > 5 --> Genera CMove M (7), CComWi (6) y CPlaBu (6)  --> OK

"SELECT string FROM Persona WHERE LENGTH(string) < 4" --> Genera 3 INSERT INTO. Restriccion de 
columna: lenght(string) > 5 --> Genera 3 cadenas de tamaño 6  --> OK(?)


- Dos restricciónes, dos columnas:

"SELECT ent, real FROM Persona WHERE ent > 30 and real != 0.02" --> [(0.01, 31), (0.01, 30), 
(0.01, 29), (0.03, 31), (0.03, 30), (0.03, 29), (0.02, 31), (0.02, 30), (0.02, 29)] -->

"SELECT ent, real FROM Persona WHERE ent > 30 and real = 0.01" --> [(0.01, 31), (0.01, 30), 
(0.01, 29), (0.0, 31), (0.0, 30), (0.0, 29), (0.02, 31), (0.02, 30), (0.02, 29)] --> Genera 3 INSERT INTO con
0.01, 30; 0.02, 29 y 0.01, 30 --> OK

"SELECT ent, real FROM Persona WHERE ent > 30 and string like 'Car%'" --> [(31, 'CarFutu'), (31, 'uarGreat inves'), 
(30, 'CarFutu'), (30, 'uarGreat inves'), (29, 'CarFutu'), (29, 'uarGreat inves')] --> Genera 2 o 3 INSERT INTO
solo con el valor válido del like --> REVISAR:::

"SELECT ent, real FROM Persona WHERE ent > 30 and string = 'Carmen'" --> [(31, 'Carmen'), (31, 'Carmem'), 
(31, 'Carmeo'), (30, 'Carmen'), (30, 'Carmem'), (30, 'Carmeo'), (29, 'Carmen'), (29, 'Carmem'), (29, 'Carmeo')] 
--> Genera 3 INSERT INTO con 31, 'Carmen'; 29, 'Carmem' y 30, 'Carmen' --> OK

"SELECT ent, real FROM Persona WHERE ent > 30 and length(string) < 9" --> [(31, 'CSeek Li'), (31, 'CNotLot p'),
(31, 'CAir feTo'), (30, 'CSeek Li'), (30, 'CNotLot p'), (30, 'CAir feTo'), (29, 'CSeek Li'), (29, 'CNotLot p'), 
(29, 'CAir feTo')] --> Genera 3 valores INSERT INTO. A veces es correcto (cadena que cumple y cadena que no cumple)
pero otras veces no --> REVISAR:::


- Dos restricciones, una columna:

"SELECT ent, real FROM Persona WHERE ent > 30 and ent < 40". --> Genera 6 INSERT INTO con 31, 30, 29 y 39, 40, 41


- Tres columnas diferentes sin nada raro:

"SELECT ent, real  FROM Persona WHERE ent > 30 and real > 0.00 and string != 'Carting'"

[(0.01, 31, 'Cartinf'), (0.01, 31, 'Cartinh'), (0.01, 31, 'Carting'), (0.01, 30, 'Cartinf'), (0.01, 30, 'Cartinh'), (0.01, 30, 'Carting'), (0.01, 29, 'Cartinf'), (0.01, 29, 'Cartinh'), (0.01, 29, 'Carting'), (0.0, 31, 'Cartinf'), (0.0, 31, 'Cartinh'), (0.0, 31, 'Carting'), (0.0, 30, 'Cartinf'), (0.0, 30, 'Cartinh'), (0.0, 30, 'Carting'), (0.0, 29, 'Cartinf'), (0.0, 29, 'Cartinh'), (0.0, 29, 'Carting'), (-0.01, 31, 'Cartinf'), (-0.01, 31, 'Cartinh'), (-0.01, 31, 'Carting'), (-0.01, 30, 'Cartinf'), (-0.01, 30, 'Cartinh'), (-0.01, 30, 'Carting'), (-0.01, 29, 'Cartinf'), (-0.01, 29, 'Cartinh'), (-0.01, 29, 'Carting')]


- Tres columnas, dos iguales:

"SELECT ent, real  FROM Persona WHERE ent > 30 and ent < 40 and string != 'Carting'"

[(31, 'Cartinf'), (31, 'Cartinh'), (31, 'Carting'), (30, 'Cartinf'), (30, 'Cartinh'), (30, 'Carting'), (29, 'Cartinf'), (29, 'Cartinh'), (29, 'Carting'), (39, 'Cartinf'), (39, 'Cartinh'), (39, 'Carting'), (40, 'Cartinf'), (40, 'Cartinh'), (40, 'Carting'), (41, 'Cartinf'), (41, 'Cartinh'), (41, 'Carting')]






"SELECT ent, real  FROM Persona WHERE ent > 30 and real > 0.00"