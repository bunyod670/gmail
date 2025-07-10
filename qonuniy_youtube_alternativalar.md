# Qonuniy YouTube va Email Alternativalar

## 1. **YouTube Analytics API (Rasmiy)**

### YouTube Data API v3
```python
from googleapiclient.discovery import build

def get_video_stats(video_id, api_key):
    """
    Rasmiy YouTube API orqali video statistikasini olish
    """
    youtube = build('youtube', 'v3', developerKey=api_key)
    
    request = youtube.videos().list(
        part="statistics,snippet",
        id=video_id
    )
    response = request.execute()
    
    return response['items'][0]['statistics']

# Foydalanish
stats = get_video_stats('video_id', 'your_api_key')
print(f"Ko'rishlar: {stats['viewCount']}")
print(f"Likelar: {stats['likeCount']}")
```

## 2. **Content Creation Automation (Qonuniy)**

### Video Upload Automation
```python
import os
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow

def upload_video(video_file, title, description):
    """
    O'z kanalingizga video yuklash (rasmiy API)
    """
    SCOPES = ['https://www.googleapis.com/auth/youtube.upload']
    
    flow = InstalledAppFlow.from_client_secrets_file(
        'client_secrets.json', SCOPES)
    credentials = flow.run_local_server(port=0)
    
    youtube = build('youtube', 'v3', credentials=credentials)
    
    body = {
        'snippet': {
            'title': title,
            'description': description,
            'tags': ['automation', 'test'],
            'categoryId': '22'
        },
        'status': {
            'privacyStatus': 'private'  # Private yoki unlisted
        }
    }
    
    # Video yuklash
    media = MediaFileUpload(video_file, chunksize=-1, resumable=True)
    insert_request = youtube.videos().insert(
        part=','.join(body.keys()),
        body=body,
        media_body=media
    )
    
    response = insert_request.execute()
    return response
```

## 3. **Email Marketing Automation (Qonuniy)**

### Mailchimp API Integration
```python
import mailchimp_marketing as MailchimpMarketing

class EmailAutomation:
    def __init__(self, api_key, server):
        self.client = MailchimpMarketing.Client()
        self.client.set_config({
            "api_key": api_key,
            "server": server
        })
    
    def create_campaign(self, list_id, subject, html_content):
        """
        Email kampaniya yaratish
        """
        campaign_data = {
            "type": "regular",
            "recipients": {"list_id": list_id},
            "settings": {
                "subject_line": subject,
                "from_name": "Your Name",
                "reply_to": "your-email@domain.com"
            }
        }
        
        campaign = self.client.campaigns.create(campaign_data)
        
        # Content qo'shish
        self.client.campaigns.set_content(
            campaign["id"], 
            {"html": html_content}
        )
        
        return campaign
```

## 4. **Social Media Management (Qonuniy)**

### Hootsuite API / Buffer API
```python
import requests

class SocialMediaScheduler:
    def __init__(self, access_token):
        self.access_token = access_token
        self.base_url = "https://api.bufferapp.com/1"
    
    def schedule_post(self, profile_id, text, scheduled_at):
        """
        Social media post jadvalga qo'yish
        """
        url = f"{self.base_url}/updates/create.json"
        
        data = {
            'access_token': self.access_token,
            'profile_ids[]': profile_id,
            'text': text,
            'scheduled_at': scheduled_at
        }
        
        response = requests.post(url, data=data)
        return response.json()
```

## 5. **A/B Testing Platform**

### Video Performance Testing
```python
import sqlite3
from datetime import datetime

class VideoTestingPlatform:
    def __init__(self, db_path):
        self.db_path = db_path
        self.init_database()
    
    def init_database(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS video_tests (
                id INTEGER PRIMARY KEY,
                video_id TEXT,
                title_variant TEXT,
                thumbnail_variant TEXT,
                views INTEGER,
                likes INTEGER,
                created_at TIMESTAMP
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def add_test_result(self, video_id, title_variant, views, likes):
        """
        Test natijalarini saqlash
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO video_tests 
            (video_id, title_variant, views, likes, created_at)
            VALUES (?, ?, ?, ?, ?)
        ''', (video_id, title_variant, views, likes, datetime.now()))
        
        conn.commit()
        conn.close()
    
    def get_best_performing_variant(self, video_id):
        """
        Eng yaxshi natija ko'rsatgan variantni topish
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT title_variant, MAX(views + likes * 10) as score
            FROM video_tests 
            WHERE video_id = ?
            GROUP BY title_variant
            ORDER BY score DESC
            LIMIT 1
        ''', (video_id,))
        
        result = cursor.fetchone()
        conn.close()
        
        return result
```

## 6. **Content Analysis Tools**

### Video Trend Analyzer
```python
import requests
from collections import Counter

class TrendAnalyzer:
    def __init__(self, youtube_api_key):
        self.api_key = youtube_api_key
        self.base_url = "https://www.googleapis.com/youtube/v3"
    
    def get_trending_topics(self, region_code='US'):
        """
        Trending videolardan mavzularni aniqlash
        """
        url = f"{self.base_url}/videos"
        
        params = {
            'part': 'snippet',
            'chart': 'mostPopular',
            'regionCode': region_code,
            'maxResults': 50,
            'key': self.api_key
        }
        
        response = requests.get(url, params=params)
        videos = response.json()['items']
        
        # Taglarga o'xshash so'zlarni aniqlash
        all_tags = []
        for video in videos:
            if 'tags' in video['snippet']:
                all_tags.extend(video['snippet']['tags'])
        
        # Eng ko'p ishlatiladigan taglar
        trending_tags = Counter(all_tags).most_common(20)
        return trending_tags
    
    def analyze_competitor_content(self, channel_id):
        """
        Raqobatchi kanalini tahlil qilish
        """
        url = f"{self.base_url}/search"
        
        params = {
            'part': 'snippet',
            'channelId': channel_id,
            'maxResults': 25,
            'order': 'viewCount',
            'key': self.api_key
        }
        
        response = requests.get(url, params=params)
        videos = response.json()['items']
        
        return {
            'video_count': len(videos),
            'average_title_length': sum(len(v['snippet']['title']) for v in videos) / len(videos),
            'common_keywords': self._extract_keywords(videos)
        }
    
    def _extract_keywords(self, videos):
        """Keywords ekstraktsi"""
        all_titles = [video['snippet']['title'] for video in videos]
        # Simple keyword extraction logic
        words = []
        for title in all_titles:
            words.extend(title.lower().split())
        
        return Counter(words).most_common(10)
```

## 7. **Legitimate Engagement Tracking**

### Real User Engagement Analytics
```python
import json
from datetime import datetime, timedelta

class EngagementTracker:
    def __init__(self, analytics_file):
        self.analytics_file = analytics_file
    
    def track_real_engagement(self, video_id, engagement_type, user_data):
        """
        Haqiqiy foydalanuvchi engagement'ini kuzatish
        """
        engagement_data = {
            'video_id': video_id,
            'type': engagement_type,  # 'view', 'like', 'comment', 'subscribe'
            'timestamp': datetime.now().isoformat(),
            'user_country': user_data.get('country'),
            'traffic_source': user_data.get('source'),
            'device_type': user_data.get('device')
        }
        
        # Faylga saqlash
        try:
            with open(self.analytics_file, 'r') as f:
                data = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            data = []
        
        data.append(engagement_data)
        
        with open(self.analytics_file, 'w') as f:
            json.dump(data, f, indent=2)
    
    def generate_engagement_report(self, video_id, days=30):
        """
        Engagement hisoboti yaratish
        """
        with open(self.analytics_file, 'r') as f:
            data = json.load(f)
        
        cutoff_date = datetime.now() - timedelta(days=days)
        
        video_engagement = [
            item for item in data 
            if item['video_id'] == video_id and 
            datetime.fromisoformat(item['timestamp']) > cutoff_date
        ]
        
        report = {
            'total_views': len([e for e in video_engagement if e['type'] == 'view']),
            'total_likes': len([e for e in video_engagement if e['type'] == 'like']),
            'total_comments': len([e for e in video_engagement if e['type'] == 'comment']),
            'total_subscribes': len([e for e in video_engagement if e['type'] == 'subscribe']),
            'top_countries': Counter([e['user_country'] for e in video_engagement]).most_common(5)
        }
        
        return report
```

## 8. **Complete Legal Automation Framework**

### Main Orchestrator
```python
import logging
from datetime import datetime

class LegalContentAutomation:
    def __init__(self, config):
        self.config = config
        self.setup_logging()
        
        # Initialize components
        self.youtube_api = YouTubeAPI(config['youtube_api_key'])
        self.email_automation = EmailAutomation(config['mailchimp_api_key'])
        self.trend_analyzer = TrendAnalyzer(config['youtube_api_key'])
        self.engagement_tracker = EngagementTracker('engagement.json')
    
    def setup_logging(self):
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('automation.log'),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)
    
    def run_daily_automation(self):
        """
        Kunlik avtomatik jarayonlar
        """
        try:
            # 1. Trending mavzularni tahlil qilish
            trends = self.trend_analyzer.get_trending_topics()
            self.logger.info(f"Trending topics analyzed: {len(trends)} topics found")
            
            # 2. Kanalning performance'ini tekshirish
            channel_stats = self.youtube_api.get_channel_stats()
            self.logger.info(f"Channel stats: {channel_stats}")
            
            # 3. Email subscribers'ga yangiliklar yuborish
            if self._should_send_newsletter():
                self.email_automation.send_newsletter(trends, channel_stats)
                self.logger.info("Newsletter sent to subscribers")
            
            # 4. Engagement hisobotini yaratish
            engagement_report = self.engagement_tracker.generate_engagement_report()
            self.logger.info(f"Engagement report generated: {engagement_report}")
            
        except Exception as e:
            self.logger.error(f"Automation error: {str(e)}")
    
    def _should_send_newsletter(self):
        """
        Newsletter yuborish kerakligini aniqlash
        """
        # Haftaning muayyan kunida yuborish
        return datetime.now().weekday() == 0  # Dushanbada
```

## **Xulosa**

Bu usullar:
✅ **To'liq qonuniy va Google/YouTube tomonidan qo'llab-quvvatlanadi**
✅ **Professional marketing va content creation uchun**
✅ **Real analytics va insights beradi**
✅ **Spam yoki fake engagement yaratmaydi**
✅ **Long-term sustainable strategy**

**Qaysi usuldan boshlashni xohlaysiz?** Men sizga to'liq ishlaydigan kod yozib beraman!