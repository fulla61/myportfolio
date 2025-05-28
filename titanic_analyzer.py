# titanic_analyzer.py

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os

# --- 設定項目 ---
OUTPUT_PROJECT_DIR = 'images/titanic_analysis'
plt.style.use('seaborn-v0_8-darkgrid')
sns.set_palette("viridis")

# --- 保存先フォルダの作成 ---
if not os.path.exists(OUTPUT_PROJECT_DIR):
    os.makedirs(OUTPUT_PROJECT_DIR)
    print(f"フォルダ '{OUTPUT_PROJECT_DIR}' を作成しました。")

try:
    train_df = pd.read_csv('train.csv')
    test_df = pd.read_csv('test.csv')
except FileNotFoundError:
    print("CSVファイルが見つかりません。train.csv, test.csv をスクリプトと同じディレクトリに配置してください。")
    exit()
print("データ読み込み完了。")

train_df['Age'].fillna(train_df['Age'].median(), inplace=True)
test_df['Age'].fillna(test_df['Age'].median(), inplace=True)
train_df['Embarked'].fillna(train_df['Embarked'].mode()[0], inplace=True)
if test_df['Fare'].isnull().any(): # test_df['Fare']の欠損値処理も確認
    test_df['Fare'].fillna(test_df['Fare'].median(), inplace=True)
train_df['Cabin_Known'] = train_df['Cabin'].notnull().astype(int)
test_df['Cabin_Known'] = test_df['Cabin'].notnull().astype(int) # test_dfにも適用しておくと良い
print("\n欠損値処理完了。")

analysis_results_summary = []

# 1. 生存率の全体像
plt.figure(figsize=(6, 4))
sns.countplot(x='Survived', data=train_df)
plt.title('Overall Survival Count (0 = Died, 1 = Survived)')
plt.xlabel('Survived')
plt.ylabel('Count')
plt.xticks([0, 1], ['Died', 'Survived'])
plt.tight_layout()
plt.savefig(os.path.join(OUTPUT_PROJECT_DIR, 'titanic_survival_overall.png'))
plt.close()
survival_rate = train_df['Survived'].value_counts(normalize=True) * 100
analysis_results_summary.append(f"Overall Survival Rate: Survived {survival_rate.get(1, 0):.2f}%, Died {survival_rate.get(0, 0):.2f}%") # .get()でキー存在確認
print(f"1. 全体生存率グラフを '{os.path.join(OUTPUT_PROJECT_DIR, 'titanic_survival_overall.png')}' に保存完了。")

# 2. 性別 (Sex) vs 生存率
plt.figure(figsize=(7, 5))
# sns.barplot(x='Sex', y='Survived', data=train_df, ci=None) # 旧
sns.barplot(x='Sex', y='Survived', data=train_df, errorbar=None) # 新
plt.title('Survival Rate by Sex')
plt.ylabel('Survival Rate')
plt.tight_layout()
plt.savefig(os.path.join(OUTPUT_PROJECT_DIR, 'titanic_survival_by_sex.png'))
plt.close()
sex_survival = train_df.groupby('Sex')['Survived'].mean() * 100
analysis_results_summary.append(f"Survival Rate by Sex: Female {sex_survival.get('female', 0):.2f}%, Male {sex_survival.get('male', 0):.2f}%") # .get()
print(f"2. 性別と生存率グラフを '{os.path.join(OUTPUT_PROJECT_DIR, 'titanic_survival_by_sex.png')}' に保存完了。")

# 3. 客室クラス (Pclass) vs 生存率
plt.figure(figsize=(7, 5))
# sns.barplot(x='Pclass', y='Survived', data=train_df, ci=None) # 旧
sns.barplot(x='Pclass', y='Survived', data=train_df, errorbar=None) # 新
plt.title('Survival Rate by Passenger Class (Pclass)')
plt.ylabel('Survival Rate')
plt.xlabel('Passenger Class')
plt.tight_layout()
plt.savefig(os.path.join(OUTPUT_PROJECT_DIR, 'titanic_survival_by_pclass.png'))
plt.close()
pclass_survival = train_df.groupby('Pclass')['Survived'].mean() * 100
analysis_results_summary.append(
    f"Survival Rate by Pclass: 1st Class {pclass_survival.get(1, 0):.2f}%, "
    f"2nd Class {pclass_survival.get(2, 0):.2f}%, 3rd Class {pclass_survival.get(3, 0):.2f}%" # .get()
)
print(f"3. 客室クラスと生存率グラフを '{os.path.join(OUTPUT_PROJECT_DIR, 'titanic_survival_by_pclass.png')}' に保存完了。")

# 4. 年齢 (Age) vs 生存率 (ヒストグラムは変更なし)
plt.figure(figsize=(10, 6))
sns.histplot(data=train_df, x='Age', hue='Survived', kde=True, multiple='stack', bins=30)
plt.title('Age Distribution by Survival Status')
plt.xlabel('Age')
plt.ylabel('Count')
plt.tight_layout()
plt.savefig(os.path.join(OUTPUT_PROJECT_DIR, 'titanic_age_distribution_survival.png'))
plt.close()
analysis_results_summary.append("Age: Children (approx. <15 years) had a higher survival rate. Elderly passengers had lower survival rates.")
print(f"4. 年齢分布と生存率グラフを '{os.path.join(OUTPUT_PROJECT_DIR, 'titanic_age_distribution_survival.png')}' に保存完了。")

# 年齢層別
bins = [0, 12, 18, 35, 60, 100]
labels = ['Child (<12)', 'Teen (12-18)', 'Young Adult (19-35)', 'Adult (36-60)', 'Senior (>60)']
train_df['AgeGroup'] = pd.cut(train_df['Age'], bins=bins, labels=labels, right=False)
plt.figure(figsize=(8, 5))
# sns.barplot(x='AgeGroup', y='Survived', data=train_df, ci=None) # 旧
sns.barplot(x='AgeGroup', y='Survived', data=train_df, errorbar=None) # 新
plt.title('Survival Rate by Age Group')
plt.ylabel('Survival Rate')
plt.xlabel('Age Group')
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.savefig(os.path.join(OUTPUT_PROJECT_DIR, 'titanic_survival_by_agegroup.png'))
plt.close()
# AgeGroupがカテゴリカル型の場合、dropna=False で集計しないとNaNグループができてしまう可能性を考慮
agegroup_survival = train_df.groupby('AgeGroup', observed=True)['Survived'].mean() * 100 # observed=True を追加 (pandas 0.25.0+)
analysis_results_summary.append(f"Survival by Age Group highlights: Child {agegroup_survival.get('Child (<12)', 0):.2f}%, Senior {agegroup_survival.get('Senior (>60)', 0):.2f}%")
print(f"4b. 年齢層別生存率グラフを '{os.path.join(OUTPUT_PROJECT_DIR, 'titanic_survival_by_agegroup.png')}' に保存完了。")

# 5. 兄弟/配偶者の数 (SibSp) vs 生存率
plt.figure(figsize=(8, 5))
# sns.barplot(x='SibSp', y='Survived', data=train_df, ci=None) # 旧
sns.barplot(x='SibSp', y='Survived', data=train_df, errorbar=None) # 新
plt.title('Survival Rate by Number of Siblings/Spouses Aboard (SibSp)')
plt.ylabel('Survival Rate')
plt.xlabel('Number of Siblings/Spouses')
plt.tight_layout()
plt.savefig(os.path.join(OUTPUT_PROJECT_DIR, 'titanic_survival_by_sibsp.png'))
plt.close()
analysis_results_summary.append("SibSp: Passengers with 1 or 2 siblings/spouses had a higher survival rate than those alone or with many.")
print(f"5. SibSpと生存率グラフを '{os.path.join(OUTPUT_PROJECT_DIR, 'titanic_survival_by_sibsp.png')}' に保存完了。")

# 6. 親/子供の数 (Parch) vs 生存率
plt.figure(figsize=(8, 5))
# sns.barplot(x='Parch', y='Survived', data=train_df, ci=None) # 旧
sns.barplot(x='Parch', y='Survived', data=train_df, errorbar=None) # 新
plt.title('Survival Rate by Number of Parents/Children Aboard (Parch)')
plt.ylabel('Survival Rate')
plt.xlabel('Number of Parents/Children')
plt.tight_layout()
plt.savefig(os.path.join(OUTPUT_PROJECT_DIR, 'titanic_survival_by_parch.png'))
plt.close()
analysis_results_summary.append("Parch: Similar to SibSp, passengers with 1-3 parents/children had better survival chances.")
print(f"6. Parchと生存率グラフを '{os.path.join(OUTPUT_PROJECT_DIR, 'titanic_survival_by_parch.png')}' に保存完了。")

# 7. 家族サイズ (FamilySize) 特徴量エンジニアリング
train_df['FamilySize'] = train_df['SibSp'] + train_df['Parch'] + 1
plt.figure(figsize=(10, 6))
# sns.barplot(x='FamilySize', y='Survived', data=train_df, ci=None) # 旧
sns.barplot(x='FamilySize', y='Survived', data=train_df, errorbar=None) # 新
plt.title('Survival Rate by Family Size')
plt.ylabel('Survival Rate')
plt.xlabel('Family Size (Self + SibSp + Parch)')
plt.tight_layout()
plt.savefig(os.path.join(OUTPUT_PROJECT_DIR, 'titanic_survival_by_familysize.png'))
plt.close()
analysis_results_summary.append("FamilySize: Small families (2-4 members) tended to survive more often than individuals or large families.")
print(f"7. 家族サイズと生存率グラフを '{os.path.join(OUTPUT_PROJECT_DIR, 'titanic_survival_by_familysize.png')}' に保存完了。")

# 8. 運賃 (Fare) vs 生存率 (ヒストグラムは変更なし)
plt.figure(figsize=(10, 6))
sns.histplot(data=train_df, x='Fare', hue='Survived', kde=True, multiple='stack', bins=40)
plt.title('Fare Distribution by Survival Status')
plt.xlabel('Fare')
plt.ylabel('Count')
plt.xlim(0, 300) # 運賃の外れ値を考慮して表示範囲を限定
plt.tight_layout()
plt.savefig(os.path.join(OUTPUT_PROJECT_DIR, 'titanic_fare_distribution_survival.png'))
plt.close()
analysis_results_summary.append("Fare: Passengers who paid higher fares had a significantly higher chance of survival.")
print(f"8. 運賃と生存率グラフを '{os.path.join(OUTPUT_PROJECT_DIR, 'titanic_fare_distribution_survival.png')}' に保存完了。")

# 9. 乗船港 (Embarked) vs 生存率
plt.figure(figsize=(7, 5))
# sns.barplot(x='Embarked', y='Survived', data=train_df, ci=None) # 旧
sns.barplot(x='Embarked', y='Survived', data=train_df, errorbar=None) # 新
plt.title('Survival Rate by Port of Embarkation')
plt.ylabel('Survival Rate')
plt.xlabel('Port of Embarkation (C=Cherbourg, Q=Queenstown, S=Southampton)')
plt.tight_layout()
plt.savefig(os.path.join(OUTPUT_PROJECT_DIR, 'titanic_survival_by_embarked.png'))
plt.close()
embarked_survival = train_df.groupby('Embarked')['Survived'].mean() * 100
analysis_results_summary.append(
    f"Survival by Embarked: Cherbourg (C) {embarked_survival.get('C', 0):.2f}%, "
    f"Queenstown (Q) {embarked_survival.get('Q', 0):.2f}%, Southampton (S) {embarked_survival.get('S', 0):.2f}%." # .get()
    " This might be correlated with Pclass."
)
print(f"9. 乗船港と生存率グラフを '{os.path.join(OUTPUT_PROJECT_DIR, 'titanic_survival_by_embarked.png')}' に保存完了。")

# 10. Cabinの有無と生存率
plt.figure(figsize=(6, 4))
# sns.barplot(x='Cabin_Known', y='Survived', data=train_df, ci=None) # 旧
sns.barplot(x='Cabin_Known', y='Survived', data=train_df, errorbar=None) # 新
plt.title('Survival Rate by Cabin Information Known')
plt.xlabel('Cabin Information Known (0 = No, 1 = Yes)')
plt.ylabel('Survival Rate')
plt.xticks([0, 1], ['Unknown', 'Known'])
plt.tight_layout()
plt.savefig(os.path.join(OUTPUT_PROJECT_DIR, 'titanic_survival_by_cabin_known.png'))
plt.close()
cabin_known_survival = train_df.groupby('Cabin_Known')['Survived'].mean() * 100
analysis_results_summary.append(f"Cabin Info: Passengers with known cabin info had a much higher survival rate ({cabin_known_survival.get(1, 0):.2f}%) than those without ({cabin_known_survival.get(0, 0):.2f}%). This is likely tied to Pclass and Fare.") # .get()
print(f"10. Cabin有無と生存率グラフを '{os.path.join(OUTPUT_PROJECT_DIR, 'titanic_survival_by_cabin_known.png')}' に保存完了。")

# --- 分析結果のサマリーをテキストファイルに保存 ---
summary_file_path = os.path.join(OUTPUT_PROJECT_DIR, 'titanic_analysis_summary.txt')
with open(summary_file_path, 'w', encoding='utf-8') as f:
    f.write("Titanic Dataset Analysis - Key Findings Summary:\n")
    f.write("===============================================\n\n")
    for i, finding in enumerate(analysis_results_summary):
        f.write(f"{i+1}. {finding}\n\n")

print(f"\n--- 全ての分析とグラフ保存が完了しました ---")
print(f"サマリーは '{summary_file_path}' に保存されました。")
print(f"グラフは '{OUTPUT_PROJECT_DIR}/' フォルダに保存されました。")