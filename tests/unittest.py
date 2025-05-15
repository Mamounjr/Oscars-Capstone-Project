import pytest
from app import add, sub, mul, div


def test_add_numbers():
    assert add(2, 3) == 5

def test_sub_numbers():
    assert sub(5, 3) == 2

def test_mul_numbers():
    assert mul(2, 3) == 6

def test_div_numbers():
    assert div(6,3) == 2
    

if __name__ == "__main__":
    unittest.main()

