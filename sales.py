"""
sales.py

Contains SalesManager class to record sales transactions and compute reports.
"""

from datetime import datetime


class SalesManager:
    """
    SalesManager stores and manages sales history.

    Each sale is stored as a dictionary with:
        sku, quantity, revenue, datetime
    """

    def __init__(self, sales=None):
        # If sales list is provided (loaded from JSON), use it.
        # Otherwise start with an empty list.
        if sales is None:
            self.sales = []
        else:
            self.sales = sales

    def record_sales(self, sku, quantity, revenue):
        """
        Record a sale in memory (self.sales).

        sku (str): product SKU sold
        quantity (int): quantity sold
        revenue (float): total revenue for that sale
        """
        if revenue <= 0:
            # If sale did not happen, do nothing
            return None

        # Create a sale record as a dictionary
        sale = {
            "sku": sku,
            "quantity": quantity,
            "revenue": revenue,
            # Datetime formatted as string for easy saving/reading
            "datetime": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }

        # Store the sale (mutable list)
        self.sales.append(sale)

    def list_sales(self):
        """
        Print all sales in a readable format (CLI use).
        """
        if not self.sales:
            print("No sales recorded.")
            return None
        else:
            for sale in self.sales:
                print(
                    f"{sale['datetime']} | SKU: {sale['sku']} | "
                    f"Qty: {sale['quantity']} | Revenue: {sale['revenue']:.2f}"
                )

    def total_revenue(self):
        """
        Compute total revenue from all recorded sales.
        """
        total = 0
        for sale in self.sales:
            total = total + sale["revenue"]
        return total