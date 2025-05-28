# project_b_visualizer.py (エラー修正版 - 4つ目のグラフ関連)

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os
# from datetime import datetime, timedelta # コメントアウト

# --- 日本語フォント設定 ---
try:
    import japanize_matplotlib
    print("SUCCESS: japanize-matplotlib imported. Japanese characters in plots should display correctly.")
except ImportError:
    print("WARNING: japanize-matplotlib not installed. Attempting to set fallback fonts.")
    font_candidates = ['IPAexGothic', 'Yu Gothic', 'Meiryo', 'Hiragino Sans', 'Noto Sans CJK JP', 'TakaoPGothic', 'MS Gothic']
    font_found = False
    for font_name in font_candidates:
        try:
            plt.rcParams['font.family'] = font_name
            print(f"INFO: Fallback font set to: {font_name}")
            font_found = True
            break
        except:
            continue
    if not font_found:
        print("CRITICAL WARNING: No suitable Japanese font found. Plots may have garbled Japanese text.")
plt.rcParams['axes.unicode_minus'] = False

# --- 出力ディレクトリ作成 ---
OUTPUT_DIR = 'images/project_b_outputs'
if not os.path.exists(OUTPUT_DIR):
    os.makedirs(OUTPUT_DIR)
    print(f"フォルダ '{OUTPUT_DIR}' を作成しました。")

# --- ダミーデータの生成パラメータ ---
num_customers = 1000
np.random.seed(42)

# --- グラフ生成関数 ---
def save_generated_plot(figure, filename, title_for_log):
    path = os.path.join(OUTPUT_DIR, filename)
    figure.tight_layout(rect=[0, 0.03, 1, 0.95])
    try:
        figure.savefig(path)
        print(f"SUCCESS: Saved plot: {path} (Title: {title_for_log})")
    except Exception as e_save:
        print(f"ERROR SAVING PLOT: {path} - {e_save}")
    plt.close(figure)

print("\n--- Generating Dummy Data and Plots ---")

# --- 1. RFM分析に基づく顧客セグメント分布 ---
# (変更なし - 前回のコード)
recency_days = np.random.randint(1, 730, num_customers)
frequency_count = np.random.poisson(1.2, num_customers) + 1
monetary_value = np.abs(np.random.normal(50000, 25000, num_customers) * frequency_count + 10000).astype(int)
reseller_indices_f = np.random.choice(num_customers, size=int(num_customers * 0.05), replace=False)
frequency_count[reseller_indices_f] = np.random.randint(10, 40, size=len(reseller_indices_f))
monetary_value[reseller_indices_f] = np.abs(np.random.normal(80000, 30000, size=len(reseller_indices_f)) * frequency_count[reseller_indices_f] + 20000).astype(int)
df_rfm = pd.DataFrame({'Recency': recency_days, 'Frequency': frequency_count, 'Monetary': monetary_value})
r_labels = [4, 3, 2, 1]; f_labels = [1, 2, 3, 4]; m_labels = [1, 2, 3, 4]
df_rfm['R_Score'] = pd.qcut(df_rfm['Recency'], q=4, labels=r_labels).astype(int)
df_rfm['F_Score'] = pd.qcut(df_rfm['Frequency'].rank(method='first'), q=4, labels=f_labels).astype(int)
df_rfm['M_Score'] = pd.qcut(df_rfm['Monetary'], q=4, labels=m_labels).astype(int)
def assign_rfm_segment(row):
    if row['R_Score'] >= 3 and row['F_Score'] >= 3 and row['M_Score'] >= 3: return '優良顧客 (高R高F高M)'
    elif row['F_Score'] >= 4: return '高頻度顧客 (転売ヤー候補)'
    elif row['R_Score'] >= 3 and row['F_Score'] >= 2: return 'アクティブ通常顧客'
    elif row['R_Score'] >= 3: return '新規・低頻度顧客'
    elif row['R_Score'] <= 2 and row['F_Score'] >= 3: return '休眠予備軍 (高F)'
    else: return '離脱懸念・低価値顧客'
df_rfm['Segment'] = df_rfm.apply(assign_rfm_segment, axis=1)
segment_distribution = df_rfm['Segment'].value_counts(normalize=True) * 100
fig1, ax1 = plt.subplots(figsize=(9, 9))
ax1.pie(segment_distribution, labels=segment_distribution.index, autopct='%1.1f%%',
        startangle=90, pctdistance=0.85, colors=sns.color_palette("Paired", len(segment_distribution)))
centre_circle = plt.Circle((0,0),0.70,fc='white')
fig1.gca().add_artist(centre_circle)
ax1.set_title('RFM分析に基づく顧客セグメント分布', fontsize=16)
ax1.axis('equal')
save_generated_plot(fig1, 'rfm_segment_distribution.png', 'RFM分析に基づく顧客セグメント分布')


# --- 2. 顧客セグメントの構成比と各セグメントの平均購買額 ---
# (変更なし - 前回のコード)
segment_avg_monetary = df_rfm.groupby('Segment')['Monetary'].mean().sort_values(ascending=False)
fig2, ax2 = plt.subplots(figsize=(10, 7))
sns.barplot(x=segment_avg_monetary.index, y=segment_avg_monetary.values, hue=segment_avg_monetary.index, ax=ax2,
            palette='viridis', order=segment_avg_monetary.index, legend=False, dodge=False)
ax2.set_title('顧客セグメント別 平均購買額', fontsize=16)
ax2.set_xlabel('顧客セグメント', fontsize=12)
ax2.set_ylabel('平均購買額 (円)', fontsize=12)
plt.xticks(rotation=45, ha='right', fontsize=10)
for i, v in enumerate(segment_avg_monetary.values):
    if pd.notnull(v):
        ax2.text(i, v + (segment_avg_monetary.max()*0.01), f"{v:,.0f}円", color='black', ha='center', va='bottom', fontsize=9)
save_generated_plot(fig2, 'customer_segments_mean_monetary.png', '顧客セグメント別 平均購買額')


# --- 3. 初回アクセスから購入までの日数分布 ---
# (変更なし - 前回のコード)
days_to_purchase = []
days_to_purchase.extend(np.zeros(int(num_customers * 0.50)))
remaining_after_day0 = num_customers - len(days_to_purchase)
days_to_purchase.extend(np.random.randint(1, 8, int(remaining_after_day0 * 0.60)))
remaining_after_week1 = num_customers - len(days_to_purchase)
days_to_purchase.extend(np.random.randint(8, 36, int(remaining_after_week1 * 0.80)))
remaining_final = num_customers - len(days_to_purchase)
days_to_purchase.extend(np.random.randint(36, 120, remaining_final))
np.random.shuffle(days_to_purchase)
df_conversion = pd.DataFrame({'DaysToPurchase': days_to_purchase})
fig3, ax3 = plt.subplots(figsize=(10, 6))
bins_conversion = [-1, 0, 7, 35, df_conversion['DaysToPurchase'].max() + 1]
labels_conversion = ['当日購入', '1-7日以内', '8-35日以内', '36日以降']
df_conversion['ConversionGroup'] = pd.cut(df_conversion['DaysToPurchase'], bins=bins_conversion, labels=labels_conversion, right=True, include_lowest=True)
conversion_counts = df_conversion['ConversionGroup'].value_counts().reindex(labels_conversion)
sns.barplot(x=conversion_counts.index, y=conversion_counts.values, hue=conversion_counts.index, ax=ax3,
            palette='coolwarm_r', order=labels_conversion, legend=False, dodge=False)
ax3.set_title('初回アクセスから購入までの日数分布', fontsize=16)
ax3.set_xlabel('購入までの期間', fontsize=12)
ax3.set_ylabel('顧客数', fontsize=12)
for i, v in enumerate(conversion_counts.values):
    if pd.notnull(v):
        ax3.text(i, v + (conversion_counts.max()*0.01), str(int(v)), color='black', ha='center', va='bottom', fontsize=10)
save_generated_plot(fig3, 'conversion_time_distribution.png', '初回アクセスから購入までの日数分布')


# --- 4. 顧客の年齢層別構成比とリピート購入率 ---
# (ダミーデータ生成 - 年齢部分)
ages_raw = []
ages_raw.extend(np.random.randint(40, 50, int(num_customers * 0.40)))
ages_raw.extend(np.random.randint(30, 40, int(num_customers * 0.30)))
ages_raw.extend(np.random.randint(20, 30, int(num_customers * 0.15)))
ages_raw.extend(np.random.randint(50, 65, int(num_customers * 0.10)))
ages_raw.extend(np.random.randint(18, 80, num_customers - len(ages_raw)))
np.random.shuffle(ages_raw)
df_age_repeat = pd.DataFrame({'Age': ages_raw, 'CustomerID': range(num_customers)})

# リピート率50%
df_age_repeat['IsRepeatCustomer'] = np.random.choice([True, False], num_customers, p=[0.5, 0.5])

# 40代のリピート率を少し上げる
forties_indices_pd = df_age_repeat[df_age_repeat['Age'].between(40,49, inclusive='both')].index
# ↓↓↓ エラー箇所修正: Pandas IndexをNumpy配列に変換してからシャッフル ↓↓↓
forties_indices_np = np.array(forties_indices_pd) # Numpy配列に変換
np.random.shuffle(forties_indices_np) # Numpy配列をシャッフル
# ↑↑↑ エラー箇所修正完了 ↑↑↑
# シャッフルされたNumpy配列を使ってインデックス指定
df_age_repeat.loc[forties_indices_np[:int(len(forties_indices_np)*0.1)], 'IsRepeatCustomer'] = True

age_bins_plot = [19, 29, 39, 49, 59, df_age_repeat['Age'].max() + 1]
age_labels_plot = ['20代', '30代', '40代', '50代', '60代以上']
df_age_repeat['AgeGroup'] = pd.cut(df_age_repeat['Age'], bins=age_bins_plot, labels=age_labels_plot, right=True, include_lowest=True)

age_group_customer_counts = df_age_repeat['AgeGroup'].value_counts().reindex(['40代', '30代', '20代', '50代', '60代以上'])
fig4, ax4 = plt.subplots(figsize=(10, 6))
sns.barplot(x=age_group_customer_counts.index, y=age_group_customer_counts.values, hue=age_group_customer_counts.index, ax=ax4,
            palette='viridis_r', order=['40代', '30代', '20代', '50代', '60代以上'], legend=False, dodge=False)
ax4.set_title('年齢層別 購入顧客数', fontsize=16)
ax4.set_xlabel('年齢層', fontsize=12)
ax4.set_ylabel('購入顧客数', fontsize=12)
for i, v in enumerate(age_group_customer_counts.values):
    if pd.notnull(v):
        ax4.text(i, v + (age_group_customer_counts.max()*0.01), str(int(v)), color='black', ha='center', va='bottom', fontsize=10)
save_generated_plot(fig4, 'age_group_customer_counts.png', '年齢層別 購入顧客数')


print(f"\nAll dummy data plots saved to {OUTPUT_DIR}")