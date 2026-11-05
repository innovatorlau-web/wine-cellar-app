import datetime
import io
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

# -------------------------------------------------------------
# LOCAL STORAGE & SESSION INVENTORY MANAGEMENT
# -------------------------------------------------------------
if "inventory" not in st.session_state:
    st.session_state.inventory = []

def get_inventory_df():
    """Returns the current inventory as a pandas DataFrame."""
    if st.session_state.inventory:
        return pd.DataFrame(st.session_state.inventory)
    return pd.DataFrame(columns=[
        "Wine Name", "Vintage", "Region", "Status", "Drink Start",
        "Peak End", "JS Score", "RP Score", "WE Score", "JR Score", "Details"
    ])

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
tab_input, tab_stock, tab_settings = st.tabs(["➕ Add New Wine", "📦 Cellar Stock List", "⚙️ Settings & Backup"])

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
            with st.spinner("Analyzing vintage charts, critic ratings, and aging curves..."):
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

        if st.button("💾 Save to My Cellar Inventory"):
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
            st.session_state.inventory.append(new_entry)
            st.success("Successfully saved to your cellar stock list!")
            del st.session_state.current_analysis
            st.rerun()

# -------------------------------------------------------------
# TAB 2: CELLAR STOCK LIST & DELETE FEATURE
# -------------------------------------------------------------
with tab_stock:
    st.subheader("📦 Your Wine Fridge Inventory")
    
    df_stock = get_inventory_df()
    
    if df_stock.empty:
        st.info("Your cellar stock list is currently empty. Add wines from the 'Add New Wine' tab or import a CSV file in Settings.")
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
        
        wine_options = [f"{idx + 1}. {row['Wine Name']} ({row['Vintage']})" for idx, row in df_stock.iterrows()]
        selected_wine_to_delete = st.selectbox("Select a wine to delete", options=wine_options)
        
        if st.button("🗑️ Delete Selected Wine"):
            if selected_wine_to_delete:
                # Extract index
                selected_idx = int(selected_wine_to_delete.split(".")[0]) - 1
                deleted_item = st.session_state.inventory.pop(selected_idx)
                st.success(f"Successfully deleted '{deleted_item['Wine Name']} ({deleted_item['Vintage']})'!")
                st.rerun()

# -------------------------------------------------------------
# TAB 3: SETTINGS, IMPORT & EXPORT
# -------------------------------------------------------------
with tab_settings:
    st.subheader("⚙️ Local Data Backup & Settings")
    
    st.markdown("### 📥 Backup & Export Inventory")
    st.markdown("Export your cellar list to a CSV file to keep an offline backup on your phone or PC.")
    
    df_current = get_inventory_df()
    if not df_current.empty:
        csv_buffer = df_current.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📄 Download Inventory CSV",
            data=csv_buffer,
            file_name=f"wine_cellar_backup_{datetime.date.today()}.csv",
            mime="text/csv"
        )
    else:
        st.caption("Add wines to your list to enable CSV download.")

    st.markdown("---")
    st.markdown("### 📤 Import Existing Inventory CSV")
    uploaded_file = st.file_uploader("Upload a previously exported wine inventory CSV", type=["csv"])
    if uploaded_file is not None:
        try:
            imported_df = pd.read_csv(uploaded_file)
            st.session_state.inventory = imported_df.to_dict(orient="records")
            st.success("Successfully restored your wine inventory from CSV!")
            st.rerun()
        except Exception as e:
            st.error(f"Failed to read CSV file: {e}")
