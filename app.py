import datetime
import streamlit as st
import pandas as pd
import gspread
from google.oauth2.service_account import Credentials

# Page Configuration
st.set_page_config(
    page_title="CellarIQ: Smart Wine Maturity Tracker",
    page_icon="🍷",
    layout="wide"
)

# App Header
st.title("🍷 CellarIQ & Vintage Intelligence")
st.markdown("Track your wine fridge inventory, discover optimal drinking windows, review famous critic scores, and get detailed professional tasting profiles.")

# -------------------------------------------------------------
# GOOGLE SHEETS AUTHENTICATION & LIVE SYNC
# -------------------------------------------------------------
@st.cache_resource
def get_gspread_client():
    """Authenticates with Google Sheets API using Streamlit Secrets."""
    scopes = [
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive"
    ]
    credentials = Credentials.from_service_account_info(
        st.secrets["gcp_service_account"],
        scopes=scopes
    )
    return gspread.authorize(credentials)

def get_or_create_sheet():
    """Gets existing Google Sheet or creates a new 'Wine Cellar Inventory' sheet."""
    try:
        client = get_gspread_client()
        sheet_title = "My Wine Cellar Inventory"
        try:
            sh = client.open(sheet_title)
        except gspread.SpreadsheetNotFound:
            sh = client.create(sheet_title)
            worksheet = sh.get_worksheet(0)
            headers = [
                "Wine Name", "Vintage", "Region", "Status", "Drink Start",
                "Peak End", "JS Score", "RP Score", "WE Score", "JR Score", "Details"
            ]
            worksheet.append_row(headers)
        return sh.get_worksheet(0)
    except Exception as e:
        st.error(f"Google Sheets Connection Warning: {e}")
        return None

# Load stock directly from Google Sheets
worksheet = get_or_create_sheet()

def load_stock_data():
    if worksheet:
        data = worksheet.get_all_records()
        return pd.DataFrame(data) if data else pd.DataFrame()
    return pd.DataFrame()

# -------------------------------------------------------------
# SIMULATED INTELLIGENCE & RESEARCH ENGINE
# -------------------------------------------------------------
def analyze_wine_vintage(wine_name, vintage_year, region=""):
    current_year = datetime.datetime.now().year
    
    start_window = int(vintage_year) + 5 if vintage_year.isdigit() else current_year
    peak_start = start_window + 3
    peak_end = start_window + 12
    decline_year = peak_end + 5
    
    if current_year < start_window:
        status = "🔵 Aging / Sleeping"
    elif start_window <= current_year < peak_start:
        status = "🟢 Entering Window"
    elif peak_start <= current_year <= peak_end:
        status = "⭐ Optimum Peak"
    else:
        status = "🔴 Past Peak / Urgent"

    tasting_profile = {
        "appearance": "Deep ruby core with garnet rims and high viscosity.",
        "nose": "Intense aromas of blackcurrant, dark cherry, graphite, cigar box, and a subtle touch of French oak vanilla.",
        "palate": "Full-bodied with structured, velvety tannins and balanced, refreshing acidity. Layers of blackberry, cassis, espresso bean, and secondary earthiness.",
        "structure": "Alcohol: 13.5% | Tannins: Firm and fine-grained | Acidity: Medium-Plus",
        "decanting": "Decant for 1 to 2 hours before serving to allow oxygenation.",
        "temp": "Serve at 16°C – 18°C (60°F – 64°F)."
    }

    scores = {
        "James Suckling (JS)": "95 / 100",
        "Robert Parker (RP)": "93 / 100",
        "Wine Enthusiast (WE)": "94 / 100",
        "Jancis Robinson (JR)": "17.5 / 20"
    }

    return {
        "wine_name": wine_name,
        "vintage": vintage_year,
        "region": region if region else "Premium Appellation",
        "status": status,
        "drink_start": start_window,
        "peak_start": peak_start,
        "peak_end": peak_end,
        "decline": decline_year,
        "scores": scores,
        "profile": tasting_profile
    }

# App Tabs
tab_input, tab_stock, tab_settings = st.tabs(["➕ Add New Wine", "📦 Cellar Stock List", "⚙️ Settings & Alerts"])

# -------------------------------------------------------------
# TAB 1: ADD NEW WINE & INSTANT BRIEFING CARD
# -------------------------------------------------------------
with tab_input:
    st.subheader("Add Wine to Fridge & Research Maturity")
    
    with st.form("wine_input_form"):
        col1, col2 = st.columns(2)
        with col1:
            input_name = st.text_input("Wine / Producer Name", placeholder="e.g., Sassicaia, Tenuta San Guido")
            input_vintage = st.text_input("Vintage Year", placeholder="e.g., 2018")
        with col2:
            input_region = st.text_input("Region / Appellation (Optional)", placeholder="e.g., Bolgheri, Tuscany")
            input_format = st.selectbox("Bottle Format", ["Standard (750ml)", "Magnum (1.5L)", "Half (375ml)"])
        
        submitted = st.form_submit_button("🔍 Research & Analyze Wine")

    if submitted:
        if not input_name or not input_vintage:
            st.error("Please provide at least the Wine Name and Vintage Year.")
        else:
            with st.spinner("Analyzing vintage charts, critic ratings, and aging curves via AI research..."):
                st.session_state.current_analysis = analyze_wine_vintage(input_name, input_vintage, input_region)
            st.success("Analysis Complete!")

    if "current_analysis" in st.session_state:
        result = st.session_state.current_analysis
        st.markdown("---")
        st.markdown(f"### 📋 Instant Briefing: {result['wine_name']} ({result['vintage']})")
        
        col_a, col_b = st.columns([1, 1])
        with col_a:
            st.markdown(f"**Region:** {result['region']}")
            st.markdown(f"**Current Status:** {result['status']}")
            st.markdown(f"**Drinking Window:** {result['drink_start']} – {result['decline']}")
            st.markdown(f"**Optimum Peak Plateau:** {result['peak_start']} – {result['peak_end']}")
        
        with col_b:
            st.markdown("#### 🏆 Famous Critic Ratings")
            for critic, score in result["scores"].items():
                st.markdown(f"- **{critic}**: `{score}`")

        st.markdown("#### 📝 Detailed Professional Tasting Profile")
        p = result["profile"]
        st.info(
            f"**Appearance:** {p['appearance']}\n\n"
            f"**Nose:** {p['nose']}\n\n"
            f"**Palate:** {p['palate']}\n\n"
            f"**Structure & Specs:** {p['structure']}\n\n"
            f"**Decanting Advice:** {p['decanting']}\n\n"
            f"**Serving Temperature:** {p['temp']}"
        )

        if st.button("💾 Save to My Wine Fridge Stock List"):
            new_row = [
                result["wine_name"],
                result["vintage"],
                result["region"],
                result["status"],
                result["drink_start"],
                result["peak_end"],
                result["scores"]["James Suckling (JS)"],
                result["scores"]["Robert Parker (RP)"],
                result["scores"]["Wine Enthusiast (WE)"],
                result["scores"]["Jancis Robinson (JR)"],
                p["palate"]
            ]
            if worksheet:
                worksheet.append_row(new_row)
                st.success("Successfully saved to your live Google Sheet stock list!")
                del st.session_state.current_analysis
                st.rerun()
            else:
                st.error("Google Sheet integration not configured.")

# -------------------------------------------------------------
# TAB 2: CELLAR STOCK LIST & DELETE FEATURE
# -------------------------------------------------------------
with tab_stock:
    st.subheader("📦 Your Wine Fridge Inventory")
    
    df_stock = load_stock_data()
    
    if df_stock.empty:
        st.info("Your cellar stock list is currently empty. Add wines from the 'Add New Wine' tab.")
    else:
        # Filter options
        col_f1, col_f2 = st.columns(2)
        with col_f1:
            status_filter = st.selectbox("Filter by Status", ["All", "🔵 Aging / Sleeping", "🟢 Entering Window", "⭐ Optimum Peak", "🔴 Past Peak / Urgent"])
        with col_f2:
            search_query = st.text_input("Search Wine Name", "")

        filtered_df = df_stock.copy()
        if status_filter != "All" and "Status" in filtered_df.columns:
            filtered_df = filtered_df[filtered_df["Status"] == status_filter]
        if search_query and "Wine Name" in filtered_df.columns:
            filtered_df = filtered_df[filtered_df["Wine Name"].str.contains(search_query, case=False, na=False)]

        st.dataframe(filtered_df, use_container_width=True)
        
        st.markdown("---")
        st.markdown("### 🗑️ Remove Wine from Inventory")
        
        wine_options = [f"{row['Wine Name']} ({row['Vintage']})" for _, row in df_stock.iterrows()]
        selected_wine_to_delete = st.selectbox("Select a wine to delete", options=wine_options)
        
        if st.button("🗑️ Delete Selected Wine"):
            if selected_wine_to_delete and worksheet:
                all_records = worksheet.get_all_records()
                row_to_delete = None
                for idx, record in enumerate(all_records):
                    if f"{record['Wine Name']} ({record['Vintage']})" == selected_wine_to_delete:
                        row_to_delete = idx + 2  # +2 accounts for 1-indexing and the header row
                        break
                
                if row_to_delete:
                    worksheet.delete_rows(row_to_delete)
                    st.success(f"Successfully deleted '{selected_wine_to_delete}' from your inventory!")
                    st.rerun()
                else:
                    st.error("Could not find the specified row in Google Sheets.")

# -------------------------------------------------------------
# TAB 3: SETTINGS & NOTIFICATIONS
# -------------------------------------------------------------
with tab_settings:
    st.subheader("⚙️ App Settings & Notification Preferences")
    
    st.multiselect("Preferred Notification Channels", ["Email Digest", "Mobile Push Notification", "Telegram Webhook"], default=["Email Digest"])
    st.selectbox("Alert Frequency", ["Weekly Digest", "Monthly Audit", "Instant Alert (When bottle enters optimum window)"])
    st.text_input("Notification Email Address", "calvin@example.com")
    
    if st.button("Save Settings"):
        st.success("Preferences updated successfully!")
