from decimal import Decimal
from django.conf import settings
from shop.models import Product


class Cart:
    """Allow to manage the shopping cart"""

    def __init__(self, request):
        """
        Initialize the shopping cart
        Creating two attributes:
            - self.session
            - self.cart
        """
        self.session = request.session
        # Is There a existent cart?
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            # Save an empty shopping cart in the session
            # In other words, create a dict inside the
            # self.session[settings.CART_SESSION_ID]
            # that will have all the ids of the products as keys
            # and as value, the quantity and price (dicts)
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart

    def add(self, product: Product, quantity=1, override_quantity=False):
        """Add a product to the shopping cart or update his quantity"""
        product_id = str(product.id)
        if product_id not in self.cart:
            self.cart[product_id] = {'quantity': 0, 'price': str(product.price)}

        if override_quantity:
            self.cart[product_id]['quantity'] = quantity
        else:
            self.cart[product_id]['quantity'] += quantity
        self.save()

    def save(self):
        """Marks the session as 'updated' to guarantee that the session
        will be saved"""
        self.session.modified = True

    def remove(self, product: Product):
        """Exclude a product from the shopping cart"""
        product_id = str(product.id)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()

    def __iter__(self):
        """
        Iterate through the items of the shopping cart and
        get the products of the database.
        Example of usage:
            - example_cart[0]
            - list(example_cart)
            - for prod in example_cart: ...
            - In cart.views.cart_detail
        """
        product_ids = self.cart.keys()
        # Get all the objects of the products and add them to the cart.
        products = Product.objects.filter(id__in=product_ids)

        cart = self.cart.copy()  # {'12345': {'quantity': 2, 'price': '3.30'},  ...}
        for product in products:
            # Add a key to the dict cart, called 'product' and his value is the Model Product.
            # Ex.: {'12345': {'quantity': 2, 'price': '3.30', 'product': <Product fanta mix 330 ml>},  ...}
            cart[str(product.id)]['product'] = product

        # Ex.: cart.values() has this -> [('quantity', 2), ('price', '3.30'), ('product', <Product fanta mix 330 ml>)]
        for item in cart.values():
            item['price'] = Decimal(item['price'])
            item['total_price'] = item['price'] * item['quantity']
            # Then the item would be something like this:
            # {'quantity': 2, 'price': 3.30, 'product': <Product fanta mix 330 ml>, 'total_price': 6.6}
            yield item

    def __len__(self):
        """Reach the total number of items in the shopping cart"""
        return sum(item['quantity'] for item in self.cart.values())

    def get_total_price(self):
        """Calculate the total value of the shopping cart"""
        return sum(Decimal(item['price']) * item['quantity'] for item in self.cart.values())

    def clear(self):
        """Clean the shopping cart"""
        # The dictionary with key 'cart' that is in self.session won't exist anymore.
        # TODO Pero esta no es la session del carrito mas no la session como tal de la jugada???
        del self.session[settings.CART_SESSION_ID]
        self.save()
