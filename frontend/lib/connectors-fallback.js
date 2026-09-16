// Auto-generated from backend/app/services/connectors_catalog.py — offline fallback for static hosting.
export const CONNECTORS_FALLBACK = [
 {
  "section": "Popular",
  "connectors": [
   {
    "id": "gmail-calendar",
    "label": "Gmail with Calendar",
    "auth": "oauth",
    "desc": "Search inbox + calendar, draft replies, schedule events.",
    "actions": [
     "search_emails",
     "list_events",
     "send_email",
     "create_event"
    ],
    "key_hint": "Google OAuth client (or app password for demo)"
   },
   {
    "id": "outlook",
    "label": "Outlook",
    "auth": "oauth",
    "desc": "Search Outlook mail + calendar, send mail, manage meetings.",
    "actions": [
     "search_emails",
     "list_events",
     "send_email"
    ],
    "key_hint": "Microsoft Graph OAuth token"
   },
   {
    "id": "hubspot",
    "label": "HubSpot",
    "auth": "api_key",
    "desc": "Query CRM contacts, companies, deals in natural language.",
    "actions": [
     "search_contacts",
     "search_companies",
     "search_deals",
     "create_contact"
    ],
    "key_hint": "HubSpot private app token"
   },
   {
    "id": "mailchimp",
    "label": "Intuit Mailchimp",
    "auth": "api_key",
    "desc": "Audiences, campaigns, open/click performance.",
    "actions": [
     "list_audiences",
     "list_campaigns",
     "campaign_stats"
    ],
    "key_hint": "Mailchimp API key + server prefix"
   },
   {
    "id": "monday",
    "label": "Monday.com",
    "auth": "api_key",
    "desc": "Boards, items, timelines and workload queries.",
    "actions": [
     "list_boards",
     "search_items",
     "create_item"
    ],
    "key_hint": "Monday.com API token"
   },
   {
    "id": "supabase",
    "label": "Supabase",
    "auth": "api_key",
    "desc": "Query Postgres tables, auth users, storage buckets.",
    "actions": [
     "list_tables",
     "query_table",
     "storage_list"
    ],
    "key_hint": "Supabase project URL + anon/service key"
   }
  ]
 },
 {
  "section": "Developer",
  "connectors": [
   {
    "id": "supabase",
    "label": "Supabase",
    "auth": "api_key",
    "desc": "Query Postgres tables, auth users, storage buckets.",
    "actions": [
     "list_tables",
     "query_table",
     "storage_list"
    ],
    "key_hint": "Supabase project URL + anon/service key"
   },
   {
    "id": "neon",
    "label": "Neon",
    "auth": "api_key",
    "desc": "Serverless Postgres branches, databases, query stats.",
    "actions": [
     "list_projects",
     "list_branches",
     "query_stats"
    ],
    "key_hint": "Neon API key"
   },
   {
    "id": "stytch",
    "label": "Stytch",
    "auth": "api_key",
    "desc": "Users, sessions, OTP / magic-link auth events.",
    "actions": [
     "search_users",
     "list_sessions"
    ],
    "key_hint": "Stytch project ID + secret"
   },
   {
    "id": "jam",
    "label": "Jam",
    "auth": "api_key",
    "desc": "Bug reports with replay, console + network capture.",
    "actions": [
     "list_reports",
     "search_reports"
    ],
    "key_hint": "Jam API token"
   },
   {
    "id": "datadog",
    "label": "Datadog",
    "auth": "api_key",
    "desc": "Monitors, incidents, logs and APM traces.",
    "actions": [
     "list_monitors",
     "search_logs",
     "list_incidents"
    ],
    "key_hint": "Datadog API + app keys"
   },
   {
    "id": "doordash-drive",
    "label": "DoorDash Drive",
    "auth": "api_key",
    "desc": "Create/track deliveries, quotes and driver status.",
    "actions": [
     "create_delivery",
     "track_delivery",
     "get_quote"
    ],
    "key_hint": "DoorDash developer credentials"
   },
   {
    "id": "huggingface",
    "label": "Hugging Face",
    "auth": "api_key",
    "desc": "Models, datasets and Spaces search + inference.",
    "actions": [
     "search_models",
     "search_datasets",
     "model_info"
    ],
    "key_hint": "HF token (read)"
   },
   {
    "id": "github",
    "label": "GitHub",
    "auth": "api_key",
    "desc": "Repos, issues, PRs and code search.",
    "actions": [
     "search_repos",
     "search_issues",
     "list_prs"
    ],
    "key_hint": "GitHub personal token"
   }
  ]
 },
 {
  "section": "Productivity",
  "connectors": [
   {
    "id": "gmail-calendar",
    "label": "Gmail with Calendar",
    "auth": "oauth",
    "desc": "Search inbox + calendar, draft replies, schedule events.",
    "actions": [
     "search_emails",
     "list_events",
     "send_email",
     "create_event"
    ],
    "key_hint": "Google OAuth client (or app password for demo)"
   },
   {
    "id": "todoist",
    "label": "Todoist",
    "auth": "api_key",
    "desc": "Tasks, projects, filters and productivity stats.",
    "actions": [
     "list_tasks",
     "search_tasks",
     "create_task"
    ],
    "key_hint": "Todoist API token"
   },
   {
    "id": "calcom",
    "label": "Cal.com",
    "auth": "api_key",
    "desc": "Event types, bookings, availability.",
    "actions": [
     "list_event_types",
     "list_bookings",
     "check_availability"
    ],
    "key_hint": "Cal.com API key"
   },
   {
    "id": "metaview",
    "label": "Metaview",
    "auth": "api_key",
    "desc": "Interview notes, summaries and hiring signals.",
    "actions": [
     "search_notes",
     "get_summary"
    ],
    "key_hint": "Metaview API key"
   },
   {
    "id": "circleback",
    "label": "Circleback",
    "auth": "api_key",
    "desc": "Meeting transcripts, action items, follow-ups.",
    "actions": [
     "search_meetings",
     "list_action_items"
    ],
    "key_hint": "Circleback API key"
   },
   {
    "id": "evernote",
    "label": "Evernote",
    "auth": "oauth",
    "desc": "Search notes, notebooks and clipped research.",
    "actions": [
     "search_notes",
     "list_notebooks"
    ],
    "key_hint": "Evernote OAuth token"
   },
   {
    "id": "slack",
    "label": "Slack",
    "auth": "oauth",
    "desc": "Search messages, channels and summaries.",
    "actions": [
     "search_messages",
     "list_channels"
    ],
    "key_hint": "Slack bot/user OAuth token"
   },
   {
    "id": "notion",
    "label": "Notion",
    "auth": "api_key",
    "desc": "Pages, databases and wiki search.",
    "actions": [
     "search_pages",
     "query_database"
    ],
    "key_hint": "Notion integration token"
   }
  ]
 },
 {
  "section": "Data & Analytics",
  "connectors": [
   {
    "id": "unwrap",
    "label": "Unwrap",
    "auth": "api_key",
    "desc": "Customer feedback themes and sentiment.",
    "actions": [
     "search_feedback",
     "list_themes"
    ],
    "key_hint": "Unwrap API key"
   },
   {
    "id": "clickup",
    "label": "ClickUp",
    "auth": "api_key",
    "desc": "Tasks, docs, goals and marketing pipeline.",
    "actions": [
     "search_tasks",
     "list_docs",
     "create_task"
    ],
    "key_hint": "ClickUp personal token"
   },
   {
    "id": "cb-insights",
    "label": "CB Insights (Self-Licensed)",
    "auth": "api_key",
    "desc": "Company, market and funding intelligence (your license).",
    "actions": [
     "search_companies",
     "market_stats"
    ],
    "key_hint": "Bring your own CB Insights license"
   },
   {
    "id": "similarweb",
    "label": "Similarweb",
    "auth": "api_key",
    "desc": "Traffic, engagement and competitor benchmarks.",
    "actions": [
     "site_stats",
     "compare_sites"
    ],
    "key_hint": "Similarweb API key"
   },
   {
    "id": "amplitude",
    "label": "Amplitude",
    "auth": "api_key",
    "desc": "Events, funnels, retention and cohorts.",
    "actions": [
     "funnel_stats",
     "search_events",
     "retention"
    ],
    "key_hint": "Amplitude API + secret keys"
   },
   {
    "id": "prisma-postgres",
    "label": "Prisma Postgres",
    "auth": "api_key",
    "desc": "Query your Prisma-managed Postgres directly.",
    "actions": [
     "list_tables",
     "query_table"
    ],
    "key_hint": "Prisma Postgres connection string"
   }
  ]
 },
 {
  "section": "Operations",
  "connectors": [
   {
    "id": "monday",
    "label": "Monday.com",
    "auth": "api_key",
    "desc": "Boards, items, timelines and workload queries.",
    "actions": [
     "list_boards",
     "search_items",
     "create_item"
    ],
    "key_hint": "Monday.com API token"
   },
   {
    "id": "atlassian",
    "label": "Atlassian",
    "auth": "api_key",
    "desc": "Jira issues + Confluence pages in one search.",
    "actions": [
     "search_issues",
     "search_pages",
     "create_issue"
    ],
    "key_hint": "Atlassian API token + email + domain"
   },
   {
    "id": "ticket-tailor",
    "label": "Ticket Tailor",
    "auth": "api_key",
    "desc": "Events, ticket sales and attendee lists.",
    "actions": [
     "list_events",
     "ticket_stats",
     "search_orders"
    ],
    "key_hint": "Ticket Tailor API key"
   },
   {
    "id": "shopify",
    "label": "Shopify",
    "auth": "api_key",
    "desc": "Orders, products, customers and refunds.",
    "actions": [
     "search_orders",
     "search_products",
     "order_stats"
    ],
    "key_hint": "Shopify Admin API token + store domain"
   },
   {
    "id": "smartsheet",
    "label": "Smartsheet",
    "auth": "api_key",
    "desc": "Sheets, rows, reports and update requests.",
    "actions": [
     "list_sheets",
     "search_rows"
    ],
    "key_hint": "Smartsheet token"
   },
   {
    "id": "carta",
    "label": "Carta",
    "auth": "api_key",
    "desc": "Cap table, valuations and stakeholder holdings.",
    "actions": [
     "cap_table",
     "list_stakeholders"
    ],
    "key_hint": "Carta API credentials"
   }
  ]
 },
 {
  "section": "Sales & Marketing",
  "connectors": [
   {
    "id": "hubspot",
    "label": "HubSpot",
    "auth": "api_key",
    "desc": "Query CRM contacts, companies, deals in natural language.",
    "actions": [
     "search_contacts",
     "search_companies",
     "search_deals",
     "create_contact"
    ],
    "key_hint": "HubSpot private app token"
   },
   {
    "id": "mailchimp",
    "label": "Intuit Mailchimp",
    "auth": "api_key",
    "desc": "Audiences, campaigns, open/click performance.",
    "actions": [
     "list_audiences",
     "list_campaigns",
     "campaign_stats"
    ],
    "key_hint": "Mailchimp API key + server prefix"
   },
   {
    "id": "clickup",
    "label": "ClickUp",
    "auth": "api_key",
    "desc": "Tasks, docs, goals and marketing pipeline.",
    "actions": [
     "search_tasks",
     "list_docs",
     "create_task"
    ],
    "key_hint": "ClickUp personal token"
   },
   {
    "id": "apollo",
    "label": "Apollo.io",
    "auth": "api_key",
    "desc": "People/company enrichment and sequences.",
    "actions": [
     "search_people",
     "enrich_company"
    ],
    "key_hint": "Apollo API key"
   },
   {
    "id": "klaviyo",
    "label": "Klaviyo",
    "auth": "api_key",
    "desc": "Flows, campaigns, segments and revenue.",
    "actions": [
     "list_flows",
     "campaign_stats",
     "search_profiles"
    ],
    "key_hint": "Klaviyo private key"
   },
   {
    "id": "airops",
    "label": "AirOps",
    "auth": "api_key",
    "desc": "Content workflows, briefs and SEO runs.",
    "actions": [
     "list_workflows",
     "run_status"
    ],
    "key_hint": "AirOps API key"
   }
  ]
 },
 {
  "section": "Creative",
  "connectors": [
   {
    "id": "lucid",
    "label": "Lucid",
    "auth": "oauth",
    "desc": "Lucidchart + Lucidspark boards and diagrams.",
    "actions": [
     "list_documents",
     "search_documents"
    ],
    "key_hint": "Lucid OAuth"
   },
   {
    "id": "whimsical",
    "label": "Whimsical",
    "auth": "api_key",
    "desc": "Boards, wireframes and mind maps.",
    "actions": [
     "list_boards",
     "search_boards"
    ],
    "key_hint": "Whimsical API token"
   },
   {
    "id": "biorender",
    "label": "BioRender",
    "auth": "api_key",
    "desc": "Scientific figures and templates.",
    "actions": [
     "search_figures",
     "list_templates"
    ],
    "key_hint": "BioRender token"
   },
   {
    "id": "figma",
    "label": "Figma",
    "auth": "api_key",
    "desc": "Files, components, comments and versions.",
    "actions": [
     "list_files",
     "search_components",
     "list_comments"
    ],
    "key_hint": "Figma personal token"
   },
   {
    "id": "twitch",
    "label": "Twitch",
    "auth": "oauth",
    "desc": "Channels, clips, VODs and stream stats.",
    "actions": [
     "search_channels",
     "top_clips",
     "stream_stats"
    ],
    "key_hint": "Twitch OAuth (client ID + token)"
   },
   {
    "id": "canva",
    "label": "Canva Enterprise",
    "auth": "oauth",
    "desc": "Brand designs, folders and team templates.",
    "actions": [
     "search_designs",
     "list_folders"
    ],
    "key_hint": "Canva Enterprise OAuth"
   }
  ]
 },
 {
  "section": "Finance",
  "connectors": [
   {
    "id": "ibisworld",
    "label": "IBISWorld",
    "auth": "api_key",
    "desc": "Industry reports, risk and outlook data.",
    "actions": [
     "industry_report",
     "search_industries"
    ],
    "key_hint": "IBISWorld credentials"
   },
   {
    "id": "carbon-arc",
    "label": "Carbon Arc",
    "auth": "api_key",
    "desc": "Alternative datasets and market signals.",
    "actions": [
     "search_datasets",
     "dataset_stats"
    ],
    "key_hint": "Carbon Arc API key"
   },
   {
    "id": "link-money",
    "label": "Link",
    "auth": "api_key",
    "desc": "Payments, payouts and transaction lookup.",
    "actions": [
     "list_payments",
     "payment_stats"
    ],
    "key_hint": "Link API credentials"
   },
   {
    "id": "angellist",
    "label": "AngelList",
    "auth": "api_key",
    "desc": "Startups, funds, talent and deal flow.",
    "actions": [
     "search_startups",
     "list_jobs"
    ],
    "key_hint": "AngelList API token"
   },
   {
    "id": "ibkr",
    "label": "Interactive Brokers (IBKR)",
    "auth": "api_key",
    "desc": "Portfolio, positions, orders and market data.",
    "actions": [
     "portfolio",
     "search_contract",
     "market_snapshot"
    ],
    "key_hint": "IBKR Client Portal Gateway"
   },
   {
    "id": "dnb",
    "label": "D&B Commercial Graph",
    "auth": "api_key",
    "desc": "Company graph, risk scores and hierarchies.",
    "actions": [
     "company_lookup",
     "risk_score"
    ],
    "key_hint": "D&B API credentials"
   }
  ]
 },
 {
  "section": "New",
  "connectors": [
   {
    "id": "evernote",
    "label": "Evernote",
    "auth": "oauth",
    "desc": "Search notes, notebooks and clipped research.",
    "actions": [
     "search_notes",
     "list_notebooks"
    ],
    "key_hint": "Evernote OAuth token"
   },
   {
    "id": "finary",
    "label": "Finary",
    "auth": "api_key",
    "desc": "Portfolio tracking across accounts.",
    "actions": [
     "portfolio",
     "holdings"
    ],
    "key_hint": "Finary API token"
   },
   {
    "id": "higgsfield",
    "label": "Higgsfield",
    "auth": "api_key",
    "desc": "Generative video scenes and jobs.",
    "actions": [
     "list_jobs",
     "create_scene"
    ],
    "key_hint": "Higgsfield API key"
   },
   {
    "id": "rings-ai",
    "label": "Rings AI",
    "auth": "api_key",
    "desc": "AI call intelligence and summaries.",
    "actions": [
     "search_calls",
     "call_summary"
    ],
    "key_hint": "Rings AI key"
   },
   {
    "id": "aries",
    "label": "Aries",
    "auth": "api_key",
    "desc": "Workflow runs and automation status.",
    "actions": [
     "list_runs",
     "run_status"
    ],
    "key_hint": "Aries API key"
   },
   {
    "id": "quantwheel",
    "label": "QuantWheel",
    "auth": "api_key",
    "desc": "Quant backtests and factor stats.",
    "actions": [
     "list_backtests",
     "factor_stats"
    ],
    "key_hint": "QuantWheel key"
   }
  ]
 },
 {
  "section": "Health",
  "connectors": [
   {
    "id": "function-health",
    "label": "Function Health",
    "auth": "oauth",
    "desc": "Biomarker panels, trends and clinician notes.",
    "actions": [
     "list_biomarkers",
     "biomarker_trend"
    ],
    "key_hint": "Function Health OAuth"
   },
   {
    "id": "medical-records",
    "label": "Medical Records",
    "auth": "file",
    "desc": "Search your uploaded clinical records privately.",
    "actions": [
     "search_records",
     "list_documents"
    ],
    "key_hint": "Upload via chat (FHIR/CCDA/PDF)"
   },
   {
    "id": "health-apps",
    "label": "Health and Fitness Apps",
    "auth": "oauth",
    "desc": "Steps, sleep, workouts and recovery trends.",
    "actions": [
     "daily_stats",
     "list_workouts",
     "sleep_trend"
    ],
    "key_hint": "Apple Health / Google Fit / wearables OAuth"
   },
   {
    "id": "benchling",
    "label": "Benchling",
    "auth": "api_key",
    "desc": "Sequences, notebooks and registry entries.",
    "actions": [
     "search_sequences",
     "search_notebooks"
    ],
    "key_hint": "Benchling API key + tenant"
   }
  ]
 }
];
