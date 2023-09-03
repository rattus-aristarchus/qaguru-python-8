from dataclasses import dataclass


@dataclass
class Product:
    """
    Класс продукта
    """
    name: str
    price: float
    description: str
    quantity: int

    def check_quantity(self, quantity) -> bool:
        if self.quantity >= quantity:
            return True
        else:
            return False

    def buy(self, quantity):
        if not self.check_quantity(quantity):
            raise ValueError
        self.quantity -= quantity

    def __hash__(self):
        return hash(self.name + self.description)


class Cart:
    """
    Класс корзины. В нем хранятся продукты, которые пользователь хочет купить.
    """

    # Словарь продуктов и их количество в корзине
    products: dict[Product, int]

    def __init__(self):
        # По умолчанию корзина пустая
        self.products = {}

    def add_product(self, product: Product, buy_count=1):
        """
        Метод добавления продукта в корзину.
        Если продукт уже есть в корзине, то увеличиваем количество
        """

        present_count = self.products.get(product)
        if present_count is None:
            present_count = 0
        new_count = present_count + buy_count
        self.products[product] = new_count

    def remove_product(self, product: Product, remove_count=None):
        """
        Метод удаления продукта из корзины.
        Если remove_count не передан, то удаляется вся позиция
        Если remove_count больше, чем количество продуктов в позиции, то удаляется вся позиция
        """
        current_count = self.products[product]
        if remove_count is None:
            del self.products[product]
        elif remove_count >= current_count:
            del self.products[product]
        else:
            self.products[product] = current_count - remove_count

    def clear(self):
        self.products.clear()

    def get_total_price(self) -> float:
        total = 0.0
        for product, in_cart in self.products.items():
            total += in_cart * product.price
        return total

    def buy(self):
        """
        Метод покупки.
        Учтите, что товаров может не хватать на складе.
        В этом случае нужно выбросить исключение ValueError
        """

        self._check_quantity()
        self._remove_products_from_storage()
        print(f"\nBought stuff for {self.get_total_price()}")
        self.clear()

    def _check_quantity(self):
        for product, quantity in self.products.items():
            if not product.check_quantity(quantity):
                raise ValueError

    def _remove_products_from_storage(self):
        for product, quantity in self.products.items():
            product.quantity -= quantity
