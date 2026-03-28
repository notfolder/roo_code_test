"""CSVファイルの読み込みとバリデーションを担当するモジュール"""

import pandas as pd
from io import StringIO


class CSVLoader:
    """CSVファイルを読み込み、数値カラムを抽出するクラス"""

    def __init__(self) -> None:
        self.dataframe: pd.DataFrame = pd.DataFrame()

    def load(self, file: object) -> None:
        """
        アップロードされたCSVファイルを読み込む。

        UTF-8エンコードで読み込みを行い、失敗した場合はValueErrorを送出する。
        読み込み成功後、self.dataframeにDataFrameをセットする。
        """
        try:
            # ファイルをバイト列として読み込み、UTF-8でデコードする
            raw_bytes = file.read()
            try:
                content = raw_bytes.decode("utf-8")
            except UnicodeDecodeError:
                raise ValueError("CSVファイルの文字コードはUTF-8のみ対応しています")

            # pandasでCSVとして解析する
            try:
                self.dataframe = pd.read_csv(StringIO(content))
            except Exception:
                raise ValueError("正しいCSV形式のファイルを選択してください")

        except ValueError:
            raise
        except Exception:
            raise ValueError("正しいCSV形式のファイルを選択してください")

    def get_numeric_columns(self) -> list[str]:
        """
        DataFrameから数値型のカラム名一覧を返す。

        数値型カラムが2件未満の場合はValueErrorを送出する。
        """
        numeric_cols = self.dataframe.select_dtypes(include="number").columns.tolist()
        if len(numeric_cols) < 2:
            raise ValueError("数値型のカラムが2件以上必要です")
        return numeric_cols
