#!/usr/bin/env python3
"""
3 Ta YouTube Kanal uchun Qonuniy Automation
Bu kod Google/YouTube qoidalarini buzmaydigan, rasmiy API'lar ishlatadi
"""

import json
import time
import logging
from datetime import datetime, timedelta
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import pickle
import os
import sqlite3
from collections import Counter

class MultiChannelAutomation:
    def __init__(self, config_file="channels_config.json"):
        self.config = self.load_config(config_file)
        self.setup_logging()
        self.setup_database()
        self.youtube_services = {}
        
    def load_config(self, config_file):
        """Kanal konfiguratsiyalarini yuklash"""
        default_config = {
            "channels": [
                {
                    "name": "Kanal_1",
                    "credentials_file": "channel1_credentials.json",
                    "api_key": "YOUR_API_KEY_1",
                    "niche": "education",
                    "target_audience": "tech"
                },
                {
                    "name": "Kanal_2", 
                    "credentials_file": "channel2_credentials.json",
                    "api_key": "YOUR_API_KEY_2",
                    "niche": "entertainment",
                    "target_audience": "general"
                },
                {
                    "name": "Kanal_3",
                    "credentials_file": "channel3_credentials.json", 
                    "api_key": "YOUR_API_KEY_3",
                    "niche": "business",
                    "target_audience": "entrepreneurs"
                }
            ]
        }
        
        try:
            with open(config_file, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            # Config fayl yaratish
            with open(config_file, 'w') as f:
                json.dump(default_config, f, indent=2)
            return default_config
    
    def setup_logging(self):
        """Logging sistemasini sozlash"""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('multi_channel.log'),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)
        
    def setup_database(self):
        """SQLite database yaratish"""
        conn = sqlite3.connect('channels_data.db')
        cursor = conn.cursor()
        
        # Kanallar jadvali
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS channels (
                id INTEGER PRIMARY KEY,
                name TEXT UNIQUE,
                channel_id TEXT,
                subscribers INTEGER,
                total_views INTEGER,
                video_count INTEGER,
                last_updated TIMESTAMP
            )
        ''')
        
        # Videolar jadvali
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS videos (
                id INTEGER PRIMARY KEY,
                channel_name TEXT,
                video_id TEXT,
                title TEXT,
                views INTEGER,
                likes INTEGER,
                comments INTEGER,
                upload_date TIMESTAMP,
                performance_score REAL
            )
        ''')
        
        # Trending mavzular jadvali
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS trending_topics (
                id INTEGER PRIMARY KEY,
                topic TEXT,
                frequency INTEGER,
                niche TEXT,
                date_found TIMESTAMP
            )
        ''')
        
        conn.commit()
        conn.close()
        
    def authenticate_channel(self, channel_config):
        """Kanalga authentication qilish"""
        SCOPES = ['https://www.googleapis.com/auth/youtube.readonly',
                  'https://www.googleapis.com/auth/youtube.upload']
        
        creds = None
        token_file = f"token_{channel_config['name']}.pickle"
        
        # Mavjud tokenni yuklash
        if os.path.exists(token_file):
            with open(token_file, 'rb') as token:
                creds = pickle.load(token)
                
        # Agar token yo'q yoki muddati o'tgan bo'lsa
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    channel_config['credentials_file'], SCOPES)
                creds = flow.run_local_server(port=0)
                
            # Tokenni saqlash
            with open(token_file, 'wb') as token:
                pickle.dump(creds, token)
                
        return build('youtube', 'v3', credentials=creds)
    
    def get_channel_stats(self, service, channel_name):
        """Kanal statistikalarini olish"""
        try:
            # O'z kanalimizning ma'lumotlarini olish
            request = service.channels().list(
                part="statistics,snippet",
                mine=True
            )
            response = request.execute()
            
            if response['items']:
                channel = response['items'][0]
                stats = channel['statistics']
                
                # Database'ga saqlash
                conn = sqlite3.connect('channels_data.db')
                cursor = conn.cursor()
                
                cursor.execute('''
                    INSERT OR REPLACE INTO channels 
                    (name, channel_id, subscribers, total_views, video_count, last_updated)
                    VALUES (?, ?, ?, ?, ?, ?)
                ''', (
                    channel_name,
                    channel['id'],
                    int(stats.get('subscriberCount', 0)),
                    int(stats.get('viewCount', 0)),
                    int(stats.get('videoCount', 0)),
                    datetime.now()
                ))
                
                conn.commit()
                conn.close()
                
                self.logger.info(f"{channel_name} - Subscribers: {stats.get('subscriberCount')}")
                return stats
                
        except Exception as e:
            self.logger.error(f"Error getting stats for {channel_name}: {e}")
            return None
    
    def analyze_trending_topics(self, service, niche, channel_name):
        """Trending mavzularni tahlil qilish"""
        try:
            # Trending videolarni olish
            request = service.videos().list(
                part="snippet,statistics",
                chart="mostPopular",
                regionCode="US",
                maxResults=50
            )
            response = request.execute()
            
            relevant_topics = []
            all_tags = []
            
            for video in response['items']:
                snippet = video['snippet']
                
                # Niche ga mos mavzularni filtrlash
                if self.is_relevant_to_niche(snippet, niche):
                    relevant_topics.append({
                        'title': snippet['title'],
                        'views': int(video['statistics'].get('viewCount', 0)),
                        'likes': int(video['statistics'].get('likeCount', 0))
                    })
                    
                    # Taglarni yig'ish
                    if 'tags' in snippet:
                        all_tags.extend(snippet['tags'])
            
            # Eng mashur taglarni aniqlash
            popular_tags = Counter(all_tags).most_common(10)
            
            # Database'ga saqlash
            self.save_trending_topics(popular_tags, niche)
            
            self.logger.info(f"{channel_name} - Found {len(relevant_topics)} relevant trending topics")
            return {
                'relevant_videos': relevant_topics,
                'popular_tags': popular_tags
            }
            
        except Exception as e:
            self.logger.error(f"Error analyzing trends for {channel_name}: {e}")
            return None
    
    def is_relevant_to_niche(self, snippet, niche):
        """Video niche ga mos kelishini tekshirish"""
        title = snippet['title'].lower()
        description = snippet.get('description', '').lower()
        
        niche_keywords = {
            'education': ['learn', 'tutorial', 'how to', 'education', 'course', 'study'],
            'entertainment': ['funny', 'comedy', 'music', 'entertainment', 'fun', 'viral'],
            'business': ['business', 'entrepreneur', 'startup', 'marketing', 'money', 'success'],
            'tech': ['technology', 'coding', 'programming', 'software', 'app', 'ai']
        }
        
        keywords = niche_keywords.get(niche, [])
        
        for keyword in keywords:
            if keyword in title or keyword in description:
                return True
        return False
    
    def save_trending_topics(self, topics, niche):
        """Trending mavzularni database'ga saqlash"""
        conn = sqlite3.connect('channels_data.db')
        cursor = conn.cursor()
        
        for topic, frequency in topics:
            cursor.execute('''
                INSERT OR REPLACE INTO trending_topics 
                (topic, frequency, niche, date_found)
                VALUES (?, ?, ?, ?)
            ''', (topic, frequency, niche, datetime.now()))
        
        conn.commit()
        conn.close()
    
    def get_video_performance(self, service, channel_name):
        """Kanal videolarining performansini tahlil qilish"""
        try:
            # Kanalning videolarini olish
            request = service.search().list(
                part="snippet",
                forMine=True,
                type="video",
                order="date",
                maxResults=25
            )
            response = request.execute()
            
            video_performance = []
            
            for item in response['items']:
                video_id = item['id']['videoId']
                
                # Video statistikalarini olish
                stats_request = service.videos().list(
                    part="statistics",
                    id=video_id
                )
                stats_response = stats_request.execute()
                
                if stats_response['items']:
                    stats = stats_response['items'][0]['statistics']
                    
                    # Performance score hisoblash
                    views = int(stats.get('viewCount', 0))
                    likes = int(stats.get('likeCount', 0))
                    comments = int(stats.get('commentCount', 0))
                    
                    performance_score = self.calculate_performance_score(views, likes, comments)
                    
                    video_data = {
                        'video_id': video_id,
                        'title': item['snippet']['title'],
                        'views': views,
                        'likes': likes,
                        'comments': comments,
                        'performance_score': performance_score,
                        'upload_date': item['snippet']['publishedAt']
                    }
                    
                    video_performance.append(video_data)
                    
                    # Database'ga saqlash
                    self.save_video_performance(channel_name, video_data)
            
            self.logger.info(f"{channel_name} - Analyzed {len(video_performance)} videos")
            return video_performance
            
        except Exception as e:
            self.logger.error(f"Error analyzing video performance for {channel_name}: {e}")
            return []
    
    def calculate_performance_score(self, views, likes, comments):
        """Video performance score hisoblash"""
        # Oddiy formula: views + (likes * 10) + (comments * 20)
        return views + (likes * 10) + (comments * 20)
    
    def save_video_performance(self, channel_name, video_data):
        """Video performance ma'lumotlarini saqlash"""
        conn = sqlite3.connect('channels_data.db')
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT OR REPLACE INTO videos 
            (channel_name, video_id, title, views, likes, comments, upload_date, performance_score)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            channel_name,
            video_data['video_id'],
            video_data['title'],
            video_data['views'],
            video_data['likes'],
            video_data['comments'],
            video_data['upload_date'],
            video_data['performance_score']
        ))
        
        conn.commit()
        conn.close()
    
    def generate_daily_report(self):
        """Kunlik hisobot yaratish"""
        conn = sqlite3.connect('channels_data.db')
        cursor = conn.cursor()
        
        # Kanallar statistikasi
        cursor.execute('SELECT * FROM channels ORDER BY subscribers DESC')
        channels = cursor.fetchall()
        
        # Eng yaxshi videolar
        cursor.execute('''
            SELECT channel_name, title, views, performance_score 
            FROM videos 
            ORDER BY performance_score DESC 
            LIMIT 10
        ''')
        top_videos = cursor.fetchall()
        
        # Trending topics
        cursor.execute('''
            SELECT topic, frequency, niche 
            FROM trending_topics 
            WHERE date_found >= date('now', '-7 days')
            ORDER BY frequency DESC 
            LIMIT 20
        ''')
        trending = cursor.fetchall()
        
        conn.close()
        
        # Hisobotni yaratish
        report = {
            'date': datetime.now().isoformat(),
            'channels': [
                {
                    'name': ch[1],
                    'subscribers': ch[3],
                    'total_views': ch[4],
                    'video_count': ch[5]
                } for ch in channels
            ],
            'top_performing_videos': [
                {
                    'channel': vid[0],
                    'title': vid[1],
                    'views': vid[2],
                    'score': vid[3]
                } for vid in top_videos
            ],
            'trending_topics': [
                {
                    'topic': trend[0],
                    'frequency': trend[1],
                    'niche': trend[2]
                } for trend in trending
            ]
        }
        
        # JSON faylga saqlash
        with open(f"daily_report_{datetime.now().strftime('%Y%m%d')}.json", 'w') as f:
            json.dump(report, f, indent=2)
        
        self.logger.info("Daily report generated successfully")
        return report
    
    def run_automation(self):
        """Asosiy automation jarayoni"""
        self.logger.info("Starting multi-channel automation...")
        
        for channel_config in self.config['channels']:
            channel_name = channel_config['name']
            
            try:
                self.logger.info(f"Processing {channel_name}...")
                
                # Authentication
                service = self.authenticate_channel(channel_config)
                self.youtube_services[channel_name] = service
                
                # Kanal statistikalarini olish
                stats = self.get_channel_stats(service, channel_name)
                
                # Trending mavzularni tahlil qilish
                trends = self.analyze_trending_topics(
                    service, 
                    channel_config['niche'], 
                    channel_name
                )
                
                # Video performance tahlil qilish
                performance = self.get_video_performance(service, channel_name)
                
                # Har kanal orasida kutish
                time.sleep(5)
                
            except Exception as e:
                self.logger.error(f"Error processing {channel_name}: {e}")
                continue
        
        # Kunlik hisobot yaratish
        report = self.generate_daily_report()
        
        self.logger.info("Multi-channel automation completed successfully!")
        return report

def main():
    """Asosiy funksiya"""
    automation = MultiChannelAutomation()
    
    # Har 24 soatda bir marta ishga tushirish uchun
    while True:
        try:
            report = automation.run_automation()
            print("✅ Automation completed successfully!")
            print(f"📊 Report: {len(report['channels'])} channels processed")
            
            # 24 soat kutish (86400 sekund)
            # Test uchun 1 soat (3600 sekund) qilish mumkin
            time.sleep(3600)  # 1 soat kutish
            
        except KeyboardInterrupt:
            print("\n🛑 Automation stopped by user")
            break
        except Exception as e:
            print(f"❌ Error in main loop: {e}")
            time.sleep(300)  # 5 daqiqa kutib qayta urinish

if __name__ == "__main__":
    main()