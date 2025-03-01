# Lending Club 2020 Train 데이터 전처리 요약

## 1. 데이터 로딩 및 초기 정리
- `lending_club_2020_train.csv` 파일을 로드 (옵션: `low_memory=False`).
- 분석에 필요하지 않은 칼럼 제거:  
  `id`, `url`, `title`, `application_type`, `next_pymnt_d`, `policy_code`, `delinq_amnt`, `hardship_flag`.

## 2. 등급(Grade) 관련 변수 인코딩
- **grade**와 **sub_grade** 칼럼을 각각 추출.
- `LabelEncoder`를 사용하여 문자열 등급을 정수형으로 변환.
- 인코딩된 값을 원래 칼럼에 덮어씀.

## 3. 결측치 처리 및 칼럼 제거
- 전체 칼럼 중 결측치 비율이 50% 이상인 칼럼은 삭제 (단, 타겟 변수인 `loan_status`는 유지).

## 4. 데이터 타입 변환 및 파생 변수 생성
- **int_rate**:  
  - "%" 기호를 제거하고 실수형으로 변환한 후 100으로 나누어 0~1 범위로 정규화.
- **fico_avg**:  
  - `fico_range_low`와 `fico_range_high`의 평균을 계산하여 새로운 칼럼으로 추가.

## 5. 순서형 변수(Ordinal) 처리
- **emp_length**:  
  - 문자열 형태의 고용 기간 값을 순서형 숫자로 매핑 (예: `< 1 year` → 0, `1 year` → 1, …, `10+ years` → 10).
  - 결측치는 -1로 채워 무직 상태를 구분.
- **term**:  
  - `' 36 months'`와 `' 60 months'`를 각각 36과 60으로 매핑.

## 6. 수치형 변수 전처리
- **revol_util**:  
  - "%" 기호 제거 후 실수형 변환, 100으로 나눠 0~1 범위로 정규화. 결측치는 평균값으로 대체.
- **tot_coll_amt**, **tot_cur_bal**, **total_rev_hi_lim**, **acc_open_past_24mths**, **avg_cur_bal**, **bc_open_to_buy**:  
  - 결측치를 각각 0, 중앙값 등 적절한 값으로 대체.
- **bc_util**:  
  - 값을 100으로 나눠 소수점 형태로 변환한 후, 결측치는 평균값으로 대체.
- **dti**:  
  - 100으로 나눠 0~1 범위의 값으로 변환.
- **mort_acc**, **num_accts_ever_120_pd**:  
  - 결측치는 중앙값으로 대체.
- 여러 계좌 관련 칼럼 및 신용 한도, 잔액 관련 칼럼:  
  - 결측치는 중앙값 또는 평균값으로 대체.

## 7. 타겟 변수 및 불필요한 칼럼 제거
- **loan_status**:  
  - 대출 상환 상태를 나타내며, (주석 처리된 부분에서는) `'Fully Paid'`를 non-default (0)로, 나머지를 default (1)로 변환하는 로직이 있음.
  - 결측치가 있는 행은 제거.
- 모델링에 불필요하다고 판단된 칼럼 제거:  
  예) `zip_code`, `fico_range_low`, `fico_range_high`, `emp_title`, 날짜 관련 칼럼들(`issue_d`, `last_pymnt_d` 등), `purpose`, `addr_state`, `earliest_cr_line`, `initial_list_status`, `last_credit_pull_d`, `debt_settlement_flag`, `mo_sin_rcnt_rev_tl_op`, `mo_sin_rcnt_tl`, `last_pymnt_amnt`, `pymnt_plan`, `total_rec_prncp`, `total_rec_int`, `total_pymnt`, `total_pymnt_inv`.

## 8. 범주형 변수 인코딩 (Nominal)
- **home_ownership**와 **verification_status** 칼럼에 대해 원-핫 인코딩 수행 (첫 번째 범주는 제거).

## 9. 추가 후처리
- 채무불이행 이후 발생하는 데이터를 가진 칼럼들 제거:  
  예) `recoveries`, `collection_recovery_fee`, `collections_12_mths_ex_med`, `tot_coll_amt`.

---

# 데이터 준비 및 분할 요약

## 1. 특성과 타겟 분리
- **특성 (X):**
  - `loan_status` 칼럼을 제외한 모든 칼럼을 사용.
- **타겟 (y):**
  - `loan_status` 칼럼을 사용.

## 2. Boolean 타입 처리
- **문제점:**
  - XGBoost는 Boolean 타입을 처리할 때 문제가 발생할 수 있음.
- **해결 방법:**
  - X의 Boolean 타입 칼럼들을 정수형(int)으로 변환.

## 3. 데이터 분할
- **Train/Test 분할:**
  - 전체 데이터를 80%의 Train 세트와 20%의 Test 세트로 분할.
  - 분할 시 `random_state=42`와 `stratify=y` 옵션을 사용하여 재현성과 클래스 분포 유지.
- **Train 데이터 내 Validation 세트 분할:**
  - Train 데이터 중 20%를 Validation 세트로 추가 분할.
  - 최종적으로 Train 세트는 전체의 75%, Validation 세트는 25%를 차지하게 됨.
  - 이 때도 `random_state=42`와 `stratify=y_train` 옵션을 사용.

## 4. 분할 결과 확인
- 각 세트의 행(row) 수를 출력하여 데이터 분할이 올바르게 이루어졌는지 확인:
  - Train 세트 크기
  - Validation 세트 크기
  - Test 세트 크기

---

# Feature Importance 분석 및 도메인 피처 반영

이 문서는 XGBoost 분류기를 활용하여 피처 중요도를 분석하고, 도메인 지식을 반영한 최종 Top 20 피처를 선정한 후, 이를 시각화하는 과정을 요약합니다.

## 1. XGBoost 분류기를 이용한 피처 중요도 분석
- **모델 학습**:  
  - XGBoost Classifier를 사용하여 학습 데이터를 기반으로 모델을 학습합니다.
- **피처 중요도 추출**:  
  - 학습 후, 모델이 산출한 각 피처의 중요도를 이용해 `Feature`와 `Importance` 컬럼을 가진 DataFrame을 생성합니다.
  - 이 DataFrame은 중요도 내림차순으로 정렬됩니다.

## 2. 도메인 피처 반영 및 최종 피처 선정
- **반드시 포함해야 하는 도메인 피처 지정**:  
  - 예를 들어, `emp_length`, `dti`, `revol_util`, `fico_avg`와 같이 도메인 지식에 기반해 반드시 포함되어야 할 피처를 미리 지정합니다.
- **피처 선택 과정**:
  - 우선, 도메인 피처 중 실제 데이터에 존재하는 피처들을 최종 선정 목록에 추가합니다.
  - 이후, 전체 피처 중요도 순으로 반복하여 도메인 피처 외의 나머지 피처들을 채워 넣습니다.
  - 최종적으로 선택된 피처의 수가 20개 이상일 경우, 도메인 피처를 우선적으로 유지하면서 중요도 순으로 20개로 강제 조정합니다.

## 3. 최종 피처 DataFrame 생성 및 시각화
- **최종 피처 DataFrame 생성**:
  - 선정된 Top 20 피처를 기준으로 원본 피처 중요도 DataFrame에서 해당 행만 필터링하고, 다시 중요도 내림차순으로 정렬합니다.
- **시각화**:
  - 수평 막대 그래프로 피처 중요도를 시각화하는 함수를 정의한 후, 최종 피처 DataFrame을 이용해 그래프를 출력합니다.
  - 이를 통해 각 피처의 상대적 중요도를 한눈에 파악할 수 있습니다.

---

# Fβ Score 기반 Threshold 튜닝 및 평가

이 문서는 XGBoost 모델을 사용하여 상위 피처를 기반으로 학습한 후, Fβ 스코어(여기서는 β=1.2)를 활용하여 임계치를 최적화하고 최적 임계치를 적용한 모델 성능을 평가하는 과정을 설명합니다.

## 1. 데이터 준비 및 상위 피처 선택
- **상위 피처 선택:**  
  - `df_top20` DataFrame에서 상위 20개 피처를 선택하여 `top_features` 리스트에 저장.
- **데이터셋 구성:**  
  - 학습, 검증, 테스트 데이터셋에서 선택된 상위 피처들만 추출하여 각각 `X_train_top`, `X_valid_top`, `X_test_top`을 구성.

## 2. XGBoost 모델 학습
- **DMatrix 변환:**  
  - 학습, 검증, 테스트 데이터를 XGBoost 전용 DMatrix 형식으로 변환.
- **모델 설정 및 학습:**  
  - GPU 사용 및 기본 파라미터(`objective`, `eval_metric`, `tree_method`, `device`, `seed`)를 설정.
  - Early Stopping을 활용하여 최대 1000 라운드 내에서 학습 수행.
  
## 3. 기본 임계치(0.5) 평가
- **예측 및 평가:**  
  - 모델이 산출한 확률 값을 임계치 0.5로 이진화하여 예측 결과 도출.
  - Accuracy, Classification Report, Confusion Matrix를 출력하여 기본 성능 확인.

## 4. 임계치 최적화 (Precision-Recall Curve 및 Fβ Score 활용)
- **Precision-Recall Curve 계산 및 시각화:**  
  - `precision_recall_curve` 함수를 사용해 임계치별 Precision과 Recall을 계산.
  - 임계치에 따른 Precision과 Recall의 변화를 그래프로 시각화하여 확인.
- **샘플링 처리:**  
  - 임계치의 개수가 너무 많으면 일정 구간으로 샘플링하여 계산량을 줄임.
- **Fβ Score 계산 및 최적 임계치 선택:**  
  - 각 샘플 임계치에서 `fbeta_score` (β=1.2)를 계산.
  - 가장 높은 Fβ Score를 주는 임계치를 최적 임계치(`best_threshold`)로 선정.

## 5. 최적 임계치 적용 후 평가
- **최적 임계치 적용:**  
  - 최적 임계치(`best_threshold`)를 사용해 모델 예측 확률을 이진 분류 결과로 변환.
- **최종 성능 평가:**  
  - 최적 임계치를 적용한 모델의 Accuracy, Classification Report, Confusion Matrix를 출력하여 성능 비교 및 평가.

---

