// @ts-check
/**
 * E2Eテストシナリオ T01〜T10
 * 設計書「13. E2Eテスト設計 - E2Eテストシナリオ一覧」に基づく
 */
const { test, expect } = require('@playwright/test');

const BASE_URL = process.env.BASE_URL || 'http://frontend';
const LOGIN_ID = process.env.ADMIN_LOGIN_ID || 'admin';
const LOGIN_PASSWORD = process.env.ADMIN_PASSWORD || 'AdminPass123';

/** 管理者としてログインするヘルパー */
async function loginAsAdmin(page) {
  await page.goto(`${BASE_URL}/login`);
  await page.locator('[data-testid="login-id"] input').fill(LOGIN_ID);
  await page.locator('[data-testid="login-password"] input').fill(LOGIN_PASSWORD);
  await page.getByTestId('login-button').click();
  await page.waitForURL(`${BASE_URL}/`);
}

// T01: 一般ユーザーが備品一覧を閲覧する
test('T01: 一般ユーザーが備品一覧を閲覧できる', async ({ page }) => {
  await page.goto(BASE_URL);
  await expect(page.getByTestId('equipment-table')).toBeVisible();
  await expect(page.getByTestId('btn-login')).toBeVisible();
  await expect(page.getByTestId('btn-lend')).not.toBeVisible();
  await expect(page.getByTestId('btn-return')).not.toBeVisible();
});

// T02: 総務担当者がログインする
test('T02: 総務担当者がログインできる', async ({ page }) => {
  await loginAsAdmin(page);
  await expect(page.getByTestId('btn-lend')).toBeVisible();
  await expect(page.getByTestId('btn-return')).toBeVisible();
  await expect(page.getByTestId('btn-manage')).toBeVisible();
  await expect(page.getByTestId('btn-history')).toBeVisible();
  await expect(page.getByTestId('btn-logout')).toBeVisible();
});

// T03: 総務担当者が備品を登録する
test('T03: 総務担当者が備品を登録できる', async ({ page }) => {
  await loginAsAdmin(page);
  await page.getByTestId('btn-manage').click();
  await page.waitForURL(`${BASE_URL}/equipment`);
  await page.getByTestId('btn-add-equipment').click();
  await page.locator('[data-testid="input-management-number"] input').fill('PC-TEST');
  await page.locator('[data-testid="input-name"] input').fill('テストPC');
  await page.locator('[data-testid="input-equipment-type"] input').fill('ノートPC');
  await page.getByTestId('btn-save-equipment').click();
  await expect(page.getByTestId('equipment-management-table')).toContainText('PC-TEST');
});

// T04: 総務担当者が備品を編集する
test('T04: 総務担当者が備品を編集できる', async ({ page }) => {
  await loginAsAdmin(page);
  // まず備品を登録する
  await page.getByTestId('btn-manage').click();
  await page.waitForURL(`${BASE_URL}/equipment`);
  await page.getByTestId('btn-add-equipment').click();
  await page.locator('[data-testid="input-management-number"] input').fill('PC-EDIT');
  await page.locator('[data-testid="input-name"] input').fill('編集前PC');
  await page.locator('[data-testid="input-equipment-type"] input').fill('ノートPC');
  await page.getByTestId('btn-save-equipment').click();
  // 編集ボタンをクリック
  const row = page.locator('tr', { hasText: 'PC-EDIT' });
  await row.getByTestId('btn-edit').click();
  await page.locator('[data-testid="input-name"] input').fill('編集後PC');
  await page.getByTestId('btn-save-equipment').click();
  await expect(page.getByTestId('equipment-management-table')).toContainText('編集後PC');
});

// T05: 総務担当者が備品を削除する
test('T05: 総務担当者が備品を削除できる', async ({ page }) => {
  await loginAsAdmin(page);
  await page.getByTestId('btn-manage').click();
  await page.waitForURL(`${BASE_URL}/equipment`);
  await page.getByTestId('btn-add-equipment').click();
  await page.locator('[data-testid="input-management-number"] input').fill('PC-DEL');
  await page.locator('[data-testid="input-name"] input').fill('削除用PC');
  await page.locator('[data-testid="input-equipment-type"] input').fill('ノートPC');
  await page.getByTestId('btn-save-equipment').click();
  // 削除ボタンをクリック
  const row = page.locator('tr', { hasText: 'PC-DEL' });
  await row.getByTestId('btn-delete').click();
  await page.getByTestId('btn-confirm-delete').click();
  await expect(page.getByTestId('equipment-management-table')).not.toContainText('PC-DEL');
});

// T06: 貸出記録を登録する
test('T06: 貸出記録を登録できる', async ({ page }) => {
  // 事前に備品を登録する
  await loginAsAdmin(page);
  await page.getByTestId('btn-manage').click();
  await page.waitForURL(`${BASE_URL}/equipment`);
  await page.getByTestId('btn-add-equipment').click();
  await page.locator('[data-testid="input-management-number"] input').fill('PC-LEND');
  await page.locator('[data-testid="input-name"] input').fill('貸出テストPC');
  await page.locator('[data-testid="input-equipment-type"] input').fill('ノートPC');
  await page.getByTestId('btn-save-equipment').click();
  // トップに戻る
  await page.goto(BASE_URL);
  // 貸出登録
  await page.getByTestId('btn-lend').click();
  await page.waitForURL(`${BASE_URL}/lending/new`);
  await page.getByTestId('select-equipment').click();
  await page.locator('.v-overlay__content .v-list-item').filter({ hasText: 'PC-LEND' }).click();
  await page.locator('[data-testid="input-borrower-name"] input').fill('山田太郎');
  await page.getByTestId('btn-save-lending').click();
  await page.waitForURL(`${BASE_URL}/`);
  await expect(page.getByTestId('equipment-table')).toContainText('貸出中');
  await expect(page.getByTestId('equipment-table')).toContainText('山田太郎');
});

// T07: 返却記録を登録する
test('T07: 返却記録を登録できる', async ({ page }) => {
  // 事前に備品登録・貸出を行う
  await loginAsAdmin(page);
  await page.getByTestId('btn-manage').click();
  await page.waitForURL(`${BASE_URL}/equipment`);
  await page.getByTestId('btn-add-equipment').click();
  await page.locator('[data-testid="input-management-number"] input').fill('PC-RET');
  await page.locator('[data-testid="input-name"] input').fill('返却テストPC');
  await page.locator('[data-testid="input-equipment-type"] input').fill('ノートPC');
  await page.getByTestId('btn-save-equipment').click();
  await page.goto(BASE_URL);
  await page.getByTestId('btn-lend').click();
  await page.waitForURL(`${BASE_URL}/lending/new`);
  await page.getByTestId('select-equipment').click();
  await page.locator('.v-overlay__content .v-list-item').filter({ hasText: 'PC-RET' }).click();
  await page.locator('[data-testid="input-borrower-name"] input').fill('佐藤花子');
  await page.getByTestId('btn-save-lending').click();
  await page.waitForURL(`${BASE_URL}/`);
  // 返却登録
  await page.getByTestId('btn-return').click();
  await page.waitForURL(`${BASE_URL}/lending/return`);
  await page.getByTestId('select-lending').click();
  await page.locator('.v-overlay__content .v-list-item').filter({ hasText: 'PC-RET' }).click();
  await page.getByTestId('btn-save-return').click();
  await page.waitForURL(`${BASE_URL}/`);
  await expect(page.getByTestId('equipment-table')).toContainText('利用可能');
});

// T08: 貸出履歴を確認する
test('T08: 貸出履歴が表示される', async ({ page }) => {
  await loginAsAdmin(page);
  // 事前に備品・貸出を作成する
  await page.getByTestId('btn-manage').click();
  await page.waitForURL(`${BASE_URL}/equipment`);
  await page.getByTestId('btn-add-equipment').click();
  await page.locator('[data-testid="input-management-number"] input').fill('PC-HIST');
  await page.locator('[data-testid="input-name"] input').fill('履歴テストPC');
  await page.locator('[data-testid="input-equipment-type"] input').fill('ノートPC');
  await page.getByTestId('btn-save-equipment').click();
  await page.goto(BASE_URL);
  await page.getByTestId('btn-lend').click();
  await page.waitForURL(`${BASE_URL}/lending/new`);
  await page.getByTestId('select-equipment').click();
  await page.locator('.v-overlay__content .v-list-item').filter({ hasText: 'PC-HIST' }).click();
  await page.locator('[data-testid="input-borrower-name"] input').fill('田中一郎');
  await page.getByTestId('btn-save-lending').click();
  await page.waitForURL(`${BASE_URL}/`);
  // 履歴確認
  await page.getByTestId('btn-history').click();
  await page.waitForURL(`${BASE_URL}/lending/history`);
  await expect(page.getByTestId('lending-history-table')).toBeVisible();
  await expect(page.getByTestId('lending-history-table')).toContainText('田中一郎');
});

// T09: 未ログイン時に操作ボタンが非表示
test('T09: 未ログイン時は操作ボタンが非表示になる', async ({ page }) => {
  await page.goto(BASE_URL);
  await expect(page.getByTestId('btn-lend')).not.toBeVisible();
  await expect(page.getByTestId('btn-return')).not.toBeVisible();
  await expect(page.getByTestId('btn-manage')).not.toBeVisible();
  await expect(page.getByTestId('btn-history')).not.toBeVisible();
  await expect(page.getByTestId('btn-login')).toBeVisible();
});

// T10: ログアウトする
test('T10: ログアウトできる', async ({ page }) => {
  await loginAsAdmin(page);
  await page.getByTestId('btn-logout').click();
  await expect(page.getByTestId('btn-login')).toBeVisible();
  await expect(page.getByTestId('btn-lend')).not.toBeVisible();
});
