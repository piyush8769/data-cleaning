"""
================================================================================
E-COMMERCE DATA CLEANING, MANIPULATION & FEATURE ENGINEERING
Author: Piyush (piyush8769)
Description:
    A step-by-step data analysis pipeline designed for learning.
    Each block addresses a single problem with clear, simple pandas methods
    and explanatory comments.
================================================================================
"""

import pandas as pd
import numpy as np


# ==============================================================================
# BLOCK 0: LOAD DATASET AND INSPECT
# ==============================================================================
# In this block, we read the raw CSV file and check its shape and column names.
file_name = "ecommerce_customer_data.csv"
df = pd.read_csv(file_name)

print("=" * 70)
print(f"BLOCK 0: Successfully loaded dataset.")
print(f"Initial Shape: {df.shape[0]} rows, {df.shape[1]} columns")
print("=" * 70)


# ==============================================================================
# BLOCK 1: FIND AND REMOVE DUPLICATE ROWS
# ==============================================================================
# Why: Duplicate orders can artificially inflate total revenue and customer counts.
# How to find: df.duplicated().sum()
# How to resolve: df.drop_duplicates()

num_duplicates = df.duplicated().sum()
print(f"\n[Block 1] Found {num_duplicates} exact duplicate rows.")

# Remove the duplicates and keep the first occurrence
df = df.drop_duplicates()
print(f"[Block 1] Rows after removing duplicates: {len(df)}")


# ==============================================================================
# BLOCK 2: STANDARDIZE TEXT (PRODUCT CATEGORIES)
# ==============================================================================
# Why: Same categories are entered in mixed cases or typos (e.g., 'Eletronics', 'ELECTR.')
# How to find: df['product_category'].value_counts()
# How to resolve: Strip whitespace, convert to title case, and replace typos.

# Step 2a: Strip whitespace and format to Title Case
df['product_category'] = df['product_category'].astype(str).str.strip().str.title()

# Step 2b: Create a dictionary to map typos to clean names
category_corrections = {
    'Eletronics': 'Electronics',
    'Electr.': 'Electronics',
    'Apparel & Clothing': 'Clothing',
    'Home And Kitchen': 'Home & Kitchen',
    'Home': 'Home & Kitchen',
    'Beauty & Care': 'Beauty & Personal Care',
    'Beauty': 'Beauty & Personal Care',
    'Sports': 'Sports & Outdoors'
}

# Step 2c: Replace the typos
df['product_category'] = df['product_category'].replace(category_corrections)
print(f"\n[Block 2] Cleaned Product Categories:\n{df['product_category'].value_counts()}")


# ==============================================================================
# BLOCK 3: STANDARDIZE COUNTRY NAMES
# ==============================================================================
# Why: Countries are entered as abbreviations ('US', 'IND') or full names ('United States').
# How to find: df['customer_country'].value_counts()
# How to resolve: Replace all variations with consistent country codes/names.

df['customer_country'] = df['customer_country'].astype(str).str.strip()

country_corrections = {
    'US': 'USA',
    'United States': 'USA',
    'U.S.A.': 'USA',
    'IND': 'India',
    'DE': 'Germany',
    'UK': 'United Kingdom',
    'CAN': 'Canada',
    'AUS': 'Australia'
}

df['customer_country'] = df['customer_country'].replace(country_corrections)
print(f"\n[Block 3] Cleaned Countries:\n{df['customer_country'].value_counts()}")


# ==============================================================================
# BLOCK 4: STANDARDIZE GENDER AND MEMBERSHIP TIER
# ==============================================================================
# Why: Contains typos like 'Mle', 'Femal', and unstandardized loyalty tier casings.
# How to resolve: Use simple dictionary mappings and replace invalid placeholders with NaN.

gender_corrections = {
    'M': 'Male',
    'Mle': 'Male',
    'F': 'Female',
    'Femal': 'Female',
    '': np.nan,
    'Unknown': np.nan,
    'None': np.nan
}
df['customer_gender'] = df['customer_gender'].replace(gender_corrections)

# Clean Membership Tier: capital case, map 'VIP' to 'Platinum'
df['membership_tier'] = df['membership_tier'].astype(str).str.strip().str.capitalize()
df['membership_tier'] = df['membership_tier'].replace({'None': np.nan, 'Nan': np.nan, 'Vip': 'Platinum'})
print(f"\n[Block 4] Cleaned Membership Tiers:\n{df['membership_tier'].value_counts(dropna=False)}")


# ==============================================================================
# BLOCK 5: CLEAN CURRENCY COLUMNS (unit_price & total_amount)
# ==============================================================================
# Why: Prices contain '$', '€', 'USD', and text like 'missing' or 'N/A'.
# How to resolve: Remove symbols, convert to numeric, and fix negative signs.

# Step 5a: Clean unit_price
df['unit_price'] = df['unit_price'].astype(str)
df['unit_price'] = df['unit_price'].str.replace('$', '', regex=False)
df['unit_price'] = df['unit_price'].str.replace('€', '', regex=False)
df['unit_price'] = df['unit_price'].str.replace('USD', '', regex=False)
df['unit_price'] = df['unit_price'].str.replace(',', '', regex=False)
df['unit_price'] = df['unit_price'].str.strip()
df['unit_price'] = pd.to_numeric(df['unit_price'], errors='coerce')

# Fix negative price errors to positive
df['unit_price'] = df['unit_price'].abs()

# Step 5b: Clean total_amount
df['total_amount'] = df['total_amount'].astype(str)
df['total_amount'] = df['total_amount'].str.replace('$', '', regex=False)
df['total_amount'] = df['total_amount'].str.replace('€', '', regex=False)
df['total_amount'] = df['total_amount'].str.replace('USD', '', regex=False)
df['total_amount'] = df['total_amount'].str.replace(',', '', regex=False)
df['total_amount'] = df['total_amount'].str.replace('N/A', '', regex=False)
df['total_amount'] = df['total_amount'].str.strip()
df['total_amount'] = pd.to_numeric(df['total_amount'], errors='coerce')

print(f"\n[Block 5] Cleaned Price Columns:")
print(f"Average Unit Price: ${df['unit_price'].mean():.2f}")
print(f"Average Total Amount: ${df['total_amount'].mean():.2f}")


# ==============================================================================
# BLOCK 6: CLEAN DISCOUNT PERCENTAGES
# ==============================================================================
# Why: discount_applied contains numbers (0.15), percentage strings ('15%'), and '?'.
# How to resolve: Clean each entry into a standard decimal (0.0 to 1.0).

def fix_discount_value(value):
    # If missing or unknown, return 0.0
    if pd.isna(value) or str(value).strip() in ['?', 'None', 'nan', '']:
        return 0.0
    text = str(value).replace('%', '').strip()
    try:
        number = float(text)
        # If entered as whole percentage (e.g. 15), convert to decimal (0.15)
        if number > 1.0:
            return number / 100.0
        return number
    except ValueError:
        return 0.0

df['discount_applied'] = df['discount_applied'].apply(fix_discount_value)
print(f"\n[Block 6] Cleaned Discounts. Max discount: {df['discount_applied'].max():.2f}, Min: {df['discount_applied'].min():.2f}")


# ==============================================================================
# BLOCK 7: PARSE DATES AND DROP INVALID DATES
# ==============================================================================
# Why: Dates have mixed formats ('YYYY-MM-DD', 'DD/MM/YYYY', 'April 15, 2023') and invalid text.
# How to resolve: pd.to_datetime with errors='coerce'.

df['order_date'] = pd.to_datetime(df['order_date'], errors='coerce', format='mixed')
df['customer_signup_date'] = pd.to_datetime(df['customer_signup_date'], errors='coerce')

# Drop rows where the order date is corrupted or missing
initial_len = len(df)
df = df.dropna(subset=['order_date'])
print(f"\n[Block 7] Parsed Dates. Dropped {initial_len - len(df)} rows with unparseable order dates.")


# ==============================================================================
# BLOCK 8: HANDLE NUMERICAL OUTLIERS AND ANOMALIES
# ==============================================================================
# Why: Real data contains negative ages (-5), unrealistic ages (150), and negative quantities.
# How to resolve: Replace impossible numbers with NaN, impute reasonable defaults.

# Step 8a: Handle Age anomalies (valid realistic range: 18 to 100)
df.loc[(df['customer_age'] < 18) | (df['customer_age'] > 100), 'customer_age'] = np.nan

# Step 8b: Handle Quantity anomalies (valid range: 1 to 50 items)
df.loc[(df['quantity'] <= 0) | (df['quantity'] > 100), 'quantity'] = np.nan
# Impute missing quantity with default 1.0
df['quantity'] = df['quantity'].fillna(1.0)

# Step 8c: Handle delivery days and ratings
df.loc[df['delivery_time_days'] < 0, 'delivery_time_days'] = np.nan
df.loc[(df['customer_rating'] < 1) | (df['customer_rating'] > 5), 'customer_rating'] = np.nan

# Step 8d: Re-calculate missing total_amount where missing
expected_total = df['unit_price'] * df['quantity'] * (1 - df['discount_applied'])
df['total_amount'] = df['total_amount'].fillna(expected_total.round(2))

print(f"\n[Block 8] Outlier handling complete. Total clean rows: {len(df)}")


# ==============================================================================
# BLOCK 9: DATA MANIPULATION - CUSTOMER-LEVEL AGGREGATION
# ==============================================================================
# Why: Analysts need customer summary metrics to understand customer lifetime behavior.
# How: Group by customer_id and aggregate spend, order count, and dates.

customer_summary = df.groupby('customer_id').agg(
    total_spend=('total_amount', 'sum'),
    total_orders=('order_id', 'nunique'),
    avg_order_value=('total_amount', 'mean'),
    first_order=('order_date', 'min'),
    last_order=('order_date', 'max')
).reset_index()

# Calculate customer lifespan in days
customer_summary['customer_lifespan_days'] = (
    customer_summary['last_order'] - customer_summary['first_order']
).dt.days

print(f"\n[Block 9] Customer Aggregation complete for {len(customer_summary)} unique customers:")
print(customer_summary.head(3))


# ==============================================================================
# BLOCK 10: AUDIT DISCREPANCIES (ACCOUNTING CHECK)
# ==============================================================================
# Why: Check if the recorded total_amount matches price * quantity * (1 - discount).

df['calculated_total'] = (df['unit_price'] * df['quantity'] * (1 - df['discount_applied'])).round(2)
df['price_difference'] = (df['total_amount'] - df['calculated_total']).round(2)

discrepancy_count = (df['price_difference'].abs() > 1.0).sum()
print(f"\n[Block 10] Audit Check: Found {discrepancy_count} orders where recorded price differed from formula.")


# ==============================================================================
# BLOCK 11: FEATURE ENGINEERING - DATE & TIME FEATURES
# ==============================================================================
# Why: Day of week, month, and weekend status help detect seasonal purchasing habits.

# Extract components from order_date
df['order_year'] = df['order_date'].dt.year
df['order_month'] = df['order_date'].dt.month
df['order_day'] = df['order_date'].dt.day
df['day_of_week'] = df['order_date'].dt.day_name()

# Weekend flag: 1 if Saturday or Sunday, else 0
df['is_weekend'] = df['order_date'].dt.dayofweek.isin([5, 6]).astype(int)

# Customer tenure in days at the time of placing this order
df['days_as_customer'] = (df['order_date'] - df['customer_signup_date']).dt.days
# Clean negative values if order date was before signup date
df['days_as_customer'] = df['days_as_customer'].clip(lower=0)

print("\n[Block 11] Added Date Features (year, month, day_of_week, is_weekend, days_as_customer).")


# ==============================================================================
# BLOCK 12: FEATURE ENGINEERING - RFM METRICS
# ==============================================================================
# Why: Recency, Frequency, and Monetary value are core metrics for customer segmentation.

# Reference date = 1 day after the latest order in data
snapshot_date = df['order_date'].max() + pd.Timedelta(days=1)

# Calculate RFM per customer
rfm = df.groupby('customer_id').agg(
    recency_days=('order_date', lambda x: (snapshot_date - x.max()).days),
    frequency_orders=('order_id', 'nunique'),
    monetary_spend=('total_amount', 'sum')
).reset_index()

# Merge RFM features back to the main dataframe
df = df.merge(rfm, on='customer_id', how='left')
print("\n[Block 12] Merged RFM features (recency_days, frequency_orders, monetary_spend).")


# ==============================================================================
# BLOCK 13: FEATURE ENGINEERING - EMAIL DOMAIN EXTRACTION
# ==============================================================================
# Why: Distinguish corporate customers from public free-email users.

def get_email_domain(email):
    if pd.isna(email) or '@' not in str(email):
        return 'unknown'
    return str(email).split('@')[-1].strip().lower()

df['email_domain'] = df['customer_email'].apply(get_email_domain)

# Corporate email flag
public_email_services = ['gmail.com', 'yahoo.com', 'outlook.com', 'hotmail.com', 'icloud.com', 'unknown']
df['is_corporate_email'] = (~df['email_domain'].isin(public_email_services)).astype(int)

print(f"\n[Block 13] Extracted email domains. Corporate email percentage: {df['is_corporate_email'].mean() * 100:.2f}%")


# ==============================================================================
# BLOCK 14: FEATURE ENGINEERING - BINNING & ENCODING
# ==============================================================================
# Why: Group ages into readable demographic groups and convert categories to numbers.

# Step 14a: Age binning
age_bins = [0, 25, 35, 50, 100]
age_labels = ['18-25', '26-35', '36-50', '50+']
df['age_group'] = pd.cut(df['customer_age'], bins=age_bins, labels=age_labels, right=True)

# Step 14b: Ordinal encoding for Membership Tier (Bronze=1, Silver=2, Gold=3, Platinum=4)
tier_map = {'Bronze': 1, 'Silver': 2, 'Gold': 3, 'Platinum': 4}
df['membership_tier_score'] = df['membership_tier'].map(tier_map).fillna(0).astype(int)

# Step 14c: One-Hot Encoding for Payment Method
payment_dummies = pd.get_dummies(df['payment_method'], prefix='pay', drop_first=True, dtype=int)
df = pd.concat([df, payment_dummies], axis=1)

print("\n[Block 14] Added Age Groups, Tier Scores, and Payment Method Dummy Variables.")


# ==============================================================================
# BLOCK 15: SAVE CLEANED & ENGINEERED DATASET
# ==============================================================================
output_file = "ecommerce_cleaned_and_engineered.csv"
df.to_csv(output_file, index=False)

print("\n" + "=" * 70)
print(f"BLOCK 15: Pipeline Completed Successfully!")
print(f"Final Cleaned Dataset Shape: {df.shape[0]} rows, {df.shape[1]} columns")
print(f"Cleaned dataset saved as: {output_file}")
print("=" * 70)
