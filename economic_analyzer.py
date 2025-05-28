# economic_analyzer.py (English labels version)

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
from datetime import datetime

# --- 日本語フォント設定はコメントアウトまたは削除 ---
# try:
#     import japanize_matplotlib
#     print("japanize-matplotlib imported successfully. Japanese font should be configured.")
# except ImportError:
#     print("Warning: japanize-matplotlib is not installed. Trying fallback fonts.")
    # ... (フォールバックフォントの設定もコメントアウト) ...

# --- グローバル設定 ---
OUTPUT_IMAGE_DIR = 'images/economic_analysis_outlook'
if not os.path.exists(OUTPUT_IMAGE_DIR):
    os.makedirs(OUTPUT_IMAGE_DIR)
    print(f"フォルダ '{OUTPUT_IMAGE_DIR}' を作成しました。")

plt.style.use('seaborn-v0_8-darkgrid')
sns.set_palette("muted")
plt.rcParams['axes.unicode_minus'] = False # マイナス記号の文字化け対策は残しておいても良い

DATA_FILE_PATH = 'world_economic_outlook.csv'

analysis_findings_summary_list = []

# --- 可視化関数 (引数のラベルを英語に戻す) ---
def save_plot_outlook(figure, filename_base, plot_title_en, xlabel_en=None, ylabel_en=None):
    path = os.path.join(OUTPUT_IMAGE_DIR, f"{filename_base}.png")
    plt.title(plot_title_en, fontsize=16, pad=20)
    if xlabel_en:
        plt.xlabel(xlabel_en, fontsize=12)
    if ylabel_en:
        plt.ylabel(ylabel_en, fontsize=12)
    plt.xticks(rotation=45, ha='right')
    figure.tight_layout()
    try:
        figure.savefig(path)
        print(f"SUCCESS: Saved plot: {path} (Title: {plot_title_en})")
    except Exception as e_save:
        print(f"ERROR SAVING PLOT: {path} - {e_save}")
    plt.close(figure)

# --- メイン分析処理 ---
if __name__ == "__main__":
    print(f"Attempting to load data from: {os.path.abspath(DATA_FILE_PATH)}")
    try:
        df = pd.read_csv(DATA_FILE_PATH)
        print(f"--- Data loaded from {DATA_FILE_PATH} ---")
        print("First 5 rows of loaded data:")
        print(df.head())
        # (他のデバッグ用print文はそのまま)
    except FileNotFoundError:
        print(f"CRITICAL ERROR: Data file not found at '{DATA_FILE_PATH}'.")
        exit()
    except Exception as e:
        print(f"CRITICAL ERROR loading data: {e}")
        exit()

    required_columns = ['Year', 'Growth_Rate', 'Category', 'Region_Country']
    missing_columns = [col for col in required_columns if col not in df.columns]
    if missing_columns:
        print(f"CRITICAL ERROR: Missing required columns in CSV: {', '.join(missing_columns)}.")
        exit()

    df['Year'] = pd.to_numeric(df['Year'], errors='coerce')
    df['Growth_Rate'] = pd.to_numeric(df['Growth_Rate'], errors='coerce')
    df.dropna(subset=['Year', 'Growth_Rate'], inplace=True)

    if df.empty:
        print("CRITICAL ERROR: DataFrame became empty after dropping NaNs in Year or Growth_Rate.")
        exit()
    df['Year'] = df['Year'].astype(int)
    if df.shape[0] == 0:
        print("CRITICAL ERROR: No valid data rows remaining after processing. Exiting.")
        exit()


    # 1. 全体傾向グラフ (英語ラベル)
    overall_trends_df = df[df['Category'] == '全体傾向'].copy() # CSVのカテゴリ名は日本語のまま
    print(f"\n--- Overall Trends Data (for plot 1) ---")
    print(f"Shape: {overall_trends_df.shape}")
    if not overall_trends_df.empty:
        print("Unique Region_Country in overall_trends_df:", overall_trends_df['Region_Country'].unique())
        fig1 = plt.figure(figsize=(10, 6))
        sns.lineplot(x='Year', y='Growth_Rate', hue='Region_Country', data=overall_trends_df, marker='o', linewidth=2.5)
        plt.ylim(0, 5)
        plt.legend(title='Economic Indicator') # 凡例タイトルを英語に
        plot_title_en = "Global Economic Growth Outlook (2022-2026)"
        plt.title(plot_title_en, fontsize=16, pad=20)
        save_plot_outlook(fig1, "overall_economic_growth_trend",
                        plot_title_en,
                        xlabel_en="Year", ylabel_en="Growth Rate (%)")
        analysis_findings_summary_list.append("Global growth is projected to be flat at 2.7%, while PPP adjusted growth is stable around 3.2%.")
    else:
        print("WARNING: No data for 'Overall Trends' plot.")


    # 2. 地域・国別の成長率推移 (英語ラベル)
    # CSVの 'Region_Country' が日本語の場合、selected_countries_for_plotも日本語にする必要がある
    # ここではCSVのRegion_Countryが日本語のままであると仮定
    selected_countries_for_plot_jp = [
        "アメリカ", "ユーロ圏", "日本", "中国", "インド", "ブラジル", "ロシア", "サウジアラビア"
    ]
    country_trends_df = df[(df['Category'] == '地域・国別の動向') & (df['Region_Country'].isin(selected_countries_for_plot_jp))].copy()
    print(f"\n--- Country Trends Data (for plot 2) ---")
    print(f"Shape: {country_trends_df.shape}")
    if not country_trends_df.empty:
        print(f"Countries found for plot 2: {country_trends_df['Region_Country'].unique()}")
        fig2 = plt.figure(figsize=(14, 8))
        sns.lineplot(x='Year', y='Growth_Rate', hue='Region_Country', data=country_trends_df, marker='o', linewidth=2)
        plt.axhline(0, color='grey', linestyle='--')
        plt.legend(title='Country/Region', bbox_to_anchor=(1.02, 1), loc='upper left') # 凡例タイトル英語
        plot_title_en = "Economic Growth Outlook for Selected Countries/Regions (2022-2026)"
        plt.title(plot_title_en, fontsize=16, pad=20)
        save_plot_outlook(fig2, "selected_countries_growth_trend",
                        plot_title_en,
                        xlabel_en="Year", ylabel_en="Growth Rate (%)")
        analysis_findings_summary_list.append("US shows a slowdown, Euro area and Japan a modest recovery, China slows, India shows stable growth.")
    else:
        print("WARNING: No data for 'Selected Countries Growth Trend' plot.")


    # 3. 特記事項 (所得グループ別成長率) (英語ラベル)
    income_group_df = df[df['Category'] == '特記事項'].copy() # CSVのカテゴリ名は日本語
    print(f"\n--- Income Group Data (for plot 3) ---")
    print(f"Shape: {income_group_df.shape}")
    if not income_group_df.empty:
        if 'Year' in income_group_df.columns and not income_group_df['Year'].isnull().all():
            latest_year_income = int(income_group_df['Year'].max())
            latest_income_df = income_group_df[income_group_df['Year'] == latest_year_income].copy()
            print(f"--- Latest Income Group Data (Year: {latest_year_income}) ---")
            print(f"Shape: {latest_income_df.shape}")
            if not latest_income_df.empty:
                fig3 = plt.figure(figsize=(8, 6))
                sns.barplot(x='Region_Country', y='Growth_Rate', data=latest_income_df, palette="viridis", errorbar=None)
                plot_title_en = f"Economic Growth Outlook by Income Group ({latest_year_income})"
                plt.title(plot_title_en, fontsize=16, pad=20)
                save_plot_outlook(fig3, "income_group_growth_latest_year",
                                plot_title_en,
                                xlabel_en="Income Group", ylabel_en="Growth Rate (%)")
                analysis_findings_summary_list.append(f"In {latest_year_income}, high-income countries are projected around 1.8%, middle-income around 4.3%, and low-income around 5.9% (2026 forecast).")
            else:
                print(f"WARNING: No data for 'Income Group Growth' plot for year {latest_year_income}.")
        else:
            print("WARNING: 'Year' column problematic in '特記事項' data. Skipping income group plot.")
    else:
        print("WARNING: No data found for Category '特記事項'. Skipping income group plot.")


    # 4. 世界貿易と商品価格の見通し (英語ラベル)
    trade_commodity_df = df[df['Category'] == '世界貿易と商品価格'].copy() # CSVのカテゴリ名は日本語
    print(f"\n--- Trade & Commodity Data (for plot 4) ---")
    print(f"Shape: {trade_commodity_df.shape}")
    if not trade_commodity_df.empty:
        # 4.1 世界貿易量
        world_trade_df = trade_commodity_df[trade_commodity_df['Region_Country'] == '世界貿易量'].copy() # CSVのRegion_Countryは日本語
        print(f"\n--- World Trade Data ---")
        print(f"Shape: {world_trade_df.shape}")
        if not world_trade_df.empty:
            fig4_1 = plt.figure(figsize=(8, 5))
            sns.lineplot(x='Year', y='Growth_Rate', data=world_trade_df, marker='o', color='teal', linewidth=2.5)
            plot_title_en = "World Trade Volume Growth Outlook"
            plt.title(plot_title_en, fontsize=16, pad=20)
            save_plot_outlook(fig4_1, "world_trade_volume_trend",
                            plot_title_en,
                            xlabel_en="Year", ylabel_en="Growth Rate (%)")
            analysis_findings_summary_list.append("World trade volume is expected to recover to around 3.2% after stagnation in 2023.")
        else:
            print("WARNING: No data for 'World Trade Volume Trend' plot.")

        # 4.2 原油価格
        oil_price_df = trade_commodity_df[trade_commodity_df['Region_Country'] == '原油価格(ブレント)'].copy() # CSVのRegion_Countryは日本語
        print(f"\n--- Oil Price Data ---")
        print(f"Shape: {oil_price_df.shape}")
        if not oil_price_df.empty:
            fig4_2 = plt.figure(figsize=(8, 5))
            sns.lineplot(x='Year', y='Growth_Rate', data=oil_price_df, marker='o', color='purple', linewidth=2.5)
            plot_title_en = "Crude Oil Price (Brent) Outlook"
            plt.title(plot_title_en, fontsize=16, pad=20)
            save_plot_outlook(fig4_2, "oil_price_brent_trend",
                            plot_title_en,
                            xlabel_en="Year", ylabel_en="Price (USD/barrel)")
            analysis_findings_summary_list.append("Brent crude oil price is projected to fall from $99.8 in 2022 to $71.0 in 2026.")
        else:
            print("WARNING: No data for 'Oil Price Brent Trend' plot.")
    else:
        print("WARNING: No data found for Category '世界貿易と商品価格'. Skipping trade/commodity plots.")


    # --- 分析結果サマリーの保存 (英語テキストに変更) ---
    summary_file_path = os.path.join(OUTPUT_IMAGE_DIR, 'economic_outlook_summary_en.txt') # ファイル名変更
    with open(summary_file_path, 'w', encoding='utf-8') as f:
        min_year_str, max_year_str = "Unknown Period", "Unknown Period"
        if not df.empty and 'Year' in df.columns and df['Year'].notna().any():
            min_year, max_year = int(df['Year'].min()), int(df['Year'].max())
            min_year_str, max_year_str = str(min_year), str(max_year)

        f.write(f"Global Economic Outlook - Analysis Summary ({min_year_str}-{max_year_str})\n") # 英語タイトル
        f.write("=======================================================================\n\n")
        f.write("This analysis is based on the provided CSV data (`world_economic_outlook.csv`).\n\n") # 英語
        f.write("Generated Graphs:\n") # 英語
        generated_files = []
        if os.path.exists(OUTPUT_IMAGE_DIR):
            generated_files = [fn for fn in os.listdir(OUTPUT_IMAGE_DIR) if fn.endswith(".png")]
        if generated_files:
            for filename in generated_files:
                f.write(f"- {filename}\n")
        else:
            f.write("- (No graphs were generated)\n") # 英語
        f.write("\nKey Points:\n") # 英語
        if analysis_findings_summary_list:
            for i, finding in enumerate(analysis_findings_summary_list):
                f.write(f"{i+1}. {finding}\n\n") # analysis_findings_summary_list の内容も英語に変更済み
        else:
            f.write("- (No specific points to highlight)\n") # 英語

    print(f"\nAnalysis summary saved to: {summary_file_path}")
    print(f"Graph saving process attempted. Output directory: {OUTPUT_IMAGE_DIR}/")
    if generated_files:
        print(f"Actually saved graph files: {generated_files}")
    else:
        print("No graph files were actually saved. Please check WARNING or CRITICAL ERROR messages in the terminal.")