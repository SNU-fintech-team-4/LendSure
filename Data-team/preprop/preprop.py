import pandas as pd
import numpy as np
import statsmodels.api as sm
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder


############################
### 상관계수 계산 후 변수 정리 ###
############################

# 원본 데이터 불러오기
file_path = "./lending_club_sample.csv"
df = pd.read_csv(file_path)

# 상관계수 행렬 계산
correlation_matrix = df.corr(numeric_only=True)

# 높은 상관관계를 가진 변수 찾기 (85% 이상)
high_corr_threshold = 0.85
upper_triangle = correlation_matrix.where(np.triu(np.ones(correlation_matrix.shape), k=1).astype(bool))
high_corr_vars = [col for col in upper_triangle.columns if any(upper_triangle[col].abs() > high_corr_threshold)]

# 높은 상관계수 변수 제거
df_filtered = df.drop(columns=high_corr_vars)

# 상관계수 히트맵 (제거 후)
plt.figure(figsize=(12, 8))
sns.heatmap(df_filtered.corr(numeric_only=True), annot=False, cmap="coolwarm", linewidths=0.5)
plt.title("Step 1: Reduced Feature Correlation Matrix (After COR Removal)")
plt.show()

print(f"제거된 상관계수 높은 변수 개수: {len(high_corr_vars)}")
print(f"제거된 변수 목록: {high_corr_vars}")

# 결측치 비율 계산
missing_ratio = df_filtered.isnull().mean()

# 50% 이상 결측치가 있는 변수 제거
threshold = 0.5
columns_to_keep = missing_ratio[missing_ratio < threshold].index
df_filtered = df_filtered[columns_to_keep].copy()

print(f"제거된 결측치 50% 이상 변수 개수: {len(df.columns) - len(columns_to_keep)}")


####################
### 남은 결측치 처리 ###
####################

# 연속형 변수와 범주형 변수 구분
numerical_cols = df_filtered.select_dtypes(include=['float64', 'int64']).columns
categorical_cols = df_filtered.select_dtypes(include=['object']).columns

# 연속형 변수: 중위수(median)로 결측치 대체
for col in numerical_cols:
    df_filtered[col] = df_filtered[col].fillna(df_filtered[col].median())

# 범주형 변수: 최빈값(mode)으로 결측치 대체
for col in categorical_cols:
    if not df_filtered[col].mode().empty:
        df_filtered[col] = df_filtered[col].fillna(df_filtered[col].mode()[0])


##################
### 파생변수 제거 ###
##################

# 필요하지 않은 변수 키워드 목록 (설명 변수, URL, 중복 정보, 사후 변수 등)
derived_variable_keywords = [
    "total_rec", "recoveries", "pymnt", "settlement", "delinq", "mths_since",
    "id", "url", "desc", "title", "zip_code", "addr_state", "policy_code",
    "issue_d", "earliest_cr_line", "last_pymnt_d", "next_pymnt_d", "last_credit_pull_d"
]

# 파생변수 및 불필요한 변수 제거
derived_variables = [col for col in df_filtered.columns if any(keyword in col.lower() for keyword in derived_variable_keywords)]
df_filtered = df_filtered.drop(columns=derived_variables)

print(f"제거된 파생변수 개수: {len(derived_variables)}")
print(f"제거된 변수 목록: {derived_variables}")


################################
### 다중공선성(VIF) 기반 변수 제거 ###
################################

# VIF 계산 함수 정의
def calculate_vif(df, features):
    vif_data = pd.DataFrame()
    vif_data["Feature"] = features
    vif_data["VIF"] = [sm.OLS(df[col], sm.add_constant(df.drop(columns=[col]))).fit().rsquared for col in features]
    vif_data["VIF"] = 1 / (1 - vif_data["VIF"])  # VIF 공식 적용
    return vif_data

# 숫자형 변수만 선택 후 VIF 계산
numerical_cols_vif = df_filtered.select_dtypes(include=['float64', 'int64']).columns

# NaN 및 Inf 값 처리
df_filtered[numerical_cols_vif] = df_filtered[numerical_cols_vif].replace([np.inf, -np.inf], np.nan)
df_filtered[numerical_cols_vif] = df_filtered[numerical_cols_vif].fillna(df_filtered[numerical_cols_vif].median())

# 분산이 0인 열(상수값만 가진 변수) 제거
zero_variance_cols = df_filtered[numerical_cols_vif].columns[df_filtered[numerical_cols_vif].nunique() == 1]
df_filtered = df_filtered.drop(columns=zero_variance_cols)

# numerical_cols_vif 업데이트
numerical_cols_vif = [col for col in numerical_cols_vif if col in df_filtered.columns]

# VIF 계산 실행
try:
    vif_df = calculate_vif(df_filtered[numerical_cols_vif], numerical_cols_vif)
    
    # ✅ VIF 10 이상인 변수 제거
    high_vif_vars = vif_df[vif_df["VIF"] > 10]["Feature"].tolist()
    df_filtered = df_filtered.drop(columns=high_vif_vars)

    print(f"제거된 VIF 높은 변수 개수: {len(high_vif_vars)}")
    print(f"제거된 변수 목록: {high_vif_vars}")

except Exception as e:
    print("VIF 계산 중 오류 발생:", e)

# 최종 데이터 저장
final_data_path = "final_lending_club.csv"
df_filtered.to_csv(final_data_path, index=False)


####################################################################
### RandomForest 이용하여 변수별 중요도 수치화 후 신용 평가에 적합한 변수 선택 ###
####################################################################

# 데이터 로드
df_filtered = pd.read_csv("final_lending_club.csv")

# 범주형 변수 Label Encoding (랜덤 포레스트 모델 적용을 위해 변환)
categorical_cols = df_filtered.select_dtypes(include=['object']).columns
df_encoded = df_filtered.copy()
for col in categorical_cols:
    le = LabelEncoder()
    df_encoded[col] = le.fit_transform(df_encoded[col])

# 타겟 변수 지정: loan_status
target_variable = "loan_status"
if target_variable in df_encoded.columns:
    X = df_encoded.drop(columns=[target_variable])
    y = df_encoded[target_variable]
else:
    raise KeyError(f"오류: '{target_variable}' 변수가 존재하지 않음")

# 랜덤 포레스트 모델 훈련 (변수 중요도 분석)
rf = RandomForestClassifier(n_estimators=100, random_state=42)
rf.fit(X, y)

# 변수 중요도 계산
feature_importances = pd.DataFrame({
    "Feature": X.columns,
    "Importance": rf.feature_importances_
}).sort_values(by="Importance", ascending=False)

# 변수 중요도 시각화
plt.figure(figsize=(12, 6))
sns.barplot(y=feature_importances["Feature"][:20], x=feature_importances["Importance"][:20], palette="Blues_r")
plt.title("Top 20 Feature Importances (RandomForest)")
plt.xlabel("Importance Score")
plt.ylabel("Feature")
plt.show()

# 중요도가 낮은 변수 제거 (상위 80% 변수만 유지)
threshold = feature_importances["Importance"].quantile(0.2)  # 하위 20% 변수 제거
selected_features = feature_importances[feature_importances["Importance"] > threshold]["Feature"].tolist()
df_filtered = df_filtered[selected_features + [target_variable]]  # 타겟 변수 포함

print(f"제거된 낮은 중요도 변수 개수: {len(feature_importances) - len(selected_features)}")
print(f"제거된 변수 목록: {set(feature_importances['Feature']) - set(selected_features)}")

# 최적화된 데이터 저장 (Feature Importance 기반)
final_data_path_fi = "final_lending_club_feature_importance.csv"
df_filtered.to_csv(final_data_path_fi, index=False)
print(f"최종 데이터 저장: {final_data_path_fi}")

# 남아 있는 변수 개수 및 목록 출력
remaining_variables = df_filtered.columns.tolist()
num_remaining_variables = len(remaining_variables)

print(f"최종 남아 있는 변수 개수: {num_remaining_variables}")
print(f"최종 남아 있는 변수 목록:\n{remaining_variables}")