"""
models.py

Contains data models (classes) for the Inventory Manager project.

This file defines the Product class, which represents a single product item.
"""


class Product:
    """
    Product represents one item in the inventory.

    Each Product object stores product information (SKU, name, price, etc.)
    and contains methods to update stock (restock/sell).
    """

    def __init__(self, sku, name, price, cost, stock=0, category="General"):
        # Instance attributes (each Product instance has its own values)
        self.sku = sku              # Immutable identifier in our design (we don't change it later)
        self.name = name            # Product name
        self.price = price          # Selling price
        self.cost = cost            # Cost price (useful for future profit calculations)
        self.stock = stock          # Mutable attribute: changes when restocking/selling
        self.category = category    # Product category (default "General")

    def restock(self, quantity):
        """
        Increase the stock for this product.

        quantity (int): number of units to add.
        """
        if quantity <= 0:
            print("Quantity must be greater than 0.")
        else:
            # Update mutable attribute stock
            self.stock = self.stock + quantity

    def sell(self, quantity):
        """
        Sell a quantity of this product if enough stock exists.

        Returns:
            revenue (float): quantity * price if sale is successful, otherwise 0.
        """
        if quantity > self.stock:
            print("Not enough stock.")
            return 0
        elif quantity <= 0:
            print("Quantity must be greater than 0.")
            return 0
        else:
            # Reduce stock and return revenue
            self.stock = self.stock - quantity
            return quantity * self.price

    def to_dict(self):
        """
        Convert this Product object into a dictionary for JSON saving.
        """
        return {
            "sku": self.sku,
            "name": self.name,
            "price": self.price,
            "cost": self.cost,
            "stock": self.stock,
            "category": self.category
        }

    @staticmethod
    def from_dict(data):
        """
        Create a Product object from a dictionary loaded from JSON.

        This is used when restoring products from products.json.
        """
        return Product(
            data["sku"],
            data["name"],
            data["price"],
            data["cost"],
            data.get("stock", 0),
            data.get("category", "General")
        )

    def __str__(self):
        """
        Magic method: defines how the object prints when you do print(product).
        """
        return f"{self.sku} | {self.name} | Price: {self.price} | Stock: {self.stock}"