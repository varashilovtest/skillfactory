from app.Calculator import Calculator


class Test_calc:
    def setup(self):
        self.calc = Calculator()

    def test_multiply(self):
        assert self.calc.multiply(2, 5) == 10

    def test_division(self):
        assert self.calc.division(5, 2) == 2.5

    def test_subtraction(self):
        assert self.calc.subtraction(18.2, 87.233) == -69.033

    def test_adding(self):
        assert self.calc.adding(22, 33) == 55
