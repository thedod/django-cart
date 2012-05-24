import datetime
import models,forms
from django.contrib.contenttypes.models import ContentType

CART_ID = 'CART-ID'

class ItemAlreadyExists(Exception):
    pass

class ItemDoesNotExist(Exception):
    pass

class Cart:
    def __init__(self, request=None):
        cart_id = request and request.session.get(CART_ID)
        if cart_id:
            try:
                cart = models.Cart.objects.get(id=cart_id, checked_out=False)
            except models.Cart.DoesNotExist:
                cart = self.new(request)
        else:
            cart = self.new(request)
        self.cart = cart

    def __iter__(self):
        for item in self.cart.item_set.all():
            yield item

    def new(self, request=None):
        cart = models.Cart(creation_date=datetime.datetime.now())
        cart.save()
        if request: request.session[CART_ID] = cart.id
        return cart

    def add(self, product, unit_price, quantity=1):
        try:
            item = models.Item.objects.get(
                cart=self.cart,
                product=product,
            )
        except models.Item.DoesNotExist:
            item = models.Item()
            item.cart = self.cart
            item.product = product
            item.unit_price = unit_price
            item.quantity = quantity
            item.save()
        else: #ItemAlreadyExists
            item.unit_price = unit_price
            item.quantity = item.quantity + int(quantity)
            item.save()

    def remove(self, product):
        try:
            item = models.Item.objects.get(
                cart=self.cart,
                product=product,
            )
        except models.Item.DoesNotExist:
            raise ItemDoesNotExist
        else:
            item.delete()

    def update(self, product, quantity, unit_price=None):
        try:
            item = models.Item.objects.get(
                cart=self.cart,
                product=product,
            )
            if quantity:
                item.quantity = quantity
                if unit_price:
                    item.unit_price = unit_price
                item.save()
            else:
                item.delete()
        except models.Item.DoesNotExist:
            if unit_price:
                if quantity: # Maybe user updated 0 to 0. Happens
                    self.add(product, unit_price, quantity)
            else:
                raise ItemDoesNotExist

    def get(self,product):
        return models.Item.objects.get(cart=self.cart, product=product)

    def count(self):
        result = 0
        for item in self.cart.item_set.all():
            result += 1 * item.quantity
        return result
        
    def summary(self):
        result = 0
        for item in self.cart.item_set.all():
            result += item.total_price
        return result

    def clear(self):
        for item in self.cart.item_set.all():
            item.delete()

    def get_formset(self):
        return forms.ItemFormSet (
            queryset = models.Item.objects.filter(cart=self.cart)
        )    
    def get_formdicts(self,formset=None):
        """template-friendly dicts with product and form.
           first item (product=None) has global management_form and errors"""
        formset = formset or self.get_formset()
        dicts = [{'product':item.product,'form':form
            } for item,form in zip(self,formset.forms)]
        if dicts:
            dicts.insert(0,
                {'product':None,'form':formset.management_form,'errors':formset.errors})
        return dicts
        

    def get_product_form(self,product):
        try:
            item = self.get(product)
        except models.Item.DoesNotExist:
            # Make a "fake item" with 0 quantity
            item = models.Item()
            # ignore item.cart. ItemForm ignores it too
            item.product = product
            item.unit_price = 0 # doesn't matter for form
            item.quantity = 0
            # don't save it (it's just for the form)
        return forms.ItemForm(instance=item)

    def lookup_product(self,content_type=None, object_id=None, form=None):
        "usage: c.lookup_product(ct,oi) or c.lookup_product(form=someform)"
        if form:
            # Note: data and not cleaned_data because maybe not form.is_valid()
            args = form.data or form.initial
            content_type = args['content_type']
            object_id = args['object_id']
        return models.Item.objects.lookup(content_type,object_id)
