import json
import os
from datetime import datetime

DATA_FILE = "pharmacy_data.json"


def load_data():
    """Loads inventory and sales history from a JSON file."""
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    return {
        "inventory": {
            "Paracetamol": {"price": 2.50, "stock": 100},
            "Ibuprofen": {"price": 3.75, "stock": 50},
        },
        "total_sales": 0.0,
        "sales_history": [],
    }


def save_data(data):
    """Saves current state to a JSON file."""
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)


def get_number_input(prompt, is_float=False):
    """Validates user input to prevent program crashes from bad inputs."""
    while True:
        try:
            val = float(input(prompt)) if is_float else int(input(prompt))
            if val < 0:
                print("Error: Value cannot be negative.")
                continue
            return val
        except ValueError:
            print("Error: Please enter a valid number.")


def view_inventory(inventory):
    if not inventory:
        print("\n[!] Inventory is empty.")
        return

    print("\n" + "=" * 55)
    print(f"{'Medicine':<20} {'Price ($)':<12} {'Stock':<10} {'Status'}")
    print("=" * 55)
    for item, details in inventory.items():
        status = "⚠️ LOW STOCK" if details["stock"] < 10 else "OK"
        print(
            f"{item:<20} ${details['price']:<11.2f} {details['stock']:<10} {status}"
        )
    print("=" * 55)


def search_medicine(inventory):
    query = input("Search medicine name: ").strip().lower()
    results = {k: v for k, v in inventory.items() if query in k.lower()}

    if results:
        print(f"\n--- Search Results for '{query}' ---")
        for item, details in results.items():
            print(
                f"• {item} | Price: ${details['price']:.2f} | Stock: {details['stock']}"
            )
    else:
        print(f"\n[!] No medicines matching '{query}' found.")


def add_medicine(data):
    name = input("Medicine Name: ").strip().capitalize()
    if not name:
        print("[!] Name cannot be empty.")
        return

    if name in data["inventory"]:
        print(f"'{name}' exists. Restocking item.")
        qty = get_number_input("Quantity to add: ", is_float=False)
        data["inventory"][name]["stock"] += qty
    else:
        price = get_number_input("Price per unit: $", is_float=True)
        qty = get_number_input("Initial stock quantity: ", is_float=False)
        data["inventory"][name] = {"price": price, "stock": qty}

    save_data(data)
    print(f"[✓] '{name}' successfully updated and saved to file.")


def sell_medicine(data):
    name = input("Medicine Name: ").strip().capitalize()
    if name not in data["inventory"]:
        print("[!] Medicine not found in inventory.")
        return

    item = data["inventory"][name]
    qty = get_number_input(
        f"Quantity to sell (Available: {item['stock']}): ", is_float=False
    )

    if qty > item["stock"]:
        print("[!] Sale failed: Insufficient stock.")
        return

    total = qty * item["price"]
    item["stock"] -= qty
    data["total_sales"] += total

    # Record sale with timestamp
    sale_record = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "item": name,
        "quantity": qty,
        "total": total,
    }
    data["sales_history"].append(sale_record)
    save_data(data)

    print("\n" + "-" * 30)
    print("         RECEIPT")
    print("-" * 30)
    print(f"Item      : {name}")
    print(f"Quantity  : {qty}")
    print(f"Unit Price: ${item['price']:.2f}")
    print(f"Total     : ${total:.2f}")
    print("-" * 30)


def view_sales_report(data):
    print("\n" + "=" * 40)
    print("          SALES REPORT")
    print("=" * 40)
    print(f"Total Revenue Generated : ${data['total_sales']:.2f}")
    print(f"Total Transactions Made : {len(data['sales_history'])}")

    if data["sales_history"]:
        print("\nRecent Transactions (Last 5):")
        for s in data["sales_history"][-5:]:
            print(
                f"  [{s['timestamp']}] {s['quantity']}x {s['item']} -> ${s['total']:.2f}"
            )
    print("=" * 40)


def remove_medicine(data):
    name = input("Medicine name to delete: ").strip().capitalize()
    if name in data["inventory"]:
        del data["inventory"][name]
        save_data(data)
        print(f"[✓] '{name}' deleted and changes saved.")
    else:
        print("[!] Medicine not found.")


def main():
    data = load_data()

    while True:
        print("\n=== PHARMACY MANAGEMENT SYSTEM v2.0 ===")
        print("1. View Inventory")
        print("2. Search Medicine")
        print("3. Add / Restock Medicine")
        print("4. Sell Medicine (Print Receipt)")
        print("5. View Sales Report")
        print("6. Delete Medicine")
        print("7. Exit")

        choice = input("\nSelect option (1-7): ").strip()

        if choice == "1":
            view_inventory(data["inventory"])
        elif choice == "2":
            search_medicine(data["inventory"])
        elif choice == "3":
            add_medicine(data)
        elif choice == "4":
            sell_medicine(data)
        elif choice == "5":
            view_sales_report(data)
        elif choice == "6":
            remove_medicine(data)
        elif choice == "7":
            print("Data auto-saved to 'pharmacy_data.json'. Exiting system!")
            break
        else:
            print("[!] Invalid option. Select a number between 1 and 7.")


if __name__ == "__main__":
    main()
