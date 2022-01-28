import unittest
import sys

class MyTestCase(unittest.TestCase):
    def test_float(self):
        for i in range(1, 17):  # Debería ser 39
            for j in range(-84, 17):
                result = gd.max_number(i, j)
                if j in range(-84, 0):
                    if i > abs(j):
                        self.assertEqual(len(str(result)), i)  # num dígitos total
                        nines = result // (10 ** abs(j))
                        self.assertEqual(len(str(nines)), i - abs(j))  # cantidad de 9 = precision - abs(scale)
                        self.assertNotIn("0", str(nines))  # no hay 0 en la zona de nueves
                        # resultado igual a zona de nueves + cantidad de 0 indicados en precision
                        self.assertEqual(str(result), str(nines) + "0" * abs(j))
                    else:
                        self.assertEqual(len(str(result)), abs(j) + 1)  # num dígitos total
                        self.assertNotIn("9", str(result)[1:])  # solo hay un nueve, en la primera posición
                        self.assertEqual("9", str(result)[0])  # el primer dígito es un nueve
                elif j in range(1, 17):  # Debería llegar a 128 pero float no soporta tanta precision, se convierte a
                    if i > j:
                        self.assertEqual(len(str(result)), i + 1)
                        self.assertEqual(str(result)[i - j], ".")
                        self.assertNotIn(str(result), "0")
                    else:
                        self.assertEqual(len(str(result)), j + 2)
                        self.assertEqual(str(result)[1], ".")
                        self.assertEqual(str(result)[0], "0")
                        self.assertEqual(str(result)[2:], "9" * j)

    def test_string(self):
        pass

if __name__ == '__main__':
    path = 'C:\\Users\\maria\\OneDrive\\Documentos\\Ing. Inf\\4º Ing. Inf\\TFG\\TiposDatos_Generadores\\src'
    sys.path.insert(0, path)
    import src.generador_datos as gd
    unittest.main()
