"""
main.py

CLI version of the Inventory & Sales Management System.

Demonstrates:
- Menus (print-based UI)
- While loops (keep program running until exit)
- Input validation helpers (read_int, read_float)
- Calls into Inventory, Storage, SalesManager classes
"""

from models import Product
from inventory import Inventory
from storage import Storage
from sales import SalesManager


def show_menu():
    """Print the main menu options."""
    print("\n===== INVENTORY & SALES MANAGER =====")
    print("1. Add product")
    print("2. Remove product")
    print("3. List products")
    print("4. Restock product")
    print("5. Sell product")
    print("6. Sales history")
    print("7. Revenue report")
    print("8. Low stock report")
    print("9. Exit")


def read_int(message):
    """
    Keep asking the user until a valid integer is provided.
    (Prevents ValueError from int("abc"))
    """
    while True:
        value = input(message).strip()
        if value.isdigit():
            return int(value)
        print("Please enter a valid integer (e.g., 10).")


def read_float(message):
    """
    Keep asking the user until a valid float is provided.
    (Prevents ValueError from float("abc"))
    """
    while True:
        value = input(message).strip()
        try:
            return float(value)
        except ValueError:
            print("Please enter a valid number (e.g., 10 or 10.5).")


def main():
    """
    Main program loop:
    - load products and sales from JSON
    - display menu
    - execute chosen action
    """
    inventory = Inventory()
    storage = Storage()

    # Load saved data at program start
    inventory.products = storage.load_products()
    sales_data = storage.load_sales()
    sales_manager = SalesManager(sales_data)

    # Menu loop
    while True:
        show_menu()
        choice = input("Choose an option (1-9): ").strip()

        if choice == "1":
            # Add product
            sku = input("Enter SKU: ").strip()
            name = input("Enter product name: ").strip()

            price = read_float("Enter selling price: ")
            cost = read_float("Enter cost price: ")
            stock = read_int("Enter starting stock: ")

            category = input("Enter category (or press Enter for General): ").strip()
            if category == "":
                category = "General"

            product = Product(sku, name, price, cost, stock, category)
            inventory.add_product(product)
            storage.save_products(inventory.products)

        elif choice == "2":
            # Remove product
            sku = input("Enter SKU to remove: ").strip()
            inventory.remove_product(sku)
            storage.save_products(inventory.products)

        elif choice == "3":
            # List products
            inventory.list_products()

        elif choice == "4":
            # Restock product
            sku = input("Enter SKU to restock: ").strip()
            quantity = read_int("Enter quantity to add: ")
            inventory.restock_product(sku, quantity)
            storage.save_products(inventory.products)

        elif choice == "5":
            # Sell product
            sku = input("Enter SKU to sell: ").strip()
            quantity = read_int("Enter quantity to sell: ")

            revenue = inventory.sell_product(sku, quantity)

            # If sale succeeded, record it and save updated data
            if revenue > 0:
                print(f"Revenue from sale: {revenue:.2f}")

                # FIX: your SalesManager method is record_sales (plural)
                sales_manager.record_sales(sku, quantity, revenue)

                storage.save_products(inventory.products)
                storage.save_sales(sales_manager.sales)

        elif choice == "6":
            # Sales history
            sales_manager.list_sales()

        elif choice == "7":
            # Revenue report
            total = sales_manager.total_revenue()
            print(f"\nTotal Revenue: {total:.2f}")

        elif choice == "8":
            # Low stock report
            inventory.low_stock_report()

        elif choice == "9":
            # Exit program
            print("Goodbye!")
            break

        else:
            print("Invalid option. Please choose 1 to 9.")


# Script entry point:
# This ensures main() runs only if we run `python main.py`,
# and not when we import this file from another module.
if __name__ == "__main__":
    main()