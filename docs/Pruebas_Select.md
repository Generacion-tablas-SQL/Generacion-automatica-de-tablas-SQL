## PRUEBAS SELECT
- Select sin where:

"SELECT ent FROM Persona". --> Genera 10 sentencias INSERT INTO


- Una restricción:

"SELECT ent FROM Persona where ent > 30". --> Genera 3 sentencias INSERT INTO, una con ent = 31,
otra ent = 30 y otra con ent = 29

"SELECT string FROM Persona WHERE real > 0" --> Genera 3 sentencias INSERT INTO con 0.01, 0.0 y 0.0
--> OK

"SELECT string FROM Persona WHERE real > 0.03" --> Genera 3 sentencias INSERT INTO con 0.03, 0.03
y 0.02

"SELECT string FROM Persona WHERE string like '%c%'" (sin restricciones de columna) --> 
Genera 2 sentencias INSERT INTO con 'Thousand shacG' y 'SaxG' --> OK

"SELECT string FROM Persona WHERE string like '_c_'" --> Genera 2 sentencias INSERT INTO con 'xcz' y 'xuc' --> OK

"SELECT string FROM Persona WHERE string like 'Carmen'" --> Carmen, jarmen --> OK

"SELECT string FROM Persona WHERE LENGTH(string) > 7"  --> CNPopula (8), CArrive (7) y CSourc (6) --> OK

"SELECT string FROM Persona WHERE REAL = NULL" --> REVISAR::::restricciones_where en búsqueda de
nombre de arg_data y arg_col

"SELECT string FROM Persona WHERE fec1 = '01/02/2000'" --> Genera mismo dia, dia anterior y dia
siguiente --> OK


- Una condición que no cumple restricción de columna:

"SELECT ent FROM Persona WHERE ent > 50" (ent < 50 en columna) --> Genera 3 INSERT INTO con 
ent = 49 y 48 --> Si no tuviera restricción unique en la columna se generaría un 2º valor 49.

"SELECT ent FROM Persona WHERE ent = 50" (ent < 50 en columna) --> Genera 2 INSERT INTO con 
ent = 49, 48. Si no tuviera restricción unique en la columna se generaría un 2º valor 49.

"SELECT string FROM Persona WHERE string like 'Car'" (length(string) > 5 en columna) --> Genera 2 INSERT INTO con 'Caraaa' y 
'Cyraaa'. --> OK

"SELECT string FROM Persona WHERE string like '%c%'" (restricción columna: like 'C%') --> Genera 10 valores que cumplen
las restricciones de la columna, pero no del where --> REVISAR::::cumple_restricciones devuelve false

"SELECT string FROM Persona WHERE LENGTH(string) > 4" (Restricción de columna: length(string) > 5 ) --> 
Genera 3 INSERT INTO con CArt Pro (8), COccur  (7) y CSHist (6)  --> OK

"SELECT string FROM Persona WHERE LENGTH(string) < 4" (Restricción de columna: length(string) > 5 ) --> Genera 3 INSERT 
INTO con  CNatur (6), CACultu (7) y CMagazPe (8)--> OK


- Dos condiciones, dos columnas (cumplen restricciones de columna) (sin restricciones unique):

"SELECT ent, real FROM Persona WHERE ent > 7 and real != 0.02" --> [(0.01, 8), (0.01, 7), (0.01, 6), (0.03, 8), 
(0.03, 7), (0.03, 6), (0.02, 8), (0.02, 7), (0.02, 6)] --> OK

"SELECT ent, real FROM Persona WHERE ent > 7 and real = 0.01" --> [(0.01, 8), (0.01, 7), (0.01, 6), (0.0, 8), (0.0, 7), 
(0.0, 6), (0.02, 8), (0.02, 7), (0.02, 6)] --> OK

"SELECT ent, string FROM Persona WHERE ent > 30 and string like 'Car%'" --> [(31, 'CarMilli'), (31, 'CjrSimple'), 
(30, 'CarMilli'), (30, 'CjrSimple'), (29, 'CarMilli'), (29, 'CjrSimple')] --> OK

"SELECT ent, string FROM Persona WHERE ent > 30 and string = 'Carmen'" --> [(31, 'Carmen'), (31, 'Carmem'), 
(31, 'Carmeo'), (30, 'Carmen'), (30, 'Carmem'), (30, 'Carmeo'), (29, 'Carmen'), (29, 'Carmem'), (29, 'Carmeo')] --> OK

"SELECT ent, string FROM Persona WHERE ent > 30 and length(string) < 9" --> [(31, 'CHistory'), (31, 'CHeavy im'), 
(31, 'CHaStar av'), (30, 'CHistory'), (30, 'CHeavy im'), (30, 'CHaStar av'), (29, 'CHistory'), (29, 'CHeavy im'), 
(29, 'CHaStar av')] --> OK


- Dos condiciones, dos columnas (cumplen restricciones de columna) (con restricciones UNIQUE):

"SELECT ent, real FROM Persona WHERE ent > 30 and real != 0.02" (UNIQUE en real) --> [(0.01, 31), (0.01, 30), 
(0.01, 29), (0.03, 31), (0.03, 30), (0.03, 29), (0.02, 31), (0.02, 30), (0.02, 29)] --> 3 INSERT INTO con (0.01, 31),
(0.03, 29), (0.02, 30) --> OK

"SELECT ent, real FROM Persona WHERE ent > 30 and real != 0.02" (UNIQUE en ent) --> [(0.01, 31), (0.01, 30), 
(0.01, 29), (0.03, 31), (0.03, 30), (0.03, 29), (0.02, 31), (0.02, 30), (0.02, 29)] --> 3 INSERT INTO con (0.01, 31),
(0.01, 30), (0.03, 29) --> OK

"SELECT ent, real FROM Persona WHERE ent > 30 and real = 0.01" (UNIQUE en real) --> [(0.01, 31), (0.01, 30), (0.01, 29),
(0.0, 31), (0.0, 30), (0.0, 29), (0.02, 31), (0.02, 30), (0.02, 29)] --> 3 INSERT INTO con (0.01, 31),
(0.03, 31), (0.02, 29) --> OK

"SELECT ent, real FROM Persona WHERE ent > 30 and real = 0.01" (UNIQUE en ent) --> [(0.01, 31), (0.01, 30), (0.01, 29),
(0.0, 31), (0.0, 30), (0.0, 29), (0.02, 31), (0.02, 30), (0.02, 29)] --> 3 INSERT INTO con (0.01, 31),
(0.01, 30), (0.02, 29) --> OK

"SELECT ent, string FROM Persona WHERE ent > 30 and string like 'Ca%'" (UNIQUE en ent) --> [(31, 'CaWay require b'),
(31, 'CwHeBu'), (30, 'CaWay require b'), (30, 'CwHeBu'), (29, 'CaWay require b'), (29, 'CwHeBu')]
 --> 3 INSERT INTO con (31, CaWay require b), (29, CaWay require b), (30, CaWay require b) --> El valor no válido
de string no siempre se genera (es aleatorio) --> OK¿?

"SELECT ent, string FROM Persona WHERE ent > 30 and string like 'Ca%'" (UNIQUE en string) --> [(31, 'CaWalk camera '), 
(31, 'CcAuthori'), (30, 'CaWalk camera '), (30, 'CcAuthori'), (29, 'CaWalk camera '), (29, 'CcAuthori')] --> 
3 INSERT INTO con (31, 'CaWalk camera '), (29, CcAuthori)--> OK

"SELECT ent, string FROM Persona WHERE ent > 30 and string = 'Carmen'" (UNIQUE en ent) --> [(31, 'Carmen'), (31, 'Carmem'), 
(31, 'Carmeo'), (30, 'Carmen'), (30, 'Carmem'), (30, 'Carmeo'), (29, 'Carmen'), (29, 'Carmem'), (29, 'Carmeo')] --> 
3 INSERT INTO con (31, Carmen), (29, Carmem), (30, Carmem) --> OK

"SELECT ent, string FROM Persona WHERE ent > 30 and length(string) < 9" (UNIQUE en string) --> [(31, 'CHistory'), (31, 'CHeavy im'), 
(31, 'CHaStar av'), (30, 'CHistory'), (30, 'CHeavy im'), (30, 'CHaStar av'), (29, 'CHistory'), (29, 'CHeavy im'), 
(29, 'CHaStar av')] --> 3 INSERT INTO con (31, Carmen), (29, Carmem), (30, Carmeo) --> OK


- Dos restricciones, dos columnas (no cumplen restricciones columna):

"SELECT ent FROM Persona WHERE ent > 50 and real != 0.02" (ent < 45 en columna) --> [(0.01, 44), (0.01, 44), (0.01, 43),
(0.03, 44), (0.03, 44), (0.03, 43), (0.02, 44), (0.02, 44), (0.02, 43)] --> 9 INSERT INTO con los valores de las 
permutaciones

"SELECT ent FROM Persona WHERE ent > 50 and real != 0.02" (ent < 45 en columna) (unique en ent) --> [(0.01, 44), 
(0.01, 44), (0.01, 43), (0.03, 44), (0.03, 44), (0.03, 43), (0.02, 44), (0.02, 44), (0.02, 43)] --> 2 INSERT INTO con
(0.01, 44) y (0.01, 43)

"SELECT string FROM Persona WHERE ent > 50 and string like 'Car'"(length(string) > 5 en columna) --> [(44, 'Caraaa'), 
(44, 'Cwraaa'), (43, 'Caraaa'), (43, 'Cwraaa'), (42, 'Caraaa'), (42, 'Cwraaa')] --> 6 INSERT INTO con los valores de 
las permutaciones --> OK


- Dos condiciones, una columna:

"SELECT ent FROM Persona WHERE ent > 30 and ent < 40". --> Genera 6 INSERT INTO con 31, 30, 29 y 39, 40, 41 --> OK

"SELECT ent FROM Persona WHERE ent > 30 and ent < 31" (UNIQUE en ent) --> 3 INSERT INTO con 31, 30, 29 y 32 --> OK

"SELECT string FROM Persona WHERE string != 'Carmen' and string like 'Car%'"



- Tres condiciones, tres columnas:

"SELECT ent, real  FROM Persona WHERE ent > 30 and real > 0.00 and string != 'Carting'"

[(0.01, 31, 'Cartinf'), (0.01, 31, 'Cartinh'), (0.01, 31, 'Carting'), (0.01, 30, 'Cartinf'), (0.01, 30, 'Cartinh'), (0.01, 30, 'Carting'), (0.01, 29, 'Cartinf'), (0.01, 29, 'Cartinh'), (0.01, 29, 'Carting'), (0.0, 31, 'Cartinf'), (0.0, 31, 'Cartinh'), (0.0, 31, 'Carting'), (0.0, 30, 'Cartinf'), (0.0, 30, 'Cartinh'), (0.0, 30, 'Carting'), (0.0, 29, 'Cartinf'), (0.0, 29, 'Cartinh'), (0.0, 29, 'Carting'), (-0.01, 31, 'Cartinf'), (-0.01, 31, 'Cartinh'), (-0.01, 31, 'Carting'), (-0.01, 30, 'Cartinf'), (-0.01, 30, 'Cartinh'), (-0.01, 30, 'Carting'), (-0.01, 29, 'Cartinf'), (-0.01, 29, 'Cartinh'), (-0.01, 29, 'Carting')]


- Tres columnas, dos iguales:

"SELECT ent, real  FROM Persona WHERE ent > 30 and ent < 40 and string != 'Carting'"

[(31, 'Cartinf'), (31, 'Cartinh'), (31, 'Carting'), (30, 'Cartinf'), (30, 'Cartinh'), (30, 'Carting'), (29, 'Cartinf'), (29, 'Cartinh'), (29, 'Carting'), (39, 'Cartinf'), (39, 'Cartinh'), (39, 'Carting'), (40, 'Cartinf'), (40, 'Cartinh'), (40, 'Carting'), (41, 'Cartinf'), (41, 'Cartinh'), (41, 'Carting')]

