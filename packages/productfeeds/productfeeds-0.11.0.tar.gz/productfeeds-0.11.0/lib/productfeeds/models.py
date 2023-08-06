class ProductError(Exception):
    pass


class Product(object):
    """
    Product model with defined required attributes
    """

    FIELDS = {
        'articlecode': None,
        'title': None,
        'category': None,
        'subcategory1': None,
        'subcategory2': None,
        'brand': None,
        'producturl': None,
        'thumburl': None,
        'imageurl': None,
        'price': None,
        'delivery': None,
        'description': None,
        'status': 1,
        'uzip_id': 'NA',
        'client': None,
    }

    def __init__(self, product_data=None):
        if product_data is not None:
            self.d = dict(product_data)
            for field in Product.FIELDS:
                if field not in product_data:
                    raise ProductError('Field `{}` does not exist in initial data dict'.format(field))
        else:
            self.d = dict(Product.FIELDS)
        self.d = self.d

    def set(self, attribute_name, value):
        """
        Set value of product attribute
        Args:
            attribute_name (str): Attribute name to be set
            value (?): Value of attribute
        """
        self.d[attribute_name] = value

    def get(self, attribute_name):
        """
        Gets value of product attribute
        Args:
            attribute_name (str): Attribute name
        Return:
            attribute value (?): Attribute value
        """
        return self.d[attribute_name]

    def to_dict(self):
        """
        Converts the product data to dict object
        Return:
            product_data (dict): Product data
        """
        return dict(self.d)
