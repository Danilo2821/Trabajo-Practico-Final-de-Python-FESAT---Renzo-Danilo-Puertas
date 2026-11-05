import unittest
from .services import calcular_emisiones_carbono

class TestCalculoEmisiones(unittest.TestCase):
    def test_calculo_nominal_default(self):
        resultado = calcular_emisiones_carbono(100)
        self.assertEqual(resultado, 40.0)

    def test_calculo_factor_personalizado(self):
        resultado = calcular_emisiones_carbono(250, factor_emision=0.5)
        self.assertEqual(resultado, 125)    

    def test_consumo_cero(self):
            resultado = calcular_emisiones_carbono(0)
            self.assertEqual(resultado, 0)    

    def test_consumo_negativo(self):
            self.assertRaises(ValueError, calcular_emisiones_carbono, -50)   
            
    


    