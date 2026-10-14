
import streamlit as st
import pandas as pd
import gspread
from google.oauth2.service_account import Credentials

st.set_page_config(
    page_title="GymRevive",
    page_icon="💪",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---------- DESIGN ----------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&display=swap');

.stApp {
    background: #101410;
    color: #F1F5EF;
    font-family: 'DM Sans', sans-serif;
}
[data-testid="stSidebar"] {
    background: #171D18;
    border-right: 1px solid #293329;
}
.block-container {
    padding-top: 2rem;
    padding-bottom: 3rem;
    max-width: 1400px;
}
h1, h2, h3, p, label {
    color: #F1F5EF;
}
[data-testid="stMetric"] {
    background: #1B231C;
    border: 1px solid #303B30;
    padding: 20px 22px;
    border-radius: 14px;
}
[data-testid="stMetricLabel"] {
    color: #A5B2A3;
}
[data-testid="stMetricValue"] {
    color: #D0FA78;
}
div[data-testid="stDataFrame"] {
    border: 1px solid #303B30;
    border-radius: 12px;
    overflow: hidden;
}
.stTextInput input, .stSelectbox div[data-baseweb="select"] {
    background: #1B231C;
}
hr {
    border-color: #303B30;
}
.small-muted {
    color: #A5B2A3;
    font-size: 13px;
}
.section-title {
    font-size: 19px;
    font-weight: 700;
    color: #F1F5EF;
    margin-bottom: 4px;
}
.brand {
    font-size: 25px;
    font-weight: 700;
    color: #D0FA78;
    letter-spacing: -1px;
}
</style>
""", unsafe_allow_html=True)

# ---------- GOOGLE SHEETS CONNECTION ----------
@st.cache_data(ttl=60)
def load_members():
    scopes = [
        "https://www.googleapis.com/auth/spreadsheets.readonly",
        "https://www.googleapis.com/auth/drive.readonly"
    ]

    credentials = Credentials.from_service_account_file(
        "credentials.json",
        scopes=scopes
    )

    client = gspread.authorize(credentials)
    spreadsheet = client.open("Members")
    worksheet = spreadsheet.worksheet("Sheet1")

    records = worksheet.get_all_records()
    return pd.DataFrame(records)

try:
    members = load_members()
    st.sidebar.success("Google Sheets connected")
except Exception as e:
    st.error("Could not connect to Google Sheets.")
    st.code(str(e))
    st.stop()

# Convert inactivity values to numbers
members["Days Inactive"] = (
    pd.Timestamp.now().normalize()
    - pd.to_datetime(members["last_visit"], errors="coerce").dt.normalize()
).dt.days

# Adapt your existing column names to the dashboard
members = members.rename(columns={
    "name": "Name",
    "days_inactive": "Days Inactive",
    "last_message_sent": "Last Message"
})

if "Status" not in members.columns:
    members["Status"] = "Active"

members["Last Message"] = members.get(
    "Last Message", pd.Series("", index=members.index)
).fillna("").replace("", "Not contacted")

today = pd.Timestamp.now().normalize()

members["Last Message"] = pd.to_datetime(
    members["Last Message"], errors="coerce", utc=True
)

members["Days Since Message"] = (
    pd.Timestamp.now(tz="UTC") - members["Last Message"]
).dt.days

members["Status"] = members.apply(
    lambda row: "Follow-up due"
    if row["Days Inactive"] >= 14
    and (
        pd.isna(row["Last Message"])
        or row["Days Since Message"] >= 7
    )
    else "Recently contacted"
    if row["Days Inactive"] >= 14
    else "Active",
    axis=1
)


# ---------- SIDEBAR ----------
with st.sidebar:
    st.markdown('<div class="brand">✳ GymRevive</div>',
                unsafe_allow_html=True)
    st.caption("RETENTION INTELLIGENCE")
    st.divider()

    page = st.radio(
        "WORKSPACE",
        ["Overview", "Members", "Campaigns"],
        label_visibility="visible"
    )

    st.divider()
    st.markdown("**Automation status**")
    st.markdown("🟢  n8n workflow configured")
    st.markdown("🟢  WhatsApp integration configured")
    st.markdown("🟢  AI message generation configured")

    st.divider()
    st.caption("PORTFOLIO DEMO · SAMPLE DATA")

# ---------- HEADER ----------
left, right = st.columns([4, 1])

with left:
    st.markdown(f"# {page}")
    st.markdown(
        '<p class="small-muted">Keep members engaged. '
        'Catch drop-offs before they become cancellations.</p>',
        unsafe_allow_html=True
    )

with right:
    st.write("")
    st.write("")
    st.button("↻ Refresh", use_container_width=True,
              on_click=lambda: st.rerun())

st.divider()

# ---------- OVERVIEW ----------
if page == "Overview":

    
    inactive = int((members["Days Inactive"] >= 14).sum())

    contacted = int(
        (
            members["Last Message"].notna()
            & (members["Days Since Message"] >= 0)
            & (members["Days Since Message"] < 30)
        ).sum()
    )

    followups = int((members["Status"] == "Follow-up due").sum())


    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Members tracked", len(members))
    c2.metric("Members at risk", inactive)
    c3.metric("Recently contacted", contacted)
    c4.metric("Follow-ups due", followups)

    st.write("")
    chart_col, summary_col = st.columns([1.6, 1])

    with chart_col:
        st.markdown(
            '<div class="section-title">Member inactivity</div>',
            unsafe_allow_html=True
        )
        st.caption("How recently members have visited")
        chart_data = pd.DataFrame({
            "Inactivity range": ["0–6 days", "7–13 days",
                                 "14–20 days", "21+ days"],
            "Members": [
                int((members["Days Inactive"] < 7).sum()),
                int(((members["Days Inactive"] >= 7) &
                     (members["Days Inactive"] < 14)).sum()),
                int(((members["Days Inactive"] >= 14) &
                     (members["Days Inactive"] < 21)).sum()),
                int((members["Days Inactive"] >= 21).sum())
            ]
        }).set_index("Inactivity range")
        st.bar_chart(chart_data, color="#D0FA78", height=250)

    with summary_col:
        st.markdown(
            '<div class="section-title">Retention snapshot</div>',
            unsafe_allow_html=True
        )
        st.caption("Live Member Data")
        st.write("Members requiring follow-up")
        st.progress(followups / max(len(members), 1))
        st.write(f"**{followups}** members need attention")
        st.divider()
        st.write("Members already contacted")
        st.progress(contacted / max(len(members), 1))
        st.write(f"**{contacted}** members have a message record")

    st.write("")
    st.markdown(
        '<div class="section-title">Members needing attention</div>',
        unsafe_allow_html=True
    )
    at_risk = members[members["Days Inactive"] >= 14].copy()
    st.dataframe(
        at_risk,
        use_container_width=True,
        hide_index=True
    )

# ---------- MEMBERS ----------
elif page == "Members":

    search = st.text_input("Search by member name", placeholder="Type a name...")
    status_options = ["All statuses"] + sorted(members["Status"].unique().tolist())
    status_filter = st.selectbox("Member status", status_options)

    filtered = members[
        members["Name"].str.contains(search, case=False, na=False)
    ]

    if status_filter != "All statuses":
        filtered = filtered[filtered["Status"] == status_filter]

    st.caption(f"{len(filtered)} member(s) found")
    st.dataframe(
        filtered,
        use_container_width=True,
        hide_index=True
    )

# ---------- CAMPAIGNS ----------
elif page == "Campaigns":

    st.markdown("### Outreach activity")
    st.caption("Review message activity from the sample dataset.")

    sent = members[members["Last Message"] != "Not contacted"]
    not_sent = members[members["Last Message"] == "Not contacted"]

    a, b = st.columns(2)
    a.metric("Contacted members", len(sent))
    b.metric("Not yet contacted", len(not_sent))

    st.markdown("#### Contact history")
    st.dataframe(sent, use_container_width=True, hide_index=True)

    st.markdown("#### Awaiting outreach")
    st.dataframe(not_sent, use_container_width=True, hide_index=True)

# ---------- FOOTER ----------
st.divider()
st.caption(
    "GymRevive · Gym member retention prototype · "
    "connected to google sheets. · Retention metrics based on current member records."
)
