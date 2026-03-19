import { differenceInMinutes, isBefore, addDays } from "date-fns";
import { Errors } from "./errors";

// 予約時間のバリデーションを行う
export function assertReservationWindow(startAt: Date, endAt: Date) {
  if (!isBefore(startAt, endAt)) {
    throw Errors.validation("開始は終了より前である必要があります");
  }
  const minutes = differenceInMinutes(endAt, startAt);
  if (minutes <= 0) {
    throw Errors.validation("時間範囲が不正です");
  }
  // 30分刻み判定
  if (startAt.getMinutes() % 30 !== 0 || endAt.getMinutes() % 30 !== 0) {
    throw Errors.validation("30分刻みで入力してください");
  }
  // 最大4時間
  if (minutes > 4 * 60) {
    throw Errors.validation("1回の予約は最大4時間までです");
  }
  // 30日先以内
  const now = new Date();
  if (isBefore(addDays(startAt, -30), now)) {
    // startAt が現在より30日超先の場合
    throw Errors.validation("予約は30日先までです");
  }
}

// キャンセル可否チェック (開始1時間前まで)
export function assertCancelable(startAt: Date) {
  const now = new Date();
  const minutes = differenceInMinutes(startAt, now);
  if (minutes < 60) {
    throw Errors.cancelWindow();
  }
}
