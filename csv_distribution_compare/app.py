"""CSV分布比較アプリ - Streamlitメインアプリ"""

import streamlit as st

from csv_loader import CSVLoader
from plot_generator import PlotGenerator


def main() -> None:
    st.title("CSV分布比較アプリ")

    # CSVファイルアップロード
    uploaded_file = st.file_uploader(
        "CSVファイルをアップロードしてください",
        type=["csv"],
    )

    if uploaded_file is None:
        st.info("CSVファイルをアップロードすると、カラム選択とグラフ表示が利用できます。")
        return

    # CSVの読み込みとバリデーション（E-01, E-02, E-03）
    loader = CSVLoader()
    try:
        loader.load(uploaded_file)
        numeric_cols = loader.get_numeric_columns()
    except ValueError as e:
        st.error(str(e))
        return

    # カラム選択（2つ）
    col1, col2 = st.columns(2)
    with col1:
        selected_col1 = st.selectbox("カラム1（比較対象1）", options=numeric_cols, index=0)
    with col2:
        # デフォルトをカラム1と異なるものにする
        default_index = 1 if len(numeric_cols) > 1 else 0
        selected_col2 = st.selectbox(
            "カラム2（比較対象2）", options=numeric_cols, index=default_index
        )

    # グラフ表示ボタン
    if not st.button("グラフを表示する"):
        return

    # 同一カラム選択のバリデーション（E-04）
    if selected_col1 == selected_col2:
        st.warning("異なる2つのカラムを選択してください")
        return

    series1 = loader.dataframe[selected_col1].dropna()
    series2 = loader.dataframe[selected_col2].dropna()

    # 有効データ件数のバリデーション（E-05）
    if len(series1) == 0 or len(series2) == 0:
        st.error("選択したカラムに有効なデータがありません")
        return

    # グラフ生成と表示
    generator = PlotGenerator()
    try:
        fig_qq = generator.generate_qq_plot(series1, series2, selected_col1, selected_col2)
        fig_hist = generator.generate_histogram(series1, series2, selected_col1, selected_col2)
    except Exception as e:
        st.error(f"グラフの生成中にエラーが発生しました: {e}")
        return

    # Q-QプロットとHistogramを左右に並べて表示
    left, right = st.columns(2)
    with left:
        st.subheader("正規Q-Qプロット")
        st.pyplot(fig_qq)
    with right:
        st.subheader("ヒストグラム")
        st.pyplot(fig_hist)


if __name__ == "__main__":
    main()
