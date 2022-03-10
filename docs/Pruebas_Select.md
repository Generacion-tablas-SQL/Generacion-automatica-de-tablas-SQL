## PRUEBAS SELECT
- Select sin where:

"SELECT ent FROM Persona". --> Genera 10 sentencias INSERT INTO

- Una restricción:

"SELECT ent FROM Persona where ent > 30". --> Genera 3 sentencias INSERT INTO, una con ent = 31,
otra ent = 30 y otra con ent = 29 

- Dos restricciónes, dos columnas:

"SELECT ent, real FROM Persona WHERE ent > 30 and real != 0.02"

[(0.01, 31), (0.01, 30), (0.01, 29), (0.03, 31), (0.03, 30), (0.03, 29), (0.02, 31), (0.02, 30), (0.02, 29)]

- Dos restricciones, una columna:

"SELECT ent, real FROM Persona WHERE ent > 30 and ent < 40". --> Genera 6 INSERT INTO con 31, 30, 29 y 39, 40, 41


- Tres columnas diferentes sin nada raro:

"SELECT ent, real  FROM Persona WHERE ent > 30 and real > 0.00 and string != 'Carting'"

[(0.01, 31, 'Cartinf'), (0.01, 31, 'Cartinh'), (0.01, 31, 'Carting'), (0.01, 30, 'Cartinf'), (0.01, 30, 'Cartinh'), (0.01, 30, 'Carting'), (0.01, 29, 'Cartinf'), (0.01, 29, 'Cartinh'), (0.01, 29, 'Carting'), (0.0, 31, 'Cartinf'), (0.0, 31, 'Cartinh'), (0.0, 31, 'Carting'), (0.0, 30, 'Cartinf'), (0.0, 30, 'Cartinh'), (0.0, 30, 'Carting'), (0.0, 29, 'Cartinf'), (0.0, 29, 'Cartinh'), (0.0, 29, 'Carting'), (-0.01, 31, 'Cartinf'), (-0.01, 31, 'Cartinh'), (-0.01, 31, 'Carting'), (-0.01, 30, 'Cartinf'), (-0.01, 30, 'Cartinh'), (-0.01, 30, 'Carting'), (-0.01, 29, 'Cartinf'), (-0.01, 29, 'Cartinh'), (-0.01, 29, 'Carting')]


- Tres columnas, dos iguales:

"SELECT ent, real  FROM Persona WHERE ent > 30 and ent < 40 and string != 'Carting'"

[(31, 'Cartinf'), (31, 'Cartinh'), (31, 'Carting'), (30, 'Cartinf'), (30, 'Cartinh'), (30, 'Carting'), (29, 'Cartinf'), (29, 'Cartinh'), (29, 'Carting'), (39, 'Cartinf'), (39, 'Cartinh'), (39, 'Carting'), (40, 'Cartinf'), (40, 'Cartinh'), (40, 'Carting'), (41, 'Cartinf'), (41, 'Cartinh'), (41, 'Carting')]


Prueba 3. 


