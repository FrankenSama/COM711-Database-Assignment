# main.py
import sqlite3
import datetime
import sys

def _display_options(all_options, title, type_name):
    """Display a numbered list of options and return selected ID"""
    option_num = 1
    option_list = []
    
    print(f"\n{title}\n")
    print("-" * 50)
    
    for option in all_options:
        code = option[0]
        desc = option[1]
        if len(option) > 2:  # Handle price display for sellers
            price = option[2]
            print(f"{option_num}.\t{desc} - £{price:.2f}")
        else:
            print(f"{option_num}.\t{desc}")
        option_num += 1
        option_list.append(code)
    
    selected_option = 0
    while selected_option <= 0 or selected_option > len(option_list):
        try:
            prompt = f"Enter the number against the {type_name} you want to choose: "
            selected_option = int(input(prompt))
            if selected_option <= 0 or selected_option > len(option_list):
                print(f"Please enter a number between 1 and {len(option_list)}")
        except ValueError:
            print("Please enter a valid number")
    
    return option_list[selected_option - 1]

def display_order_history(curr_shopper_id, cursor):
    """Display order history for a shopper"""
    try:
        sql_query = """
        SELECT so.order_id, 
               strftime('%d-%m-%Y', so.order_date) as formatted_date,
               p.product_description, 
               se.seller_name, 
               op.price,
               op.quantity,
               op.ordered_product_status
        FROM shoppers s
        JOIN shopper_orders so ON s.shopper_id = so.shopper_id
        JOIN ordered_products op ON so.order_id = op.order_id
        JOIN products p ON op.product_id = p.product_id
        JOIN sellers se ON op.seller_id = se.seller_id
        WHERE s.shopper_id = ?
        ORDER BY so.order_date DESC, so.order_id, p.product_description
        """
        
        cursor.execute(sql_query, (curr_shopper_id,))
        all_order_rows = cursor.fetchall()
        
        if not all_order_rows:
            print("\nNo orders placed by this customer")
            return
        
        print("\n" + "=" * 150)
        print("ORDER HISTORY")
        print("=" * 150)
        print(f"{'Order ID':<10} {'Order Date':<12} {'Product Description':<50} {'Seller':<20} {'Price':>10} {'Qty':>5} {'Status':<12}")
        print("-" * 150)
        
        current_order_id = None
        for row in all_order_rows:
            order_id, order_date, prod_desc, seller_name, price, quantity, status = row
            
            if current_order_id != order_id:
                print(f"\n{order_id:<10} {order_date:<12} {prod_desc:<50} {seller_name:<20} £{price:>8.2f} {quantity:>5} {status:<12}")
                current_order_id = order_id
            else:
                print(f"{'':<10} {'':<12} {prod_desc:<50} {seller_name:<20} £{price:>8.2f} {quantity:>5} {status:<12}")
        
        print("=" * 150)
        
    except sqlite3.Error as e:
        print(f"Database error: {e}")

def add_to_basket(curr_shopper_id, empty_basket, curr_basket_id, cursor, db):
    """Add items to shopping basket"""
    try:
        # Step 1: Display product categories
        sql_query = "SELECT category_id, category_description FROM categories ORDER BY category_description"
        cursor.execute(sql_query)
        categories = cursor.fetchall()
        
        if not categories:
            print("No product categories available.")
            return empty_basket, curr_basket_id
        
        selected_category = _display_options(categories, "PRODUCT CATEGORIES", "category")
        
        # Step 2: Display products in selected category
        sql_query = """
        SELECT p.product_id, p.product_description 
        FROM products p 
        WHERE p.category_id = ? 
        ORDER BY p.product_description
        """
        cursor.execute(sql_query, (selected_category,))
        products = cursor.fetchall()
        
        if not products:
            print("No products available in this category.")
            return empty_basket, curr_basket_id
        
        selected_product = _display_options(products, "PRODUCTS IN SELECTED CATEGORY", "product")
        
        # Step 3: Display sellers for selected product
        sql_query = """
        SELECT ps.seller_id, s.seller_name, ps.price 
        FROM product_sellers ps
        JOIN sellers s ON ps.seller_id = s.seller_id
        WHERE ps.product_id = ?
        ORDER BY ps.price, s.seller_name
        """
        cursor.execute(sql_query, (selected_product,))
        sellers = cursor.fetchall()
        
        if not sellers:
            print("No sellers available for this product.")
            return empty_basket, curr_basket_id
        
        selected_seller = _display_options(sellers, "SELLERS FOR SELECTED PRODUCT", "seller")
        
        # Step 4: Get quantity
        while True:
            try:
                selected_quantity = int(input("Enter the quantity you want to purchase: "))
                if selected_quantity < 1:
                    print("Quantity must be at least 1.")
                else:
                    break
            except ValueError:
                print("Please enter a valid number.")
        
        # Step 5: Get price
        sql_query = "SELECT price FROM product_sellers WHERE seller_id = ? AND product_id = ?"
        cursor.execute(sql_query, (selected_seller, selected_product))
        price_row = cursor.fetchone()
        selected_price = price_row[0] if price_row else 0
        
        # Step 6: Create or get basket
        if empty_basket:
            # Get next basket ID
            cursor.execute("SELECT seq FROM sqlite_sequence WHERE name='shopper_baskets'")
            seq_row = cursor.fetchone()
            curr_basket_id = (seq_row[0] + 1) if seq_row else 1
            
            # Create new basket
            now = datetime.datetime.now()
            sql_insert = """
            INSERT INTO shopper_baskets (basket_id, shopper_id, basket_created_date_time) 
            VALUES (?, ?, ?)
            """
            cursor.execute(sql_insert, (curr_basket_id, curr_shopper_id, now.strftime("%Y-%m-%d %H:%M:%S")))
            db.commit()
            empty_basket = False
        
        # Step 7: Add item to basket
        sql_insert = """
        INSERT INTO basket_contents (basket_id, product_id, seller_id, quantity, price)
        VALUES (?, ?, ?, ?, ?)
        """
        cursor.execute(sql_insert, (curr_basket_id, selected_product, selected_seller, 
                                  selected_quantity, selected_price))
        db.commit()
        
        print(f"\n✓ Item successfully added to your basket!")
        
    except sqlite3.Error as e:
        print(f"Database error: {e}")
        db.rollback()
    
    return empty_basket, curr_basket_id

def view_basket(curr_shopper_id, empty_basket, curr_basket_id, cursor):
    """Display current basket contents"""
    if empty_basket:
        print("\nYour basket is empty")
        return
    
    try:
        sql_query = """
        SELECT p.product_description, s.seller_name, bc.quantity, bc.price
        FROM basket_contents bc
        JOIN products p ON bc.product_id = p.product_id
        JOIN sellers s ON bc.seller_id = s.seller_id
        WHERE bc.basket_id = ?
        """
        
        cursor.execute(sql_query, (curr_basket_id,))
        basket_items = cursor.fetchall()
        
        if not basket_items:
            print("\nYour basket is empty")
            return
        
        print("\n" + "=" * 120)
        print("YOUR SHOPPING BASKET")
        print("=" * 120)
        print(f"{'Product Description':<50} {'Seller':<25} {'Qty':>5} {'Price':>10} {'Total':>15}")
        print("-" * 120)
        
        basket_total = 0
        for item in basket_items:
            product_desc, seller_name, quantity, price = item
            item_total = quantity * price
            basket_total += item_total
            
            print(f"{product_desc:<50} {seller_name:<25} {quantity:>5} £{price:>9.2f} £{item_total:>14.2f}")
        
        print("-" * 120)
        print(f"{'BASKET TOTAL':<96} £{basket_total:>14.2f}")
        print("=" * 120)
        
    except sqlite3.Error as e:
        print(f"Database error: {e}")

def checkout_basket(curr_shopper_id, empty_basket, curr_basket_id, cursor, db):
    """Checkout process"""
    if empty_basket:
        print("\nYour basket is empty. Add items before checkout.")
        return empty_basket
    
    try:
        # Display basket first
        view_basket(curr_shopper_id, empty_basket, curr_basket_id, cursor)
        
        print("\n" + "=" * 60)
        print("CHECKOUT PROCESS")
        print("=" * 60)
        
        # Get delivery address
        cursor.execute("""
            SELECT address_id, delivery_address 
            FROM shopper_delivery_addresses 
            WHERE shopper_id = ? 
            ORDER BY date_last_used DESC
            """, (curr_shopper_id,))
        
        addresses = cursor.fetchall()
        
        if not addresses:
            print("\nNo delivery address found.")
            new_address = input("Please enter a new delivery address: ")
            
            # Insert new address
            cursor.execute("""
                INSERT INTO shopper_delivery_addresses (shopper_id, delivery_address, date_last_used)
                VALUES (?, ?, DATE('now'))
                """, (curr_shopper_id, new_address))
            db.commit()
            selected_address = new_address
        elif len(addresses) == 1:
            selected_address = addresses[0][1]
            print(f"\nDelivery Address: {selected_address}")
        else:
            print("\nSelect a delivery address:")
            selected_address_id = _display_options(addresses, "DELIVERY ADDRESSES", "address")
            cursor.execute("SELECT delivery_address FROM shopper_delivery_addresses WHERE address_id = ?", 
                         (selected_address_id,))
            selected_address = cursor.fetchone()[0]
        
        # Get payment card
        cursor.execute("""
            SELECT card_id, card_number 
            FROM shopper_payment_cards 
            WHERE shopper_id = ? 
            ORDER BY date_last_used DESC
            """, (curr_shopper_id,))
        
        cards = cursor.fetchall()
        
        if not cards:
            print("\nNo payment card found.")
            new_card = input("Please enter a new card number: ")
            
            # Insert new card
            cursor.execute("""
                INSERT INTO shopper_payment_cards (shopper_id, card_number, date_last_used)
                VALUES (?, ?, DATE('now'))
                """, (curr_shopper_id, new_card))
            db.commit()
            selected_card = new_card[-4:]  # Show last 4 digits
        elif len(cards) == 1:
            selected_card = cards[0][1][-4:]
            print(f"\nPayment Card: **** **** **** {selected_card}")
        else:
            print("\nSelect a payment card:")
            selected_card_id = _display_options(cards, "PAYMENT CARDS", "card")
            cursor.execute("SELECT card_number FROM shopper_payment_cards WHERE card_id = ?", 
                         (selected_card_id,))
            selected_card = cursor.fetchone()[0][-4:]
        
        # Create order
        now = datetime.datetime.now()
        
        # Get next order ID
        cursor.execute("SELECT seq FROM sqlite_sequence WHERE name='shopper_orders'")
        seq_row = cursor.fetchone()
        next_order_id = (seq_row[0] + 1) if seq_row else 1
        
        # Insert order
        cursor.execute("""
            INSERT INTO shopper_orders (order_id, shopper_id, order_date, order_status)
            VALUES (?, ?, ?, 'Placed')
            """, (next_order_id, curr_shopper_id, now.strftime("%Y-%m-%d %H:%M:%S")))
        
        # Get basket items
        cursor.execute("""
            SELECT product_id, seller_id, quantity, price
            FROM basket_contents
            WHERE basket_id = ?
            """, (curr_basket_id,))
        
        basket_items = cursor.fetchall()
        
        # Insert ordered products
        for item in basket_items:
            product_id, seller_id, quantity, price = item
            cursor.execute("""
                INSERT INTO ordered_products (order_id, product_id, seller_id, quantity, price, ordered_product_status)
                VALUES (?, ?, ?, ?, ?, 'Placed')
                """, (next_order_id, product_id, seller_id, quantity, price))
        
        # Clear basket
        cursor.execute("DELETE FROM basket_contents WHERE basket_id = ?", (curr_basket_id,))
        cursor.execute("DELETE FROM shopper_baskets WHERE basket_id = ?", (curr_basket_id,))
        
        db.commit()
        
        print("\n" + "=" * 60)
        print("ORDER CONFIRMED!")
        print("=" * 60)
        print(f"Order ID: {next_order_id}")
        print(f"Delivery to: {selected_address}")
        print(f"Payment: **** **** **** {selected_card}")
        print(f"Status: Placed")
        print("=" * 60)
        
        empty_basket = True
        curr_basket_id = None
        
    except sqlite3.Error as e:
        print(f"Database error during checkout: {e}")
        db.rollback()
    
    return empty_basket, curr_basket_id

def main():
    """Main program function"""
    print("\n" + "=" * 50)
    print("ORINOCO ELECTRONICS SHOPPING SYSTEM")
    print("=" * 50)
    
    try:
        # Connect to database
        db = sqlite3.connect('assessment_COM711.db')
        cursor = db.cursor()
        
        # Get shopper ID
        while True:
            try:
                shopper_id = int(input("\nEnter shopper ID to begin: "))
                break
            except ValueError:
                print("Please enter a valid number.")
        
        # Verify shopper exists
        cursor.execute("SELECT shopper_first_name, shopper_surname FROM shoppers WHERE shopper_id = ?", 
                      (shopper_id,))
        shopper = cursor.fetchone()
        
        if not shopper:
            print(f"\nError: Shopper ID {shopper_id} not found.")
            db.close()
            return
        
        first_name, surname = shopper
        print(f"\nWelcome back, {first_name} {surname}!")
        
        # Check for existing basket
        cursor.execute("""
            SELECT basket_id 
            FROM shopper_baskets 
            WHERE shopper_id = ? 
            AND DATE(basket_created_date_time) = DATE('now')
            ORDER BY basket_created_date_time DESC 
            LIMIT 1
            """, (shopper_id,))
        
        basket = cursor.fetchone()
        
        if basket:
            empty_basket = False
            current_basket_id = basket[0]
        else:
            empty_basket = True
            current_basket_id = None
        
        # Main menu loop
        while True:
            print("\n" + "-" * 40)
            print("MAIN MENU")
            print("-" * 40)
            print("1. Display your order history")
            print("2. Add an item to your basket")
            print("3. View your basket")
            print("4. Checkout")
            print("5. Exit")
            print("-" * 40)
            
            try:
                choice = int(input("\nEnter your choice (1-5): "))
                
                if choice == 1:
                    display_order_history(shopper_id, cursor)
                elif choice == 2:
                    empty_basket, current_basket_id = add_to_basket(shopper_id, empty_basket, 
                                                                  current_basket_id, cursor, db)
                elif choice == 3:
                    view_basket(shopper_id, empty_basket, current_basket_id, cursor)
                elif choice == 4:
                    empty_basket, current_basket_id = checkout_basket(shopper_id, empty_basket, 
                                                                     current_basket_id, cursor, db)
                elif choice == 5:
                    print("\nThank you for shopping with Orinoco Electronics!")
                    break
                else:
                    print("Please enter a number between 1 and 5.")
                    
            except ValueError:
                print("Please enter a valid number.")
        
        db.close()
        
    except sqlite3.Error as e:
        print(f"Database connection error: {e}")

if __name__ == "__main__":
    main()