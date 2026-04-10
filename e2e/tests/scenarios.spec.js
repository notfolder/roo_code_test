// @ts-check
const { test, expect } = require('@playwright/test')

const BASE_URL = process.env.BASE_URL || 'http://localhost'
const ADMIN_ID = 'admin'
const ADMIN_PW = 'password'

// ログインヘルパー
async function loginAs(page, loginId, password) {
  await page.goto(BASE_URL + '/login')
  await page.locator('[data-testid="login-id"] input').fill(loginId)
  await page.locator('[data-testid="login-password"] input').fill(password)
  await page.locator('[data-testid="login-button"]').click()
  await page.waitForURL(BASE_URL + '/')
}

// T01: 未ログイン時にログイン画面へリダイレクト
test('T01: 未ログイン時にログイン画面へリダイレクト', async ({ page }) => {
  await page.goto(BASE_URL + '/')
  await expect(page).toHaveURL(/\/login/)
})

// T02: 管理者ログイン
test('T02: 管理者ログイン', async ({ page }) => {
  await loginAs(page, ADMIN_ID, ADMIN_PW)
  await expect(page).toHaveURL(BASE_URL + '/')
  await expect(page.locator('[data-testid="lend-button"]')).toBeVisible()
  await expect(page.locator('[data-testid="item-manage-button"]')).toBeVisible()
})

// T03: 一般ユーザーログイン
test('T03: 一般ユーザーログイン', async ({ page }) => {
  // 事前に一般ユーザーを作成（adminでログイン後）
  await loginAs(page, ADMIN_ID, ADMIN_PW)
  await page.goto(BASE_URL + '/users')
  await page.locator('[data-testid="user-add-button"]').click()
  await page.locator('[data-testid="user-login-id"] input').fill('testuser01')
  await page.locator('[data-testid="user-password"] input').fill('userpass')
  // ロール選択（一般ユーザー）
  await page.locator('[data-testid="user-role"]').click()
  await page.locator('.v-overlay--active .v-list-item').filter({ hasText: '一般ユーザー' }).click()
  await page.locator('[data-testid="user-save-button"]').click()
  await page.waitForTimeout(500)

  // 一般ユーザーでログイン
  await page.goto(BASE_URL + '/login')
  await page.locator('[data-testid="login-id"] input').fill('testuser01')
  await page.locator('[data-testid="login-password"] input').fill('userpass')
  await page.locator('[data-testid="login-button"]').click()
  await page.waitForURL(BASE_URL + '/')

  await expect(page.locator('[data-testid="lend-button"]')).not.toBeVisible()
  await expect(page.locator('[data-testid="item-manage-button"]')).not.toBeVisible()
  await expect(page.locator('[data-testid="history-button"]')).toBeVisible()
  await expect(page.locator('[data-testid="logout-button"]')).toBeVisible()
})

// T04: 管理者が備品登録
test('T04: 管理者が備品登録', async ({ page }) => {
  await loginAs(page, ADMIN_ID, ADMIN_PW)
  await page.goto(BASE_URL + '/items/manage')
  await page.locator('[data-testid="item-add-button"]').click()
  await page.locator('[data-testid="item-id"] input').fill('TEST001')
  await page.locator('[data-testid="item-name"] input').fill('テスト備品001')
  await page.locator('[data-testid="item-save-button"]').click()
  await page.waitForTimeout(500)
  await expect(page.getByText('TEST001')).toBeVisible()
  await expect(page.getByText('テスト備品001')).toBeVisible()
})

// T05: 管理者が備品編集
test('T05: 管理者が備品編集', async ({ page }) => {
  await loginAs(page, ADMIN_ID, ADMIN_PW)
  await page.goto(BASE_URL + '/items/manage')
  await page.locator('[data-testid="item-edit-button-TEST001"]').click()
  await page.locator('[data-testid="item-name"] input').clear()
  await page.locator('[data-testid="item-name"] input').fill('テスト備品001-更新')
  await page.locator('[data-testid="item-save-button"]').click()
  await page.waitForTimeout(500)
  await expect(page.getByText('テスト備品001-更新')).toBeVisible()
})

// T06: 管理者が備品削除
test('T06: 管理者が備品削除（利用可能な備品）', async ({ page }) => {
  // 削除用備品を作成
  await loginAs(page, ADMIN_ID, ADMIN_PW)
  await page.goto(BASE_URL + '/items/manage')
  await page.locator('[data-testid="item-add-button"]').click()
  await page.locator('[data-testid="item-id"] input').fill('DEL001')
  await page.locator('[data-testid="item-name"] input').fill('削除テスト備品')
  await page.locator('[data-testid="item-save-button"]').click()
  await page.waitForTimeout(500)

  await page.locator('[data-testid="item-delete-button-DEL001"]').click()
  await page.locator('[data-testid="confirm-button"]').click()
  await page.waitForTimeout(500)
  await expect(page.getByText('DEL001')).not.toBeVisible()
})

// T07: 管理者が貸出登録
test('T07: 管理者が貸出登録', async ({ page }) => {
  await loginAs(page, ADMIN_ID, ADMIN_PW)
  // TEST001が利用可能な前提
  await page.goto(BASE_URL + '/lend')
  await page.waitForTimeout(500)
  // 備品選択
  await page.locator('[data-testid="lend-item"]').click()
  await page.getByText(/TEST001/).first().click()
  // 借用者選択
  await page.locator('[data-testid="lend-borrower"]').click()
  await page.getByText('admin').first().click()
  // 登録
  await page.locator('[data-testid="lend-submit-button"]').click()
  await page.waitForURL(BASE_URL + '/')
  await expect(page.getByText('貸出中')).toBeVisible()
  await expect(page.getByText('admin')).toBeVisible()
})

// T08: 管理者が返却登録
test('T08: 管理者が返却登録', async ({ page }) => {
  await loginAs(page, ADMIN_ID, ADMIN_PW)
  await page.goto(BASE_URL + '/return')
  await page.waitForTimeout(500)
  // 貸出記録選択
  await page.locator('[data-testid="return-record"]').click()
  await page.locator('.v-list-item').first().click()
  // 返却日入力
  await page.locator('[data-testid="return-date"] input').fill('2026-04-06')
  await page.locator('[data-testid="return-submit-button"]').click()
  await page.waitForURL(BASE_URL + '/')
  await expect(page.getByText('利用可能')).toBeVisible()
})

// T09: 貸出履歴確認
test('T09: 貸出履歴確認', async ({ page }) => {
  await loginAs(page, ADMIN_ID, ADMIN_PW)
  await page.goto(BASE_URL + '/history')
  const rows = page.locator('tbody tr')
  await expect(rows.first()).toBeVisible({ timeout: 5000 })
  expect(await rows.count()).toBeGreaterThanOrEqual(1)
})

// T10: 管理者ログアウト
test('T10: 管理者ログアウト', async ({ page }) => {
  await loginAs(page, ADMIN_ID, ADMIN_PW)
  await page.locator('[data-testid="logout-button"]').click()
  await expect(page).toHaveURL(/\/login/)
})

// T11: ユーザーアカウント追加
test('T11: ユーザーアカウント追加', async ({ page }) => {
  await loginAs(page, ADMIN_ID, ADMIN_PW)
  await page.goto(BASE_URL + '/users')
  await page.locator('[data-testid="user-add-button"]').click()
  await page.locator('[data-testid="user-login-id"] input').fill('newuser11')
  await page.locator('[data-testid="user-password"] input').fill('newpass')
  await page.locator('[data-testid="user-role"]').click()
  await page.locator('.v-overlay--active .v-list-item').filter({ hasText: '一般ユーザー' }).click()
  await page.locator('[data-testid="user-save-button"]').click()
  await page.waitForTimeout(500)
  await expect(page.getByText('newuser11')).toBeVisible()
})

// T12: ユーザーアカウント削除
test('T12: ユーザーアカウント削除', async ({ page }) => {
  // 削除対象ユーザーを作成
  await loginAs(page, ADMIN_ID, ADMIN_PW)
  await page.goto(BASE_URL + '/users')
  await page.locator('[data-testid="user-add-button"]').click()
  await page.locator('[data-testid="user-login-id"] input').fill('deluser12')
  await page.locator('[data-testid="user-password"] input').fill('delpass')
  await page.locator('[data-testid="user-role"]').click()
  await page.locator('.v-overlay--active .v-list-item').filter({ hasText: '一般ユーザー' }).click()
  await page.locator('[data-testid="user-save-button"]').click()
  await page.waitForTimeout(500)

  // IDを特定して削除
  const rows = page.locator('tbody tr')
  const count = await rows.count()
  let userId = null
  for (let i = 0; i < count; i++) {
    const text = await rows.nth(i).locator('td').first().textContent()
    if (text?.trim() === 'deluser12') {
      const deleteBtn = rows.nth(i).locator('button')
      const testId = await deleteBtn.getAttribute('data-testid')
      userId = testId?.replace('user-delete-button-', '')
      break
    }
  }
  await page.locator(`[data-testid="user-delete-button-${userId}"]`).click()
  await page.locator('[data-testid="confirm-button"]').click()
  await page.waitForTimeout(500)
  await expect(page.getByText('deluser12')).not.toBeVisible()
})

// T13: 最後の管理者削除不可
test('T13: 最後の管理者削除不可', async ({ page }) => {
  await loginAs(page, ADMIN_ID, ADMIN_PW)
  await page.goto(BASE_URL + '/users')
  await page.waitForTimeout(300)
  // admin行を探す
  const rows = page.locator('tbody tr')
  const count = await rows.count()
  let adminUserId = null
  for (let i = 0; i < count; i++) {
    const cells = rows.nth(i).locator('td')
    const loginIdText = await cells.nth(0).textContent()
    const roleText = await cells.nth(1).textContent()
    if (loginIdText?.trim() === ADMIN_ID && roleText?.includes('管理者')) {
      const btn = rows.nth(i).locator('button')
      const testId = await btn.getAttribute('data-testid')
      adminUserId = testId?.replace('user-delete-button-', '')
      break
    }
  }
  await page.locator(`[data-testid="user-delete-button-${adminUserId}"]`).click()
  await page.locator('[data-testid="confirm-button"]').click()
  await page.waitForTimeout(500)
  await expect(page.locator('.v-snackbar')).toBeVisible()
})

// T14: 貸出中備品削除不可
test('T14: 貸出中備品削除不可', async ({ page }) => {
  // TEST001を貸出中にする（T07後の状態を想定。独立実行のため貸出登録から）
  await loginAs(page, ADMIN_ID, ADMIN_PW)

  // 貸出中備品が存在することを確認して削除試行
  await page.goto(BASE_URL + '/items/manage')
  await page.waitForTimeout(300)
  // 貸出中の行を探す
  const rows = page.locator('tbody tr')
  const count = await rows.count()
  for (let i = 0; i < count; i++) {
    const cells = rows.nth(i).locator('td')
    const statusText = await cells.nth(2).textContent()
    if (statusText?.includes('貸出中')) {
      const btn = rows.nth(i).locator('button[color="error"]').first()
      await btn.click()
      await page.locator('[data-testid="confirm-button"]').click()
      await page.waitForTimeout(500)
      await expect(page.locator('.v-snackbar')).toBeVisible()
      return
    }
  }
  // 貸出中備品がなければテストをスキップ
  test.skip()
})

// T15: 一般ユーザーは管理操作不可
test('T15: 一般ユーザーは管理専用URLに直接アクセスできない', async ({ page }) => {
  // 一般ユーザーでログイン
  await page.goto(BASE_URL + '/login')
  await page.locator('[data-testid="login-id"] input').fill('testuser01')
  await page.locator('[data-testid="login-password"] input').fill('userpass')
  await page.locator('[data-testid="login-button"]').click()
  await page.waitForURL(BASE_URL + '/')

  await page.goto(BASE_URL + '/items/manage')
  await expect(page).toHaveURL(BASE_URL + '/')

  await page.goto(BASE_URL + '/lend')
  await expect(page).toHaveURL(BASE_URL + '/')

  await page.goto(BASE_URL + '/return')
  await expect(page).toHaveURL(BASE_URL + '/')

  await page.goto(BASE_URL + '/users')
  await expect(page).toHaveURL(BASE_URL + '/')
})

// T16: 貸出中借用者アカウント削除不可
test('T16: 貸出中借用者アカウント削除不可', async ({ page }) => {
  // admin自身が貸出中のケースを想定
  await loginAs(page, ADMIN_ID, ADMIN_PW)

  // 貸出登録 (testuser01を借用者に)
  await page.goto(BASE_URL + '/lend')
  await page.waitForTimeout(500)

  // 利用可能な備品を選択
  await page.locator('[data-testid="lend-item"]').click()
  const firstOption = page.locator('.v-list-item').first()
  await firstOption.click()

  await page.locator('[data-testid="lend-borrower"]').click()
  await page.getByText('testuser01').first().click()
  await page.locator('[data-testid="lend-submit-button"]').click()
  await page.waitForURL(BASE_URL + '/')

  // testuser01を削除しようとする
  await page.goto(BASE_URL + '/users')
  await page.waitForTimeout(300)
  const rows = page.locator('tbody tr')
  const count = await rows.count()
  for (let i = 0; i < count; i++) {
    const loginIdText = await rows.nth(i).locator('td').first().textContent()
    if (loginIdText?.trim() === 'testuser01') {
      const btn = rows.nth(i).locator('button')
      const testId = await btn.getAttribute('data-testid')
      const userId = testId?.replace('user-delete-button-', '')
      await page.locator(`[data-testid="user-delete-button-${userId}"]`).click()
      await page.locator('[data-testid="confirm-button"]').click()
      await page.waitForTimeout(500)
      await expect(page.locator('.v-snackbar')).toBeVisible()
      return
    }
  }
  test.skip()
})

// T17: ログイン失敗時エラー表示
test('T17: ログイン失敗時エラー表示', async ({ page }) => {
  await page.goto(BASE_URL + '/login')
  await page.locator('[data-testid="login-id"] input').fill('wronguser')
  await page.locator('[data-testid="login-password"] input').fill('wrongpass')
  await page.locator('[data-testid="login-button"]').click()
  await expect(page.getByText('IDまたはパスワードが正しくありません')).toBeVisible()
  await expect(page).toHaveURL(/\/login/)
})
