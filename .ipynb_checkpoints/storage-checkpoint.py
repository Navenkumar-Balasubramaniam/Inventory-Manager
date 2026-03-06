"""
storage.py

Handles saving/loading of products and sales using JSON files.
Uses pathlib.Path to handle file paths in a clean, cross-platform way.
"""

import json
from pathlib import Path
from models import Product


class Storage:
    """
    Storage manages persistence to JSON files:
    - products.json (products data)
    - sales.json (sales history)
    """

    def __init__(self, filepath="data/products.json"):
        # Store the products filepath as a Path object
        self.filepath = Path(filepath)

        # Ensure the parent folder (data/) exists
        self.filepath.parent.mkdir(parents=True, exist_ok=True)

        # Ensure products file exists and contains valid JSON list initially
        if not self.filepath.exists():
            self.filepath.write_text("[]", encoding="utf-8")

    def save_products(self, products_dict):
        """
        Save products (dict of sku -> Product) into products.json.
        """
        products_list = []

        # Convert each Product object to a dict for JSON
        for product in products_dict.values():
            products_list.append(product.to_dict())

        # Write JSON to file
        with open(self.filepath, "w", encoding="utf-8") as f:
            json.dump(products_list, f, indent=2)

    def load_products(self):
        """
        Load products from products.json and return a dict of sku -> Product.
        """
        with open(self.filepath, "r", encoding="utf-8") as f:
            data = json.load(f)

        products = {}

        # Convert dictionaries back into Product objects
        for item in data:
            product = Product.from_dict(item)
            products[product.sku] = product

        return products

    def save_sales(self, sales_list):
        """
        Save sales (list of dicts) into sales.json.
        """
        sales_path = self.filepath.parent / "sales.json"

        # Create sales.json if missing
        if not sales_path.exists():
            sales_path.write_text("[]", encoding="utf-8")

        with open(sales_path, "w", encoding="utf-8") as f:
            json.dump(sales_list, f, indent=2)

    def load_sales(self):
        """
        Load sales from sales.json and return a list.
        """
        sales_path = self.filepath.parent / "sales.json"

        # If file doesn't exist, return an empty list
        if not sales_path.exists():
            return []

        # If JSON is invalid, return empty list instead of crashing
        try:
            with open(sales_path, "r", encoding="utf-8") as f:
                data = json.load(f)
        except json.JSONDecodeError:
            return []

        # Safety check: ensure loaded data is a list
        if not isinstance(data, list):
            return []

        return data