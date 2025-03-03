### 데이터 전처리(스케일링)
### for_grade_data.csv 파일을 이용
+ term: 36, 60밖에 없어서 0, 1로 이진 스케일링
+ emp_length: (ordinal) min-max 스케일링
+ annual_inc: 로그 후 min-max 스케일링
+ dti: 로그 후 min-max 스케일링
+ delinq_2yrs: 이진화
+ fico_avg: min-max 스케일링
+ inq_last_6mths: 이진화
+ open_acc: (ordinal)min-max 스케일링
+ pub_rec: 이진화
+ revol_bal: 로그 후 min-max 스케일링
+ revol_util: 로그 후 min-max 스케일링
+ total_acc: (ordinal)min-max 스케일링
+ acc_now_delinq: 이진화
+ tot_cur_bal: 로그 후 min-max 스케일링
+ total_rev_hi_lim: min-max 스케일링
+ avg_cur_bal: min-max 스케일링
+ bc_open_to_buy: 로그 후 min-max 스케일링
+ bc_util: 로그 후 min-max 스케일링
+ chargeoff_within_12_mths: 이진화
+ mort_acc: (ordinal)min-max 스케일링
+ num_accts_ever_120_pd: 이진화
+ num_actv_rev_tl: (ordinal)min-max 스케일링
+ num_bc_sats: (ordinal)min-max 스케일링
+ num_bc_tl: (ordinal)min-max 스케일링
+ num_op_rev_tl: (ordinal)min-max 스케일링
+ num_rev_accts: (ordinal)min-max 스케일링
+ num_rev_tl_bal_gt_0: (ordinal)min-max 스케일링
+ num_sats: (ordinal)min-max 스케일링
+ pct_tl_nvr_dlq: 로그 후 min-max 스케일링
+ percent_bc_gt_75: 로그 후 min-max 스케일링
+ pub_rec_bankruptcies: 이진화
+ tax_liens: 이진화
+ tot_hi_cred_lim: 로그 후 min-max 스케일링
+ total_bal_ex_mort: 로그 후 min-max 스케일링
+ total_bc_limit: 로그 후 min-max 스케일링
+ total_il_high_credit_limit: 로그 후 min-max 스케일링
+ 이후 나머지는 그대로(더미변수 and 타겟 변수)
+ loan_status: 0, 1로 이진화
+ grade: (ordinal) min-max 스케일링
+ sub_grade: (ordinal) min-max 스케일링
+ loan_amnt: 로그 후 min-max 스케일링
+ 이후 나머지는 그대로(타겟변수 int_rate)