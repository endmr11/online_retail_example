# Online Retail Analizi

Bu proje, online perakende satış verilerinin analizi ve müşteri segmentasyonu için geliştirilmiş bir Python uygulamasıdır.

## Özellikler

- Veri yükleme ve temizleme
- Aylık satış trendi analizi
- En çok satılan ürünlerin analizi
- RFM (Recency, Frequency, Monetary) analizi
- Müşteri segmentasyonu
- Görselleştirme ve raporlama

## Gereksinimler

- Python 3.8+
- pandas
- matplotlib
- seaborn
- openpyxl

## Kurulum

1. Projeyi klonlayın:
```bash
git clone https://github.com/yourusername/online_retail_example.git
cd online_retail_example
```

2. Gerekli paketleri yükleyin:
```bash
pip install -r requirements.txt
```

## Kullanım

1. Veri setini `online_retail.xlsx` formatında proje dizinine yerleştirin.

2. Programı çalıştırın:
```bash
python main.py
```

Program çalıştığında:
- Veri seti yüklenir ve temizlenir
- Aylık satış trendi analizi yapılır ve görselleştirilir
- En çok satılan ürünler analiz edilir ve görselleştirilir
- RFM analizi yapılır ve müşteriler segmentlere ayrılır
- Sonuçlar konsola yazdırılır ve grafikler kaydedilir

## Çıktılar

Program çalıştığında aşağıdaki çıktılar üretilir:
- `monthly_sales.png`: Aylık satış trendi grafiği
- `top_products.png`: En çok satılan ürünler grafiği
- Konsol çıktısı: Müşteri segmentleri dağılımı

## Müşteri Segmentleri

Program, müşterileri aşağıdaki segmentlere ayırır:
- Champions: En değerli müşteriler (RFM skoru: 555)
- Loyal Customers: Sadık müşteriler (RFM skoru: 5xx)
- Big Spenders: Yüksek harcama yapan müşteriler (RFM skoru: xx5)
- Hibernating: Uzun süredir alışveriş yapmayan müşteriler (RFM skoru: 1xx)
- Others: Diğer müşteriler
