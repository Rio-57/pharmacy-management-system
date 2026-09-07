inventory = {
    "Paracetamol": {"price": 2.50, "stock": 100},
    "Ibuprofen": {"price": 3.75, "stock": 50}
}

while True:
    choice = input("\n1. View  2. Add  3. Sell  4. Exit\nSelect option: ")

    if choice == '1':
        for item, details in inventory.items():
            print(f"{item}: ${details['price']:.2f} | Stock: {details['stock']}")

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
                inventory[name]["stock"] -= qty
                print(f"Total: ${qty * inventory[name]['price']:.2f}")
            else:
                print("Insufficient stock!")
        else:
            print("Medicine not found!")

    elif choice == '4':
        break
