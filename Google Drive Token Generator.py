from google_auth_oauthlib.flow import InstalledAppFlow
import os

# กำหนดสิทธิ์ที่ต้องการ
SCOPES = ['https://www.googleapis.com/auth/drive']

def main():
    # หาที่อยู่จริงของโฟลเดอร์ที่เก็บไฟล์สคริปต์นี้
    base_dir = os.path.dirname(os.path.abspath(__file__))
    
    # สร้าง path เต็มไปยังไฟล์ client_secret.json (บังคับให้หาในโฟลเดอร์เดียวกัน)
    client_secret_path = os.path.join(base_dir, 'client_secret.json')
    token_path = os.path.join(base_dir, 'token.json')

    if not os.path.exists(client_secret_path):
        print(f"❌ ไม่พบไฟล์ '{client_secret_path}'")
        print("👉 (ต้องไปโหลดจาก Google Cloud มาก่อน และเปลี่ยนชื่อเป็น client_secret.json วางไว้ที่เดียวกัน)")
        return

    print("🚀 กำลังเปิด Browser...")
    try:
        flow = InstalledAppFlow.from_client_secrets_file(
            client_secret_path, SCOPES)
        
        # รัน Local Server (Port 8080 ตามที่ตั้งไว้)
        creds = flow.run_local_server(port=8080)

        with open(token_path, 'w') as token:
            token.write(creds.to_json())
        
        print(f"\n✅ สำเร็จ! ได้ไฟล์ '{token_path}' แล้ว")
        print("👉 เอาไฟล์นี้ไปทับของเดิมใน Pi ได้เลย")
        
    except Exception as e:
        print(f"\n❌ เกิดข้อผิดพลาด: {e}")                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 

if __name__ == '__main__':
    main()