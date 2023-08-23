import unittest
import tkinter as tk
from unittest.mock import MagicMock

from calculator import Skaiciuotuvas


class TestSkaiciuotuvas(unittest.TestCase):

    def setUp(self):
        self.langas = tk.Tk()
        self.session = MagicMock()
        self.skaiciuotuvas = Skaiciuotuvas(self.langas,self.session)

    def tearDown(self):
        self.langas.destroy()

    def test_skaiciai(self):
        self.skaiciuotuvas.mygtuko_paspaudimas('1')
        self.assertEqual(self.skaiciuotuvas.ivedimo_laukas.get(), '1')

    def test_taskas(self):
        self.skaiciuotuvas.mygtuko_paspaudimas('1')
        self.skaiciuotuvas.mygtuko_paspaudimas('.')
        self.assertEqual(self.skaiciuotuvas.ivedimo_laukas.get(), '1.')

    def test_daug_tasku(self):
        self.skaiciuotuvas.mygtuko_paspaudimas('.')
        self.skaiciuotuvas.mygtuko_paspaudimas('.')
        self.assertEqual(self.skaiciuotuvas.ivedimo_laukas.get(), '.')

    def test_veiksmai(self):
        self.skaiciuotuvas.mygtuko_paspaudimas('1')
        self.skaiciuotuvas.mygtuko_paspaudimas('+')
        self.skaiciuotuvas.mygtuko_paspaudimas('2')
        self.skaiciuotuvas.mygtuko_paspaudimas('=')
        self.assertEqual(self.skaiciuotuvas.rezultato_laukas['text'], 'Rezultatas: 3')

    def test_dalyba_is_nulio(self):
        self.skaiciuotuvas.mygtuko_paspaudimas('5')
        self.skaiciuotuvas.mygtuko_paspaudimas('/')
        self.skaiciuotuvas.mygtuko_paspaudimas('0')
        self.skaiciuotuvas.mygtuko_paspaudimas('=')
        self.assertEqual(self.skaiciuotuvas.rezultato_laukas['text'], 'Dalyba iš nulio negalima')

    def test_procentas(self):
        self.skaiciuotuvas.mygtuko_paspaudimas('8')
        self.skaiciuotuvas.mygtuko_paspaudimas('0')
        self.skaiciuotuvas.mygtuko_paspaudimas('%')
        self.assertEqual(self.skaiciuotuvas.rezultato_laukas['text'], 'Procentas: 0.80')

    def test_minusine_verte(self):
        self.skaiciuotuvas.mygtuko_paspaudimas('8')
        self.skaiciuotuvas.mygtuko_paspaudimas('+/-')
        self.assertEqual(self.skaiciuotuvas.ivedimo_laukas.get(), '-8')

    def test_is_minuso(self):
        self.skaiciuotuvas.mygtuko_paspaudimas('8')
        self.skaiciuotuvas.mygtuko_paspaudimas('+/-')
        self.skaiciuotuvas.mygtuko_paspaudimas('+/-')
        self.assertEqual(self.skaiciuotuvas.ivedimo_laukas.get(), '8')

    def test_daugiau_veiksmu(self):
        self.skaiciuotuvas.mygtuko_paspaudimas('1')
        self.skaiciuotuvas.mygtuko_paspaudimas('+')
        self.skaiciuotuvas.mygtuko_paspaudimas('2')
        self.skaiciuotuvas.mygtuko_paspaudimas('-')
        self.skaiciuotuvas.mygtuko_paspaudimas('7')
        self.skaiciuotuvas.mygtuko_paspaudimas('=')
        self.assertEqual(self.skaiciuotuvas.rezultato_laukas['text'], 'Rezultatas: -4')




if __name__ == "__main__":
    unittest.main()