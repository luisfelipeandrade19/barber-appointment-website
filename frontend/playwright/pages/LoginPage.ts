import { Page, Locator, expect } from '@playwright/test';

/**
 * Page Object para a página de Login
 */
export class LoginPage {
  readonly page: Page;
  readonly emailInput: Locator;
  readonly passwordInput: Locator;
  readonly loginButton: Locator;
  readonly registerLink: Locator;
  readonly titleSocialLogin: Locator;




  constructor(page: Page) {
    this.page = page;
    this.emailInput = page.locator('#inputUsername');
    this.passwordInput = page.locator('#inputPassword');
    this.loginButton = page.locator('#loginButton');
    this.registerLink = page.getByText('Cadastrar-se');
    this.titleSocialLogin = page.locator('#titleSocialLogin');
  }

  /**
   * Navega para a página de login
   */
  async goto(): Promise<void> {
    await this.page.goto('/');
  }

  /**
   * Verifica se a página está visível
   */
  async isVisible(): Promise<boolean> {
    return await this.emailInput.isVisible();
  }

  /**
   * Preenche o campo de email
   */
  async fillEmail(email: string): Promise<void> {
    await this.emailInput.fill(email);
  }

  /**
   * Preenche o campo de senha
   */
  async fillPassword(password: string): Promise<void> {
    await this.passwordInput.fill(password);
  }

  /**
   * Clica no botão de login
   */
  async clickLogin(): Promise<void> {
    await this.loginButton.click();
  }

  /**
   * Clica no link para registro
   */
  async clickRegister(): Promise<void> {
    await this.registerLink.click();
  }

  /**
   * Verifica se o campo de email está presente e visível
   */
  async verifyEmailField(): Promise<void> {
    await expect(this.emailInput).toBeVisible();
  }

  /**
   * Verifica se o campo de senha está presente e visível
   */
  async verifyPasswordField(): Promise<void> {
    await expect(this.passwordInput).toBeVisible();
  }

  /**
   * Verifica se o botão de login está presente e visível
   */
  async verifyLoginButton(): Promise<void> {
    await expect(this.loginButton).toBeVisible();
  }
  /**
   * Verifica se o link "Cadastrar-se" está presente
   */
  async verifyRegisterLink(): Promise<void> {
    await expect(this.registerLink).toBeVisible();
  }

}

