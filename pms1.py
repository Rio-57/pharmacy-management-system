inventory = {
    "Paracetamol": {"price": 2.50, "stock": 100},
    "Ibuprofen": {"price": 3.75, "stock": 5}
}
total_sales = 0.0

while True:
    choice = input("\n1. View  2. Add  3. Sell  4. Remove  5. Sales Report  6. Exit\nSelect option: ")

    if choice == '1':
        for item, details in inventory.items():
            # Added Low Stock warning (if stock is below 10)
            low_alert = " ⚠️ LOW STOCK" if details['stock'] < 10 else ""
            print(f"{item}: ${details['price']:.2f} | Stock: {details['stock']}{low_alert}")

    elif choice == '2':
        name = input("Name: ").capitalize()
        price = float(input("Price: $"))
        qty = int(input("Quantity: "))
        if name in inventory:
            inventory[name]["stock"] += qty
        else:
            inventory[name] = {"price": price, "stock": qty}
        print("Updated!")

    elif choice == '3':
        name = input("Name: ").capitalize()
        if name in inventory:
            qty = int(input("Quantity: "))
            if qty <= inventory[name]["stock"]:
                cost = qty * inventory[name]["price"]
                inventory[name]["stock"] -= qty
                total_sales += cost  # Tracks revenue
                print(f"Total: ${cost:.2f}")
            else:
                print("Insufficient stock!")
        else:
            print("Medicine not found!")

    elif choice == '4':
        # New Feature: Remove an item
        name = input("Medicine to delete: ").capitalize()
        if name in inventory:
            del inventory[name]
            print(f"'{name}' removed from inventory.")
        else:
            print("Medicine not found!")

    elif choice == '5':
        # New Feature: Total earnings summary
        print(f"Total Sales Revenue: ${total_sales:.2f}")

    elif choice == '6':
        print("Exiting system.")
        break
