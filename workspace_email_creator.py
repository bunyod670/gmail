#!/usr/bin/env python3
"""
Google Workspace API orqali Shaxsiy Domen Email Yaratish
Bu kod to'liq qonuniy va Google tomonidan qo'llab-quvvatlanadi
"""

import json
import logging
import secrets
import string
from datetime import datetime
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import pickle
import os

class WorkspaceEmailCreator:
    def __init__(self, domain, config_file="workspace_config.json"):
        self.domain = domain
        self.config_file = config_file
        self.setup_logging()
        self.service = None
        self.load_config()
    
    def setup_logging(self):
        """Logging sistemasini sozlash"""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('workspace_emails.log'),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)
    
    def load_config(self):
        """Konfiguratsiya faylini yuklash"""
        default_config = {
            "domain": self.domain,
            "admin_email": f"admin@{self.domain}",
            "credentials_file": "credentials.json",
            "organizational_unit": "/",
            "default_password_length": 12,
            "created_users": []
        }
        
        try:
            with open(self.config_file, 'r') as f:
                self.config = json.load(f)
        except FileNotFoundError:
            self.config = default_config
            self.save_config()
    
    def save_config(self):
        """Konfiguratsiyani saqlash"""
        with open(self.config_file, 'w') as f:
            json.dump(self.config, f, indent=2)
    
    def authenticate(self):
        """Google Workspace API bilan authentication"""
        SCOPES = [
            'https://www.googleapis.com/auth/admin.directory.user',
            'https://www.googleapis.com/auth/admin.directory.group'
        ]
        
        creds = None
        token_file = 'workspace_token.pickle'
        
        # Mavjud tokenni yuklash
        if os.path.exists(token_file):
            with open(token_file, 'rb') as token:
                creds = pickle.load(token)
        
        # Token yo'q yoki muddati o'tgan bo'lsa
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    self.config['credentials_file'], SCOPES)
                creds = flow.run_local_server(port=0)
            
            # Tokenni saqlash
            with open(token_file, 'wb') as token:
                pickle.dump(creds, token)
        
        self.service = build('admin', 'directory_v1', credentials=creds)
        self.logger.info("Successfully authenticated with Google Workspace API")
    
    def generate_secure_password(self, length=12):
        """Xavfsiz parol yaratish"""
        alphabet = string.ascii_letters + string.digits + "!@#$%^&*"
        return ''.join(secrets.choice(alphabet) for _ in range(length))
    
    def create_user(self, first_name, last_name, username=None, custom_password=None):
        """Yangi foydalanuvchi yaratish"""
        if not self.service:
            self.authenticate()
        
        # Username yaratish
        if not username:
            username = f"{first_name.lower()}.{last_name.lower()}"
        
        email = f"{username}@{self.domain}"
        
        # Parol yaratish
        password = custom_password or self.generate_secure_password()
        
        user_body = {
            'name': {
                'givenName': first_name,
                'familyName': last_name
            },
            'primaryEmail': email,
            'password': password,
            'orgUnitPath': self.config['organizational_unit'],
            'suspended': False,
            'changePasswordAtNextLogin': True  # Birinchi kirishda parol o'zgartirishni majburlash
        }
        
        try:
            # Foydalanuvchini yaratish
            user = self.service.users().insert(body=user_body).execute()
            
            # Muvaffaqiyatli yaratilgan ma'lumotlarni saqlash
            user_info = {
                'email': email,
                'password': password,
                'first_name': first_name,
                'last_name': last_name,
                'created_at': datetime.now().isoformat(),
                'user_id': user['id']
            }
            
            self.config['created_users'].append(user_info)
            self.save_config()
            
            # Xavfsizlik uchun parolni logga yozmaslik
            self.logger.info(f"Successfully created user: {email}")
            
            return {
                'success': True,
                'email': email,
                'password': password,
                'user_id': user['id'],
                'message': f"User {email} created successfully"
            }
            
        except Exception as e:
            error_msg = f"Error creating user {email}: {str(e)}"
            self.logger.error(error_msg)
            return {
                'success': False,
                'email': email,
                'error': error_msg
            }
    
    def create_multiple_users(self, users_data):
        """Ko'p foydalanuvchilarni yaratish"""
        results = []
        
        for user_data in users_data:
            result = self.create_user(
                first_name=user_data['first_name'],
                last_name=user_data['last_name'],
                username=user_data.get('username'),
                custom_password=user_data.get('password')
            )
            results.append(result)
            
            # API rate limiting uchun kutish
            import time
            time.sleep(1)
        
        return results
    
    def list_users(self):
        """Barcha foydalanuvchilarni ko'rsatish"""
        if not self.service:
            self.authenticate()
        
        try:
            request = self.service.users().list(domain=self.domain)
            response = request.execute()
            
            users = response.get('users', [])
            
            users_info = []
            for user in users:
                users_info.append({
                    'email': user['primaryEmail'],
                    'name': user['name']['fullName'],
                    'suspended': user.get('suspended', False),
                    'created_time': user.get('creationTime'),
                    'last_login': user.get('lastLoginTime')
                })
            
            self.logger.info(f"Found {len(users_info)} users in domain {self.domain}")
            return users_info
            
        except Exception as e:
            self.logger.error(f"Error listing users: {str(e)}")
            return []
    
    def delete_user(self, email):
        """Foydalanuvchini o'chirish"""
        if not self.service:
            self.authenticate()
        
        try:
            self.service.users().delete(userKey=email).execute()
            
            # Config'dan ham o'chirish
            self.config['created_users'] = [
                user for user in self.config['created_users'] 
                if user['email'] != email
            ]
            self.save_config()
            
            self.logger.info(f"Successfully deleted user: {email}")
            return {'success': True, 'message': f"User {email} deleted"}
            
        except Exception as e:
            error_msg = f"Error deleting user {email}: {str(e)}"
            self.logger.error(error_msg)
            return {'success': False, 'error': error_msg}
    
    def update_user(self, email, updates):
        """Foydalanuvchi ma'lumotlarini yangilash"""
        if not self.service:
            self.authenticate()
        
        try:
            self.service.users().update(userKey=email, body=updates).execute()
            self.logger.info(f"Successfully updated user: {email}")
            return {'success': True, 'message': f"User {email} updated"}
            
        except Exception as e:
            error_msg = f"Error updating user {email}: {str(e)}"
            self.logger.error(error_msg)
            return {'success': False, 'error': error_msg}
    
    def export_users_to_file(self, filename="created_users.json"):
        """Yaratilgan foydalanuvchilarni faylga eksport qilish"""
        try:
            with open(filename, 'w') as f:
                json.dump(self.config['created_users'], f, indent=2)
            
            self.logger.info(f"Users exported to {filename}")
            return True
            
        except Exception as e:
            self.logger.error(f"Error exporting users: {str(e)}")
            return False
    
    def get_domain_info(self):
        """Domen haqida ma'lumot olish"""
        if not self.service:
            self.authenticate()
        
        try:
            # Domen foydalanuvchilarini sanash
            users = self.list_users()
            
            domain_info = {
                'domain': self.domain,
                'total_users': len(users),
                'active_users': len([u for u in users if not u['suspended']]),
                'suspended_users': len([u for u in users if u['suspended']]),
                'created_by_script': len(self.config['created_users']),
                'last_check': datetime.now().isoformat()
            }
            
            return domain_info
            
        except Exception as e:
            self.logger.error(f"Error getting domain info: {str(e)}")
            return None

def main():
    """Asosiy funksiya - misollar bilan"""
    # Domeningizni kiriting
    DOMAIN = "yourdomain.com"  # Bu yerga o'z domeningizni yozing
    
    # Email creator'ni yaratish
    creator = WorkspaceEmailCreator(DOMAIN)
    
    print("🚀 Google Workspace Email Creator")
    print(f"📧 Domain: {DOMAIN}")
    print("=" * 50)
    
    while True:
        print("\nTanlang:")
        print("1. Bitta foydalanuvchi yaratish")
        print("2. Ko'p foydalanuvchi yaratish") 
        print("3. Foydalanuvchilarni ko'rsatish")
        print("4. Domen ma'lumotlari")
        print("5. Foydalanuvchini o'chirish")
        print("6. Eksport qilish")
        print("0. Chiqish")
        
        choice = input("\nTanlovingiz (0-6): ").strip()
        
        if choice == "1":
            # Bitta foydalanuvchi yaratish
            print("\n📝 Yangi foydalanuvchi ma'lumotlari:")
            first_name = input("Ism: ").strip()
            last_name = input("Familiya: ").strip()
            username = input("Username (bo'sh qoldirish mumkin): ").strip() or None
            
            result = creator.create_user(first_name, last_name, username)
            
            if result['success']:
                print(f"\n✅ Muvaffaqiyatli yaratildi!")
                print(f"📧 Email: {result['email']}")
                print(f"🔐 Parol: {result['password']}")
                print("⚠️  Birinchi kirishda parol o'zgartirilishi kerak!")
            else:
                print(f"\n❌ Xato: {result['error']}")
        
        elif choice == "2":
            # Ko'p foydalanuvchi yaratish
            print("\n📝 Nechta foydalanuvchi yaratish kerak?")
            try:
                count = int(input("Soni: "))
                users_data = []
                
                for i in range(count):
                    print(f"\n{i+1}-foydalanuvchi:")
                    first_name = input("  Ism: ").strip()
                    last_name = input("  Familiya: ").strip()
                    
                    users_data.append({
                        'first_name': first_name,
                        'last_name': last_name
                    })
                
                print(f"\n🔄 {count} ta foydalanuvchi yaratilmoqda...")
                results = creator.create_multiple_users(users_data)
                
                success_count = len([r for r in results if r['success']])
                print(f"\n📊 Natija: {success_count}/{count} muvaffaqiyatli yaratildi")
                
                for result in results:
                    if result['success']:
                        print(f"✅ {result['email']} - {result['password']}")
                    else:
                        print(f"❌ {result['email']} - {result['error']}")
                        
            except ValueError:
                print("❌ Noto'g'ri raqam kiritildi!")
        
        elif choice == "3":
            # Foydalanuvchilarni ko'rsatish
            print("\n👥 Domen foydalanuvchilari:")
            users = creator.list_users()
            
            if users:
                for i, user in enumerate(users, 1):
                    status = "🔴 Faolsiz" if user['suspended'] else "🟢 Faol"
                    print(f"{i}. {user['email']} - {user['name']} ({status})")
            else:
                print("Foydalanuvchilar topilmadi.")
        
        elif choice == "4":
            # Domen ma'lumotlari
            print("\n📊 Domen statistikasi:")
            info = creator.get_domain_info()
            
            if info:
                print(f"🌐 Domen: {info['domain']}")
                print(f"👥 Jami foydalanuvchilar: {info['total_users']}")
                print(f"🟢 Faol: {info['active_users']}")
                print(f"🔴 Faolsiz: {info['suspended_users']}")
                print(f"🤖 Script tomonidan yaratilgan: {info['created_by_script']}")
            else:
                print("Ma'lumot olishda xato!")
        
        elif choice == "5":
            # Foydalanuvchini o'chirish
            email = input("\nO'chirish uchun email kiriting: ").strip()
            
            confirm = input(f"Haqiqatan ham {email} ni o'chirmoqchimisiz? (ha/yo'q): ").strip().lower()
            
            if confirm in ['ha', 'yes', 'y']:
                result = creator.delete_user(email)
                if result['success']:
                    print(f"✅ {email} muvaffaqiyatli o'chirildi!")
                else:
                    print(f"❌ Xato: {result['error']}")
            else:
                print("❌ Bekor qilindi.")
        
        elif choice == "6":
            # Eksport qilish
            filename = input("\nFayl nomi (created_users.json): ").strip() or "created_users.json"
            
            if creator.export_users_to_file(filename):
                print(f"✅ Ma'lumotlar {filename} ga eksport qilindi!")
            else:
                print("❌ Eksport qilishda xato!")
        
        elif choice == "0":
            print("👋 Xayr!")
            break
        
        else:
            print("❌ Noto'g'ri tanlov!")

if __name__ == "__main__":
    main()