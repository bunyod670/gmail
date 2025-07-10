#!/usr/bin/env python3
"""
Google Workspace Email Creator - Programmatik Foydalanish Misoli
Bu misolda script'ni kod orqali qanday ishlatishni ko'rsatamiz
"""

from workspace_email_creator import WorkspaceEmailCreator
import json

def create_team_emails():
    """Jamoa uchun email'lar yaratish"""
    
    # O'z domeningizni kiriting
    DOMAIN = "mycompany.com"  # Bu yerga o'z domeningizni yozing
    
    # Email creator'ni yaratish
    creator = WorkspaceEmailCreator(DOMAIN)
    
    # Jamoa a'zolari ro'yxati
    team_members = [
        {"first_name": "Ali", "last_name": "Karimov", "username": "ali.karimov"},
        {"first_name": "Dilorom", "last_name": "Abdullayeva", "username": "dilorom.abdullayeva"},
        {"first_name": "Bobur", "last_name": "Rahimov", "username": "bobur.rahimov"},
        {"first_name": "Gulnora", "last_name": "Toshmatova", "username": "gulnora.toshmatova"},
        {"first_name": "Sardor", "last_name": "Yusupov", "username": "sardor.yusupov"}
    ]
    
    print("🚀 Jamoa email'larini yaratish boshlandi...")
    print(f"📧 Domen: {DOMAIN}")
    print("=" * 50)
    
    successful_accounts = []
    failed_accounts = []
    
    # Har bir jamoa a'zosi uchun email yaratish
    for member in team_members:
        print(f"\n🔄 {member['first_name']} {member['last_name']} uchun email yaratilmoqda...")
        
        result = creator.create_user(
            first_name=member['first_name'],
            last_name=member['last_name'], 
            username=member['username']
        )
        
        if result['success']:
            successful_accounts.append({
                'name': f"{member['first_name']} {member['last_name']}",
                'email': result['email'],
                'password': result['password']
            })
            print(f"✅ Muvaffaqiyatli: {result['email']}")
        else:
            failed_accounts.append({
                'name': f"{member['first_name']} {member['last_name']}",
                'error': result['error']
            })
            print(f"❌ Xato: {result['error']}")
    
    # Natijalarni ko'rsatish
    print("\n" + "=" * 50)
    print("📊 YAKUNIY NATIJA")
    print("=" * 50)
    
    print(f"\n✅ Muvaffaqiyatli yaratildi: {len(successful_accounts)}")
    for account in successful_accounts:
        print(f"   👤 {account['name']} - {account['email']}")
    
    if failed_accounts:
        print(f"\n❌ Muvaffaqiyatsiz: {len(failed_accounts)}")
        for account in failed_accounts:
            print(f"   👤 {account['name']} - {account['error']}")
    
    # Ma'lumotlarni faylga saqlash
    save_accounts_to_file(successful_accounts)
    
    return successful_accounts

def save_accounts_to_file(accounts, filename="team_accounts.json"):
    """Yaratilgan akkauntlarni faylga saqlash"""
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(accounts, f, indent=2, ensure_ascii=False)
        
        print(f"\n💾 Akkaunt ma'lumotlari {filename} ga saqlandi!")
        return True
    except Exception as e:
        print(f"\n❌ Faylga saqlashda xato: {e}")
        return False

def create_bulk_emails_from_csv():
    """CSV fayldan ko'p email'lar yaratish"""
    import csv
    
    DOMAIN = "mycompany.com"  # O'z domeningizni kiriting
    creator = WorkspaceEmailCreator(DOMAIN)
    
    # CSV fayl yaratish (misol uchun)
    sample_csv_data = [
        ["first_name", "last_name", "department"],
        ["Ahmad", "Toshev", "IT"],
        ["Maryam", "Karimova", "HR"], 
        ["Jasur", "Rahmonov", "Finance"],
        ["Nigora", "Yuldasheva", "Marketing"],
        ["Temur", "Nazarov", "IT"]
    ]
    
    # CSV faylni yaratish
    csv_filename = "employees.csv"
    with open(csv_filename, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerows(sample_csv_data)
    
    print(f"📁 {csv_filename} fayli yaratildi (misol uchun)")
    
    # CSV fayldan o'qish va email'lar yaratish
    results = []
    
    try:
        with open(csv_filename, 'r', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            
            for row in reader:
                first_name = row['first_name']
                last_name = row['last_name']
                department = row.get('department', 'general')
                
                # Department asosida username yaratish
                username = f"{first_name.lower()}.{last_name.lower()}.{department.lower()}"
                
                print(f"\n🔄 {first_name} {last_name} ({department}) uchun email yaratilmoqda...")
                
                result = creator.create_user(
                    first_name=first_name,
                    last_name=last_name,
                    username=username
                )
                
                result['department'] = department
                results.append(result)
                
                if result['success']:
                    print(f"✅ Yaratildi: {result['email']}")
                else:
                    print(f"❌ Xato: {result['error']}")
        
        # Natijalarni ko'rsatish
        successful = [r for r in results if r['success']]
        failed = [r for r in results if not r['success']]
        
        print(f"\n📊 CSV'dan yaratish natijasi:")
        print(f"✅ Muvaffaqiyatli: {len(successful)}")
        print(f"❌ Muvaffaqiyatsiz: {len(failed)}")
        
        return results
        
    except FileNotFoundError:
        print(f"❌ {csv_filename} fayli topilmadi!")
        return []

def get_domain_statistics():
    """Domen statistikasini olish"""
    DOMAIN = "mycompany.com"  # O'z domeningizni kiriting
    creator = WorkspaceEmailCreator(DOMAIN)
    
    print("📊 Domen statistikasi yuklanmoqda...")
    
    # Domen ma'lumotlari
    domain_info = creator.get_domain_info()
    
    if domain_info:
        print(f"\n🌐 Domen: {domain_info['domain']}")
        print(f"👥 Jami foydalanuvchilar: {domain_info['total_users']}")
        print(f"🟢 Faol: {domain_info['active_users']}")
        print(f"🔴 Faolsiz: {domain_info['suspended_users']}")
        print(f"🤖 Script tomonidan yaratilgan: {domain_info['created_by_script']}")
    
    # Barcha foydalanuvchilarni ko'rsatish
    users = creator.list_users()
    
    if users:
        print(f"\n👥 Barcha foydalanuvchilar ({len(users)} ta):")
        for i, user in enumerate(users, 1):
            status = "🔴" if user['suspended'] else "🟢"
            print(f"  {i}. {status} {user['email']} - {user['name']}")
    
    return domain_info, users

def main():
    """Asosiy funksiya - qaysi funksiyani ishlatishni tanlang"""
    
    print("🚀 Google Workspace Email Creator - Programmatik Misollar")
    print("=" * 60)
    
    while True:
        print("\nQaysi misol funksiyasini ishlatmoqchisiz?")
        print("1. Jamoa uchun email'lar yaratish")
        print("2. CSV fayldan ko'p email'lar yaratish") 
        print("3. Domen statistikasini ko'rish")
        print("0. Chiqish")
        
        choice = input("\nTanlovingiz (0-3): ").strip()
        
        if choice == "1":
            accounts = create_team_emails()
            
        elif choice == "2":
            results = create_bulk_emails_from_csv()
            
        elif choice == "3":
            domain_info, users = get_domain_statistics()
            
        elif choice == "0":
            print("👋 Xayr!")
            break
            
        else:
            print("❌ Noto'g'ri tanlov!")

if __name__ == "__main__":
    main()