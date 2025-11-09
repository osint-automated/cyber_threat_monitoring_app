import streamlit as st
from pygooglenews import GoogleNews
import pandas as pd
from datetime import datetime, timedelta
from bs4 import BeautifulSoup
import dateparser

# Function to clean HTML content
def clean(t): 
    return BeautifulSoup(t or "", "html.parser").get_text().strip()

# Function to parse dates
def date(i):
    for a in ["published_parsed", "updated_parsed", "published", "updated"]:
        v = getattr(i, a, None)
        if not v: continue
        if "parsed" in a: return datetime(*v[:6])
        d = dateparser.parse(v)
        if d: return d

# Custom sidebar header with branding and styling
st.sidebar.markdown("""
    <style>
        .sidebar .sidebar-content {
            background-color: #f0f2f6;  /* Light background color for sidebar */
        }
        .sidebar .sidebar-header {
            font-size: 24px;
            color: #4CAF50;  /* Green color for header */
            font-weight: bold;
        }
        .sidebar .sidebar-subheader {
            font-size: 18px;
            color: #2E8B57;  /* Darker green for subsections */
        }
    </style>
    """, unsafe_allow_html=True)

# Sidebar title and introduction
st.sidebar.title("Cyber Threat Monitoring App")

# --- Page functions ---

# Home Page
def home_page():
    st.title("Cyber Threat Monitoring App")
    
    # Introduction to the app
    st.write("""
    This app allows you to monitor and explore various types of **cyber threats** that organizations and individuals face daily. 
    With the increasing frequency of cyberattacks, it’s essential to stay informed and take proactive measures to protect sensitive data.
    
    In this app, you can explore the latest news and incidents related to a variety of cyber threats, such as:
    - **APT Campaigns** (Advanced Persistent Threats)
    - **Data Breaches**
    - **Malware Events**
    - **Ransomware Attacks**
    - **Social Engineering Campaigns**
    - **Influence Operations** (e.g., disinformation campaigns)

    You can search for information based on specific sectors (e.g., healthcare, finance, government, etc.), allowing you to focus on the industries most relevant to you.
    """)

    # Overview of each page
    st.write("### How to Use This App")
    st.write("""
    - **Step 1**: Use the **sidebar on the left** to navigate to different pages.
    - **Step 2**: Each page allows you to search for recent incidents related to a specific cyber threat (e.g., APT campaigns, ransomware, etc.).
    - **Step 3**: On each page, you can input a **sector or keyword** (e.g., government, media, education, finance, Russia, etc.) to filter the results.
    - **Step 4**: View the search results, and you can **download them as a CSV file** for further analysis.
    
    This app sources information from recent news articles to ensure you have the latest data available.
    """)

    # Detailed description of each type of threat
    st.write("### What Are These Cyber Threats?")
    
    st.write("""
    - **APT Campaigns**: These are targeted, long-term cyberattacks by sophisticated groups. They are designed to infiltrate specific organizations to steal data, disrupt operations, or gain espionage access. The app helps you track the latest APT campaigns that have been reported in the media.
    
    - **Data Breaches**: A data breach occurs when sensitive, confidential data is exposed to unauthorized individuals. These breaches can have devastating effects on organizations, leading to reputational damage and financial loss. You can search for the most recent breaches in various sectors.
    
    - **Malware Events**: Malware includes viruses, worms, ransomware, and other malicious software designed to damage systems, steal information, or disrupt operations. This page lets you track malware incidents impacting various sectors.
    
    - **Ransomware Attacks**: Ransomware is a type of malware that locks or encrypts a victim's data and demands a ransom for its release. The app lets you track these attacks across industries, giving you insight into which sectors are targeted.
    
    - **Social Engineering Campaigns**: These attacks manipulate individuals into divulging confidential information or performing actions that harm them or their organization. They are often carried out through phishing, pretexting, or baiting. This page provides the latest data on social engineering attacks.
    
    - **Influence Operations**: Influence operations often involve the use of disinformation, fake news, or other forms of psychological manipulation to affect public opinion or sway elections. The app tracks these operations in various sectors such as politics, media, and government.
    """)

# APT Campaign Search
def apt_campaign_search():
    st.title("APT Campaign Search")
    
    # Explanation for users
    st.write("""
    **Advanced Persistent Threat (APT)** campaigns refer to long-term, targeted cyber-attacks aimed at stealing sensitive information or disrupting operations. 
    These attacks are typically carried out by well-funded and organized groups with specific objectives.
    
    In this page, you can search for recent news about APT campaigns by entering a sector (e.g., healthcare, finance, government, etc.). 
    The results will show articles related to APT campaigns affecting the sector you specify.
    
    To use this page:
    1. Enter the sector or term of interest in the text box below (e.g., healthcare, Lazaraus Group, etc.).
    2. Click the "Search" button to display the latest APT-related news articles for that sector.
    3. You can download the results as a CSV file for further analysis.
    """)
    
    sector = st.text_input("Enter a sector (e.g., healthcare, Lazaraus Group, etc.):")
    
    if st.button("Search") and sector:
        results = search_apt_campaign(sector)
        if results.empty:
            st.write("No results found.")
        else:
            st.dataframe(results, hide_index=True)
            st.download_button("Download CSV", results.to_csv(index=False), f"{sector}_apt_campaigns.csv")

def search_apt_campaign(sector):
    query = f'(intitle:"APT" OR "advanced persistent threat" OR "APT campaign" AND "cyber espionage" OR "cyber threat" OR "nation-state" OR "state-sponsored" OR "cyber operation") {sector}'
    cut = datetime.now() - timedelta(days=90)
    results = []
    for item in GoogleNews(lang="en").search(query).get("entries", []):
        publish_date = date(item)
        if publish_date and publish_date < cut: continue
        results.append({
            "Date": publish_date.date() if publish_date else None,
            "Title": getattr(item, "title", ""),
            "Link": getattr(item, "link", "")
        })
    return pd.DataFrame(results).sort_values("Date", ascending=False) if results else pd.DataFrame()

# Data Breach Search
def data_breach_search():
    st.title("Data Breach Search")
    
    # Explanation for users
    st.write("""
    A **data breach** occurs when unauthorized individuals gain access to sensitive data, often for malicious purposes. This can involve leaking personal information, credit card details, or proprietary business data.
    
    In this page, you can search for recent data breaches related to a specific sector or industry. By entering a sector (e.g., "healthcare", "finance"), 
    the app will display recent news articles on breaches in that sector.
    
    To use this page:
    1. Enter the sector you're interested in.
    2. Click "Search" to view the most recent data breach incidents.
    3. Download the results as a CSV file for your reference.
    """)
    
    sector = st.text_input("Enter a sector (e.g., healthcare, finance, etc.):")
    
    if st.button("Search") and sector:
        results = search_data_breach(sector)
        if results.empty:
            st.write("No results found.")
        else:
            st.dataframe(results, hide_index=True)
            st.download_button("Download CSV", results.to_csv(index=False), f"{sector}_data_breaches.csv")

def search_data_breach(sector):
    query = f'(intitle:"data breach" OR "data leak" AND "data exposure" OR "credential leak" OR "data compromise" OR "data theft" OR "data dump" OR "leaked database") {sector}'
    cut = datetime.now() - timedelta(days=90)
    results = []
    for item in GoogleNews(lang="en").search(query).get("entries", []):
        publish_date = date(item)
        if publish_date and publish_date < cut: continue
        results.append({
            "Date": publish_date.date() if publish_date else None,
            "Title": getattr(item, "title", ""),
            "Link": getattr(item, "link", "")
        })
    return pd.DataFrame(results).sort_values("Date", ascending=False) if results else pd.DataFrame()

# Influence Operations Search
def influence_ops_search():
    st.title("Influence Operations Search")
    
    # Explanation for users
    st.write("""
    **Influence operations** refer to activities carried out by governments, organizations, or individuals to sway public opinion or political outcomes, often through disinformation or propaganda.
    
    This page allows you to search for news articles related to influence operations and disinformation campaigns that target specific sectors or topics.
    
    To use this page:
    1. Enter a sector or keyword related to influence operations (e.g., government, media, Russia, etc.).
    2. Click "Search" to view results for the most recent news articles.
    3. Download the search results as a CSV file for further analysis.
    """)
    
    sector = st.text_input("Enter a sector or entity (e.g., government, media, Russia, etc.):")
    
    if st.button("Search") and sector:
        results = search_influence_ops(sector)
        if results.empty:
            st.write("No results found.")
        else:
            st.dataframe(results, hide_index=True)
            st.download_button("Download CSV", results.to_csv(index=False), f"{sector}_influence_ops.csv")

def search_influence_ops(sector):
    query = f'(intitle:"influence operations" OR "disinformation campaign" OR "information operation" OR "propganda" OR "government influence" OR "foreign influence") {sector}'
    cut = datetime.now() - timedelta(days=90)
    results = []
    for item in GoogleNews(lang="en").search(query).get("entries", []):
        publish_date = date(item)
        if publish_date and publish_date < cut: continue
        results.append({
            "Date": publish_date.date() if publish_date else None,
            "Title": getattr(item, "title", ""),
            "Link": getattr(item, "link", "")
        })
    return pd.DataFrame(results).sort_values("Date", ascending=False) if results else pd.DataFrame()

# Malware Events Search
def malware_events_search():
    st.title("Malware Events Search")
    
    # Explanation for users
    st.write("""
    **Malware** refers to malicious software designed to disrupt, damage, or gain unauthorized access to a computer system. This page allows you to search for news articles related to recent malware attacks or campaigns.
    
    You can filter the results by entering a sector (e.g., "healthcare", "finance"), and the app will show you relevant incidents.
    
    To use this page:
    1. Enter the sector or keyword you're interested in (e.g., government, finance, Russia, etc.).
    2. Click "Search" to view recent malware events for that sector.
    3. Download the results as a CSV file for later analysis.
    """)
    
    sector = st.text_input("Enter a sector (e.g., healthcare, finance, etc.):")
    
    if st.button("Search") and sector:
        results = search_malware_events(sector)
        if results.empty:
            st.write("No results found.")
        else:
            st.dataframe(results, hide_index=True)
            st.download_button("Download CSV", results.to_csv(index=False), f"{sector}_malware_events.csv")

def search_malware_events(sector):
    query = f'(intitle:"malware" AND "malware campaign" OR "botnet activity" OR "trojan" OR RAT OR "malicious payload" OR "malware distribution" OR "malicious software") {sector}'
    cut = datetime.now() - timedelta(days=90)
    results = []
    for item in GoogleNews(lang="en").search(query).get("entries", []):
        publish_date = date(item)
        if publish_date and publish_date < cut: continue
        results.append({
            "Date": publish_date.date() if publish_date else None,
            "Title": getattr(item, "title", ""),
            "Link": getattr(item, "link", "")
        })
    return pd.DataFrame(results).sort_values("Date", ascending=False) if results else pd.DataFrame()

# Ransomware Events Search
def ransomware_events_search():
    st.title("Ransomware Events Search")
    
    # Explanation for users
    st.write("""
    **Ransomware attacks** involve malicious software that locks or encrypts a victim’s data and demands payment for its release. 
    In this page, you can search for recent ransomware events affecting various sectors.
    
    To use this page:
    1. Enter the sector or keyword you're interested in (e.g., government, finance, Qilin Ransomware, etc.).
    2. Click "Search" to see recent ransomware attacks.
    3. You can download the results as a CSV for further analysis.
    """)
    
    sector = st.text_input("Enter a sector (e.g., healthcare, finance, etc.):")
    
    if st.button("Search") and sector:
        results = search_ransomware_events(sector)
        if results.empty:
            st.write("No results found.")
        else:
            st.dataframe(results, hide_index=True)
            st.download_button("Download CSV", results.to_csv(index=False), f"{sector}_ransomware_events.csv")

def search_ransomware_events(sector):
    query = f'(intitle:"ransomware" OR "ransomware attack" AND "ransomware incident" OR "ransomware group" OR "ransomware campaign" OR "cyber extortion" OR "ransomware") {sector}'
    cut = datetime.now() - timedelta(days=90)
    results = []
    for item in GoogleNews(lang="en").search(query).get("entries", []):
        publish_date = date(item)
        if publish_date and publish_date < cut: continue
        results.append({
            "Date": publish_date.date() if publish_date else None,
            "Title": getattr(item, "title", ""),
            "Link": getattr(item, "link", "")
        })
    return pd.DataFrame(results).sort_values("Date", ascending=False) if results else pd.DataFrame()

# Social Engineering Campaign Search
def social_engineering_campaign_search():
    st.title("Social Engineering Campaign Search")
    
    # Explanation for users
    st.write("""
    **Social engineering** refers to psychological manipulation of people into performing actions or divulging confidential information. 
    This page allows you to search for social engineering campaigns such as phishing or fraud.
    
    To use this page:
    1. Enter the sector or keyword you're interested in (e.g., government, finance, Russia, etc.).
    2. Click "Search" to view results related to social engineering campaigns targeting that sector.
    3. Download the results as a CSV for further review.
    """)
    
    sector = st.text_input("Enter a sector (e.g., finance, government, etc.):")
    
    if st.button("Search") and sector:
        results = search_social_engineering_campaign(sector)
        if results.empty:
            st.write("No results found.")
        else:
            st.dataframe(results, hide_index=True)
            st.download_button("Download CSV", results.to_csv(index=False), f"{sector}_social_engineering_campaigns.csv")

def search_social_engineering_campaign(sector):
    query = f'(intitle:"social engineering" OR "phishing" AND "social engineering attack" OR "phishing scam" OR "impersonation scam" OR "email fraud" OR "cyber fraud" OR deception" OR "fraud campaign") {sector}'
    cut = datetime.now() - timedelta(days=90)
    results = []
    for item in GoogleNews(lang="en").search(query).get("entries", []):
        publish_date = date(item)
        if publish_date and publish_date < cut: continue
        results.append({
            "Date": publish_date.date() if publish_date else None,
            "Title": getattr(item, "title", ""),
            "Link": getattr(item, "link", "")
        })
    return pd.DataFrame(results).sort_values("Date", ascending=False) if results else pd.DataFrame()

# --- Main App Logic ---
# Sidebar navigation using st.radio
page = st.sidebar.radio("Select a page", [
    "Home",
    "APT Campaign Search", 
    "Data Breach Search", 
    "Influence Ops Search", 
    "Malware Events Search", 
    "Ransomware Events Search", 
    "Social Engineering Campaign Search"
])

# Display content based on the selected page
if page == "Home":
    home_page()
elif page == "APT Campaign Search":
    apt_campaign_search()
elif page == "Data Breach Search":
    data_breach_search()
elif page == "Influence Ops Search":
    influence_ops_search()
elif page == "Malware Events Search":
    malware_events_search()
elif page == "Ransomware Events Search":
    ransomware_events_search()
elif page == "Social Engineering Campaign Search":
    social_engineering_campaign_search()
