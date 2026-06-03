"""
Vercel serverless entry — single FastAPI app mounting all marketplace services.
Docker/EC2 deployments continue to use start_all.sh with separate ports.
"""

from __future__ import annotations

import os
import sys
from pathlib import Path

# Project root (parent of api/) on Python path for service imports
ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

# Configure URLs and DB before service modules read environment
if os.environ.get("VERCEL"):
    vercel_url = (os.environ.get("VERCEL_URL") or "").strip().rstrip("/")
    if vercel_url and not vercel_url.startswith("http"):
        vercel_url = f"https://{vercel_url}"
    if vercel_url:
        os.environ.setdefault("AUTH_SERVICE_URL", vercel_url)
        os.environ.setdefault("AGENT_BASE_URL", vercel_url)
    os.environ.setdefault("DB_PATH", "/tmp/users.db")

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from mangum import Mangum

from auth_service import app as auth_app
from orchestrator import app as orch_app
from research1 import app as research_app
from writer2 import app as writer_app
from analyst3 import app as analyst_app

app = FastAPI(title="Agent Marketplace", version="1.0.0", docs_url=None, redoc_url=None)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Agent microservices (path-based routing for Vercel)
app.mount("/agents/research", research_app)
app.mount("/agents/writer", writer_app)
app.mount("/agents/analyst", analyst_app)

# Auth routes (real handlers)
for route in auth_app.routes:
    app.routes.append(route)

# Orchestrator routes (skip /auth/* proxies — auth_app already serves them)
for route in orch_app.routes:
    path = getattr(route, "path", "") or ""
    if path.startswith("/auth"):
        continue
    app.routes.append(route)


@app.get("/health")
async def health():
    return {"status": "ok", "platform": "vercel"}


handler = Mangum(app, lifespan="off")
