"""
app.py

Streamlit UI for Inventory & Sales Management System.

This file provides a simple web interface with pages:
- Add Product
- Restock Product
- Sell Product
- Reports (Revenue, Low stock, Sales history)

It uses the same backend classes:
Product, Inventory, Storage, SalesManager
"""

import streamlit as st
from models import Product
from inventory import Inventory
from storage import Storage
from sales import SalesManager


# ---------- INITIALIZATION ----------
# Create storage and load saved data from JSON files
storage = Storage()

inventory = Inventory()
inventory.products = storage.load_products()

sales_data = storage.load_sales()
sales_manager = SalesManager(sales_data)


# ---------- SIDEBAR NAVIGATION ----------
st.sidebar.title("Inventory Manager")
page = st.sidebar.radio(
    "Go to",
    ["Add Product", "Restock Product", "Sell Product", "Reports"]
)

st.title("📦 Inventory & Sales Manager")


# ==================================================
# PAGE 1 — ADD PRODUCT
# ==================================================
if page == "Add Product":
    st.header("Add New Product")

    # Streamlit input widgets
    sku = st.text_input("SKU")
    name = st.text_input("Product Name")
    price = st.number_input("Selling Price", min_value=0.0)
    cost = st.number_input("Cost Price", min_value=0.0)
    stock = st.number_input("Starting Stock", min_value=0)
    category = st.text_input("Category", value="General")

    # When button is clicked, create Product and save
    if st.button("Add Product"):
        if sku and name:
            product = Product(sku, name, price, cost, stock, category)
            inventory.add_product(product)

            # Persist updated product list
            storage.save_products(inventory.products)

            st.success("Product added successfully!")
        else:
            st.error("SKU and Name are required.")


# ==================================================
# PAGE 2 — RESTOCK
# ==================================================
elif page == "Restock Product":
    st.header("Restock Product")

    if inventory.products:
        sku = st.selectbox("Select Product", list(inventory.products.keys()))
        quantity = st.number_input("Quantity to Add", min_value=1)

        if st.button("Restock"):
            inventory.restock_product(sku, quantity)
            storage.save_products(inventory.products)
            st.success("Product restocked successfully!")
    else:
        st.info("No products available.")


# ==================================================
# PAGE 3 — SELL PRODUCT
# ==================================================
elif page == "Sell Product":
    st.header("Sell Product")

    if inventory.products:
        sku = st.selectbox("Select Product", list(inventory.products.keys()))
        quantity = st.number_input("Quantity to Sell", min_value=1)

        if st.button("Sell"):
            revenue = inventory.sell_product(sku, quantity)

            if revenue > 0:
                # Record sale using SalesManager and save everything
                sales_manager.record_sales(sku, quantity, revenue)

                storage.save_products(inventory.products)
                storage.save_sales(sales_manager.sales)

                st.success(f"Sale completed! Revenue: {revenue:.2f}")
            else:
                st.warning("Sale could not be completed.")
    else:
        st.info("No products available.")


# ==================================================
# PAGE 4 — REPORTS
# ==================================================
elif page == "Reports":
    st.header("Reports")

    # Total Revenue Report
    st.subheader("Total Revenue")
    total = sales_manager.total_revenue()
    st.write(f"Total Revenue: {total:.2f}")

    # Low Stock Products Report
    st.subheader("Low Stock Products")
    threshold = st.number_input("Low Stock Threshold", min_value=0, value=5)

    found = False
    for product in inventory.products.values():
        if product.stock <= threshold:
            st.write(product)
            found = True

    if not found:
        st.write("No low stock products.")

    # Sales History Report
    st.subheader("Sales History")

    if sales_manager.sales:
        for sale in sales_manager.sales:
            st.write(
                f"{sale['datetime']} | SKU: {sale['sku']} | "
                f"Qty: {sale['quantity']} | Revenue: {sale['revenue']:.2f}"
            )
    else:
        st.write("No sales recorded.")