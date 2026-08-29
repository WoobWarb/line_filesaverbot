# Project Map

> Auto-generated. Read this first to understand the codebase.

## File Tree
```
  📄 Google Drive Token Generator.py
  📄 New Text Document.txt
  📄 agent-map.py
  📄 chat_log.db
  📄 client_secret.json
  📄 credentials.json
  📄 deploy.bat
  📄 file-saver-479919-feb9641cc74e.json
  📄 filesaver_bot.py
  📄 filesaver_bot.py.bak
  📄 filesaverbot_V1.rar
  📄 generate_admin_rich_menu.py
  📄 generate_rich_menu.py
  📄 import_chat.py
  📄 journal.md
  📄 nct_filesaverbot_logo.png
  📄 promptpay.py
  📄 rich_menu.jpg
  📄 rich_menu.png
  📄 rich_menu_admin.jpg
  📄 rich_menu_new.jpg
  📄 rich_menu_old.jpg
  📄 server_check.py
  📄 setup_admin_rich_menu.py
  📄 setup_rich_menu.py
  📄 temp_list.py
  📄 temp_reimport.py
  📄 test_pkce.py
  📄 test_pkce2.py
  📄 token.json
  📄 token.json.bak
  📄 weekly_cron.log
  📄 weekly_summary.py
  📂 .claude/
    📄 settings.json
    📄 settings.local.json
  📂 deploy/
    📄 filesaverbot.service
    📄 nginx.conf
  📂 extracted_v1/
    📂 filesaverbot/
      📄 credentials.json
      📄 filesaver_bot.py
      📄 token.json
      📂 pending_uploads/
  📂 filesaverbot/
    📄 credentials.json
    📄 filesaver_bot.py
    📄 token.json
    📂 pending_uploads/
  📂 pending_uploads/
    📄 BOQ_R1.xlsx
    📄 DataSheets20260501.Zip
    📄 Proforma Invoice-HW20260501A.pdf
    📄 Proforma Invoice-HW20260501A.xlsx
    📄 jpg_612011750552240367.jpg
    📄 jpg_612011753169224235.jpg
    📄 jpg_612011755903647814.jpg
    📄 jpg_612012250714865921.jpg
  📂 RAW_Chat/
    📄 [LINE]3king Axie.txt
    📄 [LINE]Discuss nCt blue.txt
    📄 [LINE]PM All Project(NCT).txt
  📂 scratch/
    📄 check_token.py
    📄 deploy_bot_vps.py
    📄 deploy_richmenu_via_vps.py
    📄 deploy_user_menu.py
    📄 log_search_results.txt
    📄 pi_logs.txt
    📄 read_last_lines.py
    📄 search_user_tokens.py
    📄 update_journal_html.py
    📂 pi/
      📄 check_configs.py
      📄 check_dhcpcd.py
      📄 check_logs.py
      📄 check_network.py
      📄 check_pi_dmesg.py
      📄 check_pi_error.py
      📄 check_pi_full_logs.py
      📄 check_pi_linebot_v3.py
      📄 check_pi_logs.py
      📄 check_pi_oom.py
      📄 check_pi_swap.py
      📄 check_pi_venv.py
      📄 check_service.py
      📄 check_swap_file.py
      📄 check_tailscale.py
      📄 compare_dir.py
      📄 compare_versions.py
      📄 deploy.py
      📄 deploy_bot_pi.py
      📄 deploy_weekly_summary.py
      📄 download_all_remote.py
      📄 download_token.py
      📄 enable_pi_swap.py
      📄 find_bot.py
      📄 fix_dns_permanent.py
      📄 fix_dns_tailscale.py
      📄 fix_dns_temp.py
      📄 get_public_ip.py
      📄 list_filesaverbot.py
      📄 list_remote.py
      📄 manual_dns_fix.py
      📄 quick_check_pi.py
      📄 read_service.py
      📄 revert_pi_weekly_summary.py
      📄 test_direct_conn.py
      📄 test_ip_ping.py
      📄 test_nslookup.py
      📄 test_ping.py
      📄 update_service.py
      📄 view_pi_details.py
    📂 vps/
      📄 change_domain_vps.py
      📄 check_service_logs.py
      📄 check_vps_client_secret.py
      📄 check_vps_cron.py
      📄 check_vps_logs.py
      📄 copy_deploy_files.py
      📄 deploy_vps.py
      📄 deploy_weekly_vps.py
      📄 finalize_vps.py
      📄 inspect_nginx.py
      📄 inspect_vps.py
      📄 read_vps_env.py
      📄 remove_vps_weekly.py
      📄 restart_service.py
      📄 search_logs.py
      📄 setup_vps_cron.py
      📄 setup_vps_packages.py
      📄 test_vps_conn.py
      📄 update_vps_secret.py
      📄 view_live_logs.py
  📂 static/
    📄 logo_120.png
  📂 templates/
    📄 admin_dashboard.html
    📄 admin_login.html
    📄 auth.html
    📄 index.html
    📄 privacy.html
    📄 success.html
    📄 terms.html
```

## File Contexts

- **`Google Drive Token Generator.py`** — # กำหนดสิทธิ์ที่ต้องการ SCOPES = ['https://www.googleapis.com/auth/drive']
- **`New Text Document.txt`** — line-bot-save-files-to-drive@file-saver-479919.iam.gserviceaccount.com https://drive.google.com/drive/u/0/folders/19kjaPia0hFhREVpJdTdTj-Jnp4xyPp3K
- **`agent-map.py`** — IGNORE_DIRS = {
- **`chat_log.db`** — [Binary or unreadable]
- **`client_secret.json`** — {"web":{"client_id":"924021028932-5n28hfaek8bcpc9g9ac7dhpiv1ihm8of.apps.googleusercontent.com","project_id":"filesaverbot","auth_uri":"https://account...
- **`credentials.json`** — { "type": "service_account", "project_id": "file-saver-479919", "private_key_id": "60082fddc695c53ff61eb45375bccfcf68a6f8ab", "private_key": "-----BEG...
- **`deploy.bat`** — @echo off set VPS_IP=178.128.59.217 set VPS_USER=root set DEST_DIR=/root/filesaverbot
- **`file-saver-479919-feb9641cc74e.json`** — { "type": "service_account", "project_id": "file-saver-479919", "private_key_id": "feb9641cc74e0c495e8a469dbe3baa1a0b28684c", "private_key": "-----BEG...
- **`filesaver_bot.py`**
- **`filesaver_bot.py.bak`**
- **`filesaverbot_V1.rar`** — [Binary or unreadable]
- **`generate_admin_rich_menu.py`** — """ generate_admin_rich_menu.py - สร้างรูป Admin Rich Menu ปุ่มพิเศษสำหรับแอดมิน: สถานะระบบ | Admin List | อนุมัติ | สรุปแชท | เก็บตก | แจ้งโอน """
- **`generate_rich_menu.py`** — """ Regenerates rich_menu.jpg without underlines using Pillow + Leelawadee font. Run: python generate_rich_menu.py """
- **`import_chat.py`**
- **`journal.md`** — # FileSaverBot Journal ## Project Purpose จุดประสงค์ของบอทตัวนี้คือช่วยเซฟไฟล์จากแชท LINE (ที่มักจะหมดอายุ) ไปเก็บรักษาไว้ที่ Google Drive โดยอัตโนมัต...
- **`promptpay.py`** — def crc16_ccitt(data: str) -> str: data_bytes = data.encode('utf-8') crc = 0xFFFF for byte in data_bytes: crc ^= (byte << 8)
- **`server_check.py`** — sys.stdout.reconfigure(encoding='utf-8')
- **`setup_admin_rich_menu.py`** — """ setup_admin_rich_menu.py รันครั้งเดียวเพื่อสร้าง Admin Rich Menu และผูกกับแอดมินทุกคนในระบบ """
- **`setup_rich_menu.py`** — """ setup_rich_menu.py รันสคริปต์นี้ครั้งเดียวเพื่อสร้าง Rich Menu ใน LINE Bot """
- **`temp_list.py`** — genai.configure(api_key=[REDACTED_API_KEY]) try: for m in genai.list_models():
- **`temp_reimport.py`** — DB_FILE = '/home/nctlite/filesaverbot/chat_log.db'
- **`test_pkce.py`** — flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file( 'client_secret.json',
- **`test_pkce2.py`** — print("fetch_token kwargs:", google_auth_oauthlib.flow.Flow.fetch_token.__code__.co_varnames) print("authorization_url kwargs:", google_auth_oauthlib....
- **`token.json`** — {"token": "[REDACTED_OAUTH_TOKEN]...
- **`token.json.bak`** — {"token": "[REDACTED_OAUTH_TOKEN]...
- **`weekly_cron.log`** — /home/nctlite/filesaverbot/weekly_summary.py:76: LineBotSdkDeprecatedIn30: Call to deprecated class TextMessage. (Use 'from linebot.v3.webhooks import...
- **`weekly_summary.py`**
- **`.claude/settings.json`** — { "permissions": { "allow": [ "Bash(curl -s -o /dev/null -w \"%{http_code}\" https://filesaver.deathwolftech.site/)", "Bash(curl -s -o /dev/null -w \"...
- **`.claude/settings.local.json`** — { "permissions": { "allow": [ "Bash(pip show *)", "Bash(pip list *)",
- **`deploy/filesaverbot.service`** — [Unit] Description=File Saver LINE Bot Service (SaaS Version) After=network.target [Service]
- **`deploy/nginx.conf`** — server { listen 80; server_name _; # Replace with your domain name (e.g. bot.yourdomain.com) location / {
- **`extracted_v1/filesaverbot/credentials.json`** — { "type": "service_account", "project_id": "file-saver-479919", "private_key_id": "60082fddc695c53ff61eb45375bccfcf68a6f8ab", "private_key": "-----BEG...
- **`extracted_v1/filesaverbot/filesaver_bot.py`**
- **`extracted_v1/filesaverbot/token.json`** — {"token": "[REDACTED_OAUTH_TOKEN]...
- **`filesaverbot/credentials.json`** — { "type": "service_account", "project_id": "file-saver-479919", "private_key_id": "60082fddc695c53ff61eb45375bccfcf68a6f8ab", "private_key": "-----BEG...
- **`filesaverbot/filesaver_bot.py`**
- **`filesaverbot/token.json`** — {"token": "[REDACTED_OAUTH_TOKEN]...
- **`pending_uploads/BOQ_R1.xlsx`** — [Binary or unreadable]
- **`pending_uploads/Proforma Invoice-HW20260501A.pdf`** — [Binary or unreadable]
- **`pending_uploads/Proforma Invoice-HW20260501A.xlsx`** — [Binary or unreadable]
- **`RAW_Chat/[LINE]3king Axie.txt`** — 2026.02.25 Wednesday 09:41 Torre https://www.chiangmainews.co.th/social/3888473/ 09:42 Torre Photos 09:42 NCT_FileSaverBot ✅ บันทึกเรียบร้อย: img_6025...
- **`RAW_Chat/[LINE]Discuss nCt blue.txt`** — 2026.02.25 Wednesday 14:25 Torre @Chet_^o^78🤎🤎 share contact ต้น ให้พี่เก่ง ด้วยนะ ที่จะไปคุยงาน civil 14:26 Torre จริงๆ ถ้าเป็นไปได้ก็ลองดูงานอื่นๆมา...
- **`RAW_Chat/[LINE]PM All Project(NCT).txt`** — 2026.03.15 Sunday 21:28 Torre Torre added Chet_^o^789🤎🤎, DeathWolf 222324, Tong! to the group. <a href="line://nv/group/settings/groupname/chatId=c291...
- **`scratch/check_token.py`**
- **`scratch/deploy_bot_vps.py`** — sys.stdout.reconfigure(encoding='utf-8') host    = '178.128.59.217' username= 'root'
- **`scratch/deploy_richmenu_via_vps.py`** — """ Upload rich_menu.jpg to VPS then run deploy_user_menu.py remotely. """ sys.stdout.reconfigure(encoding='utf-8')
- **`scratch/deploy_user_menu.py`** — load_dotenv() token = os.getenv('LINE_CHANNEL_ACCESS_TOKEN')
- **`scratch/log_search_results.txt`** — --- Line 103 --- 98: {"step_index":272,"source":"MODEL","type":"PLANNER_RESPONSE","status":"DONE","created_at":"2026-05-26T12:03:32Z","tool_calls":[{"...
- **`scratch/pi_logs.txt`** — === JOURNALCTL LOGS === พ.ค. 26 21:22:19 raspberrypi systemd[1]: Started filesaverbot.service - File Saver Line Bot. พ.ค. 26 21:22:36 raspberrypi pyth...
- **`scratch/read_last_lines.py`** — sys.stdout.reconfigure(encoding='utf-8') with open(r"C:\Users\user\.gemini\antigravity\brain\d7c3ed78-3274-4649-9d63-de097996e574\.system_generated\lo...
- **`scratch/search_user_tokens.py`** — sys.stdout.reconfigure(encoding='utf-8') with open(r"C:\Users\user\.gemini\antigravity\brain\d7c3ed78-3274-4649-9d63-de097996e574\.system_generated\lo...
- **`scratch/update_journal_html.py`** — def update_journal(): agents_dir = r"d:\00_Python\FileSaverBot\.agents" md_path = os.path.join(agents_dir, "Agent-Journal.md")
- **`scratch/pi/check_configs.py`** — host = '100.100.52.93'
- **`scratch/pi/check_dhcpcd.py`** — host = '100.100.52.93' port = 22 username = 'nctlite'
- **`scratch/pi/check_logs.py`** — # Set output encoding to utf-8 sys.stdout.reconfigure(encoding='utf-8')
- **`scratch/pi/check_network.py`** — host = '100.100.52.93' port = 22 username = 'nctlite'
- **`scratch/pi/check_pi_dmesg.py`** — sys.stdout.reconfigure(encoding='utf-8')
- **`scratch/pi/check_pi_error.py`** — sys.stdout.reconfigure(encoding='utf-8')
- **`scratch/pi/check_pi_full_logs.py`** — host = '100.100.52.93' username = 'nctlite'
- **`scratch/pi/check_pi_linebot_v3.py`** — sys.stdout.reconfigure(encoding='utf-8') host, port, username, password = '100.100.52.93', 22, 'nctlite', '121212' ssh = paramiko.SSHClient()
- **`scratch/pi/check_pi_logs.py`** — sys.stdout.reconfigure(encoding='utf-8')
- **`scratch/pi/check_pi_oom.py`** — sys.stdout.reconfigure(encoding='utf-8')
- **`scratch/pi/check_pi_swap.py`** — sys.stdout.reconfigure(encoding='utf-8')
- **`scratch/pi/check_pi_venv.py`** — sys.stdout.reconfigure(encoding='utf-8') host, port, username, password = '100.100.52.93', 22, 'nctlite', '121212' ssh = paramiko.SSHClient()
- **`scratch/pi/check_service.py`** — # Set output encoding to utf-8 sys.stdout.reconfigure(encoding='utf-8')
- **`scratch/pi/check_swap_file.py`** — sys.stdout.reconfigure(encoding='utf-8')
- **`scratch/pi/check_tailscale.py`** — # Set output encoding to utf-8 sys.stdout.reconfigure(encoding='utf-8')
- **`scratch/pi/compare_dir.py`** — host = '100.100.52.93' port = 22
- **`scratch/pi/compare_versions.py`** — host = '100.100.52.93'
- **`scratch/pi/deploy.py`** — host = '100.100.52.93' port = 22
- **`scratch/pi/deploy_bot_pi.py`** — sys.stdout.reconfigure(encoding='utf-8') host, port, username, password = '100.100.52.93', 22, 'nctlite', '121212' LOCAL  = r'd:\00_Python\FileSaverBo...
- **`scratch/pi/deploy_weekly_summary.py`** — sys.stdout.reconfigure(encoding='utf-8')
- **`scratch/pi/download_all_remote.py`** — host = '100.100.52.93'
- **`scratch/pi/download_token.py`** — host = '100.100.52.93' port = 22
- **`scratch/pi/enable_pi_swap.py`** — sys.stdout.reconfigure(encoding='utf-8')
- **`scratch/pi/find_bot.py`** — host = '100.100.52.93' port = 22 username = 'nctlite'
- **`scratch/pi/fix_dns_permanent.py`** — host = '100.100.52.93' port = 22 username = 'nctlite'
- **`scratch/pi/fix_dns_tailscale.py`** — host = '100.100.52.93' port = 22 username = 'nctlite'
- **`scratch/pi/fix_dns_temp.py`** — host = '100.100.52.93' port = 22 username = 'nctlite'
- **`scratch/pi/get_public_ip.py`** — host = '100.100.52.93' port = 22 username = 'nctlite'
- **`scratch/pi/list_filesaverbot.py`** — host = '100.100.52.93' port = 22
- **`scratch/pi/list_remote.py`** — host = '100.100.52.93' port = 22
- **`scratch/pi/manual_dns_fix.py`** — host = '100.100.52.93' port = 22 username = 'nctlite'
- **`scratch/pi/quick_check_pi.py`** — sys.stdout.reconfigure(encoding='utf-8')
- **`scratch/pi/read_service.py`** — host = '100.100.52.93' port = 22 username = 'nctlite'
- **`scratch/pi/revert_pi_weekly_summary.py`** — sys.stdout.reconfigure(encoding='utf-8') host, port, username, password = '100.100.52.93', 22, 'nctlite', '121212' REMOTE_PATH = '/home/nctlite/filesa...
- **`scratch/pi/test_direct_conn.py`** — host = '100.100.52.93' port = 22 username = 'nctlite'
- **`scratch/pi/test_ip_ping.py`** — host = '100.100.52.93' port = 22 username = 'nctlite'
- **`scratch/pi/test_nslookup.py`** — host = '100.100.52.93' port = 22 username = 'nctlite'
- **`scratch/pi/test_ping.py`** — host = '100.100.52.93' port = 22 username = 'nctlite'
- **`scratch/pi/update_service.py`** — host = '100.100.52.93' port = 22 username = 'nctlite'
- **`scratch/pi/view_pi_details.py`** — sys.stdout.reconfigure(encoding='utf-8')
- **`scratch/vps/change_domain_vps.py`** — sys.stdout.reconfigure(encoding='utf-8')
- **`scratch/vps/check_service_logs.py`** — sys.stdout.reconfigure(encoding='utf-8')
- **`scratch/vps/check_vps_client_secret.py`** — sys.stdout.reconfigure(encoding='utf-8') host = '178.128.59.217' username = 'root'
- **`scratch/vps/check_vps_cron.py`** — sys.stdout.reconfigure(encoding='utf-8') host = '178.128.59.217' username = 'root'
- **`scratch/vps/check_vps_logs.py`** — sys.stdout.reconfigure(encoding='utf-8') host = '178.128.59.217' username = 'root'
- **`scratch/vps/copy_deploy_files.py`** — host = '178.128.59.217' username = 'root'
- **`scratch/vps/deploy_vps.py`** — host = '178.128.59.217'
- **`scratch/vps/deploy_weekly_vps.py`** — sys.stdout.reconfigure(encoding='utf-8') host = '178.128.59.217' username = 'root'
- **`scratch/vps/finalize_vps.py`** — sys.stdout.reconfigure(encoding='utf-8')
- **`scratch/vps/inspect_nginx.py`** — sys.stdout.reconfigure(encoding='utf-8')
- **`scratch/vps/inspect_vps.py`** — # Ensure UTF-8 output encoding sys.stdout.reconfigure(encoding='utf-8')
- **`scratch/vps/read_vps_env.py`** — sys.stdout.reconfigure(encoding='utf-8')
- **`scratch/vps/remove_vps_weekly.py`** — sys.stdout.reconfigure(encoding='utf-8') host = '178.128.59.217' username = 'root'
- **`scratch/vps/restart_service.py`** — sys.stdout.reconfigure(encoding='utf-8')
- **`scratch/vps/search_logs.py`** — sys.stdout.reconfigure(encoding='utf-8') with open(r"C:\Users\user\.gemini\antigravity\brain\d7c3ed78-3274-4649-9d63-de097996e574\.system_generated\lo...
- **`scratch/vps/setup_vps_cron.py`** — sys.stdout.reconfigure(encoding='utf-8') host = '178.128.59.217' username = 'root'
- **`scratch/vps/setup_vps_packages.py`** — sys.stdout.reconfigure(encoding='utf-8')
- **`scratch/vps/test_vps_conn.py`** — host = '178.128.59.217' username = 'root'
- **`scratch/vps/update_vps_secret.py`** — sys.stdout.reconfigure(encoding='utf-8')
- **`scratch/vps/view_live_logs.py`** — sys.stdout.reconfigure(encoding='utf-8')
- **`templates/admin_dashboard.html`** — <!DOCTYPE html> <html lang="th"> <head> <meta charset="UTF-8"> <meta name="viewport" content="width=device-width, initial-scale=1.0">
- **`templates/admin_login.html`** — <!DOCTYPE html> <html lang="th"> <head> <meta charset="UTF-8"> <meta name="viewport" content="width=device-width, initial-scale=1.0">
- **`templates/auth.html`** — <!DOCTYPE html> <html lang="en"> <head> <meta charset="UTF-8"> <meta name="viewport" content="width=device-width, initial-scale=1.0">
- **`templates/index.html`** — <!DOCTYPE html> <html lang="th"> <head> <meta charset="UTF-8"> <meta name="viewport" content="width=device-width, initial-scale=1.0">
- **`templates/privacy.html`** — <!DOCTYPE html> <html lang="th"> <head> <meta charset="UTF-8"> <meta name="viewport" content="width=device-width, initial-scale=1.0">
- **`templates/success.html`** — <!DOCTYPE html> <html lang="en"> <head> <meta charset="UTF-8"> <meta name="viewport" content="width=device-width, initial-scale=1.0">
- **`templates/terms.html`** — <!DOCTYPE html> <html lang="th"> <head> <meta charset="UTF-8"> <meta name="viewport" content="width=device-width, initial-scale=1.0">
