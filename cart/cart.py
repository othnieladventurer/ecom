from django.conf import settings
from decimal import Decimal, ROUND_HALF_UP
from product.models import Product


class Cart(object):
    def __init__(self, request):
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)

        if not cart:
            cart = self.session[settings.CART_SESSION_ID] = {}
        
        self.cart = cart

    def __iter__(self):
        """
        Iterate over the items in the cart and get the products from the database.
        """
        product_ids = self.cart.keys()
        products = Product.objects.filter(id__in=product_ids)

        for product in products:
            self.cart[str(product.id)]['product'] = product

        for item in self.cart.values():
            # Use the exact price, no division by 100
            item['total_price'] = item['product'].price * item['quantity']
            yield item

    def __len__(self):
        return sum(item['quantity'] for item in self.cart.values())

    def save(self):
        self.session[settings.CART_SESSION_ID] = self.cart
        self.session.modified = True

    def add(self, product_id, quantity=1, update_quantity=False):
        product_id = str(product_id)

        if product_id not in self.cart:
            self.cart[product_id] = {'quantity': 1, 'id': product_id}
        
        if update_quantity:
            self.cart[product_id]['quantity'] += int(quantity)

            if self.cart[product_id]['quantity'] == 0:
                self.remove(product_id)
            
        self.save()

    def remove(self, product_id):
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()


    def clear(self):
        del self.session[settings.CART_SESSION_ID]
        self.session.modified = True


    def get_total_cost(self):
        """
        Get the total cost of the items in the cart without dividing by 100.
        """
        product_ids = self.cart.keys()
        products = Product.objects.filter(id__in=product_ids)

        for product in products:
            self.cart[str(product.id)]['product'] = product

        return sum(item['product'].price * item['quantity'] for item in self.cart.values())

    def get_item(self, product_id):
        if product_id in self.cart:
            return self.cart[str(product_id)]
        else:
            return None
