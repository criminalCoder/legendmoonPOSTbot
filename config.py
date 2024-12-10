import re, os

id_pattern = re.compile(r'^.\d+$') 

API_ID = os.environ.get("API_ID", "23265307")

API_HASH = os.environ.get("API_HASH", "cc2b82ee80cabeba9a3408a6972d0ab2")

BOT_TOKEN = os.environ.get("BOT_TOKEN", "8086094628:AAHTmVS3pgy_n4CiUI8w4lOua80Sji60Enk") 

FORCE_SUB = os.environ.get("FORCE_SUB", "LazyDeveloper") 

DB_NAME = os.environ.get("DB_NAME","Yashkalvar07")     

DB_URL = os.environ.get("DB_URL","mongodb+srv://Yashkalvar07:Yashkalvar07@yashkalvar07.cylum.mongodb.net/?retryWrites=true&w=majority")

FLOOD = int(os.environ.get("FLOOD", "10"))

START_PIC = os.environ.get("START_PIC", "https://i.ibb.co/rv8Lds3/ALL-RENAMER-LOGO-YASH-GOYAL.jpg")

ADMIN = [int(admin) if id_pattern.search(admin) else admin for admin in os.environ.get('ADMIN', '5965340120 6126812037 6864533113').split()]

CHANNELS = [int(ch) if id_pattern.search(ch) else ch for ch in os.environ.get('CHANNELS', '-1002449706784 -1002442299587 -1002288308631 -1002490685829 -1002243470797 -1002260629607').split()]

CHANNEL_LINK1 = os.environ.get("CHANNEL_LINK1", "https://t.me/LazyDeveloper")

CHANNEL_LINK2 = os.environ.get("CHANNEL_LINK2", "https://t.me/LazyDeveloper")

PORT = os.environ.get('PORT', '8080')

Lazy_session = {}
Lazy_api_id ={}
Lazy_api_hash ={}

String_Session  = "None"

Permanent_4gb = "-100XXX"