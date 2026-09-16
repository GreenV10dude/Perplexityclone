"""Full connector catalog — every plugin from the product screenshots, grouped by section.

Sections: Popular, Developer, Productivity, Data & Analytics, Operations,
Sales & Marketing, Creative, Finance, New, Health.

Auth kinds: oauth (connect via provider OAuth), api_key (paste a token),
mcp (point at a Model Context Protocol server URL), file (local/CSV upload).
Without credentials every connector runs in clearly-labeled demo mode.
"""
from __future__ import annotations

SECTIONS = ["Popular", "Developer", "Productivity", "Data & Analytics",
            "Operations", "Sales & Marketing", "Creative", "Finance", "New", "Health"]

# id, label, sections, auth, key_hint, description, actions
CONNECTORS = [
    # ---- Popular ----
    {"id": "gmail-calendar", "label": "Gmail with Calendar", "sections": ["Popular", "Productivity"], "auth": "oauth",
     "key_hint": "Google OAuth client (or app password for demo)",
     "desc": "Search inbox + calendar, draft replies, schedule events.",
     "actions": ["search_emails", "list_events", "send_email", "create_event"]},
    {"id": "outlook", "label": "Outlook", "sections": ["Popular"], "auth": "oauth",
     "key_hint": "Microsoft Graph OAuth token",
     "desc": "Search Outlook mail + calendar, send mail, manage meetings.",
     "actions": ["search_emails", "list_events", "send_email"]},
    {"id": "hubspot", "label": "HubSpot", "sections": ["Popular", "Sales & Marketing"], "auth": "api_key",
     "key_hint": "HubSpot private app token",
     "desc": "Query CRM contacts, companies, deals in natural language.",
     "actions": ["search_contacts", "search_companies", "search_deals", "create_contact"]},
    {"id": "mailchimp", "label": "Intuit Mailchimp", "sections": ["Popular", "Sales & Marketing"], "auth": "api_key",
     "key_hint": "Mailchimp API key + server prefix",
     "desc": "Audiences, campaigns, open/click performance.",
     "actions": ["list_audiences", "list_campaigns", "campaign_stats"]},
    {"id": "monday", "label": "Monday.com", "sections": ["Popular", "Operations"], "auth": "api_key",
     "key_hint": "Monday.com API token",
     "desc": "Boards, items, timelines and workload queries.",
     "actions": ["list_boards", "search_items", "create_item"]},
    {"id": "supabase", "label": "Supabase", "sections": ["Popular", "Developer"], "auth": "api_key",
     "key_hint": "Supabase project URL + anon/service key",
     "desc": "Query Postgres tables, auth users, storage buckets.",
     "actions": ["list_tables", "query_table", "storage_list"]},
    # ---- Developer ----
    {"id": "neon", "label": "Neon", "sections": ["Developer"], "auth": "api_key",
     "key_hint": "Neon API key",
     "desc": "Serverless Postgres branches, databases, query stats.",
     "actions": ["list_projects", "list_branches", "query_stats"]},
    {"id": "stytch", "label": "Stytch", "sections": ["Developer"], "auth": "api_key",
     "key_hint": "Stytch project ID + secret",
     "desc": "Users, sessions, OTP / magic-link auth events.",
     "actions": ["search_users", "list_sessions"]},
    {"id": "jam", "label": "Jam", "sections": ["Developer"], "auth": "api_key",
     "key_hint": "Jam API token",
     "desc": "Bug reports with replay, console + network capture.",
     "actions": ["list_reports", "search_reports"]},
    {"id": "datadog", "label": "Datadog", "sections": ["Developer"], "auth": "api_key",
     "key_hint": "Datadog API + app keys",
     "desc": "Monitors, incidents, logs and APM traces.",
     "actions": ["list_monitors", "search_logs", "list_incidents"]},
    {"id": "doordash-drive", "label": "DoorDash Drive", "sections": ["Developer"], "auth": "api_key",
     "key_hint": "DoorDash developer credentials",
     "desc": "Create/track deliveries, quotes and driver status.",
     "actions": ["create_delivery", "track_delivery", "get_quote"]},
    # ---- Productivity ----
    {"id": "todoist", "label": "Todoist", "sections": ["Productivity"], "auth": "api_key",
     "key_hint": "Todoist API token",
     "desc": "Tasks, projects, filters and productivity stats.",
     "actions": ["list_tasks", "search_tasks", "create_task"]},
    {"id": "calcom", "label": "Cal.com", "sections": ["Productivity"], "auth": "api_key",
     "key_hint": "Cal.com API key",
     "desc": "Event types, bookings, availability.",
     "actions": ["list_event_types", "list_bookings", "check_availability"]},
    {"id": "metaview", "label": "Metaview", "sections": ["Productivity"], "auth": "api_key",
     "key_hint": "Metaview API key",
     "desc": "Interview notes, summaries and hiring signals.",
     "actions": ["search_notes", "get_summary"]},
    {"id": "circleback", "label": "Circleback", "sections": ["Productivity"], "auth": "api_key",
     "key_hint": "Circleback API key",
     "desc": "Meeting transcripts, action items, follow-ups.",
     "actions": ["search_meetings", "list_action_items"]},
    {"id": "evernote", "label": "Evernote", "sections": ["Productivity", "New"], "auth": "oauth",
     "key_hint": "Evernote OAuth token",
     "desc": "Search notes, notebooks and clipped research.",
     "actions": ["search_notes", "list_notebooks"]},
    # ---- Data & Analytics ----
    {"id": "unwrap", "label": "Unwrap", "sections": ["Data & Analytics"], "auth": "api_key",
     "key_hint": "Unwrap API key",
     "desc": "Customer feedback themes and sentiment.",
     "actions": ["search_feedback", "list_themes"]},
    {"id": "clickup", "label": "ClickUp", "sections": ["Data & Analytics", "Sales & Marketing"], "auth": "api_key",
     "key_hint": "ClickUp personal token",
     "desc": "Tasks, docs, goals and marketing pipeline.",
     "actions": ["search_tasks", "list_docs", "create_task"]},
    {"id": "cb-insights", "label": "CB Insights (Self-Licensed)", "sections": ["Data & Analytics"], "auth": "api_key",
     "key_hint": "Bring your own CB Insights license",
     "desc": "Company, market and funding intelligence (your license).",
     "actions": ["search_companies", "market_stats"]},
    {"id": "similarweb", "label": "Similarweb", "sections": ["Data & Analytics"], "auth": "api_key",
     "key_hint": "Similarweb API key",
     "desc": "Traffic, engagement and competitor benchmarks.",
     "actions": ["site_stats", "compare_sites"]},
    {"id": "amplitude", "label": "Amplitude", "sections": ["Data & Analytics"], "auth": "api_key",
     "key_hint": "Amplitude API + secret keys",
     "desc": "Events, funnels, retention and cohorts.",
     "actions": ["funnel_stats", "search_events", "retention"]},
    {"id": "prisma-postgres", "label": "Prisma Postgres", "sections": ["Data & Analytics"], "auth": "api_key",
     "key_hint": "Prisma Postgres connection string",
     "desc": "Query your Prisma-managed Postgres directly.",
     "actions": ["list_tables", "query_table"]},
    # ---- Operations ----
    {"id": "atlassian", "label": "Atlassian", "sections": ["Operations"], "auth": "api_key",
     "key_hint": "Atlassian API token + email + domain",
     "desc": "Jira issues + Confluence pages in one search.",
     "actions": ["search_issues", "search_pages", "create_issue"]},
    {"id": "ticket-tailor", "label": "Ticket Tailor", "sections": ["Operations"], "auth": "api_key",
     "key_hint": "Ticket Tailor API key",
     "desc": "Events, ticket sales and attendee lists.",
     "actions": ["list_events", "ticket_stats", "search_orders"]},
    {"id": "shopify", "label": "Shopify", "sections": ["Operations"], "auth": "api_key",
     "key_hint": "Shopify Admin API token + store domain",
     "desc": "Orders, products, customers and refunds.",
     "actions": ["search_orders", "search_products", "order_stats"]},
    {"id": "smartsheet", "label": "Smartsheet", "sections": ["Operations"], "auth": "api_key",
     "key_hint": "Smartsheet token",
     "desc": "Sheets, rows, reports and update requests.",
     "actions": ["list_sheets", "search_rows"]},
    {"id": "carta", "label": "Carta", "sections": ["Operations"], "auth": "api_key",
     "key_hint": "Carta API credentials",
     "desc": "Cap table, valuations and stakeholder holdings.",
     "actions": ["cap_table", "list_stakeholders"]},
    # ---- Sales & Marketing ----
    {"id": "apollo", "label": "Apollo.io", "sections": ["Sales & Marketing"], "auth": "api_key",
     "key_hint": "Apollo API key",
     "desc": "People/company enrichment and sequences.",
     "actions": ["search_people", "enrich_company"]},
    {"id": "klaviyo", "label": "Klaviyo", "sections": ["Sales & Marketing"], "auth": "api_key",
     "key_hint": "Klaviyo private key",
     "desc": "Flows, campaigns, segments and revenue.",
     "actions": ["list_flows", "campaign_stats", "search_profiles"]},
    {"id": "airops", "label": "AirOps", "sections": ["Sales & Marketing"], "auth": "api_key",
     "key_hint": "AirOps API key",
     "desc": "Content workflows, briefs and SEO runs.",
     "actions": ["list_workflows", "run_status"]},
    # ---- Creative ----
    {"id": "lucid", "label": "Lucid", "sections": ["Creative"], "auth": "oauth",
     "key_hint": "Lucid OAuth",
     "desc": "Lucidchart + Lucidspark boards and diagrams.",
     "actions": ["list_documents", "search_documents"]},
    {"id": "whimsical", "label": "Whimsical", "sections": ["Creative"], "auth": "api_key",
     "key_hint": "Whimsical API token",
     "desc": "Boards, wireframes and mind maps.",
     "actions": ["list_boards", "search_boards"]},
    {"id": "biorender", "label": "BioRender", "sections": ["Creative"], "auth": "api_key",
     "key_hint": "BioRender token",
     "desc": "Scientific figures and templates.",
     "actions": ["search_figures", "list_templates"]},
    {"id": "figma", "label": "Figma", "sections": ["Creative"], "auth": "api_key",
     "key_hint": "Figma personal token",
     "desc": "Files, components, comments and versions.",
     "actions": ["list_files", "search_components", "list_comments"]},
    {"id": "twitch", "label": "Twitch", "sections": ["Creative"], "auth": "oauth",
     "key_hint": "Twitch OAuth (client ID + token)",
     "desc": "Channels, clips, VODs and stream stats.",
     "actions": ["search_channels", "top_clips", "stream_stats"]},
    {"id": "canva", "label": "Canva Enterprise", "sections": ["Creative"], "auth": "oauth",
     "key_hint": "Canva Enterprise OAuth",
     "desc": "Brand designs, folders and team templates.",
     "actions": ["search_designs", "list_folders"]},
    # ---- Finance ----
    {"id": "ibisworld", "label": "IBISWorld", "sections": ["Finance"], "auth": "api_key",
     "key_hint": "IBISWorld credentials",
     "desc": "Industry reports, risk and outlook data.",
     "actions": ["industry_report", "search_industries"]},
    {"id": "carbon-arc", "label": "Carbon Arc", "sections": ["Finance"], "auth": "api_key",
     "key_hint": "Carbon Arc API key",
     "desc": "Alternative datasets and market signals.",
     "actions": ["search_datasets", "dataset_stats"]},
    {"id": "link-money", "label": "Link", "sections": ["Finance"], "auth": "api_key",
     "key_hint": "Link API credentials",
     "desc": "Payments, payouts and transaction lookup.",
     "actions": ["list_payments", "payment_stats"]},
    {"id": "angellist", "label": "AngelList", "sections": ["Finance"], "auth": "api_key",
     "key_hint": "AngelList API token",
     "desc": "Startups, funds, talent and deal flow.",
     "actions": ["search_startups", "list_jobs"]},
    {"id": "ibkr", "label": "Interactive Brokers (IBKR)", "sections": ["Finance"], "auth": "api_key",
     "key_hint": "IBKR Client Portal Gateway",
     "desc": "Portfolio, positions, orders and market data.",
     "actions": ["portfolio", "search_contract", "market_snapshot"]},
    {"id": "dnb", "label": "D&B Commercial Graph", "sections": ["Finance"], "auth": "api_key",
     "key_hint": "D&B API credentials",
     "desc": "Company graph, risk scores and hierarchies.",
     "actions": ["company_lookup", "risk_score"]},
    # ---- New ----
    {"id": "finary", "label": "Finary", "sections": ["New"], "auth": "api_key",
     "key_hint": "Finary API token",
     "desc": "Portfolio tracking across accounts.",
     "actions": ["portfolio", "holdings"]},
    {"id": "higgsfield", "label": "Higgsfield", "sections": ["New"], "auth": "api_key",
     "key_hint": "Higgsfield API key",
     "desc": "Generative video scenes and jobs.",
     "actions": ["list_jobs", "create_scene"]},
    {"id": "rings-ai", "label": "Rings AI", "sections": ["New"], "auth": "api_key",
     "key_hint": "Rings AI key",
     "desc": "AI call intelligence and summaries.",
     "actions": ["search_calls", "call_summary"]},
    {"id": "aries", "label": "Aries", "sections": ["New"], "auth": "api_key",
     "key_hint": "Aries API key",
     "desc": "Workflow runs and automation status.",
     "actions": ["list_runs", "run_status"]},
    {"id": "quantwheel", "label": "QuantWheel", "sections": ["New"], "auth": "api_key",
     "key_hint": "QuantWheel key",
     "desc": "Quant backtests and factor stats.",
     "actions": ["list_backtests", "factor_stats"]},
    # ---- Health ----
    {"id": "function-health", "label": "Function Health", "sections": ["Health"], "auth": "oauth",
     "key_hint": "Function Health OAuth",
     "desc": "Biomarker panels, trends and clinician notes.",
     "actions": ["list_biomarkers", "biomarker_trend"]},
    {"id": "medical-records", "label": "Medical Records", "sections": ["Health"], "auth": "file",
     "key_hint": "Upload via chat (FHIR/CCDA/PDF)",
     "desc": "Search your uploaded clinical records privately.",
     "actions": ["search_records", "list_documents"]},
    {"id": "health-apps", "label": "Health and Fitness Apps", "sections": ["Health"], "auth": "oauth",
     "key_hint": "Apple Health / Google Fit / wearables OAuth",
     "desc": "Steps, sleep, workouts and recovery trends.",
     "actions": ["daily_stats", "list_workouts", "sleep_trend"]},
    {"id": "benchling", "label": "Benchling", "sections": ["Health"], "auth": "api_key",
     "key_hint": "Benchling API key + tenant",
     "desc": "Sequences, notebooks and registry entries.",
     "actions": ["search_sequences", "search_notebooks"]},
    # ---- Extras (requested earlier, kept working) ----
    {"id": "huggingface", "label": "Hugging Face", "sections": ["Developer"], "auth": "api_key",
     "key_hint": "HF token (read)",
     "desc": "Models, datasets and Spaces search + inference.",
     "actions": ["search_models", "search_datasets", "model_info"]},
    {"id": "github", "label": "GitHub", "sections": ["Developer"], "auth": "api_key",
     "key_hint": "GitHub personal token",
     "desc": "Repos, issues, PRs and code search.",
     "actions": ["search_repos", "search_issues", "list_prs"]},
    {"id": "slack", "label": "Slack", "sections": ["Productivity"], "auth": "oauth",
     "key_hint": "Slack bot/user OAuth token",
     "desc": "Search messages, channels and summaries.",
     "actions": ["search_messages", "list_channels"]},
    {"id": "notion", "label": "Notion", "sections": ["Productivity"], "auth": "api_key",
     "key_hint": "Notion integration token",
     "desc": "Pages, databases and wiki search.",
     "actions": ["search_pages", "query_database"]},
]

BY_ID = {c["id"]: c for c in CONNECTORS}


def grouped() -> list[dict]:
    """Catalog grouped in SECTIONS order for the UI."""
    out = []
    for s in SECTIONS:
        items = [c for c in CONNECTORS if s in c["sections"]]
        if items:
            out.append({"section": s, "connectors": items})
    return out


def connector_context(ids: list[str]) -> str:
    """Short prompt note so the LLM actually uses linked apps."""
    ids = [i for i in (ids or []) if i in BY_ID]
    if not ids:
        return ""
    lines = ["Connected apps (user-linked; use their actions when relevant, say when using demo data):"]
    for i in ids:
        c = BY_ID[i]
        lines.append(f"- {c['label']}: {', '.join(c['actions'][:4])}")
    return "\n".join(lines)


async def execute(connector_id: str, action: str, params: dict | None = None,
                  credential: str = "", mcp_url: str = "") -> dict:
    """Run a connector action.

    - If an MCP server URL is supplied, proxy the call there (real integration path).
    - Else return clearly-labeled demo data shaped like the real response.
    """
    params = params or {}
    c = BY_ID.get(connector_id)
    if not c:
        return {"ok": False, "error": f"unknown connector '{connector_id}'"}
    if action not in c["actions"]:
        return {"ok": False, "error": f"unknown action '{action}' for {c['label']}",
                "actions": c["actions"]}

    if mcp_url:
        try:
            import httpx
            async with httpx.AsyncClient(timeout=15.0) as client:
                r = await client.post(mcp_url, json={
                    "connector": connector_id, "action": action, "params": params,
                    "credential": bool(credential),
                })
                r.raise_for_status()
                return {"ok": True, "demo": False, "connector": connector_id,
                        "action": action, "result": r.json()}
        except Exception as e:
            return {"ok": True, "demo": True, "connector": connector_id, "action": action,
                    "warning": f"MCP call failed ({e}); showing demo data.",
                    "result": _demo(connector_id, action, params)}

    if credential:
        # No per-vendor secrets stored server-side in this build; credentials stay
        # in the browser. We still shape a live-looking response and mark the path.
        return {"ok": True, "demo": True, "connector": connector_id, "action": action,
                "warning": "Credential received client-side only; vendor call runs in a full deployment. Showing demo-shaped data.",
                "result": _demo(connector_id, action, params)}

    return {"ok": True, "demo": True, "connector": connector_id, "action": action,
            "result": _demo(connector_id, action, params)}


def _demo(connector_id: str, action: str, params: dict) -> dict:
    q = str(params.get("query") or params.get("q") or "demo")
    if action.startswith("search") or action.startswith("list") or action.startswith("top"):
        return {"items": [
            {"name": f"{connector_id} result 1 for '{q}'", "id": "demo-1", "updated": "2026-09-01"},
            {"name": f"{connector_id} result 2 for '{q}'", "id": "demo-2", "updated": "2026-08-28"},
            {"name": f"{connector_id} result 3 for '{q}'", "id": "demo-3", "updated": "2026-08-20"},
        ], "count": 3}
    if action.startswith("create") or action.startswith("send"):
        return {"created": True, "id": "demo-new-1", "echo": params}
    if "stat" in action or "trend" in action or "portfolio" in action or "retention" in action:
        return {"period": "last_30d", "series": [12, 19, 15, 24, 31, 28, 36], "summary": f"Demo {action} for {connector_id}"}
    return {"action": action, "params": params, "note": f"Demo {action} on {connector_id}"}
