# FileSaverBot Journal

## Project Purpose
จุดประสงค์ของบอทตัวนี้คือช่วยเซฟไฟล์จากแชท LINE (ที่มักจะหมดอายุ) ไปเก็บรักษาไว้ที่ Google Drive โดยอัตโนมัติ เพื่อป้องกันไฟล์สูญหายและให้ผู้ใช้สามารถเข้าถึงได้ตลอดเวลา

## Notes
- สร้างเมื่อ: 2026-05-27
- เทคโนโลยีหลัก: Python, LINE Messaging API, Google Drive API
- IP VPS (Production): 178.128.59.217

## Recent Updates (2026-05-27)
**Bug Fixes & OAuth Authentication Overhaul:**
1. **Google Cloud Settings:** Changed LINE Login Channel status from "Developing" to "Published" to fix LINE LIFF 400 Bad Request.
2. **HTML/JS Fixes:** Fixed a syntax error in `templates/auth.html` (script tags inside style tags) which prevented `liff.init()` from running.
3. **External Browser Fix (Error 403: disallowed_useragent):** Google blocks OAuth in LINE's in-app browser. Updated `auth.html` to intercept the login button click and use `liff.openWindow({ url: authUrl, external: true })` to force open Safari/Chrome.
4. **OAuth User Cap:** Clarified that the "100 user cap" is normal for unverified Google apps requesting sensitive Drive scopes. Kept status as "In production" and added the developer email to "Test users" to bypass the "Access blocked" screen.
5. **Insecure Transport Fix:** Added `os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'` to bypass `insecure_transport` errors when the Flask app is behind a reverse proxy (like Cloudflare/Nginx) that terminates HTTPS.
6. **PKCE Missing Code Verifier Fix:** Solved `(invalid_grant) Missing code verifier` by explicitly enabling PKCE (`autogenerate_code_verifier=True`) in `google_auth_oauthlib`. Created a global in-memory dictionary `pkce_store = {}` to temporarily cache the `code_verifier` (using LINE's `state` / `source_id` as the key) during the redirect phase, and restored it in the callback `/google/callback` before calling `fetch_token()`.
7. **Deployment Automation:** Created `deploy.bat` to easily deploy updates via `scp` and `ssh` to the VPS (`178.128.59.217`) and automatically restart the `filesaverbot` systemd service.
