import { config } from "../config";

// パスワードポリシー: 長さと英数混在を検証
export function validatePasswordPolicy(password: string): boolean {
  if (password.length < config.passwordMinLength) return false;
  const hasLetter = /[A-Za-z]/.test(password);
  const hasDigit = /[0-9]/.test(password);
  return hasLetter && hasDigit;
}
