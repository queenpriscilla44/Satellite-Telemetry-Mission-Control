import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from pathlib import Path
from datetime import datetime
import numpy as np
# --------------------------------
# PAGE CONFIGURATION
# --------------------------------

st.set_page_config(
    page_title="SAT-001 | Mission Control",
    page_icon="🛰️",
    layout="wide",
    initial_sidebar_state="expanded"
)


CSV_FILE = Path(__file__).resolve().parent.parent / "telemetry.csv"
ALERT_FILE = Path(__file__).resolve().parent / "alerts.csv"
# --------------------------------
# PERSISTENT ALERT STORAGE
# --------------------------------

def save_alerts(alert_records):

    if not alert_records:
        return

    new_alerts = pd.DataFrame(alert_records)

    if ALERT_FILE.exists():

        existing_alerts = pd.read_csv(ALERT_FILE)

        combined_alerts = pd.concat(
            [existing_alerts, new_alerts],
            ignore_index=True
        )

    else:
        combined_alerts = new_alerts

    combined_alerts = combined_alerts.drop_duplicates(
        subset=["Time", "Status", "Fault Level", "Reason"]
    )

    combined_alerts.to_csv(
        ALERT_FILE,
        index=False
    )


def read_saved_alerts():

    if not ALERT_FILE.exists():
        return pd.DataFrame(
            columns=["Time", "Status", "Fault Level", "Reason"]
        )

    return pd.read_csv(ALERT_FILE)
# --------------------------------
# PROFESSIONAL DARK THEME
# --------------------------------

st.markdown("""
<style>
.stApp {
    background: linear-gradient(135deg, #07111f, #0b1728);
    color: #e5edf7;
}

.block-container {
    padding-top: 2rem;
    padding-bottom: 2rem;
    max-width: 1500px;
}

h1, h2, h3 {
    color: #eaf3ff !important;
}

section[data-testid="stMetric"] {
    background: #12243a;
    border: 1px solid #233c59;
    padding: 18px;
    border-radius: 12px;
}

section[data-testid="stMetric"] label {
    color: #9eb5d0 !important;
}

section[data-testid="stMetric"] [data-testid="stMetricValue"] {
    color: #ffffff !important;
}

.mission-header {
    background: linear-gradient(100deg, #102b49, #153c5c);
    padding: 25px;
    border: 1px solid #315575;
    border-radius: 15px;
    margin-bottom: 20px;
}

.mission-label {
    color: #8fc8ff;
    font-size: 13px;
    letter-spacing: 2px;
    font-weight: bold;
}

.mission-title {
    color: #ffffff;
    font-size: 30px;
    font-weight: 700;
    margin-top: 8px;
}

.mission-subtitle {
    color: #b8cee3;
    font-size: 14px;
    margin-top: 5px;
}

.status-box {
    padding: 16px;
    border-radius: 12px;
    margin: 10px 0 20px 0;
    font-weight: 600;
    border: 1px solid;
}

.status-normal {
    background: #103526;
    border-color: #23865a;
    color: #75e6ac;
}

.status-warning {
    background: #3c2e13;
    border-color: #b88725;
    color: #ffd477;
}

.status-critical, .status-invalid {
    background: #421d25;
    border-color: #bd4555;
    color: #ff9ba6;
}

div[data-testid="stDataFrame"] {
    border: 1px solid #233c59;
    border-radius: 10px;
}

.stDownloadButton button {
    background: #174c78;
    color: white;
    border: 1px solid #3977a8;
    border-radius: 8px;
}
</style>
""", unsafe_allow_html=True)

# --------------------------------
# HEADER
# --------------------------------

st.title("🛰️ SAT-001 | SATELLITE MISSION CONTROL")

st.caption(
    "SPACECRAFT TELEMETRY • FLIGHT OPERATIONS • SYSTEM MONITORING"
)
st.info(
    "🛰️ SIMULATION MODE — "
    "Displaying educational satellite telemetry. "
    "Not connected to a real spacecraft."
)
# --------------------------------
# READ C-GENERATED CSV DATA
# --------------------------------

# --------------------------------
# CLOUD TELEMETRY GENERATOR
# --------------------------------

def create_cloud_telemetry():

    times = pd.date_range(
        end=datetime.now(),
        periods=50,
        freq="2s"
    )

    rng = np.random.default_rng()

    df = pd.DataFrame({
        "Time": times,
        "Temperature": rng.uniform(25, 35, 50),
        "Battery Voltage": rng.uniform(7.2, 8.2, 50),
        "Current": rng.uniform(1.0, 2.0, 50),
        "Altitude": rng.uniform(500, 520, 50),
        "Gyroscope": rng.uniform(0.1, 0.8, 50),
        "Validity": ["VALID"] * 50,
        "Fault Level": [0] * 50
    })

    return df

def read_telemetry():

    if not CSV_FILE.exists():
        return create_cloud_telemetry()
    try:
        df = pd.read_csv(CSV_FILE)

        required_columns = [
            "Time", "Temperature", "Battery Voltage",
            "Current", "Altitude", "Gyroscope",
            "Validity", "Fault Level"
        ]

        if not all(col in df.columns for col in required_columns):
            st.error("CSV file is missing required columns.")
            return pd.DataFrame()

        df["Time"] = pd.to_datetime(df["Time"], errors="coerce")

        numeric_columns = [
            "Temperature", "Battery Voltage",
            "Current", "Altitude", "Gyroscope",
            "Fault Level"
        ]

        for col in numeric_columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")

        df = df.dropna(
            subset=["Time"] + numeric_columns
        )

        return df.tail(50)

    except (OSError, pd.errors.ParserError, UnicodeDecodeError) as error:
        st.error(f"Could not read telemetry.csv: {error}")
        return pd.DataFrame()


# --------------------------------
# HEALTH STATUS
# --------------------------------

def get_status(data):

    if str(data["Validity"]).upper() != "VALID":
        return "INVALID"

    fault_level = int(data["Fault Level"])

    if fault_level >= 2:
        return "CRITICAL"
    elif fault_level == 1:
        return "WARNING"

    return "NORMAL"


# --------------------------------
# CHART FUNCTION
# --------------------------------

def create_chart(df, column, title, unit):

    fig = px.line(
        df,
        x="Time",
        y=column,
        title=title,
        markers=True
    )

    fig.update_traces(
        line=dict(width=3),
        marker=dict(size=6)
    )

    fig.update_layout(
        template="plotly_dark",
        paper_bgcolor="#0d1b2c",
        plot_bgcolor="#0d1b2c",
        font=dict(color="#dce8f5"),
        title_font=dict(size=17),
        margin=dict(l=15, r=15, t=50, b=15),
        height=310,
        xaxis_title="Time",
        yaxis_title=unit,
        hovermode="x unified"
    )

    fig.update_xaxes(showgrid=True, gridcolor="#243b53")
    fig.update_yaxes(showgrid=True, gridcolor="#243b53")

    return fig


# --------------------------------
# LIVE INSTRUMENT GAUGE
# --------------------------------

def create_gauge(value, title, unit, minimum, maximum):

    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=value,
        number={"suffix": unit},
        title={"text": title},
        gauge={
            "axis": {"range": [minimum, maximum]},
            "bar": {"color": "#39c5f0"},
            "bgcolor": "#12243a",
            "borderwidth": 1,
            "bordercolor": "#315575"
        }
    ))

    fig.update_layout(
        template="plotly_dark",
        paper_bgcolor="#0d1b2c",
        font={"color": "#dce8f5"},
        height=250,
        margin=dict(l=20, r=20, t=45, b=10)
    )

    return fig


# --------------------------------
# 3D EARTH AND SATELLITE ORBIT
# --------------------------------

def create_orbit_visualization():

    # Generate Earth surface coordinates
    u = np.linspace(0, 2 * np.pi, 50)
    v = np.linspace(0, np.pi, 50)

    x = 1.0 * np.outer(np.cos(u), np.sin(v))
    y = 1.0 * np.outer(np.sin(u), np.sin(v))
    z = 1.0 * np.outer(np.ones(np.size(u)), np.cos(v))

    fig = go.Figure()

    # Earth
    fig.add_trace(go.Surface(
        x=x,
        y=y,
        z=z,
        colorscale=[
            [0, "#102f55"],
            [0.5, "#1675b9"],
            [1, "#56c5e8"]
        ],
        showscale=False,
        opacity=0.95,
        name="Earth"
    ))

    # Simulated satellite orbit
    theta = np.linspace(0, 2 * np.pi, 200)

    orbit_x = 1.7 * np.cos(theta)
    orbit_y = 1.7 * np.sin(theta)
    orbit_z = 0.25 * np.sin(2 * theta)

    fig.add_trace(go.Scatter3d(
        x=orbit_x,
        y=orbit_y,
        z=orbit_z,
        mode="lines",
        line=dict(color="#39c5f0", width=5),
        name="Simulated Orbit"
    ))

    # Simulated satellite position
    fig.add_trace(go.Scatter3d(
        x=[orbit_x[35]],
        y=[orbit_y[35]],
        z=[orbit_z[35]],
        mode="markers+text",
        marker=dict(size=7, color="#ffcc33"),
        text=["SAT-001"],
        textposition="top center",
        name="Satellite"
    ))

    fig.update_layout(
        template="plotly_dark",
        paper_bgcolor="#0d1b2c",
        scene=dict(
            bgcolor="#0d1b2c",
            xaxis=dict(visible=False),
            yaxis=dict(visible=False),
            zaxis=dict(visible=False),
            aspectmode="data"
        ),
        height=500,
        margin=dict(l=0, r=0, t=20, b=0),
        showlegend=True
    )

    return fig


# --------------------------------
# LIVE DASHBOARD
# --------------------------------

@st.fragment(run_every="2s")
def live_dashboard():

    df = read_telemetry()

    
    if df.empty:
        st.warning(
            "No telemetry records found. "
            "Start the C simulator to generate data."
        )
        return

    latest = df.iloc[-1]
    status = get_status(latest)
    temperature = latest["Temperature"]
    battery = latest["Battery Voltage"]
    current = latest["Current"]
    altitude = latest["Altitude"]
    gyroscope = latest["Gyroscope"]

    data_source_label = (
        "C SIMULATOR"
        if CSV_FILE.exists()
        else "CLOUD SIMULATION"
    )

    data_source_description = (
        "C-based satellite simulator"
        if CSV_FILE.exists()
        else "Cloud-generated simulated telemetry"
    )


     
    # --------------------------------
    # SATELLITE OVERVIEW
    # --------------------------------

    st.subheader("Mission Overview")

    info1, info2, info3, info4, info5 = st.columns(5)

    info1.metric(
        "Satellite ID",
        "SAT-001"
    )

    info2.metric(
        "Mission Mode",
        "SIMULATION"
    )

    info3.metric(
        "Telemetry Feed",
        "RECEIVING"
    )

    info4.metric(
        "Health Status",
        status
    )

    info5.metric(
        "Data Source",
        data_source_label
    )

    st.caption(
        f"Last telemetry update: {latest['Time'].strftime('%H:%M:%S')} | "
        f"Data source: {data_source_description}"
    )

    # --------------------------

    # --------------------------------
    # SENSOR METRIC CARDS
    # --------------------------------

    st.subheader("Live Telemetry Parameters")

    c1, c2, c3, c4, c5 = st.columns(5)
    

    c2.metric(
        "🔋 Battery Voltage",
        f"{latest['Battery Voltage']:.2f} V"
    )

    c3.metric(
        "⚡ Current",
        f"{latest['Current']:.2f} A"
    )

    c4.metric(
        "🛰️ Altitude",
        f"{latest['Altitude']:.2f} km"
    )

    c5.metric(
        "🧭 Gyroscope",
        f"{latest['Gyroscope']:.2f} °/s"
    )
     # --------------------------------
    # LIVE INSTRUMENT GAUGES
    # --------------------------------

    st.subheader("Live Instrument Gauges")

    g1, g2, g3 = st.columns(3)

    with g1:
        st.plotly_chart(
            create_gauge(
                temperature, "Temperature", " °C", 0, 60
            ),
            width="stretch"
        )

    with g2:
        st.plotly_chart(
            create_gauge(
                battery, "Battery Voltage", " V", 0, 10
            ),
            width="stretch"
        )

    with g3:
        st.plotly_chart(
            create_gauge(
                current, "Current", " A", 0, 4
            ),
            width="stretch"
        )

    g4, g5 = st.columns(2)

    with g4:
        st.plotly_chart(
            create_gauge(
                altitude, "Satellite Altitude", " km", 0, 700
            ),
            width="stretch"
        )

    with g5:
        st.plotly_chart(
            create_gauge(
                gyroscope, "Angular Rate", " °/s", 0, 5
            ),
            width="stretch"
        )
    
    # --------------------------------
    # EARTH AND ORBIT VISUALIZATION
    # --------------------------------

    st.subheader("Earth & Satellite Orbit")

    st.caption(
        "SIMULATED ORBITAL VISUALIZATION — NOT REAL-TIME SPACECRAFT POSITION"
    )

    orbit_col1, orbit_col2 = st.columns([2, 1])

    with orbit_col1:
        st.plotly_chart(
            create_orbit_visualization(),
            width="stretch"
        )

    with orbit_col2:
        st.markdown("### ORBITAL INFORMATION")

        st.metric("Satellite ID", "SAT-001")
        st.metric("Orbit Type", "SIMULATED LEO")
        st.metric("Orbit Status", "NOMINAL")
        st.metric("Position", "SIMULATED")
    
    # --------------------------------
    # MISSION EVENT TIMELINE
    # --------------------------------

    st.subheader("Mission Event Timeline")

    st.caption("SIMULATED MISSION EVENTS")

    mission_events = [
        ("SYSTEM", "Telemetry simulator initialized", "NORMAL"),
        ("COMMUNICATION", "Communication link established", "NORMAL"),
        ("TELEMETRY", "Telemetry data received from SAT-001", "NORMAL"),
        ("HEALTH", "Satellite health check completed", status),
    ]

    if status == "WARNING":
        mission_events.append(
            ("ALERT", "Warning threshold exceeded", "WARNING")
        )

    elif status == "CRITICAL":
        mission_events.append(
            ("ALERT", "Critical fault detected", "CRITICAL")
        )

    elif status == "INVALID":
        mission_events.append(
            ("ALERT", "Invalid telemetry reading detected", "INVALID")
        )

    for event_type, event_description, event_status in reversed(mission_events):

        if event_status == "CRITICAL":
            st.error(f"🔴 {event_type} | {event_description}")

        elif event_status == "WARNING":
            st.warning(f"🟠 {event_type} | {event_description}")

        elif event_status == "INVALID":
            st.error(f"⚠️ {event_type} | {event_description}")

        else:
            st.success(f"🟢 {event_type} | {event_description}")

    # --------------------------------
    # HEALTH AND ALERT PANEL
    # --------------------------------

    st.subheader("Satellite Health & Alerts")

    status_classes = {
        "NORMAL": "status-normal",
        "WARNING": "status-warning",
        "CRITICAL": "status-critical",
        "INVALID": "status-invalid"
    }

    status_messages = {
        "NORMAL": "NORMAL — Satellite operating normally.",
        "WARNING": "WARNING — Abnormal sensor readings detected.",
        "CRITICAL": "CRITICAL — Immediate attention required!",
        "INVALID": "INVALID — Telemetry validation failed."
    }

    st.markdown(
        f'<div class="status-box {status_classes[status]}">'
        f'{status_messages[status]}'
        '</div>',
        unsafe_allow_html=True
    )

    st.caption(
        f"Validity: {latest['Validity']} | "
        f"Fault Level: {int(latest['Fault Level'])} | "
        f"Last Reading: {latest['Time']}"
    )
    
        # --------------------------------
    # ENGINEERING THRESHOLD MONITORING
    # --------------------------------

    st.subheader("Sensor Threshold Monitoring")

    temperature = latest["Temperature"]
    battery = latest["Battery Voltage"]
    current = latest["Current"]
    altitude = latest["Altitude"]
    gyroscope = latest["Gyroscope"]
    
    def sensor_status(value, low=None, high=None, critical_low=None):
        if critical_low is not None and value < critical_low:
            return "CRITICAL"

        if low is not None and value < low:
            return "WARNING"

        if high is not None and value > high:
            return "WARNING"

        return "NORMAL"

    threshold_data = [
        {
            "Sensor": "Temperature",
            "Reading": f"{temperature:.2f} °C",
            "Configured Limit": "0 to 50 °C",
            "Status": sensor_status(temperature, low=0, high=50)
        },
        {
            "Sensor": "Battery Voltage",
            "Reading": f"{battery:.2f} V",
            "Configured Limit": "Above 6.0 V",
            "Status": sensor_status(battery, critical_low=6)
        },
        {
            "Sensor": "Current",
            "Reading": f"{current:.2f} A",
            "Configured Limit": "0 to 3.0 A",
            "Status": sensor_status(current, low=0, high=3)
        },
        {
            "Sensor": "Altitude",
            "Reading": f"{altitude:.2f} km",
            "Configured Limit": "400 to 550 km",
            "Status": sensor_status(altitude, low=400, high=550)
        },
        {
            "Sensor": "Gyroscope",
            "Reading": f"{gyroscope:.2f} °/s",
            "Configured Limit": "0 to 3.0 °/s",
            "Status": sensor_status(gyroscope, low=0, high=3)
        }
    ]

    threshold_df = pd.DataFrame(threshold_data)

    if str(latest["Validity"]).upper() != "VALID":
        threshold_df["Status"] = "INVALID"

    st.dataframe(
        threshold_df,
        width="stretch",
        hide_index=True
    )

    # --------------------------------
    # TELEMETRY GRAPHS
    # --------------------------------

    st.subheader("Live Telemetry Analytics")

    left, right = st.columns(2)

    with left:
        st.plotly_chart(
            create_chart(
                df, "Temperature",
                "Temperature Monitoring", "°C"
            ),
            width="stretch"
        )

        st.plotly_chart(
            create_chart(
                df, "Current",
                "Current Consumption", "A"
            ),
            width="stretch"
        )

        st.plotly_chart(
            create_chart(
                df, "Gyroscope",
                "Gyroscope Monitoring", "°/s"
            ),
            width="stretch"
        )

    with right:
        st.plotly_chart(
            create_chart(
                df, "Battery Voltage",
                "Battery Voltage Monitoring", "V"
            ),
            width="stretch"
        )

        st.plotly_chart(
            create_chart(
                df, "Altitude",
                "Altitude Monitoring", "km"
            ),
            width="stretch"
        )

    # --------------------------------
    # RECENT TELEMETRY TABLE
    # --------------------------------

    st.subheader("Recent Telemetry Records")

    st.dataframe(
        df.tail(10).sort_values("Time", ascending=False),
        width="stretch",
        hide_index=True
    )


    
    # --------------------------------
    # HISTORICAL TELEMETRY ANALYSIS
    # --------------------------------

    st.subheader("Historical Telemetry Analytics")

    st.caption(
        "ANALYSIS OF RECORDED SIMULATED SATELLITE TELEMETRY"
    )

    historical_df = df.copy()

    historical_df["Time"] = pd.to_datetime(
        historical_df["Time"],
        errors="coerce"
    )

    sensor_columns = [
        "Temperature",
        "Battery Voltage",
        "Current",
        "Altitude",
        "Gyroscope"
    ]

    for column in sensor_columns:
        historical_df[column] = pd.to_numeric(
            historical_df[column],
            errors="coerce"
        )

    historical_df = historical_df.dropna(
        subset=["Time"]
    ).sort_values("Time")

    if not historical_df.empty:

        # TELEMETRY STATISTICS

        st.markdown("### Telemetry Statistics")

        stat1, stat2, stat3, stat4 = st.columns(4)

        stat1.metric(
            "Recorded Samples",
            len(historical_df)
        )

        stat2.metric(
            "Average Temperature",
            f"{historical_df['Temperature'].mean():.2f} °C"
        )

        stat3.metric(
            "Average Battery",
            f"{historical_df['Battery Voltage'].mean():.2f} V"
        )

        stat4.metric(
            "Maximum Current",
            f"{historical_df['Current'].max():.2f} A"
        )

        # SENSOR PARAMETER SELECTION

        st.markdown("### Historical Sensor Trends")

        selected_parameter = st.selectbox(
            "Select Telemetry Parameter",
            sensor_columns
        )

        historical_fig = px.line(
            historical_df,
            x="Time",
            y=selected_parameter,
            title=f"{selected_parameter} Over Time",
            markers=True
        )

        historical_fig.update_layout(
            template="plotly_dark",
            paper_bgcolor="#0d1b2c",
            plot_bgcolor="#0d1b2c",
            font={"color": "#dce8f5"},
            height=400,
            xaxis_title="Time",
            yaxis_title=selected_parameter
        )

        st.plotly_chart(
            historical_fig,
            width="stretch"
        )

        # SUMMARY TABLE

        st.markdown("### Sensor Performance Summary")

        summary_df = historical_df[sensor_columns].agg(
            ["mean", "min", "max", "std"]
        ).round(2)

        summary_df.index = [
            "Average",
            "Minimum",
            "Maximum",
            "Standard Deviation"
        ]

        st.dataframe(
            summary_df,
            width="stretch"
        )

    else:
        st.warning("No historical telemetry records available.")

    

    # --------------------------------
    # FAULT HISTORY AND ALERT LOGGING
    # --------------------------------

    st.subheader("Fault History & Alert Log")

    alert_records = []

    for _, row in df.iterrows():

        validity = str(row["Validity"]).upper()
        fault_level = int(row["Fault Level"])

        if validity != "VALID":
            alert_status = "INVALID"
            reasons = ["Telemetry validation failed"]

        elif fault_level == 2:
            alert_status = "CRITICAL"
            reasons = []

            if row["Battery Voltage"] < 6.0:
                reasons.append("Low battery voltage")

        elif fault_level == 1:
            alert_status = "WARNING"
            reasons = []

            if row["Temperature"] > 50.0 or row["Temperature"] < 0.0:
                reasons.append("Temperature outside normal range")

            if row["Current"] > 3.0:
                reasons.append("High current consumption")

            if row["Altitude"] < 400.0 or row["Altitude"] > 550.0:
                reasons.append("Altitude outside target range")

            if row["Gyroscope"] > 3.0:
                reasons.append("Excessive gyroscope movement")

        else:
            continue

        alert_records.append({
            "Time": row["Time"],
            "Status": alert_status,
            "Fault Level": fault_level,
            "Reason": ", ".join(reasons) if reasons else "Fault detected"
        })

    # --------------------------------
    # SAVE AND LOAD PERSISTENT ALERTS
    # --------------------------------

    save_alerts(alert_records)

    saved_alerts = read_saved_alerts()

    if not saved_alerts.empty:

        alert_df = saved_alerts.copy()

        alert_df = alert_df.sort_values(
            "Time",
            ascending=False
        )

        st.dataframe(
            alert_df,
            width="stretch",
            hide_index=True
        )
        st.download_button(
        label="Download Alert History",
        data=alert_df.to_csv(index=False),
        file_name="satellite_alert_history.csv",
        mime="text/csv"
        )
        st.metric(
            "Total Saved Alerts",
            len(alert_df)
        )

    else:
        st.success("No faults detected in saved alert history.")

    st.caption(
        "Persistent alert history is stored in alerts.csv."
    )

    # --------------------------------
    # DOWNLOAD CSV
    # --------------------------------

    st.subheader("Mission Data Export")

    st.download_button(
        label="⬇️ Download Telemetry CSV",
        data=df.to_csv(index=False).encode("utf-8"),
        file_name="satellite_telemetry.csv",
        mime="text/csv"
    )

    st.caption(
        "Data source: C Satellite Telemetry Simulator | "
        "Dashboard refresh interval: 2 seconds"
    )


# --------------------------------
# RUN DASHBOARD
# --------------------------------

live_dashboard()
