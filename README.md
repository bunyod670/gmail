# 📧 Google Workspace Email Creator

**O'z domeningizda email akkauntlari yaratish uchun qonuniy va professional tool**

## 🎯 Bu Nima?

Bu loyiha **Google Workspace Admin API** orqali **o'z domeningizda** email akkauntlari yaratish imkonini beradi. Bu:

- ✅ **To'liq qonuniy** - Google rasmiy API'si
- ✅ **Xavfsiz** - Admin huquqlari talab qilinadi  
- ✅ **Professional** - Korporativ foydalanish uchun
- ✅ **Avtomatik** - Ko'p akkaunt bir vaqtda yaratish

## 📁 Loyiha Tuzilishi

```
workspace-email-creator/
├── workspace_email_creator.py    # Asosiy script
├── example_usage.py             # Programmatik misollar
├── requirements.txt             # Python dependencies
├── SETUP_GUIDE.md              # Batafsil o'rnatish qo'llanmasi
└── README.md                   # Bu fayl
```

## 🚀 Tezkor Boshlash

### 1. Dependencies o'rnatish
```bash
pip install -r requirements.txt
```

### 2. Google Workspace setup
1. [Google Cloud Console](https://console.cloud.google.com/) da loyiha yarating
2. **Admin SDK API** ni yoqing
3. **OAuth 2.0 credentials** yuklab oling (`credentials.json`)
4. [Google Admin Console](https://admin.google.com/) da admin huquqlarini bering

### 3. Script ishga tushirish
```bash
python3 workspace_email_creator.py
```

**Batafsil setup uchun [SETUP_GUIDE.md](SETUP_GUIDE.md) ga qarang**

## 🎮 Foydalanish

### Interaktiv Interfeys
```bash
python3 workspace_email_creator.py
```

Menyu tanlovi:
- **1** - Bitta foydalanuvchi yaratish
- **2** - Ko'p foydalanuvchi yaratish
- **3** - Mavjud foydalanuvchilarni ko'rish
- **4** - Domen statistikasi
- **5** - Foydalanuvchini o'chirish
- **6** - Ma'lumotlarni eksport qilish

### Programmatik Foydalanish

```python
from workspace_email_creator import WorkspaceEmailCreator

# Email creator'ni yaratish
creator = WorkspaceEmailCreator("mycompany.com")

# Bitta foydalanuvchi yaratish
result = creator.create_user("Ali", "Karimov", "ali.karimov")

if result['success']:
    print(f"Email: {result['email']}")
    print(f"Parol: {result['password']}")
```

**Ko'proq misollar [example_usage.py](example_usage.py) da**

## 🔧 Funksiyalar

### ✅ Email Yaratish
- Bitta yoki ko'p akkaunt
- Avtomatik username yaratish
- Xavfsiz parol generatsiya
- CSV fayldan import

### ✅ Boshqarish
- Foydalanuvchilarni ko'rish
- Akkauntlarni o'chirish/yangilash
- Status o'zgartirish (faol/faolsiz)
- Domen statistikasi

### ✅ Xavfsizlik
- OAuth 2.0 authentication
- Xavfsiz parol yaratish
- Birinchi kirishda parol o'zgartirishni majburlash
- Barcha amaliyotlar logging

### ✅ Avtomatizatsiya
- CSV fayl bilan ishlash
- JSON eksport/import
- Error handling
- Rate limiting

## 📊 Misollar

### Jamoa uchun email'lar yaratish
```python
team_members = [
    {"first_name": "Ali", "last_name": "Karimov"},
    {"first_name": "Gulnora", "last_name": "Toshmatova"},
    {"first_name": "Bobur", "last_name": "Rahimov"}
]

results = creator.create_multiple_users(team_members)
```

### CSV fayldan ko'p email yaratish
```python
# employees.csv dan o'qish va email'lar yaratish
results = create_bulk_emails_from_csv()
```

### Domen statistikasi
```python
domain_info = creator.get_domain_info()
print(f"Jami foydalanuvchilar: {domain_info['total_users']}")
```

## 🔒 Xavfsizlik

### Talab qilinadigan Huquqlar
- Google Workspace **Super Admin** yoki **User Management Admin**
- Domain ga to'liq admin huquqlari
- Google Cloud loyihasida API access

### Himoyalangan Ma'lumotlar
- **credentials.json** - OAuth credentials (maxfiy!)
- **workspace_config.json** - Yaratilgan akkauntlar va parollar
- **workspace_token.pickle** - Authentication tokenlar

⚠️ **Bu fayllarni boshqalarga ko'rsatmang!**

## 📝 Konfiguratsiya

### Asosiy Sozlamalar
```json
{
  "domain": "mycompany.com",
  "admin_email": "admin@mycompany.com", 
  "organizational_unit": "/",
  "default_password_length": 12
}
```

### Advanced Sozlamalar
- Organizational Unit tanlash
- Parol policy'si
- Rate limiting
- Logging darajasi

## 🚨 Talablar

### Texnik Talablar
- **Python 3.7+**
- **Google Workspace** account (admin bilan)
- **O'z domeningiz** va DNS access
- Internet connection

### Google Workspace Talablar
- Faol Workspace subscription
- Domain ownership verification
- Admin Console access
- API access yoqilgan

## ❌ Muammolarni Hal Qilish

### Tez-tez uchraydigan xatolar:

**"Permission denied"**
```
Sabab: Admin huquqlari yo'q
Yechim: Google Admin Console'da huquqlarni tekshiring
```

**"Domain not found"**
```
Sabab: Domen noto'g'ri yozilgan
Yechim: Script'da DOMAIN ni to'g'rilang
```

**"API not enabled"**
```
Sabab: Admin SDK API yoqilmagan  
Yechim: Google Cloud Console'da API'ni yoqing
```

**"Invalid credentials"**
```
Sabab: credentials.json noto'g'ri
Yechim: Yangi OAuth credentials yuklab oling
```

## 📞 Yordam

### Log Fayllar
- **workspace_emails.log** - Barcha amaliyotlar
- **workspace_config.json** - Yaratilgan akkauntlar
- Console output - Real-time status

### Debug
1. Log fayllarni tekshiring
2. Google Admin Console'da huquqlarni tekshiring  
3. API quotas va limits'ni tekshiring
4. Domain DNS sozlamalarini tekshiring

## 🔄 Yangilanishlar

### Version 1.0.0 (Joriy)
- ✅ Asosiy email yaratish funksiyasi
- ✅ Ko'p akkaunt yaratish
- ✅ CSV import/export
- ✅ Domen boshqaruvi
- ✅ Security features

### Rejalashtirilgan (v1.1)
- 🔄 Group management
- 🔄 Email aliases
- 🔄 Advanced reporting
- 🔄 Bulk operations

## 🎉 Natija

Ushbu tool orqali siz:

- ✅ **Professional email'lar** yarata olasiz
- ✅ **Xavfsiz va qonuniy** tarzda
- ✅ **Ko'p akkaunt** bir vaqtda
- ✅ **To'liq avtomatik** jarayonda
- ✅ **Google standarti** bo'yicha

---

**🚀 O'z domeningizda professional email yaratishni boshlang!**

> **Eslatma:** Bu tool faqat o'zingizga tegishli domen va Google Workspace akkauntingiz bilan ishlaydi. Bu to'liq qonuniy va Google tomonidan qo'llab-quvvatlanadigan usul.