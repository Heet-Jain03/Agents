# Deploy to Vercel (GitHub → Vercel)

**Repository:** [github.com/Heet-Jain03/Agents](https://github.com/Heet-Jain03/Agents)

## 1. Push to GitHub

```bash
cd c:\Users\heetj\OneDrive\Documents\MarketPlace-main
git init
git add .
git commit -m "Add Vercel deployment configuration"
git branch -M main
git remote add origin https://github.com/Heet-Jain03/Agents.git
git push -u origin main
```

If `origin` already exists, update it instead:

```bash
git remote set-url origin https://github.com/Heet-Jain03/Agents.git
git push -u origin main
```

On Windows, the first commit may be on `master`; run `git branch -M main` before pushing.

## 2. Import in Vercel

1. Go to [vercel.com](https://vercel.com) → **Add New Project**
2. Import **[Heet-Jain03/Agents](https://github.com/Heet-Jain03/Agents)**
3. Framework preset: **Other** (Vercel detects `vercel.json` and Python)
4. Root directory: project root (default)

## 3. Environment variables (required)

In **Project → Settings → Environment Variables**, add:

| Variable | Notes |
|----------|--------|
| `JWT_SECRET` | 64-char hex (`python -c "import secrets; print(secrets.token_hex(32))"`) |
| `INTERNAL_SECRET` | Another random hex string |
| `AGENT_TOKEN_RESEARCH` | Random string |
| `AGENT_TOKEN_WRITER` | Random string |
| `AGENT_TOKEN_ANALYST` | Random string |
| `GROQ_API_KEY` | Or `OPENROUTER_API_KEY` |

Apply to **Production**, **Preview**, and **Development**.

## 4. Deploy

Click **Deploy**. Your app will be at:

- UI: `https://<your-vercel-project>.vercel.app/` (from `public/index.html`)
- API: same origin (`/auth/*`, `/orchestrate`, `/agents/research`, etc.)

## 5. Notes

- **SQLite** uses `/tmp/users.db` on Vercel (ephemeral; users reset on cold starts). For production persistence, use Vercel Postgres or another hosted DB later.
- **Function timeout**: `maxDuration` is 60s (Pro). Hobby plan may cap at 10s — long agent runs may need Pro or an external host for agents.
- **Docker/EC2** still works unchanged via `Dockerfile` and `start_all.sh`.
