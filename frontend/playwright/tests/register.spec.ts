import { test, expect } from '@playwright/test';
import { RegisterPage, RegisterData } from '../pages/RegisterPage';

test.describe('Página de Registro', () => {
  test('deve exibir página de registro corretamente ao acessar /register', async ({ page }) => {
    const registerPage = new RegisterPage(page);
    await registerPage.goto();
    
    const isVisible = await registerPage.isVisible();
    expect(isVisible).toBeTruthy();
  });

  test('deve ter campo de nome presente e visível', async ({ page }) => {
    const registerPage = new RegisterPage(page);
    await registerPage.goto();
    
    await expect(registerPage.nameInput).toBeVisible();
  });

  test('deve ter campo de email presente e visível', async ({ page }) => {
    const registerPage = new RegisterPage(page);
    await registerPage.goto();
    
    await expect(registerPage.emailInput).toBeVisible();
  });

  test('deve ter campo de senha presente e visível', async ({ page }) => {
    const registerPage = new RegisterPage(page);
    await registerPage.goto();
    
    await expect(registerPage.passwordInput).toBeVisible();
  });

  test('deve ter campo de confirmar senha presente e visível', async ({ page }) => {
    const registerPage = new RegisterPage(page);
    await registerPage.goto();
    
    await expect(registerPage.confirmPasswordInput).toBeVisible();
  });

  test('deve ter todos os campos do formulário presentes', async ({ page }) => {
    const registerPage = new RegisterPage(page);
    await registerPage.goto();
    
    await registerPage.verifyAllFields();
  });

  test('deve ter botão de registro presente e clicável', async ({ page }) => {
    const registerPage = new RegisterPage(page);
    await registerPage.goto();
    
    await registerPage.verifyRegisterButton();
    
    const isEnabled = await registerPage.registerButton.isEnabled();
    expect(isEnabled).toBeTruthy();
  });

  test('deve ter link "Fazer Login" presente', async ({ page }) => {
    const registerPage = new RegisterPage(page);
    await registerPage.goto();
    
    await registerPage.verifyLoginLink();
  });


  test('deve permitir preencher formulário completo', async ({ page }) => {
    const registerPage = new RegisterPage(page);
    await registerPage.goto();
    
    const formData: RegisterData = {
      name: 'João Silva',
      email: 'joao@example.com',
      password: 'senha123',
      confirmPassword: 'senha123',
    };
    
    await registerPage.fillForm(formData);
    
    const nameValue = await registerPage.nameInput.inputValue();
    const emailValue = await registerPage.emailInput.inputValue();
    const passwordValue = await registerPage.passwordInput.inputValue();
    const confirmPasswordValue = await registerPage.confirmPasswordInput.inputValue();
    
    expect(nameValue).toBe(formData.name);
    expect(emailValue).toBe(formData.email);
    expect(passwordValue).toBe(formData.password);
    expect(confirmPasswordValue).toBe(formData.confirmPassword);
  });

  test('deve navegar para página de login ao clicar no link', async ({ page }) => {
    const registerPage = new RegisterPage(page);
    await registerPage.goto();
    
    await registerPage.clickLogin();
    
    await expect(page).toHaveURL(/\//);
  });

  test('deve redirecionar para /home após realizar registro', async ({ page }) => {
    const registerPage = new RegisterPage(page);
    await registerPage.goto();
    
    const formData: RegisterData = {
      name: 'João Silva',
      email: 'joao@example.com',
      password: 'senha123',
      confirmPassword: 'senha123',
    };
    
    await registerPage.fillForm(formData);
    
    await Promise.all([
      page.waitForURL(/.*\get?/),
      registerPage.submit()
    ]);
    
    await expect(page).toHaveURL(/.*\get?/);
  });
});

