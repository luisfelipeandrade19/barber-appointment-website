import { Page, Locator, expect } from '@playwright/test';

/**
 * Interface para dados do formulário de registro
 */
export interface RegisterData {
  name: string;
  email: string;
  password: string;
  confirmPassword: string;
}

/**
 * Page Object para a página de Registro
 */
export class RegisterPage {
  readonly page: Page;
  readonly nameInput: Locator;
  readonly emailInput: Locator;
  readonly passwordInput: Locator;
  readonly confirmPasswordInput: Locator;
  readonly registerButton: Locator;
  readonly loginLink: Locator;


  constructor(page: Page) {
    this.page = page;
    this.nameInput = page.locator('#userNamer');
    this.emailInput = page.locator('#inputUsername');
    this.passwordInput = page.locator('#inputPassword');
    this.confirmPasswordInput = page.locator('#confirmPassword');
    this.registerButton = page.locator('#registerButton');
    this.loginLink = page.getByText('Fazer Login');
 
  }

  /**
   * Navega para a página de registro
   */
  async goto(): Promise<void> {
    await this.page.goto('/register');
  }

  /**
   * Verifica se a página está visível
   */
  async isVisible(): Promise<boolean> {
    return await this.nameInput.isVisible();
  }

  /**
   * Preenche o campo de nome
   */
  async fillName(name: string): Promise<void> {
    await this.nameInput.fill(name);
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
   * Preenche o campo de confirmar senha
   */
  async fillConfirmPassword(password: string): Promise<void> {
    await this.confirmPasswordInput.fill(password);
  }

  /**
   * Preenche todo o formulário com os dados fornecidos
   */
  async fillForm(data: RegisterData): Promise<void> {
    await this.fillName(data.name);
    await this.fillEmail(data.email);
    await this.fillPassword(data.password);
    await this.fillConfirmPassword(data.confirmPassword);
  }

  /**
   * Submete o formulário
   */
  async submit(): Promise<void> {
    await this.registerButton.click();
  }

  /**
   * Clica no link para login
   */
  async clickLogin(): Promise<void> {
    await this.loginLink.click();
  }

  /**
   * Verifica se todos os campos estão presentes e visíveis
   */
  async verifyAllFields(): Promise<void> {
    await expect(this.nameInput).toBeVisible();
    await expect(this.emailInput).toBeVisible();
    await expect(this.passwordInput).toBeVisible();
    await expect(this.confirmPasswordInput).toBeVisible();
  }

  /**
   * Verifica se o botão de registro está presente e visível
   */
  async verifyRegisterButton(): Promise<void> {
    await expect(this.registerButton).toBeVisible();
  }

 
  /**
   * Verifica se o link "Fazer Login" está presente
   */
  async verifyLoginLink(): Promise<void> {
    await expect(this.loginLink).toBeVisible();
  }
}

