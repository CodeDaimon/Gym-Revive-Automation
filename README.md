
# GymRevive — AI Gym Retention Automation

An automation project that helps gyms identify inactive members and send personalized WhatsApp comeback messages.

## Features
- Detects members inactive for 14+ days
- Generates personalized messages using Ollama (Llama 3.2)
- Sends WhatsApp template messages through Meta Cloud API
- Enforces a 7-day contact cooldown
- Updates member records in Google Sheets
- Streamlit dashboard for member monitoring and retention metrics

## Tech Stack
- n8n — workflow automation
- Ollama — local AI message generation
- Meta WhatsApp Cloud API — messaging
- Google Sheets — member database
- Python and Streamlit — dashboard

## How It Works
Google Sheets → n8n inactivity checks → Ollama message generation → WhatsApp → Google Sheets update → Streamlit dashboard

## Setup
1. Install Python 3.13+.
2. Install dependencies:
   `python -m pip install streamlit pandas gspread google-auth`
3. Configure Google service-account credentials locally.
4. Configure n8n, Ollama, and Meta WhatsApp Cloud API.
5. Run the dashboard:
   `python -m streamlit run app.py`
## Screenshots

### Dashboard
dashboard1.png

### n8n Automation Workflow
screenshots/n8nworkflow.png

## Security
Never commit credentials, API tokens, private keys, or real member personal data.

## 🚀 Future Improvements

**Campaign Analytics** — Track messages sent, delivery status, and member responses.
**Automated Membership Renewal Reminders** — Notify members before their memberships expire.
**Referral System** — Encourage existing members to invite friends with referral offers.
**Member Retention Insights** — Identify inactivity patterns and members at risk of dropping out.
**Gym Management Dashboard** — Add search, filters, and improved campaign reporting.
**Error Handling & Retry Logic** — Make workflows more reliable when APIs or services fail.
**Production Deployment** — Deploy the application for access beyond the local machine.
**Multi-Gym Support** — Allow multiple gyms to manage their own member data and campaigns.

*These features are planned and may change as the project evolves.*
