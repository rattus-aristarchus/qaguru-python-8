"""
Протестируйте классы из модуля homework/models.py
"""
import pytest

from models import Product, Cart


@pytest.fixture
def product():
    return Product("book", 100, "This is a book", 1000)


@pytest.fixture
def product_1():
    return Product("another_book", 50, "This is another book", 500)


class TestProducts:
    """
    Тестовый класс - это способ группировки ваших тестов по какой-то тематике
    Например, текущий класс группирует тесты на класс Product
    """

    def test_product_check_quantity(self, product):
        assert product.check_quantity(1) == True

    def test_product_buy(self, product):
        product.buy(1)
        assert product.quantity == 999

    def test_product_buy_more_than_available(self, product):
        with pytest.raises(ValueError):
            product.buy(1001)


@pytest.fixture
def cart_with_a_book(product):
    cart = Cart()
    cart.products[product] = 12
    return cart


@pytest.fixture
def cart_with_two_books(product, product_1):
    cart = Cart()
    cart.products[product] = 3
    cart.products[product_1] = 8
    return cart


@pytest.fixture()
def excessive_cart(product):
    cart = Cart()
    cart.products[product] = 2000
    return cart


class TestCart:

    def test_add_existing_product(self, cart_with_a_book):
        cart = cart_with_a_book
        book = list(cart.products)[0]
        cart.add_product(product=book, buy_count=1)
        assert cart.products[book] == 13

    def test_add_new_product(self, product):
        cart = Cart()
        cart.add_product(product=product, buy_count=13)
        assert cart.products[product] == 13

    def test_remove_product_unspecified(self, cart_with_a_book):
        cart = cart_with_a_book
        book = list(cart.products)[0]
        cart.remove_product(book)
        assert len(cart.products) == 0

    def test_remove_product_everything(self, cart_with_a_book):
        cart = cart_with_a_book
        book = list(cart.products)[0]
        cart.remove_product(book, 12)
        assert len(cart.products) == 0

    def test_remove_product(self, cart_with_a_book):
        cart = cart_with_a_book
        book = list(cart.products)[0]
        cart.remove_product(book, 6)
        assert cart.products[book] == 6

    def test_clear(self, cart_with_two_books):
        cart = cart_with_two_books
        cart.clear()
        assert len(cart.products) == 0

    def test_get_total_price(self, cart_with_two_books):
        assert cart_with_two_books.get_total_price() == 700.0

    def test_buy(self, cart_with_two_books):
        cart = cart_with_two_books
        book_0 = list(cart.products)[0]
        book_1 = list(cart.products)[1]
        cart.buy()
        assert len(cart.products) == 0
        assert book_0.quantity == 997
        assert book_1.quantity == 492

    def test_buy_too_much(self, excessive_cart):
        with pytest.raises(ValueError):
            excessive_cart.buy()
