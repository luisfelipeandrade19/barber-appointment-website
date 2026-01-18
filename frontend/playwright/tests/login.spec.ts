import { test, expect } from '@playwright/test';
import { LoginPage } from '../pages/LoginPage';

test.describe('Página de Login', () => {
  test('deve exibir página de login corretamente ao acessar /', async ({ page }) => {
    const loginPage = new LoginPage(page);
    await loginPage.goto();
    
    const isVisible = await loginPage.isVisible();
    expect(isVisible).toBeTruthy();
  });

  test('deve ter campo de email presente e visível', async ({ page }) => {
    const loginPage = new LoginPage(page);
    await loginPage.goto();
    
    await loginPage.verifyEmailField();
  });

  test('deve ter campo de senha presente e visível', async ({ page }) => {
    const loginPage = new LoginPage(page);
    await loginPage.goto();
    
    await loginPage.verifyPasswordField();
  });

  test('deve ter botão de login presente e clicável', async ({ page }) => {
    const loginPage = new LoginPage(page);
    await loginPage.goto();
    
    await loginPage.verifyLoginButton();
    
    const isEnabled = await loginPage.loginButton.isEnabled();
    expect(isEnabled).toBeTruthy();
  });

  test('deve ter link "Cadastrar-se" presente', async ({ page }) => {
    const loginPage = new LoginPage(page);
    await loginPage.goto();
    
    await loginPage.verifyRegisterLink();
  });


  test('deve permitir preencher email e senha', async ({ page }) => {
    const loginPage = new LoginPage(page);
    await loginPage.goto();
    
    const testEmail = 'test@example.com';
    const testPassword = 'senha123';
    
    await loginPage.fillEmail(testEmail);
    await loginPage.fillPassword(testPassword);
    
    const emailValue = await loginPage.emailInput.inputValue();
    const passwordValue = await loginPage.passwordInput.inputValue();
    
    expect(emailValue).toBe(testEmail);
    expect(passwordValue).toBe(testPassword);
  });

  test('deve navegar para página de registro ao clicar no link', async ({ page }) => {
    const loginPage = new LoginPage(page);
    await loginPage.goto();
    
    await loginPage.clickRegister();
    
    await expect(page).toHaveURL(/.*\/register/);
  });

  test('deve redirecionar para /home após realizar login', async ({ page }) => {
    const loginPage = new LoginPage(page);
    await loginPage.goto();
    
    const testEmail = 'test@example.com';
    const testPassword = 'senha123';
    
    await loginPage.fillEmail(testEmail);
    await loginPage.fillPassword(testPassword);
    

    await Promise.all([
      page.waitForURL(/.*\get?/),
      loginPage.clickLogin()
    ]);
    
    await expect(page).toHaveURL(/.*\get?/);
  });
});

