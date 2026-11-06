import csv
import random
import datetime

# Seed for reproducibility
random.seed(42)

TOTAL_ROWS = 35000

first_names = [
    "James", "Mary", "John", "Patricia", "Robert", "Jennifer", "Michael", "Linda",
    "William", "Elizabeth", "David", "Barbara", "Richard", "Susan", "Joseph", "Jessica",
    "Thomas", "Sarah", "Charles", "Karen", "Christopher", "Nancy", "Daniel", "Lisa",
    "Matthew", "Betty", "Anthony", "Margaret", "Mark", "Sandra", "Donald", "Ashley",
    "Steven", "Kimberly", "Paul", "Emily", "Andrew", "Donna", "Joshua", "Michelle",
    "Rahul", "Priya", "Amit", "Sneha", "Vikram", "Ananya", "Rohan", "Pooja", "Arjun", "Neha",
    "Wei", "Li", "Hao", "Yuki", "Kenji", "Carlos", "Maria", "Sofia", "Mateo", "Lucas"
]

last_names = [
    "Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia", "Miller", "Davis",
    "Rodriguez", "Martinez", "Hernandez", "Lopez", "Gonzalez", "Wilson", "Anderson",
    "Thomas", "Taylor", "Moore", "Jackson", "Martin", "Lee", "Perez", "Thompson",
    "White", "Harris", "Sanchez", "Clark", "Ramirez", "Lewis", "Robinson", "Walker",
    "Sharma", "Patel", "Verma", "Gupta", "Singh", "Kumar", "Iyer", "Rao", "Nair", "Mehta",
    "Tanaka", "Sato", "Chen", "Wang", "Zhang", "Silva", "Santos", "Muller", "Schmidt"
]

countries = ["USA", "United States", "US", "U.S.A.", "India", "IND", "Germany", "DE", "United Kingdom", "UK", "Canada", "CAN", "Australia", "AUS", None]
cities_map = {
    "USA": ["New York", "Los Angeles", "Chicago", "Houston", "Phoenix", "San Francisco", "Seattle", "Austin"],
    "India": ["Mumbai", "Delhi", "Bengaluru", "Hyderabad", "Chennai", "Pune", "Kolkata"],
    "Germany": ["Berlin", "Munich", "Hamburg", "Frankfurt", "Cologne", "Stuttgart"],
    "United Kingdom": ["London", "Manchester", "Birmingham", "Leeds", "Glasgow", "Liverpool"],
    "Canada": ["Toronto", "Vancouver", "Montreal", "Calgary", "Ottawa"],
    "Australia": ["Sydney", "Melbourne", "Brisbane", "Perth", "Adelaide"]
}

genders = ["Male", "Female", "M", "F", "Femal", "Mle", "Non-Binary", "Other", "", "Unknown", None]

categories_products = {
    "Electronics": [
        ("Wireless Noise Canceling Headphones", 120.0, 350.0),
        ("Smartphone 5G 128GB", 400.0, 1100.0),
        ("4K Ultra HD Smart TV 55\"", 350.0, 900.0),
        ("Mechanical Gaming Keyboard", 45.0, 160.0),
        ("Bluetooth Portable Speaker", 25.0, 120.0),
        ("Smart Fitness Watch", 60.0, 280.0),
        ("USB-C Fast Charging Hub", 15.0, 45.0)
    ],
    "Clothing": [
        ("Classic Cotton Crewneck T-Shirt", 15.0, 40.0),
        ("Slim Fit Denim Jeans", 35.0, 95.0),
        ("Waterproof Winter Parka Jacket", 80.0, 250.0),
        ("Athletic Running Shoes", 50.0, 150.0),
        ("Merino Wool Casual Sweater", 40.0, 110.0),
        ("Formal Leather Dress Shoes", 60.0, 180.0)
    ],
    "Home & Kitchen": [
        ("Stainless Steel Espresso Machine", 150.0, 650.0),
        ("Non-Stick Ceramic Cookware Set 10pc", 75.0, 220.0),
        ("Robotic Vacuum Cleaner with LiDAR", 200.0, 550.0),
        ("Air Fryer Max XL 5.8Qt", 60.0, 160.0),
        ("Microfiber Queen Bedding Sheet Set", 25.0, 70.0)
    ],
    "Beauty & Personal Care": [
        ("Hydrating Hyaluronic Acid Serum", 18.0, 48.0),
        ("Ultrasonic Electric Toothbrush", 35.0, 90.0),
        ("Organic Argan Hair Care Oil", 12.0, 32.0),
        ("Luxury Fragrance Eau De Parfum 100ml", 60.0, 190.0)
    ],
    "Sports & Outdoors": [
        ("High-Density Non-Slip Yoga Mat", 18.0, 50.0),
        ("Adjustable Quick-Lock Dumbbells Set", 120.0, 380.0),
        ("Insulated Stainless Water Bottle 32oz", 15.0, 35.0),
        ("Ultralight Camping 2-Person Tent", 70.0, 210.0)
    ]
}

category_messy_variants = {
    "Electronics": ["Electronics", "ELECTRONICS", "electronics", "Eletronics", "electr."],
    "Clothing": ["Clothing", "Apparel & Clothing", "clothing", "CLOTHING"],
    "Home & Kitchen": ["Home & Kitchen", "home & kitchen", "Home and Kitchen", "Home"],
    "Beauty & Personal Care": ["Beauty & Personal Care", "Beauty", "beauty & care", "BEAUTY"],
    "Sports & Outdoors": ["Sports & Outdoors", "Sports", "sports & outdoors", "SPORTS"]
}

payment_methods = ["Credit Card", "credit_card", "PayPal", "Debit Card", "UPI", "Net Banking", "Cash on Delivery", "COD", "Crypto", None, ""]
tiers = ["Bronze", "Silver", "Gold", "Platinum", "VIP", None, "bronze", "SILVER"]
order_statuses = ["Delivered", "Delivered", "Delivered", "Delivered", "Shipped", "Processing", "Cancelled", "Refunded", "Returned", None]

# Generate a pool of 6,000 unique customers for realistic customer repeat purchase patterns
customer_pool = []
for i in range(1, 6001):
    c_id = f"CUST-{i:05d}"
    fn = random.choice(first_names)
    ln = random.choice(last_names)
    
    # 5% chance of missing email, 5% messy email, otherwise clean
    email_rand = random.random()
    if email_rand < 0.05:
        email = None
    elif email_rand < 0.10:
        email = f" {fn.lower()}.{ln.lower()}@@email.com "
    else:
        domains = ["gmail.com", "yahoo.com", "outlook.com", "icloud.com", "company.org", "hotmail.com"]
        email = f"{fn.lower()}.{ln.lower()}{random.randint(1, 999)}@{random.choice(domains)}"
    
    # Outliers in age: negative ages, extremely high ages (e.g. 150), missing age
    age_rand = random.random()
    if age_rand < 0.04:
        age = None
    elif age_rand < 0.05:
        age = -random.randint(1, 10)  # negative age
    elif age_rand < 0.06:
        age = random.randint(120, 160)  # outlier age
    else:
        age = random.randint(18, 75)
        
    gender = random.choice(genders)
    
    raw_country = random.choice(["USA", "India", "Germany", "United Kingdom", "Canada", "Australia"])
    country_alias = random.choice(["USA", "United States", "US"] if raw_country == "USA" else 
                                  ["India", "IND"] if raw_country == "India" else
                                  ["Germany", "DE"] if raw_country == "Germany" else
                                  ["United Kingdom", "UK"] if raw_country == "United Kingdom" else
                                  ["Canada", "CAN"] if raw_country == "Canada" else ["Australia", "AUS"])
    city = random.choice(cities_map[raw_country])
    if random.random() < 0.05:
        city = f"  {city.upper()}  " # whitespace & casing
    
    signup_year = random.choice([2020, 2021, 2022, 2023, 2024])
    signup_month = random.randint(1, 12)
    signup_day = random.randint(1, 28)
    signup_date = datetime.date(signup_year, signup_month, signup_day)
    
    tier = random.choice(tiers)
    
    customer_pool.append({
        "customer_id": c_id,
        "first_name": fn,
        "last_name": ln,
        "email": email,
        "age": age,
        "gender": gender,
        "country": country_alias,
        "city": city,
        "signup_date": signup_date,
        "membership_tier": tier
    })

fieldnames = [
    "order_id",
    "customer_id",
    "customer_name",
    "customer_email",
    "customer_age",
    "customer_gender",
    "customer_country",
    "customer_city",
    "customer_signup_date",
    "membership_tier",
    "order_date",
    "product_category",
    "product_name",
    "unit_price",
    "quantity",
    "discount_applied",
    "total_amount",
    "payment_method",
    "order_status",
    "delivery_time_days",
    "customer_rating",
    "returns_flag"
]

rows = []
start_date = datetime.date(2022, 1, 1)

for i in range(1, TOTAL_ROWS + 1):
    order_id = f"ORD-{2022 + random.randint(0, 3)}-{i:06d}"
    cust = random.choice(customer_pool)
    
    # Order date must generally be after signup date, but 1% corrupted before signup
    days_after = random.randint(0, 750)
    if random.random() < 0.01:
        o_date = cust["signup_date"] - datetime.timedelta(days=random.randint(5, 100))
    else:
        o_date = cust["signup_date"] + datetime.timedelta(days=days_after)
    
    # Date formatting inconsistency
    d_fmt_choice = random.random()
    if d_fmt_choice < 0.60:
        order_date_str = o_date.strftime("%Y-%m-%d") # 2023-04-15
    elif d_fmt_choice < 0.80:
        order_date_str = o_date.strftime("%d/%m/%Y") # 15/04/2023
    elif d_fmt_choice < 0.93:
        order_date_str = o_date.strftime("%B %d, %Y") # April 15, 2023
    elif d_fmt_choice < 0.98:
        order_date_str = o_date.strftime("%m-%d-%Y") # 04-15-2023
    else:
        order_date_str = random.choice(["invalid_date", "2099-99-99", "N/A", ""])
        
    signup_date_str = cust["signup_date"].strftime("%Y-%m-%d") if random.random() > 0.05 else "NULL"
    
    # Category and product
    cat = random.choice(list(categories_products.keys()))
    messy_cat = random.choice(category_messy_variants[cat])
    prod_tuple = random.choice(categories_products[cat])
    prod_name = prod_tuple[0]
    base_price = round(random.uniform(prod_tuple[1], prod_tuple[2]), 2)
    
    # Quantity with outliers
    q_rand = random.random()
    if q_rand < 0.02:
        quantity = -random.randint(1, 3) # negative quantity
    elif q_rand < 0.03:
        quantity = random.randint(500, 9999) # absurd wholesale quantity
    elif q_rand < 0.05:
        quantity = None # missing
    else:
        quantity = random.choices([1, 2, 3, 4, 5, 8], weights=[55, 25, 10, 5, 3, 2])[0]
        
    # Unit price formatting inconsistency (strings with $, commas, EUR, or clean float)
    p_rand = random.random()
    if p_rand < 0.15:
        unit_price_val = f"${base_price:,.2f}"
    elif p_rand < 0.20:
        unit_price_val = f"USD {base_price:.2f}"
    elif p_rand < 0.23:
        unit_price_val = f"€{base_price:.2f}"
    elif p_rand < 0.26:
        unit_price_val = f"  {base_price}  "
    elif p_rand < 0.28:
        unit_price_val = -base_price # negative price error
    elif p_rand < 0.30:
        unit_price_val = "missing"
    else:
        unit_price_val = base_price

    # Discount (0% to 40%)
    discount_pct = random.choices([0.0, 0.05, 0.10, 0.15, 0.20, 0.25, 0.35, 0.50], weights=[45, 15, 15, 10, 8, 4, 2, 1])[0]
    # Sometimes discount is string with '%' or null
    d_style = random.random()
    if d_style < 0.10:
        discount_str = f"{int(discount_pct * 100)}%"
    elif d_style < 0.15:
        discount_str = None
    elif d_style < 0.18:
        discount_str = "?"
    else:
        discount_str = discount_pct

    # Total amount calculation (deliberately miscalculated in 3% of cases for verification practice)
    qty_num = quantity if (isinstance(quantity, (int, float)) and quantity > 0) else 1
    calculated_total = round(base_price * qty_num * (1 - discount_pct), 2)
    if random.random() < 0.04:
        calculated_total = round(calculated_total * random.uniform(1.2, 2.5), 2) # discrepancy
    
    t_style = random.random()
    if t_style < 0.12:
        total_str = f"${calculated_total:,.2f}"
    elif t_style < 0.15:
        total_str = "N/A"
    else:
        total_str = calculated_total
        
    # Delivery time in days
    status = random.choice(order_statuses)
    if status in ["Cancelled"]:
        delivery_days = None
    else:
        deliv_rand = random.random()
        if deliv_rand < 0.05:
            delivery_days = random.randint(-5, 0) # negative delivery time anomaly
        elif deliv_rand < 0.08:
            delivery_days = random.randint(60, 150) # extreme delay
        elif deliv_rand < 0.15:
            delivery_days = None
        else:
            delivery_days = random.randint(1, 14)
            
    # Rating 1 to 5
    rating_rand = random.random()
    if rating_rand < 0.25:
        rating = None # many unrated
    elif rating_rand < 0.27:
        rating = random.choice([0, 6, 10]) # invalid ratings
    else:
        rating = random.choices([1, 2, 3, 4, 5], weights=[6, 7, 15, 32, 40])[0]

    # Returns flag (target variable candidate)
    if status in ["Returned", "Refunded"]:
        returned = 1
    elif status == "Cancelled":
        returned = None
    else:
        returned = 1 if random.random() < 0.08 else 0

    full_name = f"{cust['first_name']} {cust['last_name']}"
    if random.random() < 0.08:
        full_name = f"{cust['first_name'].lower()} {cust['last_name'].upper()}"

    row = {
        "order_id": order_id,
        "customer_id": cust["customer_id"],
        "customer_name": full_name,
        "customer_email": cust["email"],
        "customer_age": cust["age"],
        "customer_gender": cust["gender"],
        "customer_country": cust["country"],
        "customer_city": cust["city"],
        "customer_signup_date": signup_date_str,
        "membership_tier": cust["membership_tier"],
        "order_date": order_date_str,
        "product_category": messy_cat,
        "product_name": prod_name,
        "unit_price": unit_price_val,
        "quantity": quantity,
        "discount_applied": discount_str,
        "total_amount": total_str,
        "payment_method": random.choice(payment_methods),
        "order_status": status,
        "delivery_time_days": delivery_days,
        "customer_rating": rating,
        "returns_flag": returned
    }
    rows.append(row)

# Inject intentional duplicate rows (exact duplicate transactions)
num_dupes = 350
for _ in range(num_dupes):
    chosen_row = dict(random.choice(rows))
    rows.append(chosen_row)

random.shuffle(rows)

output_path = r"C:\Users\piyus\.gemini\antigravity\scratch\data_analysis_practice\ecommerce_customer_churn_practice.csv"

with open(output_path, mode="w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(rows)

print(f"Successfully generated {len(rows)} records into: {output_path}")
