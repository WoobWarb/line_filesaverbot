# Universal Agent Skill: Context + Journal + Map

**Version:** 3.2
**Compatible:** Claude Code, Antigravity, Cursor, Windsurf, GitHub Copilot, any LLM agent

---

## Rules for AI Agent

When working on this project, follow these rules automatically:

### 1. Read Project Map First

If `.agents/PROJECT_MAP.md` exists, read it before searching or reading files.
This saves tokens and prevents hallucinations about project structure.

If `.agents/pipeline.md` exists, read it before running any build, test, lint, or deploy commands.
This tells you the exact commands for this project — don't guess or use defaults.

### 2. Pre-Journaling (BEFORE coding)

Before making any code changes, write an entry in `.agents/Agent-Journal.md`:

```markdown
---
## [YYYY-MM-DD] | Short description of task
**Status:** 🔄 In Progress
**Type:** [🚀 Feature | 🐛 Fix | 🎨 UI | 🔧 Refactor | 📦 Setup | 📄 Docs]
**Impact:** [🟢 Low | 🟡 Medium | 🔴 High]

### TL;DR
> One-line summary of what will be done.

### 📝 Planned Actions
- [ ] Action 1
- [ ] Action 2

### 🤔 Decisions
- Why this approach was chosen

### 📂 Files to Change
- `path/to/file` — what will change
---
```

### 3. Step-by-Step Logging (DURING coding)

**This is critical for token-limit recovery.** Before EACH action, log it in the journal so that if the session is interrupted (token limit, crash, switching AI), the next agent can pick up exactly where you left off.

**Rule:** Write the step BEFORE you execute it. Update it AFTER.

```markdown
### 🔨 Execution Log
1. ✅ `Created src/services/auth.ts` — JWT service with login/register
2. ✅ `Modified prisma/schema.prisma` — Added User model with email/password fields
3. ✅ `Created src/routes/auth.routes.ts` — POST /login, POST /register endpoints
4. ⏳ `Modifying src/middleware/auth.ts` — Adding JWT verification middleware
5. 🔲 `Create src/tests/auth.test.ts` — Unit tests for auth service
6. 🔲 `Update .env.example` — Add JWT_SECRET variable
```

**Status icons:**
- 🔲 = Planned (not started)
- ⏳ = About to do / in progress
- ✅ = Done
- ❌ = Failed / skipped (add reason)

**When token limit hits or you switch AI, the new agent reads this log and knows:**
- What is already done (✅)
- What was in progress (⏳) — may need to verify/complete
- What remains (🔲) — continue from here

### 4. Completion (AFTER coding)

Update the same entry:
- Change status to `✅ Complete` (or `⚠️ Partial` / `❌ Failed`)
- Check off completed actions
- Add any notes or blockers discovered

### 5. Generate HTML Companion (AFTER every journal update)

**"HTML is the new Markdown"** — After writing or updating `Agent-Journal.md`, generate a companion `Agent-Journal.html` that opens instantly in any browser without needing a file upload.

Create `.agents/Agent-Journal.html` with this exact structure:

```html
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Agent Journal</title>
</head>
<body>
<script>
window.JOURNAL_DATA = `PASTE_ESCAPED_MD_CONTENT_HERE`;
</script>
<!-- Viewer source: copy the full contents of journal-viewer.html below this line -->
VIEWER_HTML_PLACEHOLDER
</body>
</html>
```

**Steps to generate:**
1. Read the current `.agents/Agent-Journal.md` content
2. Escape any backtick (`` ` ``) characters in the content: replace `` ` `` with `` \` ``
3. Create `.agents/Agent-Journal.html` using the template above
4. In `window.JOURNAL_DATA = \`...\``, paste the escaped markdown between the backticks
5. The viewer will auto-detect this data and display the dashboard immediately — no file upload needed

**Why this matters:** Long markdown files don't get read. An HTML dashboard always gets opened.

### 6. Session Context

Update `.agents/active.md` with current task focus so the next session can resume.
Include the last completed step number so the next agent knows the exact resume point.

### 7. Technical Decisions

For significant architectural decisions, add notes to `.agents/topics/[topic].md`.

### 8. Handoff Protocol (when token limit is near or switching AI)

If you sense the conversation is getting long or the user mentions switching:
1. Update all ⏳ steps to their actual status (✅ or ❌)
2. Write a `### 🔄 Handoff Note` at the bottom of the current entry:

```markdown
### 🔄 Handoff Note
**Last completed step:** 3 of 6
**Resume from:** Step 4 — `Modifying src/middleware/auth.ts`
**Current state:** Auth service and routes are working, schema migrated. Need middleware + tests.
**Important context:** Using RS256 algorithm for JWT, not HS256. See .env.example for key paths.
```

---

## File Structure

```
.agents/
├── AGENTS.md           # This rules file (universal)
├── Agent-Journal.md    # Human-readable work diary (source of truth)
├── Agent-Journal.html  # ✨ Auto-generated HTML companion — open in browser
├── active.md           # Current task context (for AI resume)
├── pipeline.md         # Build, test, lint, and deploy commands for this project
├── PROJECT_MAP.md      # Auto-generated codebase map
├── graph.json          # Machine-readable project graph
├── sessions/           # Detailed session checkpoints
├── topics/             # Architectural decision records
├── index/              # Filesystem snapshots
└── private/            # Git-ignored local notes
```

---

## Platform-Specific Integration

### Claude Code
Add to project `CLAUDE.md`:
```
Read and follow .agents/AGENTS.md for journaling rules.
```

### Cursor / Windsurf
Rules are auto-added to `.cursorrules` / `.windsurfrules` by the installer.

### Antigravity
Register as skill in `.antigravity/extensions.json`:
```json
{
  "id": "unified-agent-skill",
  "name": "Agent Context + Journal",
  "enabled": true,
  "path": "./unified-skill.md"
}
```

### Any Other Agent
Just tell it: "Follow the rules in .agents/AGENTS.md"

---

## Journal Format Reference

### Full Entry (features, big changes)
```markdown
## [2026-05-16] | Built payment integration
**Status:** ✅ Complete
**Type:** 🚀 Feature | **Impact:** 🔴 High

### TL;DR
> Integrated Stripe for one-time payments with webhook handling.

### 📝 Planned Actions
- [x] Create payment service
- [x] Add webhook endpoint
- [x] Update database schema
- [ ] ⏳ Add subscription support (next sprint)

### 🔨 Execution Log
1. ✅ `Created src/services/payment.ts` — Stripe SDK init, createCheckout(), handleWebhook()
2. ✅ `Created src/api/webhooks/stripe.ts` — Webhook signature verification + event routing
3. ✅ `Modified prisma/schema.prisma` — Added Payment model (id, amount, status, stripeId)
4. ✅ `Ran prisma migrate` — Migration 20260516_payments applied
5. ✅ `Modified src/app.ts` — Registered webhook route with raw body parser

### 🤔 Decisions
- Stripe over PayPal: better developer experience, lower fees in TH
- Webhook-first: ensures payment state is always accurate

### ⚠️ Risks & Blockers
- Need production Stripe keys before deploy

### 📂 Files Changed
- `src/services/payment.ts` — Payment service with Stripe SDK
- `src/api/webhooks/stripe.ts` — Webhook handler
- `prisma/schema.prisma` — Added Payment model

### 💡 Notes
- Test with `stripe listen --forward-to localhost:3000/api/webhooks/stripe`
```

### Entry interrupted by token limit (partial work)
```markdown
## [2026-05-16] | Adding user authentication
**Status:** ⚠️ Partial
**Type:** 🚀 Feature | **Impact:** 🔴 High

### TL;DR
> JWT-based auth with login/register. Interrupted at step 4 of 6.

### 🔨 Execution Log
1. ✅ `Created src/services/auth.ts` — JWT service with login/register
2. ✅ `Modified prisma/schema.prisma` — Added User model
3. ✅ `Created src/routes/auth.routes.ts` — POST /login, POST /register
4. ⏳ `Modifying src/middleware/auth.ts` — JWT verification middleware (INCOMPLETE)
5. 🔲 `Create src/tests/auth.test.ts` — Unit tests
6. 🔲 `Update .env.example` — Add JWT_SECRET

### 🔄 Handoff Note
**Last completed step:** 3 of 6
**Resume from:** Step 4 — auth middleware was started but not tested
**Current state:** Auth service + routes work. Schema migrated. Middleware file exists but verify() not wired up.
**Important context:** Using RS256 (not HS256). Key pair in /keys/ folder.
```

### Mini Entry (quick fixes, small changes)
```markdown
## [2026-05-16] | Fixed login redirect loop
**Status:** ✅ Complete | **Type:** 🐛 Fix | **Impact:** 🟡 Medium
- ✅ Fixed infinite redirect in `src/middleware/auth.ts` line 42
- Root cause: missing `return` after `redirect()` call
```

---

## Commands (for agents that support them)

| Command | Action |
|---------|--------|
| `@agents show active` | Show current task context |
| `@agents resume` | Load context and continue work |
| `@agents update map` | Regenerate PROJECT_MAP.md |
| `@agents list sessions` | Show recent session files |
| `@agents generate html` | Regenerate `Agent-Journal.html` from current `.md` |
