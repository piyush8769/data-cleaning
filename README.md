# E-Commerce Data Cleaning, Manipulation & Feature Engineering (Jupyter Notebook)

A complete, beginner-friendly **Jupyter Notebook (`.ipynb`)** data analysis project for real-world messy e-commerce transaction data.

This project demonstrates **how to find**, **how to resolve**, and **how to engineer features** across 15 modular, well-commented blocks without nested or overly complex one-liners.

---

## 📁 Repository Contents

* **[`data_cleaning_and_feature_engineering.ipynb`](data_cleaning_and_feature_engineering.ipynb)**: The interactive Jupyter Notebook with markdown explanation cells and executed code output cells.
* `ecommerce_customer_data.csv`: The raw dataset (35,000+ rows) with intentional real-world anomalies, messy strings, and mixed date formats.
* `ecommerce_cleaned_and_engineered.csv`: The final cleaned and feature-engineered dataset ready for analytics/ML models.
* `generate_dataset.py`: Python script used to generate the dataset.

---

## 🛠️ Notebook Structure & Steps

Each step is an isolated cell addressing a single problem with clear diagnostic logic:

### Phase 1: Data Cleaning
1. **Deduplication:** Find exact duplicate rows using `df.duplicated()` and remove them with `df.drop_duplicates()`.
2. **Text Standardization:** Fix irregular capitalization, whitespace, and typos (`Eletronics` $\to$ `Electronics`).
3. **Country Standardizations:** Map abbreviated country codes (`US`, `IND`, `DE`) to unified country names.
4. **Demographic Cleaning:** Standardize gender labels and membership loyalty tiers.
5. **Currency & Numeric Casting:** Strip currency symbols (`$`, `€`, `USD`) and commas from price columns, and convert to `float64`.
6. **Discount Handling:** Convert mixed percentage representations (`"15%"`, `0.15`, `"?"`) to decimal floats.
7. **Date Parsing:** Handle multi-format dates (`YYYY-MM-DD`, `DD/MM/YYYY`, `Month Day, Year`) with `errors='coerce'`.
8. **Outlier & Logical Anomaly Treatment:**
   * Filter impossible human ages ($<18$ or $>100$).
   * Filter negative purchase quantities.
   * Re-calculate corrupted total amounts using unit price, quantity, and discount.

### Phase 2: Data Manipulation & Aggregations
9. **Customer-Level Aggregations:** Group by customer to calculate total spend, order count, average order value (AOV), and customer lifespan.
10. **Accounting Discrepancy Check:** Compare recorded `total_amount` against formula calculation to isolate billing errors.

### Phase 3: Feature Engineering
11. **Date & Temporal Features:** Extract `order_year`, `order_month`, `day_of_week`, `is_weekend`, and `days_as_customer`.
12. **RFM Metrics:** Derive customer Recency (days since last purchase), Frequency (total orders), and Monetary value (total spend).
13. **Text / Domain Extraction:** Parse email domains and flag corporate vs. personal webmail buyers.
14. **Discretization & Encoding:**
    * Age bracket binning: `18-25`, `26-35`, `36-50`, `50+`.
    * Ordinal encoding for loyalty tier (`Bronze` $\to 1$, `Silver` $\to 2$, `Gold` $\to 3$, `Platinum` $\to 4$).
    * One-Hot Encoding (`pd.get_dummies`) for payment methods.
15. **Save Clean Output:** Export to `ecommerce_cleaned_and_engineered.csv`.

---

## 🚀 How to Open and Run

You can view the notebook directly in GitHub, or open it in Jupyter Lab / VS Code / Google Colab:

```bash
# 1. Clone repository
git clone https://github.com/piyush8769/data-cleaning.git
cd data-cleaning

# 2. Launch Jupyter
jupyter notebook data_cleaning_and_feature_engineering.ipynb
```

---

## 📊 Results Summary

* **Initial Data:** 35,350 rows $\times$ 22 columns
* **Removed Duplicates:** 350 exact duplicate rows
* **Cleaned Rows Remaining:** 34,296 valid rows
* **Final Output Features:** 45 columns (including RFM, dummy variables, date parts, and domain tags)
