"""
inventory.py

Contains the Inventory class which manages Product objects.

Inventory uses composition:
- Inventory "has" many Product instances stored in a dictionary.
"""

from models import Product


class Inventory:
    """
    Inventory stores and manages multiple products.

    products is a dict:
        key   = SKU (string)
        value = Product object
    """

    def __init__(self):
        # Collection: dictionary of SKU -> Product
        self.products = {}

    def add_product(self, product):
        """
        Add a Product to inventory.

        product (Product): the product instance to add
        """
        if product.sku in self.products:
            print("Product with this SKU already exists.")
        else:
            self.products[product.sku] = product
            print("Product added successfully.")

    def remove_product(self, sku):
        """
        Remove a product from inventory using its SKU.
        """
        if sku not in self.products:
            print("SKU not found.")
        else:
            del self.products[sku]
            print("Product removed successfully.")

    def list_products(self):
        """
        Print all products currently in inventory.
        """
        if len(self.products) == 0:
            print("No products in inventory.")
        else:
            # Loop through values (Product objects)
            for product in self.products.values():
                print(product)

    def find_product(self, sku):
        """
        Return the Product object for the given SKU, or None if not found.
        """
        if sku in self.products:
            return self.products[sku]
        else:
            return None

    def restock_product(self, sku, quantity):
        """
        Restock a product identified by SKU.
        """
        product = self.find_product(sku)
        if product is None:
            print("SKU not found.")
        else:
            # Delegates stock update logic to Product class
            product.restock(quantity)

    def sell_product(self, sku, quantity):
        """
        Sell a product identified by SKU.

        Returns:
            revenue (float): returned by Product.sell()
        """
        product = self.find_product(sku)
        if product is None:
            print("SKU not found.")
            return 0
        else:
            return product.sell(quantity)

    def low_stock_report(self, threshold=5):
        """
        Print products with stock <= threshold.
        """
        print("\nLow Stock Products:")
        found = False

        for product in self.products.values():
            if product.stock <= threshold:
                print(product)
                found = True

        if not found:
            print("No low stock products.")