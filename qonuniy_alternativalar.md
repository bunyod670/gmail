# Qonuniy Email Alternativalar

## 1. **Test Email Servislari**

### Mailsac (Bepul va Premium)
```python
import requests

def get_temp_email():
    # Mailsac API orqali vaqtinchalik email olish
    email = f"test{random.randint(1000,9999)}@mailsac.com"
    return email

def check_inbox(email):
    # Xabarlarni tekshirish
    url = f"https://mailsac.com/api/addresses/{email}/messages"
    response = requests.get(url)
    return response.json()
```

### 10MinuteMail
```python
import requests

class TempMail:
    def __init__(self):
        self.base_url = "https://10minutemail.com"
    
    def get_email(self):
        # Vaqtinchalik email olish
        response = requests.get(f"{self.base_url}/10MinuteMail/index.html")
        # Email parse qilish
        return email
```

## 2. **Google Workspace API (Qonuniy)**

### Setup
```bash
pip install google-api-python-client google-auth google-auth-oauthlib
```

### Kod
```python
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials

def create_user_workspace(admin_email, new_user_data):
    """
    Google Workspace Admin API orqali foydalanuvchi yaratish
    Faqat admin huquqi bor foydalanuvchilar uchun
    """
    service = build('admin', 'directory_v1', credentials=creds)
    
    user_body = {
        'name': {
            'givenName': new_user_data['first_name'],
            'familyName': new_user_data['last_name']
        },
        'primaryEmail': new_user_data['email'],
        'password': new_user_data['password'],
        'orgUnitPath': '/'
    }
    
    try:
        user = service.users().insert(body=user_body).execute()
        return user
    except Exception as e:
        print(f"Xato: {e}")
        return None
```

## 3. **Email Testing Libraries**

### Mailtrap (Test Environment)
```python
import smtplib
from email.mime.text import MIMEText

def send_test_email():
    # Mailtrap test server
    server = smtplib.SMTP('smtp.mailtrap.io', 2525)
    server.login('your_username', 'your_password')
    
    msg = MIMEText('Test xabar')
    msg['Subject'] = 'Test'
    msg['From'] = 'test@example.com'
    msg['To'] = 'recipient@example.com'
    
    server.send_message(msg)
    server.quit()
```

## 4. **Mock Email Service**

### Local Test Server
```python
import smtpd
import asyncore
import threading

class MockSMTPServer(smtpd.SMTPServer):
    def process_message(self, peer, mailfrom, rcpttos, data, **kwargs):
        print(f"Email keldi: {mailfrom} -> {rcpttos}")
        print(f"Mazmun: {data.decode()}")

def start_mock_server():
    server = MockSMTPServer(('localhost', 1025), None)
    asyncore.loop()

# Background'da ishga tushirish
thread = threading.Thread(target=start_mock_server)
thread.daemon = True
thread.start()
```

## 5. **Email Validation Service**

### Real Email Checker
```python
import re
import dns.resolver
import smtplib

def validate_email(email):
    """Email manzilni tekshirish"""
    # Format tekshirish
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    if not re.match(pattern, email):
        return False, "Noto'g'ri format"
    
    # Domain tekshirish
    domain = email.split('@')[1]
    try:
        mx_records = dns.resolver.resolve(domain, 'MX')
        if not mx_records:
            return False, "Domain mavjud emas"
    except:
        return False, "DNS xatosi"
    
    return True, "To'g'ri email"
```

## 6. **Selenium bilan Qonuniy Test**

### Test Account Creation
```python
from selenium import webdriver
from selenium.webdriver.common.by import By

def test_registration_form():
    """
    O'zingizning test saytingizda ro'yxatdan o'tishni test qilish
    """
    driver = webdriver.Chrome()
    
    try:
        # O'z test saytingizga boring
        driver.get("http://localhost:3000/register")
        
        # Test ma'lumotlari
        driver.find_element(By.NAME, "email").send_keys("test@example.com")
        driver.find_element(By.NAME, "password").send_keys("test123")
        driver.find_element(By.NAME, "submit").click()
        
        # Natijani tekshiring
        success_msg = driver.find_element(By.CLASS_NAME, "success")
        assert "muvaffaqiyatli" in success_msg.text.lower()
        
    finally:
        driver.quit()
```

## 7. **Environment Setup**

### .env faylida konfiguratsiya
```bash
# .env
TEST_EMAIL_DOMAIN=@test.localhost
MAILTRAP_USER=your_username
MAILTRAP_PASS=your_password
WORKSPACE_ADMIN_EMAIL=admin@yourcompany.com
```

### Config loader
```python
import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    TEST_EMAIL_DOMAIN = os.getenv('TEST_EMAIL_DOMAIN', '@test.localhost')
    MAILTRAP_USER = os.getenv('MAILTRAP_USER')
    MAILTRAP_PASS = os.getenv('MAILTRAP_PASS')
```

## **Xulosa**

Bu usullar:
✅ Qonuniy va xavfsiz
✅ Google tomonidan qo'llab-quvvatlanadi
✅ Professional ishda ishlatiladi
✅ IP bloklanmaydi
✅ Spam yaratmaydi

**Tavsiya:** Yuqoridagi usullardan birini tanlang va men sizga to'liq ishlaydigan kod yozib beraman!