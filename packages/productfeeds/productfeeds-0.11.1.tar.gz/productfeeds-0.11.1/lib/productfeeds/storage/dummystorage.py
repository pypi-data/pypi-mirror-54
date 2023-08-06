from productfeeds.storage.base import AbstractStorage


class DummyStorage(AbstractStorage):

    def __init__(self, config=None):
        self.products = []
        self.config = config

    def clear(self):
        self.products = []

    def save_product(self, product):
        """
        Saves product to MySQL table
        Args:
            product (models.Product): Product object to be saved in MySQL table
        Return:
            None
        """
        self.products.append(product)
        field = 'title'
        if 'field' in self.config:
            field = self.config['field']
        print("Saved: {} | {}".format(product.d['articlecode'], product.d[field]))
