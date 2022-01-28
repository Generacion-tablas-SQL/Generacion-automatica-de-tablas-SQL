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

    def test_max_num(self):
        self.assertEqual(gd.max_number(6, 2), 9999.99)
        self.assertEqual(gd.max_number(6, 0), 999999)
        self.assertEqual(gd.max_number(6, -2), 999900)
        self.assertEqual(gd.max_number(6, -6), 9000000)

        self.assertEqual(gd.max_number(6, 6), 0.999999)
        self.assertEqual(gd.max_number(2, 6), 0.999999)

    def test_string_gen(self):
        # 1
        self.assertGreaterEqual(len(gd.generate_string({"min": 5, "max": 10, "eq": None, "neq": None, "like": "C%",
                                                        "scale": None, "tipo": "varchar"})), 5)
        self.assertLessEqual(len(gd.generate_string({"min": 5, "max": 10, "eq": None, "neq": None, "like": "C%",
                                                     "scale": None, "tipo": "varchar"})), 10)
        self.assertRegex(gd.generate_string({"min": 5, "max": 10, "eq": None, "neq": None, "like": "C%", "scale": None,
                                             "tipo": "varchar"}), "^C\D")

        # 2
        self.assertGreaterEqual(len(gd.generate_string({"min": 10, "max": 20, "eq": "hola que tal", "neq": None,
                                                        "like": None, "scale": None, "tipo": "varchar"})), 10)
        self.assertLessEqual(len(gd.generate_string({"min": 10, "max": 20, "eq": "hola que tal", "neq": None,
                                                     "like": None, "scale": None, "tipo": "varchar"})), 20)
        self.assertRegex(gd.generate_string({"min": 10, "max": 20, "eq": None, "neq": None, "like": "hola que tal",
                                                        "scale": None, "tipo": "varchar"}), "hola que tal")

    def test_num_gen(self):
        # 1
        self.assertGreaterEqual(gd.generate_number({"min": -10, "max": 900, "eq": None, "neq": None, "like": None, "scale": 0,
                                             "tipo": "int"}), -10)
        self.assertLessEqual(gd.generate_number({"min": -10, "max": 900, "eq": None, "neq": None, "like": None, "scale": 0,
                                "tipo": "varchar"}), 900)
        # 2
        self.assertGreaterEqual(gd.generate_number({"min": -99953.56, "max": -672.78, "eq": None, "neq": None, "like": None, "scale": 2,
                                "tipo": "int"}), -99953.56)
        self.assertLessEqual(
            gd.generate_number({"min": -99953.56, "max": -672.78, "eq": None, "neq": None, "like": None, "scale": 2,
                                "tipo": "int"}), -672.78)


if __name__ == '__main__':
    path = 'C:\\Users\\maria\\OneDrive\\Documentos\\Ing. Inf\\4º Ing. Inf\\TFG\\TiposDatos_Generadores\\src'
    sys.path.insert(0, path)
    import src.generador_datos as gd
    unittest.main()
