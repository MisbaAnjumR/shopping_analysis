import pandas as pd
from sqlalchemy import create_engine

def main():
    print("Loading dataset...")
    df = pd.read_csv('dataset.csv')

    print("\n--- Dataset Info ---")
    df.info()

    print("\n--- Summary Statistics ---")
    print(df.describe(include='all'))

    print("\n--- Missing Values Before Cleaning ---")
    print(df.isnull().sum())

    # Imputing missing values in Review Rating column with the median rating of the product category
    df['Review Rating'] = df.groupby('Category')['Review Rating'].transform(lambda x: x.fillna(x.median()))

    print("\n--- Missing Values After Cleaning ---")
    print(df.isnull().sum())

    # Renaming columns according to snake casing for better readability and documentation
    df.columns = df.columns.str.lower()
    df.columns = df.columns.str.replace(' ','_')
    df = df.rename(columns={'purchase_amount_(usd)':'purchase_amount'})

    # create a new column age_group
    labels = ['Young Adult', 'Adult', 'Middle-aged', 'Senior']
    df['age_group'] = pd.qcut(df['age'], q=4, labels=labels)

    # create new column purchase_frequency_days
    frequency_mapping = {
        'Fortnightly': 14,
        'Weekly': 7,
        'Monthly': 30,
        'Quarterly': 90,
        'Bi-Weekly': 14,
        'Annually': 365,
        'Every 3 Months': 90
    }
    df['purchase_frequency_days'] = df['frequency_of_purchases'].map(frequency_mapping)

    # Dropping promo code used column (since it's identical to discount_applied)
    if 'promo_code_used' in df.columns:
        df = df.drop('promo_code_used', axis=1)

    print("\n--- Final Cleaned Dataset Columns ---")
    print(df.columns.tolist())

    print("\nSaving cleaned data to SQLite Database ('customer_behavior.db')...")
    engine = create_engine('sqlite:///customer_behavior.db')
    df.to_sql('customer', engine, if_exists='replace', index=False)
    
    print("\nData successfully saved! Reading top 5 rows back from database to verify:")
    print(pd.read_sql('SELECT * FROM customer LIMIT 5;', engine))

if __name__ == "__main__":
    main()
