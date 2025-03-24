[통계데이터 사이언스_4조] LendSure
====================================

전체적인 설명
---------
해당 파일은 SNU 빅데이터 핀테크 과정 '통계데이터사이언스'과목의 4조의 최종 결과물입니다.

각 폴더 설명
---------
# 00. data(Github file size 이슈로 repository에는 미포함)
- 모델 구축에 사용된 데이터
- 3종류의 파일이 존재
    - 수정 데이터 : train_trd_timeline.csv, test_trd_timeline.csv
    - 열 데이터 : trd_features.csv
    - 무위험 자산 수익률 데이터 : t-bill_3M.csv, tbill_15_mod.csv

# 01. code
- 모델을 train하고 test할 때 사용한 코드가 들어가 있습니다.
- 파일 설명
    - 00_data_cleansing.ipynb : 데이터 전처리 코드
    - 01_model.ipynb : 부도 예측 모델 코드 (LendSure Model) - train_trd_timeline.csv 자료 사용
    - 02_result.ipynb : 모델 성능 도출 - test_trd_timeline.csv 자료 사용

# 02. model
- 01_model.ipynb를 통해 모델이 들어가 있습니다.
- 3개의 파일 존재
    - default_pred_xgb.pkl : XGBoost 모델 증 best model
    - default_pred_lgb.pkl : LightBM 모델 중 best model
    - best_default_model.pkl : 최종적으로 선정된 모델 = LendSure model, XGBoost 선정

# 03. document
- 2종류의 파일이 들어있습니다.
- 중간발표 자료 : 4조_중간발표.pdf, 4조_중간발표.pptx
- 최종 보고서 : 4조_최종보고서.hwp, 4조_최종보고서.pdf
