# Google Workspace Email Creator - Setup Guide

## 🎯 Bu Nima?

Bu script **Google Workspace API** orqali **o'z domeningizda** email akkauntlari yaratish uchun. Bu **to'liq qonuniy** va Google tomonidan qo'llab-quvvatlanadigan usul.

## ✅ Talablar

1. **Google Workspace akkaunt** (admin huquqi bilan)
2. **O'z domeningiz** (example.com)
3. **Python 3.7+**
4. **Internet aloqasi**

## 🚀 1-qadam: Google Cloud Console'da Setup

### 1.1 Loyiha yaratish
1. [Google Cloud Console](https://console.cloud.google.com/) ga kiring
2. Yangi loyiha yarating yoki mavjud loyihani tanlang
3. **Project ID** ni eslab qoling

### 1.2 Google Workspace Admin API yoqish
1. Cloud Console'da **APIs & Services > Library** ga boring
2. "Admin SDK API" ni qidiring va **Enable** qiling
3. "Google Workspace Admin SDK" ni ham yoqing

### 1.3 Credentials yaratish
1. **APIs & Services > Credentials** ga boring
2. **+ CREATE CREDENTIALS > OAuth client ID** tugmasini bosing
3. **Application type**: "Desktop application" tanlang
4. **Name**: "Workspace Email Creator" deb nomlang
5. **CREATE** tugmasini bosing
6. **Download JSON** tugmasini bosing va faylni `credentials.json` deb saqlang

## 🔧 2-qadam: Google Workspace Admin Setup

### 2.1 Domain Admin huquqlari
1. [Google Admin Console](https://admin.google.com/) ga kiring
2. **Admin roles** bo'limiga boring  
3. O'zingizga **Super Admin** yoki **User Management Admin** roli berilganligini tekshiring

### 2.2 API access yoqish
1. Admin Console'da **Security > API controls** ga boring
2. **Domain-wide delegation** ni yoqing
3. **Manage Domain Wide Delegation** tugmasini bosing

## 🛠️ 3-qadam: Python Environment Setup

### 3.1 Virtual Environment yaratish
```bash
# Virtual environment yaratish
python3 -m venv workspace_env

# Aktivlashtirish (Linux/Mac)
source workspace_env/bin/activate

# Aktivlashtirish (Windows)
workspace_env\Scripts\activate
```

### 3.2 Dependencies o'rnatish
```bash
pip install -r requirements.txt
```

### 3.3 Fayllarni joylashtirish
```
workspace_email_creator/
├── workspace_email_creator.py
├── requirements.txt
├── credentials.json          # Google Cloud Console'dan
├── workspace_config.json     # Avtomatik yaratiladi
└── SETUP_GUIDE.md           # Bu fayl
```

## ⚙️ 4-qadam: Konfiguratsiya

### 4.1 Script'da domenni o'zgartirish
`workspace_email_creator.py` faylida:
```python
# 282-qatorni topib, o'z domeningizga o'zgartiring
DOMAIN = "yourdomain.com"  # Bu yerga o'z domeningizni yozing
```

**Misol:**
```python
DOMAIN = "mycompany.com"
```

### 4.2 Birinchi authentication
```bash
python3 workspace_email_creator.py
```

Script birinchi marta ishlaganda:
1. Browser ochiladi
2. Google akkauntingiz bilan login qiling
3. **Allow** tugmasini bosing
4. Browser'ni yoping

## 🎮 5-qadam: Ishlatish

### 5.1 Script ishga tushirish
```bash
python3 workspace_email_creator.py
```

### 5.2 Menyular

**1. Bitta foydalanuvchi yaratish**
- Ism va familiya kiriting
- Username ixtiyoriy
- Avtomatik xavfsiz parol yaratiladi

**2. Ko'p foydalanuvchi yaratish**
- Soni kiriting (masalan: 5)
- Har biri uchun ism/familiya kiriting
- Hammasiga avtomatik email va parol yaratiladi

**3. Foydalanuvchilarni ko'rsatish**
- Domeningizdagi barcha foydalanuvchilar
- Status (faol/faolsiz)
- Yaratilish vaqti

**4. Domen ma'lumotlari**
- Jami foydalanuvchilar soni
- Faol/faolsiz statistika
- Script tomonidan yaratilganlar

## 📂 6-qadam: Yaratilgan Ma'lumotlar

### 6.1 Saqlangan fayllar
- **workspace_config.json**: Barcha yaratilgan foydalanuvchilar
- **workspace_emails.log**: Barcha amaliyotlar logi
- **workspace_token.pickle**: Authentication ma'lumotlari

### 6.2 Email ma'lumotlari
Har bir yaratilgan email uchun:
```json
{
  "email": "john.doe@yourcompany.com",
  "password": "A3f9K2mP8xR1",
  "first_name": "John",
  "last_name": "Doe",
  "created_at": "2024-01-15T10:30:00",
  "user_id": "123456789"
}
```

## 🔒 7-qadam: Xavfsizlik

### 7.1 Parol xavfsizligi
- Har bir parol avtomatik yaratiladi (12 ta belgi)
- Harflar, raqamlar va maxsus belgilar
- Birinchi kirishda o'zgartirilishi majbur

### 7.2 Fayl xavfsizligi
- `credentials.json` - maxfiy fayl, boshqalarga ko'rsatmang
- `workspace_config.json` - parollar bor, xavfsiz saqlang
- `.pickle` fayllar - authentication ma'lumotlari

## ❌ Muammolarni Hal Qilish

### 1. "Permission denied" xatosi
```
Sabab: Admin huquqlari yo'q
Yechim: Google Admin Console'da Super Admin roli bering
```

### 2. "Domain not found" xatosi  
```
Sabab: Domen noto'g'ri yozilgan
Yechim: Script'da DOMAIN ni to'g'ri kiriting
```

### 3. "API not enabled" xatosi
```
Sabab: Admin SDK API yoqilmagan
Yechim: Google Cloud Console'da API'ni yoqing
```

### 4. "Invalid credentials" xatosi
```
Sabab: credentials.json fayli noto'g'ri
Yechim: Yangi credentials.json yuklab oling
```

## 🔧 Advanced Konfiguratsiya

### Organizational Unit o'zgartirish
```python
# workspace_config.json da
"organizational_unit": "/IT Department"
```

### Parol uzunligini o'zgartirish
```python
# workspace_config.json da  
"default_password_length": 16
```

### Admin email o'zgartirish
```python
# workspace_config.json da
"admin_email": "admin@yourcompany.com"
```

## 🚀 Production uchun Tavsiyalar

1. **Virtual Environment** ishlating
2. **Backup** qiling (config fayllarni)  
3. **Log monitoring** qo'shing
4. **Rate limiting** ga rioya qiling
5. **Error handling** kengaytiring

## 📞 Yordam

Agar muammo yuzaga kelsa:
1. **Log faylni** tekshiring (`workspace_emails.log`)
2. **Config faylni** tekshiring
3. **Google Admin Console** da huquqlarni tekshiring
4. **API quotas** ni tekshiring

## ✅ Test Qilish

1. Bitta test email yarating
2. Gmail'ga kirib ko'ring
3. Parolni o'zgartiring
4. Email yuborish/qabul qilishni test qiling

---

**🎉 Tayyor! Endi o'z domeningizda email'lar yarata olasiz!**