"""日付レンジなど共通バリデーション。"""
from datetime import date, timedelta


def validate_reservation_range(start: date, end: date) -> None:
    if start > end:
        raise ValueError("開始日は終了日以前にしてください")
    if (end - start).days > 6:
        # 7日間まで許容(0〜6差分)
        raise ValueError("予約は最長7日までです")
    if start > date.today() + timedelta(days=30):
        raise ValueError("開始日は30日先までです")

