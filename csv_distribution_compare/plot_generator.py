"""Q-Qプロットとヒストグラムの生成を担当するモジュール"""

import math

import japanize_matplotlib  # noqa: F401  日本語フォントを自動適用する
import matplotlib
import matplotlib.figure
import matplotlib.pyplot as plt
import pandas as pd
from scipy import stats


class PlotGenerator:
    """2つのpandas.Seriesを受け取り、グラフFigureを生成するクラス（ステートレス）"""

    # グラフ描画に使用する色の定義
    _COLOR_1 = "#1f77b4"  # 青
    _COLOR_2 = "#ff7f0e"  # 橙

    def generate_qq_plot(
        self,
        series1: pd.Series,
        series2: pd.Series,
        label1: str,
        label2: str,
    ) -> matplotlib.figure.Figure:
        """
        2つのSeriesの正規Q-Qプロットを重ねて描画したFigureを返す。

        scipy.stats.probplotで各Seriesの理論正規分位点と実測分位点を計算し、
        同一グラフに重ねてプロットする。各Seriesに参照線（正規分布に一致する場合の直線）を描画する。
        """
        fig, ax = plt.subplots(figsize=(6, 5))

        # Series1 のQ-Qプロット
        (osm1, osr1), (slope1, intercept1, _) = stats.probplot(
            series1.dropna(), dist="norm"
        )
        ax.scatter(osm1, osr1, color=self._COLOR_1, alpha=0.6, s=20, label=label1)
        # 参照線の描画
        ref_x1 = [min(osm1), max(osm1)]
        ax.plot(
            ref_x1,
            [slope1 * x + intercept1 for x in ref_x1],
            color=self._COLOR_1,
            linestyle="--",
            linewidth=1,
        )

        # Series2 のQ-Qプロット
        (osm2, osr2), (slope2, intercept2, _) = stats.probplot(
            series2.dropna(), dist="norm"
        )
        ax.scatter(osm2, osr2, color=self._COLOR_2, alpha=0.6, s=20, label=label2)
        # 参照線の描画
        ref_x2 = [min(osm2), max(osm2)]
        ax.plot(
            ref_x2,
            [slope2 * x + intercept2 for x in ref_x2],
            color=self._COLOR_2,
            linestyle="--",
            linewidth=1,
        )

        self._apply_common_graph_settings(
            ax,
            title="正規Q-Qプロット",
            xlabel="理論分位点",
            ylabel="実測分位点",
        )
        fig.tight_layout()
        return fig

    def generate_histogram(
        self,
        series1: pd.Series,
        series2: pd.Series,
        label1: str,
        label2: str,
    ) -> matplotlib.figure.Figure:
        """
        2つのSeriesのヒストグラムを半透明で重ねて描画したFigureを返す。

        ビン数はスタージェスの公式（1 + log2(n) の切り上げ）で自動計算する。
        2つのSeriesのデータ件数の大きい方を基準にビン数を計算する。
        """
        fig, ax = plt.subplots(figsize=(6, 5))

        # ビン数をスタージェスの公式で計算（データ件数の大きい方を基準にする）
        n = max(len(series1.dropna()), len(series2.dropna()))
        bins = math.ceil(1 + math.log2(n)) if n > 0 else 10

        ax.hist(
            series1.dropna(),
            bins=bins,
            color=self._COLOR_1,
            alpha=0.5,
            label=label1,
        )
        ax.hist(
            series2.dropna(),
            bins=bins,
            color=self._COLOR_2,
            alpha=0.5,
            label=label2,
        )

        self._apply_common_graph_settings(
            ax,
            title="ヒストグラム",
            xlabel="値",
            ylabel="頻度",
        )
        fig.tight_layout()
        return fig

    def _apply_common_graph_settings(
        self,
        ax: plt.Axes,
        title: str,
        xlabel: str,
        ylabel: str,
    ) -> None:
        """
        グラフの共通設定（タイトル・軸ラベル・凡例・グリッド）を適用する。

        Q-Qプロット・ヒストグラム両方で使用する共通処理を集約したメソッド。
        """
        ax.set_title(title, fontsize=13)
        ax.set_xlabel(xlabel, fontsize=11)
        ax.set_ylabel(ylabel, fontsize=11)
        ax.legend(fontsize=10)
        ax.grid(True, linestyle="--", alpha=0.5)
