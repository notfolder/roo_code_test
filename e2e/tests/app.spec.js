import { expect, test } from '@playwright/test'

const ADMIN_EMAIL = 'admin@example.com'
const ADMIN_PASSWORD = 'admin1234'

async function login(page, email = ADMIN_EMAIL, password = ADMIN_PASSWORD) {
  await page.goto('/login')
  await page.getByLabel('メールアドレス').fill(email)
  await page.getByLabel('パスワード').fill(password)
  await page.getByRole('button', { name: 'ログイン' }).click()
  await expect(page).toHaveURL(/\/$/)
}

test('ログインと備品一覧表示', async ({ page }) => {
  await login(page)
  await expect(page.getByRole('main').getByText('備品一覧')).toBeVisible()
  await expect(page.getByTestId('item-row-PC-001')).toBeVisible()
  await expect(page.getByTestId('item-row-PC-002')).toBeVisible()
  await expect(page.getByTestId('item-row-MON-010')).toBeVisible()
})

test('備品登録と備品編集', async ({ page }) => {
  await login(page)
  const unique = `E2E-${Date.now()}`

  await page.getByRole('button', { name: '備品登録' }).click()
  await page.getByLabel('資産管理番号').fill(unique)
  await page.getByLabel('名称').fill('E2E Device')
  await page.getByRole('button', { name: '保存' }).click()

  const createdRow = page.locator('tr', { hasText: unique })
  await expect(createdRow).toBeVisible()

  await createdRow.getByRole('button', { name: '編集' }).click()
  await page.getByLabel('名称').fill('E2E Device Updated')
  await page.getByRole('button', { name: '保存' }).click()
  await expect(createdRow).toContainText('E2E Device Updated')
})

test('貸出処理と返却処理', async ({ page }) => {
  await login(page)
  const targetRow = page.locator('tr', { hasText: 'PC-001' })

  await targetRow.getByRole('button', { name: '貸出' }).click()
  await page.getByRole('button', { name: '貸出を確定' }).click()
  await expect(targetRow).toContainText('貸出中')

  await targetRow.getByRole('button', { name: '返却' }).click()
  await page.getByRole('button', { name: '返却を確定' }).click()
  await expect(targetRow).toContainText('貸出可')
})

test('ユーザー登録・一覧・詳細・編集・削除', async ({ page }) => {
  await login(page)
  await page.getByRole('link', { name: 'ユーザー管理' }).click()
  await expect(page).toHaveURL(/\/users$/)

  const unique = Date.now()
  const initialEmail = `e2e-user-${unique}@example.com`
  const updatedEmail = `e2e-user-updated-${unique}@example.com`

  await page.getByRole('button', { name: 'ユーザー登録' }).click()
  await page.getByLabel('氏名').fill('E2E User')
  await page.getByLabel('メール').fill(initialEmail)
  await page.getByLabel('パスワード').fill('password1234')
  await page.getByRole('button', { name: '保存' }).click()

  const createdUserRow = page.locator('tr', { hasText: initialEmail })
  await expect(createdUserRow).toBeVisible()

  await createdUserRow.getByRole('button', { name: '詳細' }).click()
  await expect(page.getByText(initialEmail)).toBeVisible()
  await page.getByRole('button', { name: '閉じる' }).click()

  await createdUserRow.getByRole('button', { name: '編集' }).click()
  await page.getByLabel('メール').fill(updatedEmail)
  await page.getByLabel('氏名').fill('E2E User Updated')
  await page.getByRole('button', { name: '保存' }).click()

  const updatedUserRow = page.locator('tr', { hasText: updatedEmail })
  await expect(updatedUserRow).toBeVisible()

  await updatedUserRow.getByRole('button', { name: '削除' }).click()
  await expect(updatedUserRow).toContainText('削除済')
})
