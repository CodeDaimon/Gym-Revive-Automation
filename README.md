
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

## Security
Never commit credentials, API tokens, private keys, or real member personal data.

## Current Status
Portfolio prototype tested with sample member records and Meta WhatsApp test setup. Not yet deployed for a real gym.
