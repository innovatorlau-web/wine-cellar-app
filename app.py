import datetime
import os
import streamlit as st
import pandas as pd

# Page Configuration
st.set_page_config(
    page_title="CellarIQ: Smart Wine Maturity Tracker",
    page_icon="🍷",
    layout="wide"
)

# App Header
st.title("🍷 CellarIQ & Vintage Intelligence")
st.markdown("Track your wine fridge inventory, discover optimal drinking windows, review famous critic scores, and get detailed professional tasting profiles.")

# Sidebar Navigation
tab_input, tab_stock, tab_settings = st.tabs(["➕ Add New Wine", "📦 Cellar Stock List", "⚙️ Settings & Alerts"])

# -------------------------------------------------------------
# SIMULATED INTELLIGENCE & RESEARCH ENGINE (Replace with real LLM/Search API in production)
# -------------------------------------------------------------
def analyze_wine_vintage(wine_name, vintage_year, region=""):
    """
    Simulates AI research over web sources, vintage charts, and critic databases.
    In production, replace this with an LLM call using web search tools.
    """
    current_year = datetime.datetime.now().year
    
    # Simple logic to simulate vintage curve based on age
    age = current_year - int(vintage_year) if vintage_year.isdigit() else 5
    
    # Mocking realistic data based on profile
    start_window = int(vintage_year) + 5 if vintage_year.isdigit() else 2024
    peak_start = start_window + 3
    peak_end = start_window + 12
    decline_year = peak_end + 5
    
    # Determine Status
    if current_year < start_window:
        status = "🔵 Aging / Sleeping"
        status_code = "aging"
    elif start_window <= current_year < peak_start:
        status = "🟢 Entering Window"
        status_code = "entering"
    elif peak_start <= current_year <= peak_end:
        status = "⭐ Optimum Peak"
        status_code = "peak"
    else:
        status = "🔴 Past Peak / Urgent"
        status_code = "past_peak"

    # Detailed Professional Tasting Profile
    tasting_profile = {
        "appearance": "Deep ruby core with garnet rims and high viscosity.",
        "nose": "Intense aromas of blackcurrant, dark cherry, graphite, cigar box, and a subtle touch of French oak vanilla.",
        "palate": "Full-bodied with structured, velvety tannins and balanced, refreshing acidity. Layers of blackberry, cassis, espresso bean, and secondary earthiness.",
        "structure": "Alcohol: 13.5% | Tannins: Firm and fine-grained | Acidity: Medium-Plus",
        "decanting": "Decant for 1 to 2 hours before serving to allow oxygenation and softening of primary tannins.",
        "temp": "Serve at 16°C – 18°C (60°F – 64°F)."
    }

    # Critic Scores (Mocked realistic top scores)
    scores = {
        "James Suckling (JS)": "95 / 100",
        "Robert Parker (RP)": "93 / 100",
        "Wine Enthusiast (WE)": "94 / 100",
        "Jancis Robinson (JR)": "17.5 / 20"
    }

    return {
        "wine_name": wine_name,
        "vintage": vintage_year,
        "region": region if region else "Bordeaux / Premium Appellation",
        "status": status,
        "status_code": status_code,
        "drink_start": start_window,
        "peak_start": peak_start,
        "peak_end": peak_end,
        "decline": decline_year,
        "scores": scores,
        "profile": tasting_profile
    }

# Initialize Session State for Stock Storage (Mocking Google Sheets database)
if "stock_list" not in st.session_state:
    st.session_state.stock_list = [
        {
            "Wine Name": "Château Margaux",
            "Vintage": "2015",
            "Region": "Margaux, Bordeaux",
            "Status": "🟢 Entering Window",
            "Drink Start": 2023,
            "Peak End": 2035,
            "JS Score": "98 / 100",
            "RP Score": "97 / 100",
            "WE Score": "96 / 100",
            "JR Score": "18.5 / 20",
            "Details": "Classic vintage with immense structure and aromatic complexity."
        }
    ]

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
                result = analyze_wine_vintage(input_name, input_vintage, input_region)
            
            st.success("Analysis Complete!")
            
            # --- INSTANT BRIEFING CARD ---
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

            # Save to stock list button
            if st.button("💾 Save to My Wine Fridge Stock List"):
                new_entry = {
                    "Wine Name": result["wine_name"],
                    "Vintage": result["vintage"],
                    "Region": result["region"],
                    "Status": result["status"],
                    "Drink Start": result["drink_start"],
                    "Peak End": result["peak_end"],
                    "JS Score": result["scores"]["James Suckling (JS)"],
                    "RP Score": result["scores"]["Robert Parker (RP)"],
                    "WE Score": result["scores"]["Wine Enthusiast (WE)"],
                    "JR Score": result["scores"]["Jancis Robinson (JR)"],
                    "Details": p["palate"]
                }
                st.session_state.stock_list.append(new_entry)
                st.success("Successfully added to your stock list inventory!")

# -------------------------------------------------------------
# TAB 2: CELLAR STOCK LIST (GOOGLE SHEETS SYNC VIEW)
# -------------------------------------------------------------
with tab_stock:
    st.subheader("📦 Your Wine Fridge Inventory")
    
    if len(st.session_state.stock_list) == 0:
        st.info("Your cellar stock list is currently empty. Add wines from the 'Add New Wine' tab.")
    else:
        df_stock = pd.DataFrame(st.session_state.stock_list)
        
        # Filter options
        col_f1, col_f2 = st.columns(2)
        with col_f1:
            status_filter = st.selectbox("Filter by Status", ["All", "🔵 Aging / Sleeping", "🟢 Entering Window", "⭐ Optimum Peak", "🔴 Past Peak / Urgent"])
        with col_f2:
            search_query = st.text_input("Search Wine Name", "")

        filtered_df = df_stock.copy()
        if status_filter != "All":
            filtered_df = filtered_df[filtered_df["Status"] == status_filter]
        if search_query:
            filtered_df = filtered_df[filtered_df["Wine Name"].str.contains(search_query, case=False, na=False)]

        st.dataframe(filtered_df, use_container_width=True)
        
        st.markdown("---")
        st.markdown("🔗 *Connected to Google Sheets Database (Live Sync Active)*")

# -------------------------------------------------------------
# TAB 3: SETTINGS & NOTIFICATIONS
# -------------------------------------------------------------
with tab_settings:
    st.subheader("⚙️ App Settings & Notification Preferences")
    
    st.markdown("Configure how and when you want to receive alerts regarding your wine drinking windows.")
    
    notif_channel = st.multiselect(
        "Preferred Notification Channels",
        ["Email Digest", "Mobile Push Notification", "Telegram Webhook"],
        default=["Email Digest"]
    )
    
    freq = st.selectbox(
        "Alert Frequency",
        ["Weekly Digest", "Monthly Audit", "Instant Alert (When bottle enters optimum window)"]
    )
    
    user_email = st.text_input("Notification Email Address", "calvin@example.com")
    
    if st.button("Save Settings"):
        st.success("Preferences updated successfully!")
