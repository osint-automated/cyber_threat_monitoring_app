import streamlit as st
import pandas as pd
import requests
from datetime import datetime
import os

st.set_page_config(page_title="Cyber Threat Monitoring App", page_icon=":shield:")

# --------------------------
# NewsAPI Configuration
# --------------------------
NEWSAPI_KEY = st.secrets["newsapi"]["api_key"]
BASE_URL = "https://newsapi.org/v2/everything"

# --------------------------
# Helper Functions
# --------------------------
def fetch_news(query, page_size=50):
    """Fetch news articles from NewsAPI and return a DataFrame."""
    params = {
        "q": query,
        "language": "en",
        "pageSize": page_size,
        "sortBy": "publishedAt",
        "apiKey": NEWSAPI_KEY
    }
    try:
        response = requests.get(BASE_URL, params=params)
        response.raise_for_status()
        data = response.json()
        if data.get("status") != "ok":
            st.error(f"NewsAPI error: {data.get('message')}")
            return pd.DataFrame(columns=["Date", "Title", "Link", "Source"])
        articles = data.get("articles", [])
        results = []
        for art in articles:
            results.append({
                "Date": datetime.strptime(art["publishedAt"], "%Y-%m-%dT%H:%M:%SZ").date(),
                "Title": art["title"],
                "Link": art["url"],
                "Source": art["source"]["name"]
            })
        return pd.DataFrame(results)
    except requests.exceptions.RequestException as e:
        st.error(f"Network error: {e}")
        return pd.DataFrame(columns=["Date", "Title", "Link", "Source"])

# --------------------------
# Sidebar & Styling
# --------------------------
st.sidebar.markdown("""
<style>
.sidebar .sidebar-content { background-color: #f0f2f6; }
.sidebar .sidebar-header { font-size: 24px; color: #4CAF50; font-weight: bold; }
.sidebar .sidebar-subheader { font-size: 18px; color: #2E8B57; }
</style>
""", unsafe_allow_html=True)

st.sidebar.title("Cyber Threat Monitoring App")

# --------------------------
# Home Page
# --------------------------
def home_page():
    st.title("Cyber Threat Monitoring App")
    st.markdown("""
Welcome to the **Cyber Threat Monitoring App**!  
This application allows you to monitor and explore a variety of cyber threats affecting organizations and individuals worldwide.

You can explore the latest news for:

- **APT Campaigns** (Advanced Persistent Threats)
- **Data Breaches**
- **Malware Events**
- **Ransomware Attacks**
- **Social Engineering Campaigns**
- **Influence Operations** (e.g., disinformation campaigns)

### How to Use This App
1. Use the **sidebar** to navigate between different pages.
2. Each page allows you to search for recent incidents related to a specific cyber threat.
3. Enter a **sector, organization, or keyword** (e.g., healthcare, government, Russia) to filter results.
4. View the results and **download them as CSV** for further analysis.

### Understanding Cyber Threats
- **APT Campaigns**: Targeted, long-term attacks by sophisticated groups aimed at stealing data or disrupting operations.
- **Data Breaches**: Unauthorized access to sensitive data leading to exposure of personal or corporate information.
- **Malware Events**: Malicious software attacks (viruses, worms, trojans) designed to compromise systems or data.
- **Ransomware Attacks**: Malware that encrypts a victim's data and demands ransom for its release.
- **Social Engineering Campaigns**: Psychological manipulation attacks like phishing or fraud targeting individuals or organizations.
- **Influence Operations**: Disinformation campaigns or propaganda aimed at influencing public opinion or decision-making.
""", unsafe_allow_html=True)

# --------------------------
# Page Functions
# --------------------------
def apt_campaign_search():
    st.title("APT Campaign Search")
    st.markdown("""
**Advanced Persistent Threat (APT) campaigns** refer to long-term, targeted cyber-attacks by sophisticated groups.  
These attacks are aimed at stealing sensitive information or disrupting operations.

**How to use this page:**
1. Enter a sector or keyword (e.g., healthcare, Lazarus Group) below.
2. Click "Search" to view recent APT-related news.
3. Download results as CSV for further analysis.
""", unsafe_allow_html=True)
    sector = st.text_input("Enter a sector or keyword:")
    if st.button("Search") and sector:
        query = f'(APT OR "advanced persistent threat" OR "cyber espionage" OR "state-sponsored") AND ("{sector}")'
        results = fetch_news(query)
        if results.empty:
            st.write("No results found.")
        else:
            st.dataframe(results, hide_index=True)
            st.download_button("Download CSV", results.to_csv(index=False), f"{sector}_apt_campaigns.csv")

def data_breach_search():
    st.title("Data Breach Search")
    st.markdown("""
**Data breaches** occur when sensitive information is accessed by unauthorized individuals.  
They can involve leaked personal information, credit card details, or corporate data.

**How to use this page:**
1. Enter a sector or keyword (e.g., healthcare, finance) below.
2. Click "Search" to view recent data breach news.
3. Download results as CSV for further analysis.
""", unsafe_allow_html=True)
    sector = st.text_input("Enter a sector or keyword:")
    if st.button("Search") and sector:
        query = f'("data breach" OR "data leak" OR "data exposure") AND ("{sector}")'
        results = fetch_news(query)
        if results.empty:
            st.write("No results found.")
        else:
            st.dataframe(results, hide_index=True)
            st.download_button("Download CSV", results.to_csv(index=False), f"{sector}_data_breaches.csv")

def malware_events_search():
    st.title("Malware Events Search")
    st.markdown("""
**Malware** refers to malicious software designed to disrupt or compromise systems.  

**How to use this page:**
1. Enter a sector or keyword below.
2. Click "Search" to view recent malware events.
3. Download results as CSV for analysis.
""", unsafe_allow_html=True)
    sector = st.text_input("Enter a sector or keyword:")
    if st.button("Search") and sector:
        query = f'(malware OR botnet OR trojan OR RAT OR "remote access trojan") AND ("{sector}")'
        results = fetch_news(query)
        if results.empty:
            st.write("No results found.")
        else:
            st.dataframe(results, hide_index=True)
            st.download_button("Download CSV", results.to_csv(index=False), f"{sector}_malware_events.csv")

def ransomware_events_search():
    st.title("Ransomware Events Search")
    st.markdown("""
**Ransomware** encrypts victim data and demands a ransom.  

**How to use this page:**
1. Enter a sector or keyword below.
2. Click "Search" to see recent ransomware attacks.
3. Download results as CSV.
""", unsafe_allow_html=True)
    sector = st.text_input("Enter a sector or keyword:")
    if st.button("Search") and sector:
        query = f'(ransomware OR "ransomware attack" OR "ransomware incident") AND ("{sector}")'
        results = fetch_news(query)
        if results.empty:
            st.write("No results found.")
        else:
            st.dataframe(results, hide_index=True)
            st.download_button("Download CSV", results.to_csv(index=False), f"{sector}_ransomware_events.csv")

def social_engineering_campaign_search():
    st.title("Social Engineering Campaign Search")
    st.markdown("""
**Social engineering** involves manipulating individuals to disclose sensitive information or perform harmful actions.  

**How to use this page:**
1. Enter a sector or keyword below.
2. Click "Search" to view recent phishing or fraud campaigns.
3. Download results as CSV.
""", unsafe_allow_html=True)
    sector = st.text_input("Enter a sector or keyword:")
    if st.button("Search") and sector:
        query = f'(phishing OR "social engineering" OR fraud OR "credential theft") AND ("{sector}")'
        results = fetch_news(query)
        if results.empty:
            st.write("No results found.")
        else:
            st.dataframe(results, hide_index=True)
            st.download_button("Download CSV", results.to_csv(index=False), f"{sector}_social_engineering_campaigns.csv")

def influence_ops_search():
    st.title("Influence Operations Search")
    st.markdown("""
**Influence operations** are campaigns designed to sway public opinion or decision-making, often via disinformation.  

**How to use this page:**
1. Enter a sector or keyword below.
2. Click "Search" to view recent influence operations.
3. Download results as CSV.
""", unsafe_allow_html=True)
    sector = st.text_input("Enter a sector or keyword:")
    if st.button("Search") and sector:
        query = f'(disinformation OR propaganda OR "influence operation" OR "information warfare") AND ("{sector}")'
        results = fetch_news(query)
        if results.empty:
            st.write("No results found.")
        else:
            st.dataframe(results, hide_index=True)
            st.download_button("Download CSV", results.to_csv(index=False), f"{sector}_influence_ops.csv")

# --------------------------
# Main App Logic
# --------------------------
page = st.sidebar.radio("Select a page", [
    "Home",
    "APT Campaign Search",
    "Data Breach Search",
    "Malware Events Search",
    "Ransomware Events Search",
    "Social Engineering Campaign Search",
    "Influence Ops Search"
])

if page == "Home":
    home_page()
elif page == "APT Campaign Search":
    apt_campaign_search()
elif page == "Data Breach Search":
    data_breach_search()
elif page == "Malware Events Search":
    malware_events_search()
elif page == "Ransomware Events Search":
    ransomware_events_search()
elif page == "Social Engineering Campaign Search":
    social_engineering_campaign_search()
elif page == "Influence Ops Search":
    influence_ops_search()
