### loan_status_pred 모델에 쓸 데이터 전처리
+ loan_amnt: 로그 후 min-max 스케일링
+ funded_amnt: 로그 후 min-max 스케일링
+ funded_amnt_inv: 로그 후 min-max 스케일링
+ term: 36, 60밖에 없어서 0, 1로 이진 스케일링
+ int_rate: 로그 후 min-max 스케일링
+ installment: 로그 후 min-max 스케일링
+ grade: (ordinal) min-max 스케일링
+ sub_grade: (ordinal) min-max 스케일링
+ emp_length: (ordinal) min-max 스케일링
+ annual_inc: 로그 후 min-max 스케일링
+ loan_status: 0, 1로 이진화(이미 되있음)
+ dti: 로그 후 min-max 스케일링
+ delinq_2yrs: 이진화
+ fico_avg: min-max 스케일링
+ inq_last_6mths: 이진화
+ open_acc: (ordinal)min-max 스케일링
+ pub_rec: 이진화
+ revol_bal: 로그 후 min-max 스케일링
+ revol_util: 로그 후 min-max 스케일링
+ total_acc: (ordinal)min-max 스케일링
+ out_prncp: 칼럼 드랍
+ out_prncp_inv: 칼럼 드랍
+ total_rec_late_fee: 칼럼 드랍(일단 드랍하고 생각해보자)
+ last_fico_range_high: min-max 스케일링
+ last_fico_range_low: min-max 스케일링
+ acc_now_delinq: 이진화
+ tot_cur_bal: 로그 후 min-max 스케일링
+ open_acc_6m: (ordinal)min-max 스케일링
+ open_act_il: (ordinal)min-max 스케일링
+ open_il_12m: (ordinal)min-max 스케일링
+ open_il_24m: (ordinal)min-max 스케일링
+ mths_since_rcnt_il: (ordinal)min-max 스케일링
+ total_bal_il: 로그 후 min-max 스케일링
+ il_util: 결측값 많아서 드랍
+ open_rv_12m: (ordinal)min-max 스케일링
+ open_rv_24m: (ordinal)min-max 스케일링
+ max_bal_bc: 로그 후 min-max 스케일링
+ all_util: 로그 후 min-max 스케일링
+ total_rev_hi_lim: 로그 후 min-max 스케일링
+ inq_fi: 이진화
+ total_cu_tl: (ordinal)min-max 스케일링
+ inq_last_12m: 이진화
+ acc_open_past_24mths: (ordinal)min-max 스케일링
+ avg_cur_bal: 로그 후 min-max 스케일링
+ bc_open_to_buy: 로그 후 min-max 스케일링
+ bc_util: 로그 후 min-max 스케일링
+ chargeoff_within_12_mths: 이진화
+ mort_acc: (ordinal)min-max 스케일링
+ num_accts_ever_120_pd: 이진화
+ num_actv_bc_tl: (ordinal)min-max 스케일링
+ num_actv_rev_tl: (ordinal)min-max 스케일링
+ num_bc_sats: (ordinal)min-max 스케일링
+ num_bc_tl: (ordinal)min-max 스케일링
+ num_il_tl: (ordinal)min-max 스케일링
+ num_op_rev_tl: (ordinal)min-max 스케일링
+ num_rev_accts: (ordinal)min-max 스케일링
+ num_rev_tl_bal_gt_0: (ordinal)min-max 스케일링
+ num_sats: (ordinal)min-max 스케일링
+ num_tl_120dpd_2m: 이진화
+ num_tl_30dpd: 이진화
+ num_tl_90g_dpd_24m: 이진화
+ num_tl_op_past_12m: (ordinal)min-max 스케일링
+ pct_tl_nvr_dlq: 로그 후 min-max 스케일링
+ percent_bc_gt_75: 로그 후 min-max 스케일링
+ pub_rec_bankruptcies: 이진화
+ tax_liens: 이진화
+ tot_hi_cred_lim: 로그 후 min-max 스케일링
+ total_bal_ex_mort: 로그 후 min-max 스케일링
+ total_bc_limit: 로그 후 min-max 스케일링
+ total_il_high_credit_limit: 로그 후 min-max 스케일링
+ 이후 나머진 그대로