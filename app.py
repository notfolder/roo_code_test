import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats

st.set_page_config(page_title="正規 Q-Q プロット可視化アプリ", layout="wide")

st.title("正規 Q-Q プロット可視化アプリ")

uploaded_file = st.file_uploader("CSV ファイルをアップロードしてください", type=["csv"])

if uploaded_file is not None:
    try:
        df = pd.read_csv(uploaded_file)

        numeric_columns = df.select_dtypes(include=[np.number]).columns.tolist()

        if len(numeric_columns) == 0:
            st.error("数値カラムが含まれていません。")
        else:
            col1, col2 = st.columns(2)

            with col1:
                selected_col1 = st.selectbox(
                    "比較する数値カラムを選択（左）", numeric_columns, key="col1"
                )

            with col2:
                selected_col2 = st.selectbox(
                    "比較する数値カラムを選択（右）", numeric_columns, key="col2"
                )

            if selected_col1 and selected_col2:
                if selected_col1 == selected_col2:
                    st.warning("異なる 2 つのカラムを選択してください。")
                else:
                    data1 = df[selected_col1].dropna().sort_values()
                    data2 = df[selected_col2].dropna().sort_values()

                    if len(data1) == 0 or len(data2) == 0:
                        st.error("有効なデータがありません。")
                    elif len(data1) < 3 or len(data2) < 3:
                        st.error("データ数が少なすぎます（最小 3 件必要）。")
                    else:
                        mean1, std1 = data1.mean(), data1.std()
                        mean2, std2 = data2.mean(), data2.std()

                        if std1 == 0 or std2 == 0:
                            st.error(
                                "標準偏差が 0 のカラムがあります。変化するデータがありません。"
                            )
                        else:
                            n1, n2 = len(data1), len(data2)

                            theoretical_quantiles1 = stats.norm.ppf(
                                np.arange(1, n1 + 1) / (n1 + 1)
                            )
                            theoretical_quantiles2 = stats.norm.ppf(
                                np.arange(1, n2 + 1) / (n2 + 1)
                            )

                            sample_quantiles1 = data1.values
                            sample_quantiles2 = data2.values

                            fig, axes = plt.subplots(1, 2, figsize=(14, 6))

                            for i, ax in enumerate(axes):
                                if i == 0:
                                    sample_q = sample_quantiles1
                                    theo_q = theoretical_quantiles1
                                    col_name = selected_col1
                                    color = "#e74c3c"
                                else:
                                    sample_q = sample_quantiles2
                                    theo_q = theoretical_quantiles2
                                    col_name = selected_col2
                                    color = "#3498db"

                                ax.scatter(
                                    theo_q,
                                    sample_q,
                                    color=color,
                                    alpha=0.6,
                                    label=col_name,
                                )

                                min_val = min(theo_q.min(), sample_q.min())
                                max_val = max(theo_q.max(), sample_q.max())
                                ax.plot(
                                    [min_val, max_val],
                                    [min_val, max_val],
                                    "r--",
                                    linewidth=2,
                                    label="45 度参照線",
                                )

                                ax.set_xlabel("理論分位数（正規分布）")
                                ax.set_ylabel("標本分位数")
                                ax.set_title(f"{col_name} の正規 Q-Q プロット")
                                ax.legend()
                                ax.grid(True, alpha=0.3)

                                if i == 1:
                                    ax.legend()

                            plt.tight_layout()
                            st.pyplot(fig)

                            stats_df = pd.DataFrame(
                                {
                                    "カラム名": [selected_col1, selected_col2],
                                    "平均": [mean1, mean2],
                                    "標準偏差": [std1, std2],
                                    "最小値": [data1.min(), data2.min()],
                                    "最大値": [data1.max(), data2.max()],
                                    "データ数": [len(data1), len(data2)],
                                }
                            )

                            st.subheader("基本統計量")
                            st.table(stats_df)

    except Exception as e:
        st.error(f"エラーが発生しました：{str(e)}")

else:
    st.info("CSV ファイルをアップロードして開始してください。")
