# K-Means 이용한 클러스터링 예제
from sklearn.cluster import KMeans

df_ext_mat = df_ext.as_matrix()
km = KMeans(n_clusters = 4).fit(df_ext_mat)
labels = km.labels_

# group 변수 생성
df_ext['group'] = labels

# 숫자 to 그룹명 변경
group_name = {0: 'gr_hwp',
              1: 'gr_pdf',
              2: 'gr_xls',
              3: 'gr_doc'}

df_ext['group'] = df_ext['group'].replace(group_name)

# 그룹별 전환율 함수 생성
def conv_rt_by_grp(gr):
    df_gr_screen = df_cluster[df_cluster['group'] == gr]\
                     .groupby(["datetime", "screen"])['sessionid']\
                     .nunique().unstack().fillna(0).astype(int)

    conver_cnt = df_gr_screen.mean().apply(lambda x: int(x)).sort_values(ascending=False)
    conver_rt = [conver_cnt[i + 1] / (conver_cnt[i] * 1.0) * 100 for i in range(len(conver_cnt)) if i < 6]
    conver_rt = pd.Series(conver_rt, index=fun_label).fillna(0)
    return conver_rt

# 그룹별 전환율 산출
conv_rt_pdf = conv_rt_by_grp('gr_pdf')
conv_rt_doc = conv_rt_by_grp('gr_doc')
conv_rt_xls = conv_rt_by_grp('gr_xls')
conv_rt_hwp = conv_rt_by_grp('gr_hwp')

# 가중치 부여
weights = [1, 1.3, 1.5, 2, 2.1, 2.2]

def weight_avg(gr):
    w = (gr.values * weights).sum() / len(gr)
    return w

# 가중치 함수 적용
gr_pdf_w = weight_avg(conv_rt_pdf)
gr_doc_w = weight_avg(conv_rt_doc)
gr_xls_w = weight_avg(conv_rt_xls)
gr_hwp_w = weight_avg(conv_rt_hwp)

# 데이터프레임으로 변환
zip([gr_pdf_avg, gr_doc_avg, gr_xls_avg, gr_hwp_avg], [gr_pdf_w, gr_doc_w, gr_xls_w, gr_hwp_w])

avg_df = pd.DataFrame(list(zip([gr_pdf_avg, gr_doc_avg, gr_xls_avg, gr_hwp_avg],\
                                   [gr_pdf_w, gr_doc_w, gr_xls_w, gr_hwp_w])), \
                                   columns = ['mean', 'wg_mean'],\
                                   index = ['gr_pdf', 'gr_doc', 'gr_xls', 'gr_hwp'])

# 가중치 부여 결과 시각화
avg_df.plot(kind='barh')
plt.tight_layout()