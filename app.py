import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# =========================================================
# PAGE CONFIG
# =========================================================
st.set_page_config(
    page_title="Israel–Palestine Conflict Analysis",
    page_icon="🕊️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =========================================================
# CUSTOM DARK THEME CSS
# =========================================================
st.markdown("""
    <style>
    /* App background */
    .stApp {
        background: radial-gradient(circle at top left, #14181f 0%, #0b0e13 100%);
        color: #e6e6e6;
    }

    /* Sidebar */
    section[data-testid="stSidebar"] {
        background-color: #10131a;
        border-right: 1px solid #262b36;
    }

    /* Headings */
    h1, h2, h3, h4 {
        color: #f5f5f5 !important;
        font-family: 'Segoe UI', sans-serif;
        letter-spacing: 0.3px;
    }

    /* Main title banner */
    .main-title {
        text-align: center;
        padding: 28px 10px;
        border-radius: 16px;
        background: linear-gradient(135deg, #1f2937 0%, #111827 100%);
        border: 1px solid #2d3441;
        margin-bottom: 25px;
        box-shadow: 0 4px 20px rgba(0,0,0,0.4);
    }
    .main-title h1 {
        font-size: 2.3rem;
        margin: 0;
        background: linear-gradient(90deg, #60a5fa, #a78bfa, #f472b6);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    .main-title p {
        color: #9ca3af;
        margin-top: 6px;
        font-size: 0.95rem;
    }

    /* KPI Cards */
    .kpi-card {
        background: linear-gradient(145deg, #171b24, #12151c);
        border: 1px solid #262b36;
        border-radius: 14px;
        padding: 18px 14px;
        text-align: center;
        box-shadow: 0 4px 14px rgba(0,0,0,0.35);
        transition: transform 0.2s ease, border-color 0.2s ease;
        height: 130px;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        outline: none;
        overflow: hidden;
    }
    .kpi-card:hover {
        transform: translateY(-4px);
        border-color: #3b82f6;
    }
    .kpi-card:focus,
    .kpi-card:focus-within,
    .kpi-card *:focus {
        outline: none !important;
        box-shadow: 0 4px 14px rgba(0,0,0,0.35) !important;
    }
    .kpi-value {
        font-size: 1.6rem;
        font-weight: 700;
        color: #60a5fa;
        line-height: 1.25;
        word-break: break-word;
        max-width: 100%;
    }
    .kpi-label {
        font-size: 0.78rem;
        color: #9ca3af;
        margin-top: 6px;
        text-transform: uppercase;
        letter-spacing: 0.6px;
        line-height: 1.3;
    }

    /* Section headers */
    .section-header {
        border-left: 4px solid #60a5fa;
        padding-left: 12px;
        margin: 18px 0 10px 0;
        font-size: 1.15rem;
        font-weight: 600;
        color: #f0f0f0;
    }

    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 6px;
    }
    .stTabs [data-baseweb="tab"] {
        background-color: #171b24;
        border-radius: 10px 10px 0 0;
        padding: 10px 18px;
        color: #9ca3af;
        border: 1px solid #262b36;
        border-bottom: none;
    }
    .stTabs [aria-selected="true"] {
        background-color: #1f2937 !important;
        color: #60a5fa !important;
    }

    /* Dataframe */
    .stDataFrame {
        border-radius: 12px;
        overflow: hidden;
        border: 1px solid #262b36;
    }

    /* Metric widgets (native) */
    div[data-testid="stMetric"] {
        background-color: #171b24;
        border: 1px solid #262b36;
        padding: 12px;
        border-radius: 12px;
    }

    footer {visibility: hidden;}
    #MainMenu {visibility: hidden;}
    </style>
""", unsafe_allow_html=True)

# Plotly dark template default
px.defaults.template = "plotly_dark"
PALETTE = px.colors.sequential.Blues_r + px.colors.qualitative.Set2

# =========================================================
# HEADER
# =========================================================
st.markdown("""
    <div class="main-title">
        <h1>🕊️ Israel–Palestine Conflict Analysis</h1>
        <p>Interactive dashboard exploring incident patterns, demographics, and regional trends</p>
    </div>
""", unsafe_allow_html=True)

# =========================================================
# SIDEBAR — UPLOAD + FILTERS
# =========================================================
st.sidebar.title("📂 Data & Filters")
upload_file = st.sidebar.file_uploader("Upload CSV dataset", type="csv")

if upload_file is not None:
    df = pd.read_csv(upload_file)

    # ---- Parse dates early so filters can use year/month ----
    df['date_of_event'] = pd.to_datetime(df['date_of_event'], errors='coerce')
    df['year'] = df['date_of_event'].dt.year
    df['month'] = df['date_of_event'].dt.month_name()

    st.sidebar.markdown("---")
    st.sidebar.subheader("🔎 Filter Data")

    # Region filter
    regions = sorted(df['event_location_region'].dropna().unique().tolist())
    selected_regions = st.sidebar.multiselect("Event Location Region", regions, default=regions)

    # Gender filter
    genders = sorted(df['gender'].dropna().unique().tolist())
    selected_genders = st.sidebar.multiselect("Gender", genders, default=genders)

    # Year filter
    years = sorted(df['year'].dropna().unique().tolist())
    if years:
        selected_years = st.sidebar.select_slider(
            "Year Range",
            options=years,
            value=(min(years), max(years))
        )
    else:
        selected_years = None

    # Apply filters
    filtered_df = df[
        df['event_location_region'].isin(selected_regions) &
        df['gender'].isin(selected_genders)
    ]
    if selected_years:
        filtered_df = filtered_df[
            (filtered_df['year'] >= selected_years[0]) &
            (filtered_df['year'] <= selected_years[1])
        ]

    st.sidebar.markdown("---")
    st.sidebar.caption(f"Showing **{len(filtered_df):,}** of **{len(df):,}** records")

    # =====================================================
    # KPI ROW
    # =====================================================
    no_event = len(filtered_df)
    top_region = filtered_df['event_location_region'].mode()[0] if not filtered_df.empty else "N/A"
    top_injury = filtered_df['type_of_injury'].mode()[0] if not filtered_df.empty else "N/A"
    avg_age = round(filtered_df['age'].mean(), 1) if not filtered_df.empty else 0
    hostilities_pct = (
        round((filtered_df['took_part_in_the_hostilities'] == 'Yes').mean() * 100, 1)
        if not filtered_df.empty else 0
    )

    k1, k2, k3, k4, k5 = st.columns(5)
    kpis = [
        (k1, f"{no_event:,}", "Total Events"),
        (k2, top_region, "Top Region"),
        (k3, top_injury, "Most Common Injury"),
        (k4, f"{avg_age}", "Average Age"),
        (k5, f"{hostilities_pct}%", "Involved in Hostilities"),
    ]
    for col, val, label in kpis:
        col.markdown(f"""
            <div class="kpi-card">
                <div class="kpi-value">{val}</div>
                <div class="kpi-label">{label}</div>
            </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # =====================================================
    # SIDEBAR SUMMARY TABLES (kept, styled)
    # =====================================================
    with st.sidebar.expander("📊 Citizenship Breakdown"):
        st.dataframe(filtered_df['citizenship'].value_counts(), use_container_width=True)
    with st.sidebar.expander("📍 Region Breakdown"):
        st.dataframe(filtered_df['event_location_region'].value_counts(), use_container_width=True)
    with st.sidebar.expander("⚔️ Hostilities: Participants"):
        st.dataframe(
            filtered_df[filtered_df['took_part_in_the_hostilities'] == 'Yes']['citizenship'].value_counts(),
            use_container_width=True
        )
    with st.sidebar.expander("🕊️ Hostilities: Non-Participants"):
        st.dataframe(
            filtered_df[filtered_df['took_part_in_the_hostilities'] == 'No']['citizenship'].value_counts(),
            use_container_width=True
        )
    with st.sidebar.expander("🔫 Weapon / Ammunition Counts"):
        st.dataframe(filtered_df['ammunition'].value_counts(), use_container_width=True)

    # =====================================================
    # TABS FOR MAIN CONTENT
    # =====================================================
    tab1, tab2, tab3, tab4 = st.tabs(["📈 Overview", "🧍 Demographics", "🗺️ Regional Insights", "🕓 Timeline"])

    # ---------------- TAB 1: OVERVIEW ----------------
    with tab1:
        st.markdown('<div class="section-header">Injury Types & Gender Distribution</div>', unsafe_allow_html=True)
        c1, c2 = st.columns(2)

        with c1:
            type_of_injury = filtered_df['type_of_injury'].value_counts()
            fig = px.bar(
                type_of_injury,
                x=type_of_injury.values,
                y=type_of_injury.index,
                orientation='h',
                color=type_of_injury.values,
                color_continuous_scale='Blues',
                labels={'x': 'Count', 'y': 'Injury Type'},
                title="Type of Injuries"
            )
            fig.update_layout(coloraxis_showscale=False, plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)')
            st.plotly_chart(fig, use_container_width=True)

        with c2:
            mf_counts = filtered_df['gender'].value_counts()
            fig = px.pie(
                mf_counts,
                names=mf_counts.index,
                values=mf_counts.values,
                hole=0.5,
                title="Male / Female Distribution",
                color_discrete_sequence=px.colors.qualitative.Set2
            )
            fig.update_traces(
                textinfo='percent+label',
                textfont=dict(color='white', size=13),
                marker=dict(line=dict(color='#0b0e13', width=2))
            )
            fig.update_layout(
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                legend=dict(orientation='h', yanchor='bottom', y=-0.25, xanchor='center', x=0.5, font=dict(color='white')),
                margin=dict(t=60, b=80, l=20, r=20),
                title=dict(font=dict(color='white', size=16))
            )
            st.plotly_chart(fig, use_container_width=True)

        st.markdown('<div class="section-header">Injury Type Breakdown (Grouped)</div>', unsafe_allow_html=True)
        injurytype = filtered_df['type_of_injury'].value_counts()
        if not injurytype.empty:
            threshold = injurytype.sum() * 0.02
            main_inj = injurytype[injurytype >= threshold].copy()
            other_sum = injurytype[injurytype < threshold].sum()
            if other_sum > 0:
                main_inj['Other'] = other_sum

            fig = px.pie(
                main_inj,
                names=main_inj.index,
                values=main_inj.values,
                title="Injury Types (small categories grouped as 'Other')",
                color_discrete_sequence=px.colors.qualitative.Set3
            )
            fig.update_traces(
                textposition='inside',
                textinfo='percent+label',
                textfont=dict(color='white', size=13),
                marker=dict(line=dict(color='#0b0e13', width=2))
            )
            fig.update_layout(
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                showlegend=True,
                legend=dict(
                    orientation='h',
                    yanchor='bottom', y=-0.25,
                    xanchor='center', x=0.5,
                    font=dict(color='white')
                ),
                margin=dict(t=60, b=80, l=20, r=20),
                title=dict(font=dict(color='white', size=16))
            )
            st.plotly_chart(fig, use_container_width=True)

    # ---------------- TAB 2: DEMOGRAPHICS ----------------
    with tab2:
        st.markdown('<div class="section-header">Age Distribution</div>', unsafe_allow_html=True)
        c1, c2 = st.columns(2)

        with c1:
            fig = px.histogram(
                filtered_df, x="age", nbins=30,
                title="Age Distribution",
                color_discrete_sequence=["#60a5fa"]
            )
            fig.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)')
            st.plotly_chart(fig, use_container_width=True)

        with c2:
            genderInc = filtered_df.groupby('gender').size().reset_index(name="incident_count")
            fig = px.bar(
                genderInc, x='gender', y='incident_count',
                title="Incident Count by Gender",
                color='gender',
                color_discrete_sequence=px.colors.qualitative.Set2
            )
            fig.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)')
            st.plotly_chart(fig, use_container_width=True)

        st.markdown('<div class="section-header">Incident Count by Nationality</div>', unsafe_allow_html=True)
        IncidentcountbyNat = filtered_df.groupby('citizenship').size().reset_index(name='incident_count')
        IncidentcountbyNat = IncidentcountbyNat.sort_values('incident_count', ascending=False)
        fig = px.bar(
            IncidentcountbyNat, x='citizenship', y='incident_count',
            title="Incidents by Nationality",
            color='incident_count',
            color_continuous_scale='Blues'
        )
        fig.update_layout(coloraxis_showscale=False, plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig, use_container_width=True)

        with st.expander("📋 View Raw Nationality Table"):
            st.dataframe(IncidentcountbyNat, use_container_width=True)

    # ---------------- TAB 3: REGIONAL INSIGHTS ----------------
    with tab3:
        st.markdown('<div class="section-header">Region-Level Patterns</div>', unsafe_allow_html=True)
        c1, c2 = st.columns(2)

        with c1:
            eventregion = filtered_df['event_location_region'].value_counts()
            fig = px.bar(
                eventregion, x=eventregion.index, y=eventregion.values,
                title="Event Location Region Count",
                color=eventregion.values,
                color_continuous_scale='Purples',
                labels={'x': 'Region', 'y': 'Count'}
            )
            fig.update_layout(coloraxis_showscale=False, plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)')
            st.plotly_chart(fig, use_container_width=True)

        with c2:
            residencecountbyreg = filtered_df.groupby('event_location_region')['place_of_residence'].nunique()
            fig = px.pie(
                residencecountbyreg,
                names=residencecountbyreg.index,
                values=residencecountbyreg.values,
                title="Unique Residences by Region",
                hole=0.4,
                color_discrete_sequence=px.colors.qualitative.Set3
            )
            fig.update_traces(
                textinfo='percent+label',
                textfont=dict(color='white', size=13),
                marker=dict(line=dict(color='#0b0e13', width=2))
            )
            fig.update_layout(
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                legend=dict(orientation='h', yanchor='bottom', y=-0.25, xanchor='center', x=0.5, font=dict(color='white')),
                margin=dict(t=60, b=80, l=20, r=20),
                title=dict(font=dict(color='white', size=16))
            )
            st.plotly_chart(fig, use_container_width=True)

        st.markdown('<div class="section-header">Average Age by Region</div>', unsafe_allow_html=True)
        regionavgage = filtered_df.groupby('event_location_region')['age'].mean().sort_values(ascending=False)
        fig = px.bar(
            regionavgage, x=regionavgage.index, y=regionavgage.values,
            title="Average Age by Region",
            color=regionavgage.values,
            color_continuous_scale='Sunset',
            labels={'x': 'Region', 'y': 'Average Age'}
        )
        fig.update_layout(coloraxis_showscale=False, plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig, use_container_width=True)

    # ---------------- TAB 4: TIMELINE ----------------
    with tab4:
        st.markdown('<div class="section-header">Events Over Time</div>', unsafe_allow_html=True)

        time_df = filtered_df.dropna(subset=['date_of_event']).copy()
        time_events = time_df.groupby(['year', 'month']).size().reset_index(name='incident_count')
        time_events['year_month'] = pd.to_datetime(
            time_events['year'].astype(int).astype(str) + '-' + time_events['month'], format='%Y-%B'
        )
        time_events = time_events.sort_values('year_month')

        fig = px.line(
            time_events, x='year_month', y='incident_count',
            title="Incident Count Over Time",
            markers=True,
            color_discrete_sequence=["#60a5fa"]
        )
        fig.update_traces(fill='tozeroy', line=dict(width=3))
        fig.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig, use_container_width=True)

        st.markdown('<div class="section-header">Yearly Totals</div>', unsafe_allow_html=True)
        yearly = time_df.groupby('year').size().reset_index(name='incident_count')
        fig = px.bar(
            yearly, x='year', y='incident_count',
            title="Incidents per Year",
            color='incident_count',
            color_continuous_scale='Blues'
        )
        fig.update_layout(coloraxis_showscale=False, plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig, use_container_width=True)

    # =====================================================
    # RAW DATA VIEW
    # =====================================================
    with st.expander("🗃️ View Full Filtered Dataset"):
        st.dataframe(filtered_df, use_container_width=True)

else:
    st.markdown("""
        <div style="text-align:center; padding: 60px; color:#9ca3af;">
            <h3>👋 Welcome</h3>
            <p>Upload a CSV file from the sidebar to begin exploring the dashboard.</p>
        </div>
    """, unsafe_allow_html=True)