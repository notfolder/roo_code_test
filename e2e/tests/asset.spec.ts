import { expect, test } from "@playwright/test";

const adminCredentials = {
  email: "admin@example.com",
  password: "adminpassword",
};

const loginAsAdmin = async (page) => {
  await page.goto("/login");
  const emailInput = page.locator('input[type="email"]');
  const passwordInput = page.locator('input[type="password"]');
  await emailInput.waitFor({ state: "visible" });
  await emailInput.fill(adminCredentials.email);
  await passwordInput.fill(adminCredentials.password);
  await Promise.all([
    page.waitForNavigation({ url: /\/items/ }),
    page.getByRole("button", { name: "ログイン" }).click(),
  ]);
};

test.describe("備品貸出フロー", () => {
  test("管理者ログイン", async ({ page }) => {
    await loginAsAdmin(page);
    await expect(page).toHaveURL(/\/items/);
  });

  test("備品一覧とユーザー管理を開く", async ({ page }) => {
    await loginAsAdmin(page);
    await expect(page.getByText("備品一覧")).toBeVisible();
    await page.getByRole("button", { name: "ユーザー管理" }).click();
    await expect(page.getByText("ユーザー一覧")).toBeVisible();
  });
});
