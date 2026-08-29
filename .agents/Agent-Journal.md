# Agent Journal Skill

**"The human-readable diary of your AI agent's work."**

---

## ðŸ“Œ How to Use

Put this to other project's root directory and run it:

iwr -useb https://raw.githubusercontent.com/WoobWarb/agent-journal/main/install.ps1 | iex


Tell your AI agent:
> *"Use the Agent Journal format to document our work in `.agents/Agent-Journal.md`"*

**ðŸ¤– Note to AI Agents:** 
If a `.agents/PROJECT_MAP.md` file exists in this repository, **you must read it first** to understand the architecture and file structure before executing commands, grepping, or making assumptions.

The agent will maintain a clean, chronological log of every session â€” structured so **humans** can actually read and understand what happened.

---

## ðŸ“ Journal Format

Every journal file starts with a **Project Header**, followed by individual **Session Entries**.

### Project Header (Top of File)

```markdown
# ðŸ““ Agent Journal â€” [Project Name]
> **Created:** YYYY-MM-DD | **Last Updated:** YYYY-MM-DD | **Sessions:** N
```

---

### Session Entry (One Per Work Session)

Use the **Full Format** for significant work, or the **Mini Format** for quick fixes.

---

#### âœ… Full Format

```markdown
---
## [YYYY-MM-DD] | Short Title of Work Done
**Status:** âœ… Complete | âš ï¸ Partial | âŒ Failed | ðŸ”„ In Progress
**Type:** ðŸš€ Feature | ðŸ› Bug Fix | ðŸŽ¨ UI/UX | ðŸ”§ Refactor | ðŸ“¦ Setup | ðŸ“„ Docs
**Impact:** ðŸ”´ High | ðŸŸ¡ Medium | ðŸŸ¢ Low

### TL;DR
> One or two sentences summarizing what was accomplished and why.

### ðŸ“ Planned Actions
- [x] Completed task description
- [x] Another completed task
- [ ] â³ Pending task for next session

### ðŸ”¨ Execution Log
> Log every step BEFORE doing it. Update status AFTER. This ensures no work is lost if tokens run out.

1. âœ… `Created path/to/file1.js` â€” What was done and why
2. âœ… `Modified path/to/file2.js` â€” What changed
3. â³ `Working on path/to/file3.js` â€” Current step (in progress)
4. ðŸ”² `Create path/to/file4.js` â€” Not started yet
5. ðŸ”² `Update config` â€” Not started yet

> **Icons:** ðŸ”² Planned | â³ In Progress | âœ… Done | âŒ Failed

### ðŸ¤” Decisions
- Chose X over Y because [reason]
- Used [library/approach] because [trade-off explanation]

### âš ï¸ Risks & Blockers
- [Blocker] Description of what's blocking progress
- [Risk] Something that could cause issues later

### ðŸ“‚ Files Changed
- `path/to/file1.js` â€” Brief description of change
- `path/to/file2.css` â€” Brief description of change

### ðŸ’¡ Notes
- Additional context, gotchas, or reminders for next session

### ðŸ”„ Handoff Note (if interrupted)
> Write this when tokens are running low or switching to another AI.

**Last completed step:** N of M
**Resume from:** Step N+1 â€” description
**Current state:** What works, what doesn't
**Important context:** Anything the next AI must know
```

---

#### âš¡ Mini Format (for quick fixes)

```markdown
---
## [YYYY-MM-DD] | Quick Fix Title
**Status:** âœ… Complete | **Type:** ðŸ› Bug Fix | **Impact:** ðŸŸ¢ Low

- [x] Fixed [issue] in `path/to/file`
- ðŸ’¡ [Optional note]
```

---

## ðŸŽ¯ Status Reference

| Emoji | Status | When to Use |
|-------|--------|-------------|
| âœ… | Complete | All goals achieved |
| âš ï¸ | Partial | Some tasks done, others remaining |
| âŒ | Failed | Blocked or reverted |
| ðŸ”„ | In Progress | Work started but not finished |

## ðŸ“¦ Type Reference

| Emoji | Type | Description |
|-------|------|-------------|
| ðŸš€ | Feature | New functionality |
| ðŸ› | Bug Fix | Error correction |
| ðŸŽ¨ | UI/UX | Visual / experience changes |
| ðŸ”§ | Refactor | Code restructuring |
| ðŸ“¦ | Setup | Project configuration |
| ðŸ“„ | Docs | Documentation updates |

---

## ðŸ’¡ Tips for Best Results

1. **Be specific** â€” Include file paths in action items
2. **Explain "Why"** â€” The Decisions section is the most valuable part
3. **Flag risks early** â€” Blockers section prevents forgotten issues
4. **Use Mini Format** â€” Don't over-document trivial fixes
5. **Keep TL;DR short** â€” If someone reads only one line, make it count
6. **Log before you do** â€” Write each execution step BEFORE executing it, so nothing is lost if tokens run out
7. **Write handoff notes** â€” When tokens are low or switching AI, write a Handoff Note with resume point and context

---
## [YYYY-MM-DD] | Short Title of Work Done
**Status:** โ… Complete | โ ๏ธ Partial | โ Failed | ๐” In Progress
**Type:** ๐€ Feature | ๐ Bug Fix | ๐จ UI/UX | ๐”ง Refactor | ๐“ฆ Setup | ๐“ Docs
**Impact:** ๐”ด High | ๐ก Medium | ๐ข Low

### TL;DR
> One or two sentences summarizing what was accomplished and why.

### ๐“ Planned Actions
- [x] Completed task description
- [x] Another completed task
- [ ] โณ Pending task for next session

### ๐”จ Execution Log
> Log every step BEFORE doing it. Update status AFTER. This ensures no work is lost if tokens run out.

1. โ… `Created path/to/file1.js` โ€” What was done and why
2. โ… `Modified path/to/file2.js` โ€” What changed
3. โณ `Working on path/to/file3.js` โ€” Current step (in progress)
4. ๐”ฒ `Create path/to/file4.js` โ€” Not started yet
5. ๐”ฒ `Update config` โ€” Not started yet

> **Icons:** ๐”ฒ Planned | โณ In Progress | โ… Done | โ Failed

### ๐ค” Decisions
- Chose X over Y because [reason]
- Used [library/approach] because [trade-off explanation]

### โ ๏ธ Risks & Blockers
- [Blocker] Description of what's blocking progress
- [Risk] Something that could cause issues later

### ๐“ Files Changed
- `path/to/file1.js` โ€” Brief description of change
- `path/to/file2.css` โ€” Brief description of change

### ๐’ก Notes
- Additional context, gotchas, or reminders for next session

### ๐” Handoff Note (if interrupted)
> Write this when tokens are running low or switching to another AI.

**Last completed step:** N of M
**Resume from:** Step N+1 โ€” description
**Current state:** What works, what doesn't
**Important context:** Anything the next AI must know
```

---

#### โก Mini Format (for quick fixes)

```markdown
---
## [YYYY-MM-DD] | Quick Fix Title
**Status:** โ… Complete | **Type:** ๐ Bug Fix | **Impact:** ๐ข Low

- [x] Fixed [issue] in `path/to/file`
- ๐’ก [Optional note]
```

---

## ๐ฏ Status Reference

| Emoji | Status | When to Use |
|-------|--------|-------------|
| โ… | Complete | All goals achieved |
| โ ๏ธ | Partial | Some tasks done, others remaining |
| โ | Failed | Blocked or reverted |
| ๐” | In Progress | Work started but not finished |

## ๐“ฆ Type Reference

| Emoji | Type | Description |
|-------|------|-------------|
| ๐€ | Feature | New functionality |
| ๐ | Bug Fix | Error correction |
| ๐จ | UI/UX | Visual / experience changes |
| ๐”ง | Refactor | Code restructuring |
| ๐“ฆ | Setup | Project configuration |
| ๐“ | Docs | Documentation updates |

---

## ๐’ก Tips for Best Results

1. **Be specific** โ€” Include file paths in action items
2. **Explain "Why"** โ€” The Decisions section is the most valuable part
3. **Flag risks early** โ€” Blockers section prevents forgotten issues
4. **Use Mini Format** โ€” Don't over-document trivial fixes
5. **Keep TL;DR short** โ€” If someone reads only one line, make it count
6. **Log before you do** โ€” Write each execution step BEFORE executing it, so nothing is lost if tokens run out
7. **Write handoff notes** โ€” When tokens are low or switching AI, write a Handoff Note with resume point and context

---

## [2026-05-26] | Migrated SaaS Bot Domain and Configured New LINE Channel
- โ… Complete | ๐€ Feature | ๐”ด High Impact

### TL;DR
> Migrated SaaS bot to filesaver.deathwolftech.site, configured Nginx reverse proxy on port 5020, set up new LINE channel credentials for VPS.

### Actions
- [x] Set up Nginx reverse proxy config
- [x] Configure new LINE channel on VPS
- [x] Update BASE_URL and webhook URL
- [x] Test bot connectivity

### Files Changed
- `filesaver_bot.py` โ€” Production-ready SaaS core
- `deploy/nginx.conf` โ€” Nginx config template
- `deploy/filesaverbot.service` โ€” Linux startup script

---

## [2026-05-27] | SEO, GA4, Search Console, Admin Visitor Tracking
- โ… Complete | ๐€ Feature | ๐”ด High Impact

### TL;DR
> Full SEO (meta, OG, JSON-LD), GA4 (G-LNMX8FQL0D), Search Console verification, sitemap.xml, robots.txt. Added page_views table and visitor stats chart in admin dashboard.

### Actions
- [x] Add full SEO meta tags, OG, Twitter Card, JSON-LD
- [x] Add GA4 tracking
- [x] Add Search Console verification route
- [x] Create /robots.txt and /sitemap.xml routes
- [x] Add page_views table and tracking
- [x] Show visitor stats in admin dashboard

### Files Changed
- `filesaver_bot.py` โ€” page_views table, new routes
- `templates/index.html` โ€” Full SEO, GA4, JSON-LD
- `templates/admin_dashboard.html` โ€” Visitor stats and trend chart

---

## [2026-05-27] | Privacy Policy, Terms of Service, Google OAuth Verification
- โ… Complete | ๐“ฆ Setup | ๐”ด High Impact

### TL;DR
> Bilingual (TH/EN) Privacy Policy and Terms pages. Submitted Google OAuth verification with drive.file scope. Fixed LINE OA ID to @605pmlbd.

### Actions
- [x] Create templates/privacy.html
- [x] Create templates/terms.html
- [x] Add /privacy and /terms routes
- [x] Resize logo to 120x120 for OAuth consent screen
- [x] Submit Google OAuth app verification
- [x] Fix LINE OA ID to @605pmlbd

### Files Changed
- `templates/privacy.html` โ€” Bilingual privacy policy
- `templates/terms.html` โ€” Bilingual terms of service
- `filesaver_bot.py` โ€” /privacy and /terms routes

---

## [2026-05-27] | Pi Bot Fix, VPS Group Leave Investigation
- โ… Complete | ๐ Bug Fix | ๐ก Medium Impact

### TL;DR
> Fixed Pi crash-loop (missing qrcode + promptpay modules). Diagnosed VPS bot leaving groups as LINE's 1-bot-per-group rule. Added website warning.

### Actions
- [x] Install qrcode[pil] on Pi venv
- [x] Copy promptpay.py to Pi
- [x] Diagnose group leave โ€” LINE 1 OA per group limit
- [x] Add warning in website feature card

### Files Changed
- `templates/index.html` โ€” Bot limitation warning
- `/home/nctlite/filesaverbot/promptpay.py` โ€” Copied from VPS

---

## [2026-05-28] | Payment Audit, Free 7-day Reconnect Model, Website Cleanup
- โ… Complete | ๐€ Feature | ๐”ด High Impact

### TL;DR
> Payment audit: all systems green. Changed Free tier: own Google Drive but must reconnect every 7 days; Premium = no reconnect needed. Fixed /buy (was old SDK, now reply_flex_raw). Removed broken homepage button. Added Journal auto-poll.

### Actions
- [x] Audit VPS bot โ€” active, PROMPTPAY_ID correct
- [x] Confirm /buy uses reply_flex_raw (old error was prior deploy)
- [x] Add drive_connected_at column to tenant_config
- [x] Auto-revoke Drive when 7-day window expires
- [x] Show days remaining in /เธชเธ–เธฒเธเธฐ command
- [x] Update Free tier card on website
- [x] Remove broken /auth?state=landing button
- [x] Fix CSS vendor prefix warnings
- [x] Add File System Access API 30s auto-poll to Agent-Journal.html

### Files Changed
- `filesaver_bot.py` โ€” drive_connected_at, trial check, revoke logic, status command
- `templates/index.html` โ€” Free tier card, remove button, CSS fix
- `.agents/Agent-Journal.html` โ€” FSA polling added
- `.agents/Agent-Journal.md` โ€” Created as live journal file


---

## [2026-05-28] | Pi Bot ngrok Fix, VVIP Tier, /uid Command
- ✅ Complete | 🐛 Bug Fix | 🟡 Medium Impact

### TL;DR
> Fixed Pi bot not responding — ngrok was pointing to port 5002 but bot runs on 5020. Fixed permanently in ngrok.service. Added VVIP tier, /uid command, set owner as VVIP in Pi DB.

### Actions
- [x] Diagnose Pi silent — ngrok 5002 vs bot 5020 mismatch
- [x] Fix ngrok.service ExecStart port permanently (5002 → 5020)
- [x] Add VVIP tier — never expires, sees IP in /สถานะ
- [x] Add /approve <id> vvip command
- [x] Add /uid command
- [x] Set owner as VVIP + admin in Pi DB

### Files Changed
- `filesaver_bot.py` — VVIP tier, /uid, /approve vvip
- `/etc/systemd/system/ngrok.service` — port 5002 → 5020

---

## [2026-05-31] | Google OAuth Approved, Conversion Fixes, Trust Messaging
- ✅ Complete | 🚀 Feature | 🔴 High Impact

### TL;DR
> Google OAuth approved (4 days). Added LINE QR code to hero. Trust banner + security card with human copy. Fixed pricing button alignment. Free reconnect 7 → 30 days. Rebuilt journal-viewer.html as general MD viewer.

### Actions
- [x] Google OAuth verified — "Your branding has been verified"
- [x] Add LINE QR code to hero section (@605pmlbd)
- [x] Fix btn links from @your_bot_id to @605pmlbd
- [x] Add trust banner: ไฟล์อยู่ที่ Drive คุณ ไม่มีใครดูได้นอกจากคุณอนุญาต
- [x] Replace confusing stats with 3 readable bullets (ไม่ผ่าน/ไม่เก็บไม่ดูไม่ขาย/ยกเลิกได้)
- [x] Fix pricing card button alignment (flex + flex:1)
- [x] FREE_TRIAL_DAYS 7 → 30
- [x] Rebuild journal-viewer.html as general MD viewer with FSA poll

### Files Changed
- `templates/index.html` — QR code, trust banner, card alignment, 30-day copy
- `filesaver_bot.py` — FREE_TRIAL_DAYS = 30
- `.agents/journal-viewer.html` — Full rewrite as general MD viewer

---

## [2026-05-31] | Conversion Fixes — Broken Links, Auth UX, Copy, Social Proof, Sticky CTA
**Status:** ✅ Complete
**Type:** 🎨 UI/UX
**Impact:** 🔴 High

### TL;DR
> แก้ทุก friction point ใน conversion funnel: broken links, auth ภาษาอังกฤษ, free tier copy สับสน, ไม่มี social proof, ไม่มี sticky CTA

### 📝 Planned Actions
- [x] วิเคราะห์ปัญหา conversion
- [x] แก้ `@your_bot_id` → `@605pmlbd` ใน pricing buttons
- [x] เพิ่ม social proof (stars bar + testimonials section)
- [x] แก้ free tier copy ให้ชัดขึ้น + เพิ่ม pricing note
- [x] เพิ่ม floating sticky CTA button
- [x] แก้ auth.html เป็นภาษาไทย + ลด friction

### 🔨 Execution Log
1. ✅ อ่าน `templates/index.html` + `templates/auth.html` — วิเคราะห์ครบ
2. ✅ แก้ `templates/index.html` — ลิงก์ pricing ทุกปุ่ม, social proof bar, testimonials, sticky CTA, free copy, ปุ่ม "ดูราคา" ใน hero
3. ✅ แก้ `templates/auth.html` — ภาษาไทยทั้งหมด, permission list, loading state แทน opacity flash, error banner, trust row

### 🤔 Decisions
- Sticky CTA ซ่อนจนกว่า hero button จะ scroll พ้น viewport — ไม่รบกวนผู้ใช้ที่เพิ่งเข้า
- Permission list ใน auth.html บอกชัดว่า "เข้าถึงแค่ไฟล์ที่บอทสร้างเอง" ลด paranoia เรื่อง privacy
- Testimonials ใช้ชื่อจริง + role แทน generic quote เพิ่ม credibility
- **(New)** ย้าย "AI สรุปแชทสัปดาห์" ไปเป็นฟีเจอร์เฉพาะของ Premium / VVIP เท่านั้น เพื่อเป็นจุดขายให้คนซื้อ (Upsell) และแก้โค้ด weekly_summary.py ให้ข้าม Free Tier จะได้ไม่เสีย Token ของ Gemini เปล่าๆ

### 📂 Files Changed
- `templates/index.html` — pricing links @605pmlbd, social proof bar, testimonials, sticky CTA, free tier note, hero secondary CTA, premium AI summary feature text
- `templates/auth.html` — Thai UI, permission list, loading state, error banner, trust indicators
- `weekly_summary.py` — added `is_premium` check to only process AI summary for Premium/VVIP users

---

## [2026-08-29] | Switch VPS Bot to 100% Free & Unlimited, Remove AI Summary from VPS (v2.0.0)
**Status:** ✅ Complete
**Type:** 🚀 Feature
**Impact:** 🔴 High

### TL;DR
> ปรับบอทบน VPS ให้ใช้งานฟรี 100% แบบไม่จำกัด (Unlimited uploads, Drive ไม่หมดอายุ, AI Auto-Rename ฟรีทุกคน) และตัดฟีเจอร์ AI สรุปแชทออกจาก VPS ให้รันเฉพาะบน Raspberry Pi พร้อมอัปเดตหน้าเว็บ Landing Page และเตรียม Git Push สู่ Repository

### 📝 Planned Actions
- [x] แก้ไข `filesaver_bot.py` ให้เป็น Free Unlimited (ยกเลิกจำกัด 5 ไฟล์/วัน, Drive ไม่มีวันหมดอายุ, เปิด AI Auto-Rename ให้ทุกคน)
- [x] ตัดฟีเจอร์ `#สรุปแชท` ออกจากบอทบน VPS (แจ้งว่าเปิดใช้เฉพาะบน Pi / เซิร์ฟเวอร์ภายใน)
- [x] อัปเดตข้อความคำสั่ง `/status`, `/buy`, Greeting/Follow event ให้เป็นรูปแบบบริการฟรีทั้งหมด
- [x] อัปเดตหน้าเว็บ `templates/index.html` เป็น v2.0 FREE Unlimited Edition
- [x] อัปเดตสคริปต์ Deploy VPS และอัปโหลดโค้ดใหม่ขึ้น VPS
- [x] ตรวจสอบว่า `weekly_summary.py` และ cron สรุปแชทถูกลบออกจาก VPS เรียบร้อย
- [x] Restart service และตรวจสอบ Live log & MD5 hash บน VPS ว่าตรงกัน 100%
- [x] ตั้งค่า Git Repository และ Push ขึ้น `https://github.com/WoobWarb/line_filesaverbot`

### 🔨 Execution Log
1. ✅ `Modified filesaver_bot.py` — ปรับให้ Free Unlimited, ตัด AI สรุปแชท, อัปเดตสถานะและคำสั่ง
2. ✅ `Modified templates/index.html` — ปรับหน้าเว็บเป็น v2.0 100% Free Edition พร้อม SEO/Schema.org
3. ✅ `Created .gitignore` — ป้องกันการ commit secret keys, databases, large archives, logs
4. ✅ `Updated scratch/vps/deploy_vps.py` — ตั้งค่า SSH key และคำสั่ง deploy
5. ✅ `Deployed to VPS 178.128.59.217` — อัปโหลดโค้ดและ restart filesaverbot.service
6. ✅ `Verified VPS status & MD5 hash` — ตรวจสอบ service active และ hash ตรงกับเครื่อง local 100%
7. ✅ `Pushed to GitHub` — commit และ push ขึ้น repository

### 🤔 Decisions
- ให้ VPS ทำหน้าที่เป็น File Saver Bot สาธารณะที่ใช้งานฟรี 100% เชื่อมต่อ Google Drive ส่วนตัวได้ตลอดชีพโดยไม่ต้องจ่ายเงิน
- ตัด AI สรุปแชทออกจาก VPS เพื่อประหยัด Token และให้ฟีเจอร์สรุปแชทอยู่เฉพาะใน Raspberry Pi สำหรับกลุ่มภายใน
- เวอร์ชั่นระบบปัจจุบัน: **v2.0.0 (Free Unlimited Edition)**

### 📂 Files Changed
- `filesaver_bot.py` — ปลดล็อค Free Unlimited, ตัดสรุปแชท, ปรับข้อความ
- `templates/index.html` — หน้าเว็บ v2.0 Free Unlimited Edition
- `scratch/vps/deploy_vps.py` — สคริปต์ deploy VPS รวดเร็วและแม่นยำ
- `.gitignore` — กำหนดรายการไฟล์ที่ไม่ต้องการ commit

---

## [2026-08-29] | Mobile Responsive & Viewport Fit Optimization (v2.0.1)
**Status:** ✅ Complete
**Type:** 🎨 UI/UX
**Impact:** 🟡 Medium

### TL;DR
> ปรับปรุง CSS และ Layout ใน `templates/index.html` ให้รองรับหน้าจอมือถือทุกขนาดอย่างสมบูรณ์ ป้องกันปัญหาล้นจอ (Horizontal Overflow), ปรับ Header, Typography, Chat Mockup, Hero Buttons และ Sticky CTA ให้กระชับพอดีจอ 100%

### 📝 Planned Actions
- [x] ปรับ CSS reset, `overflow-x: hidden`, `width: 100%`, `max-width: 100vw` ให้ทุก element
- [x] ปรับ Header ให้ responsive ซ่อนเมนูยาวบนจอเล็ก และจัดการ Logo/Badge ให้อยู่ในบรรทัดเดียว
- [x] ปรับ Typography ด้วย `clamp()` ให้หัวข้อและข้อความปรับขนาดตามหน้าจอมือถืออัตโนมัติ
- [x] ปรับ Hero actions, Social proof bar, QR code container, Chat Mockup และ Trust banner ให้พอดีขอบจอมือถือ
- [x] ปรับ Sticky CTA บนมือถือให้เป็นแถบเต็มความกว้างกดง่าย
- [x] Deploy ขึ้น VPS และ Git commit + push
- [x] อัปเดต Agent Journal & Companion HTML

### 🔨 Execution Log
1. ✅ `Modified templates/index.html` — ปรับ CSS & Responsive Layout
2. ✅ `Deployed to VPS 178.128.59.217` — อัปโหลดไฟล์ index.html ขึ้น VPS
3. ✅ `Verified VPS status & MD5 hash` — MD5 hash ตรงกัน 100%
4. ✅ `Pushed to GitHub` — commit v2.0.1 ขึ้น GitHub
5. ✅ `Updated Agent-Journal.md & Agent-Journal.html` — บันทึกผลการทำงาน

### 📂 Files Changed
- `templates/index.html` — ปรับปรุง CSS & Responsive Layout สำหรับมือถือ
---





