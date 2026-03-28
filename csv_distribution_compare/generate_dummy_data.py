"""ダミーデータ生成スクリプト

正規分布の純粋なカラムと、複数分布が混合したカラムを含むCSVを生成する。
"""

import numpy as np
import pandas as pd

rng = np.random.default_rng(seed=42)
N = 500  # データ件数


def normal_only() -> np.ndarray:
    """純粋な正規分布（平均50, 標準偏差5）"""
    return rng.normal(loc=50, scale=5, size=N)


def normal_plus_chisq() -> np.ndarray:
    """正規分布(平均50, std=4) + カイ二乗分布(自由度4, スケール1.5) の混合

    カイ二乗分布は右裾が重いため、正規分布からの外れ具合がQ-Qプロットで視覚的にわかりやすい。
    """
    base = rng.normal(loc=50, scale=4, size=N)
    skew = rng.chisquare(df=4, size=N) * 1.5
    return base + skew


def bimodal_normal() -> np.ndarray:
    """2つの正規分布を混合した二峰性分布

    前半250件: 平均45, std=3
    後半250件: 平均58, std=3
    ヒストグラムで双峰が明確に現れ、Q-Qプロットで正規分布から大きく外れる。
    """
    group_a = rng.normal(loc=45, scale=3, size=N // 2)
    group_b = rng.normal(loc=58, scale=3, size=N // 2)
    mixed = np.concatenate([group_a, group_b])
    rng.shuffle(mixed)
    return mixed


def normal_plus_outliers() -> np.ndarray:
    """正規分布(平均50, std=5) に外れ値を混入したカラム

    データの約5%に一様分布由来の外れ値を混ぜる。
    Q-Qプロットの両端で直線から外れるパターンが確認できる。
    """
    base = rng.normal(loc=50, scale=5, size=N)
    # 約5%のインデックスを外れ値で上書き
    outlier_idx = rng.choice(N, size=int(N * 0.05), replace=False)
    base[outlier_idx] = rng.uniform(low=20, high=80, size=len(outlier_idx))
    return base


df = pd.DataFrame(
    {
        "正規分布": normal_only(),
        "正規+カイ二乗": normal_plus_chisq(),
        "二峰性混合": bimodal_normal(),
        "外れ値混入": normal_plus_outliers(),
    }
)

output_path = "dummy_data.csv"
df.to_csv(output_path, index=False, encoding="utf-8")
print(f"生成完了: {output_path}  ({N}件 × {len(df.columns)}カラム)")
print(df.describe().round(2))
