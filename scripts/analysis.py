import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# 设置绘图风格
sns.set_style('whitegrid')

# 确保目标文件夹存在
output_dir = '../data'
if not os.path.exists(output_dir):
    os.makedirs(output_dir)
figures_dir = '../output/figures'
if not os.path.exists(figures_dir):
    os.makedirs(figures_dir)

# 步骤 1：加载和清洗数据
df = pd.read_csv('../data/Online_Retail.csv')
df = df.dropna(subset=['CustomerID'])
df = df[~df['InvoiceNo'].str.startswith('C')]
df = df[(df['Quantity'] > 0) & (df['UnitPrice'] > 0)]
df['InvoiceDate'] = pd.to_datetime(df['InvoiceDate'])
df['CustomerID'] = df['CustomerID'].astype(int)
df['TotalPrice'] = df['Quantity'] * df['UnitPrice']
df.to_csv(os.path.join(output_dir, 'cleaned_retail.csv'), index=False)
print("清洗后数据规模：", df.shape)

# 步骤 2：月度 GMV 趋势
df['Month'] = df['InvoiceDate'].dt.to_period('M')
monthly_gmv = df.groupby('Month')['TotalPrice'].sum()
plt.figure(figsize=(12, 6))
monthly_gmv.plot(kind='line', marker='o')
plt.title('Monthly GMV Trend')
plt.xlabel('Month')
plt.ylabel('GMV (GBP)')
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig(os.path.join(figures_dir, 'monthly_gmv_trend.png'))
plt.show()

# 步骤 3：货币价值分布
rfm = df.groupby('CustomerID')['TotalPrice'].sum().reset_index(name='Monetary')
plt.figure(figsize=(10, 6))
plt.hist(rfm['Monetary'], bins=30, edgecolor='black')
plt.title('Monetary Value Distribution')
plt.xlabel('Monetary (GBP)')
plt.ylabel('Count')
plt.tight_layout()
plt.savefig(os.path.join(figures_dir, 'monetary_distribution.png'))
plt.show()

# 步骤 4：畅销商品
top_products = df.groupby('Description').agg({
    'TotalPrice': 'sum',
    'Quantity': 'sum'
}).sort_values('TotalPrice', ascending=False).head(10)
top_products['Avg_Price'] = top_products['TotalPrice'] / top_products['Quantity']
print("Top 10 Products:\n", top_products)
plt.figure(figsize=(10, 6))
top_products['TotalPrice'].plot(kind='barh')
plt.title('Top 10 Products by Sales')
plt.xlabel('Sales (GBP)')
plt.ylabel('Product')
plt.gca().invert_yaxis()
plt.tight_layout()
plt.savefig(os.path.join(figures_dir, 'top_10_products.png'))
plt.show()

# 步骤 5：RFM 客户分群
current_date = df['InvoiceDate'].max() + pd.Timedelta(days=1)
rfm = df.groupby('CustomerID').agg({
    'InvoiceDate': lambda x: (current_date - x.max()).days,
    'InvoiceNo': 'nunique',
    'TotalPrice': 'sum'
}).rename(columns={
    'InvoiceDate': 'Recency',
    'InvoiceNo': 'Frequency',
    'TotalPrice': 'Monetary'
})
rfm['R_Score'] = pd.qcut(rfm['Recency'], 5, labels=[5, 4, 3, 2, 1])
rfm['F_Score'] = pd.qcut(rfm['Frequency'].rank(method='first'), 5, labels=[1, 2, 3, 4, 5])
rfm['M_Score'] = pd.qcut(rfm['Monetary'], 5, labels=[1, 2, 3, 4, 5])
rfm['RFM_Score'] = rfm['R_Score'].astype(str) + rfm['F_Score'].astype(str) + rfm['M_Score'].astype(str)
high_value = rfm[rfm['RFM_Score'] == '555']
print(f"高价值客户数: {len(high_value)}")

# 步骤 6：12 月数据完整性
december_data = df[df['InvoiceDate'].dt.month == 12]
december_daily = december_data.groupby(december_data['InvoiceDate'].dt.date).agg({
    'InvoiceNo': 'nunique',
    'TotalPrice': 'sum'
}).rename(columns={'InvoiceNo': 'Order_Count', 'TotalPrice': 'GMV'})
print("12 月每日订单和 GMV:\n", december_daily)

# 步骤 7：订单量与 GMV 关系
plt.figure(figsize=(10, 6))
ax1 = december_daily['GMV'].plot(kind='line', marker='o', color='blue', label='GMV')
ax2 = ax1.twinx()
december_daily['Order_Count'].plot(kind='line', marker='s', color='red', ax=ax2, label='Order Count')
ax1.set_xlabel('Date')
ax1.set_ylabel('GMV (GBP)', color='blue')
ax2.set_ylabel('Order Count', color='red')
plt.title('December Daily GMV and Order Count')
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig(os.path.join(figures_dir, 'december_gmv_orders.png'))
plt.show()

# 步骤 8：高价值客户贡献
total_gmv = rfm['Monetary'].sum()
top_20_percent = rfm.nlargest(int(len(rfm) * 0.2), 'Monetary')
top_20_gmv = top_20_percent['Monetary'].sum()
print(f"Top 20% 客户 GMV: {top_20_gmv:.2f} GBP")
print(f"占总 GMV 比例: {top_20_gmv / total_gmv * 100:.2f}%")