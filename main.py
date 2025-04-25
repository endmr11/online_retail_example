import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
from typing import Dict, List, Tuple
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
log = logging.getLogger(__name__)

SEGMENTS = {
    '555': 'Champions',
    '5': 'Loyal Customers',
    '5': 'Big Spenders',
    '1': 'Hibernating'
}

def load_data(file_path: str) -> pd.DataFrame:
    try:
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Dosya bulunamadı: {file_path}")
        
        data = pd.read_excel(file_path, engine='openpyxl')
        
        if data.empty:
            raise ValueError("Veri seti boş!")
            
        log.info(f"Veri seti başarıyla yüklendi. Boyut: {data.shape}")
        return data
    except Exception as e:
        log.error(f"Veri yükleme hatası: {str(e)}")
        raise

def clean_data(data: pd.DataFrame) -> pd.DataFrame:
    data = data.dropna(subset=['Customer ID'])
    
    data = data[(data["Quantity"] > 0) & (data["Price"] > 0)]
    
    data = data.reset_index(drop=True)
    
    data["TotalPrice"] = data["Quantity"] * data["Price"]
    
    data['InvoiceDate'] = pd.to_datetime(data['InvoiceDate'])
    data["Year"] = data["InvoiceDate"].dt.year
    data["Month"] = data["InvoiceDate"].dt.month
    data["Day"] = data["InvoiceDate"].dt.day
    data["Weekday"] = data["InvoiceDate"].dt.day_name()
    
    log.info("Veri temizleme işlemleri tamamlandı")
    return data

def analyze_monthly_sales(df: pd.DataFrame) -> pd.DataFrame:
    monthly_sales = df.groupby(["Year", "Month"])["TotalPrice"].sum().reset_index()
    monthly_sales["Date"] = pd.to_datetime(monthly_sales[["Year", "Month"]].assign(DAY=1))
    return monthly_sales

def plot_monthly_sales(monthly_sales: pd.DataFrame, save_path: str = None):
    plt.figure(figsize=(12,6))
    sns.lineplot(data=monthly_sales, x="Date", y="TotalPrice", marker='o')
    plt.title("Aylık Toplam Satış Trendi")
    plt.xlabel("Tarih")
    plt.ylabel("Toplam Satış (£)")
    plt.grid(True)
    plt.tight_layout()
    if save_path:
        plt.savefig(save_path)
    plt.show()

def analyze_top_products(df: pd.DataFrame, n: int = 10) -> pd.Series:
    return df.groupby("Description")["Quantity"].sum().sort_values(ascending=False).head(n)

def plot_top_products(top_products: pd.Series, save_path: str = None):
    plt.figure(figsize=(12,6))
    sns.barplot(x=top_products.values, y=top_products.index, palette="viridis")
    plt.title("En Çok Satılan 10 Ürün (Adet Bazlı)")
    plt.xlabel("Toplam Satış Adedi")
    plt.ylabel("Ürün")
    plt.tight_layout()
    if save_path:
        plt.savefig(save_path)
    plt.show()

def perform_rfm_analysis(df: pd.DataFrame) -> pd.DataFrame:
    ref_date = df["InvoiceDate"].max() + pd.Timedelta(days=1)
    
    rfm = df.groupby("Customer ID").agg({
        "InvoiceDate": lambda x: (ref_date - x.max()).days,
        "Invoice": "nunique",
        "TotalPrice": "sum"
    }).reset_index()
    
    rfm.columns = ["Customer ID", "Recency", "Frequency", "Monetary"]
    
    rfm["R_Score"] = pd.qcut(rfm["Recency"], 5, labels=[5,4,3,2,1])
    rfm["F_Score"] = pd.qcut(rfm["Frequency"].rank(method='first'), 5, labels=[1,2,3,4,5])
    rfm["M_Score"] = pd.qcut(rfm["Monetary"], 5, labels=[1,2,3,4,5])
    
    rfm["RFM_Score"] = rfm["R_Score"].astype(str) + rfm["F_Score"].astype(str) + rfm["M_Score"].astype(str)
    
    return rfm

def segment_customers(rfm: pd.DataFrame) -> pd.DataFrame:
    def segment(rfm_score):
        if rfm_score == '555':
            return 'Champions'
        elif rfm_score.startswith('5'):
            return 'Loyal Customers'
        elif rfm_score.endswith('5'):
            return 'Big Spenders'
        elif rfm_score[0] == '1':
            return 'Hibernating'
        else:
            return 'Others'
    
    rfm["Segment"] = rfm["RFM_Score"].apply(segment)
    return rfm

def main():
    try:
        data = load_data("online_retail.xlsx")
        
        data = clean_data(data)
        
        monthly_sales = analyze_monthly_sales(data)
        plot_monthly_sales(monthly_sales, "monthly_sales.png")
        
        top_products = analyze_top_products(data)
        plot_top_products(top_products, "top_products.png")
        
        rfm = perform_rfm_analysis(data)
        rfm = segment_customers(rfm)
        
        print("\nMüşteri Segmentleri Dağılımı:")
        print(rfm["Segment"].value_counts())
        
    except Exception as e:
        log.error(f"Program çalıştırılırken hata oluştu: {str(e)}")
        raise

if __name__ == "__main__":
    main()
