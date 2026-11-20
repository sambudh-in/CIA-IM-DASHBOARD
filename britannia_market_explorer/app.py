
import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
import plotly.express as px
import numpy as np
import math

# ============================================================
# BRITANNIA | GLOBAL MARKET INTELLIGENCE SYSTEM
# Complete Streamlit Application
# ============================================================

st.set_page_config(
    page_title="Britannia | Global Market Intelligence",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ============================================================
# 1. PROFESSIONAL DESIGN SYSTEM
# ============================================================

BG = "#07130F"
PANEL = "#10251D"
PANEL2 = "#153328"
GREEN = "#20D68A"
GLOW = "#42E6A0"
WHITE = "#DCE9E2"
MUTED = "#91A99C"
BORDER = "#244638"

st.markdown(f"""
<style>
.stApp {{
    background: radial-gradient(
        ellipse at 50% 20%,
        #10281E 0%,
        #07130F 65%,
        #040B08 100%
    );
    color: {WHITE};
}}

[data-testid="stHeader"] {{
    background: transparent;
}}

[data-testid="stAppViewContainer"] {{
    background: transparent;
}}

.block-container {{
    max-width: 1800px;
    padding: 1.3rem 2rem 2rem 2rem;
}}

h1,h2,h3,h4,p,label {{
    color: {WHITE} !important;
}}

[data-testid="stCaptionContainer"] p {{
    color: {MUTED} !important;
}}

[data-testid="stMetric"] {{
    background: {PANEL};
    border: 1px solid {BORDER};
    border-radius: 14px;
    padding: 18px;
    min-height: 112px;
}}

[data-testid="stMetricLabel"],
[data-testid="stMetricLabel"] p {{
    color: {MUTED} !important;
}}

[data-testid="stMetricValue"] {{
    color: {GLOW} !important;
    font-weight: 750;
}}

[data-testid="stSidebar"] {{
    background: #091810;
}}

[data-baseweb="select"] > div,
[data-baseweb="input"] > div {{
    background: {PANEL};
    border-color: {BORDER};
    color: {WHITE};
}}

.stButton > button {{
    background: {PANEL2};
    color: {WHITE};
    border: 1px solid {BORDER};
    border-radius: 9px;
}}

.stButton > button:hover {{
    border-color: {GREEN};
    color: {GLOW};
}}

[data-testid="stDataFrame"] {{
    border: 1px solid {BORDER};
    border-radius: 10px;
}}

[data-testid="stRadio"] > div {{
    gap: 7px;
}}

[data-testid="stRadio"] label {{
    background: {PANEL};
    border: 1px solid {BORDER};
    border-radius: 8px;
    padding: 7px 12px;
}}

[data-testid="stRadio"] label:hover {{
    border-color: {GREEN};
}}

hr {{
    border-color: {BORDER};
}}

.panel-title {{
    color: {GLOW};
    font-size: 12px;
    font-weight: 800;
    letter-spacing: 1.4px;
    margin-bottom: 12px;
}}

.big-number {{
    color: {GLOW};
    font-size: 29px;
    font-weight: 800;
}}

.status {{
    color: {GREEN};
    font-size: 11px;
    letter-spacing: 1.6px;
    font-weight: bold;
}}

[data-testid="stPlotlyChart"] {{
    background: transparent;
}}

.stSuccess {{
    background: #103326;
    border: 1px solid #205D43;
}}

.stInfo {{
    background: #10251D;
    border: 1px solid #244638;
}}

</style>
""", unsafe_allow_html=True)


# ============================================================
# 2. RESEARCH DATA
# Original project figures retained
# ============================================================

market = pd.DataFrame({
    "Year": [2023, 2024, 2025, 2026, 2027, 2028],
    "Market Size": [4.70, 4.98, 5.28, 5.60, 5.93, 6.29]
})

risk = pd.DataFrame({
    "Factor": [
        "Economic",
        "Political",
        "Legal",
        "Environmental",
        "Cultural",
        "Technological"
    ],
    "Score": [4, 3, 3, 3, 2, 2]
})

segments = pd.DataFrame({
    "Segment": [
        "Indian-origin households",
        "Price-sensitive mass market",
        "Young urban professionals",
        "Health-conscious families",
        "Lunchbox and school-snack parents"
    ],
    "Score": [3.9, 3.2, 2.9, 2.3, 3.7]
})

trade = pd.DataFrame({
    "Trade Flow": [
        "India to South Africa",
        "South Africa to India"
    ],
    "Value": [10, 8]
})


# ============================================================
# 3. CHART FUNCTIONS
# ============================================================

def style_chart(fig, height=340):

    fig.update_layout(
        template="plotly_dark",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(
            color=WHITE,
            family="Arial",
            size=12
        ),
        height=height,
        margin=dict(l=15, r=15, t=35, b=15),
        xaxis=dict(
            gridcolor="#1C392B",
            zerolinecolor=BORDER
        ),
        yaxis=dict(
            gridcolor="#1C392B",
            zerolinecolor=BORDER
        ),
        legend=dict(
            bgcolor="rgba(0,0,0,0)"
        )
    )

    return fig


def show_chart(fig, height=340):

    st.plotly_chart(
        style_chart(fig, height),
        use_container_width=True,
        config={
            "displayModeBar": False,
            "responsive": True
        }
    )


# ============================================================
# 4. ANIMATED INTERACTIVE GLOBE
# Native Canvas renderer
# No Three.js module dependency
# ============================================================


# ============================================================
# 4. ANIMATED INTERACTIVE 3D EARTH
# Accurate Natural Earth country boundaries
# WebGL rendering using Globe.gl
# ============================================================

def display_animated_globe():

    html = r"""
    <!DOCTYPE html>
    <html>
    <head>
    <meta charset="UTF-8">

    <style>
    * {
        box-sizing: border-box;
    }

    html, body {
        margin: 0;
        padding: 0;
        width: 100%;
        height: 100%;
        overflow: hidden;
        background: #07130F;
        font-family: Arial, sans-serif;
    }

    #wrap {
        position: relative;
        width: 100%;
        height: 100%;
        background:
            radial-gradient(
                circle at 50% 45%,
                #102B20 0%,
                #07130F 65%,
                #040B08 100%
            );
    }

    #globeViz {
        width: 100%;
        height: calc(100% - 65px);
        position: relative;
        overflow: hidden;
        cursor: grab;
    }

    #globeViz:active {
        cursor: grabbing;
    }

    #globeViz canvas {
        display: block;
        outline: none;
    }

    .hud {
        position: absolute;
        top: 12px;
        z-index: 10;
        padding: 9px 12px;
        border: 1px solid #244638;
        border-radius: 7px;
        background: rgba(7,19,15,0.88);
        font-size: 10px;
        letter-spacing: 1.2px;
        pointer-events: none;
    }

    #title {
        left: 12px;
        color: #42E6A0;
    }

    #fps {
        right: 12px;
        color: #42E6A0;
    }

    #controls {
        height: 65px;
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 12px;
        flex-wrap: wrap;
        background: #07130F;
        padding: 5px;
    }

    .ctrl {
        background: #10251D;
        color: #42E6A0;
        border: 1px solid #244638;
        border-radius: 7px;
        padding: 9px 14px;
        font-size: 10px;
        font-weight: bold;
        cursor: pointer;
    }

    .ctrl:hover {
        background: #153328;
        border-color: #42E6A0;
    }

    #speed {
        width: 100px;
        accent-color: #20D68A;
        cursor: pointer;
    }

    .control-label {
        color: #91A99C;
        font-size: 10px;
        letter-spacing: .5px;
        white-space: nowrap;
    }

    #loading {
        position: absolute;
        top: 50%;
        left: 50%;
        transform: translate(-50%,-50%);
        color: #42E6A0;
        font-size: 12px;
        letter-spacing: 2px;
        text-align: center;
        z-index: 20;
    }

    #error {
        color: #FF8A80;
        font-size: 12px;
        max-width: 400px;
        line-height: 1.6;
    }

    @media(max-width:600px) {
        #controls {
            gap: 5px;
        }

        .ctrl {
            padding: 7px 9px;
        }

        #speed {
            width: 65px;
        }
    }
    </style>

    </head>

    <body>

    <div id="wrap">

        <div id="title" class="hud">
            BRITANNIA GLOBAL CONNECTIVITY
        </div>

        <div id="fps" class="hud">
            FPS: --
        </div>

        <div id="loading">
            INITIALISING ACCURATE 3D EARTH...
        </div>

        <div id="globeViz"></div>

        <div id="controls">

            <button class="ctrl" id="pause">
                Ⅱ PAUSE
            </button>

            <button class="ctrl" id="reset">
                ↺ RESET VIEW
            </button>

            <span class="control-label">
                ROTATION SPEED
            </span>

            <input
                type="range"
                id="speed"
                min="0"
                max="2"
                step="0.05"
                value="0.42"
            >

            <span class="control-label" id="status">
                GLOBE ACTIVE
            </span>

        </div>

    </div>

    <!-- 3D Globe Library -->
    <script src="https://unpkg.com/globe.gl"></script>

    <!-- TopoJSON Conversion Library -->
    <script src="https://unpkg.com/topojson-client@3"></script>

    <script>

    (async function() {

        "use strict";

        const container = document.getElementById("globeViz");

        const loading = document.getElementById("loading");

        const fpsElement = document.getElementById("fps");

        const status = document.getElementById("status");

        const pauseButton = document.getElementById("pause");

        const speedSlider = document.getElementById("speed");

        let globe = null;

        let running = true;

        let speed = 0.42;

        let frameCount = 0;

        let previousFPS = performance.now();

        // --------------------------------------------
        // COUNTRY COORDINATES
        // --------------------------------------------

        const INDIA = {
            lat: 20.5937,
            lng: 78.9629,
            name: "INDIA"
        };

        const SOUTH_AFRICA = {
            lat: -29.0,
            lng: 24.0,
            name: "SOUTH AFRICA"
        };

        // --------------------------------------------
        // LOAD ACTUAL NATURAL EARTH DATA
        // --------------------------------------------

        try {

            if (typeof Globe !== "function") {
                throw new Error("Globe.gl library failed to load.");
            }

            if (typeof topojson === "undefined") {
                throw new Error("TopoJSON library failed to load.");
            }

            const response = await fetch(
                "https://cdn.jsdelivr.net/npm/world-atlas@2/countries-110m.json"
            );

            if (!response.ok) {
                throw new Error("Unable to download geographic data.");
            }

            const worldData = await response.json();

            // Convert actual geographic boundaries
            // from TopoJSON to GeoJSON.

            const countries = topojson.feature(
                worldData,
                worldData.objects.countries
            ).features;

            // ----------------------------------------
            // CREATE THE 3D GLOBE
            // ----------------------------------------

            globe = Globe()(container)

                .width(container.clientWidth)
                .height(container.clientHeight)

                .backgroundColor("#07130F")

                .showAtmosphere(true)

                .atmosphereColor("#20D68A")

                .atmosphereAltitude(0.18)

                .showGraticules(true)

                // Actual country polygons
                .polygonsData(countries)

                .polygonCapColor(country => {

                    const name = country.properties.name;

                    if (
                        name === "India" ||
                        name === "South Africa"
                    ) {
                        return "#398A5D";
                    }

                    return "#245B3D";

                })

                .polygonSideColor(() => "rgba(15,70,45,0.45)")

                .polygonStrokeColor(() => "#4B9B70")

                .polygonAltitude(country => {

                    const name = country.properties.name;

                    return (
                        name === "India" ||
                        name === "South Africa"
                    ) ? 0.012 : 0.006;

                })

                .polygonsTransitionDuration(0)

                // ------------------------------------
                // TRADE CONNECTION
                // ------------------------------------

                .arcsData([{

                    startLat: INDIA.lat,
                    startLng: INDIA.lng,

                    endLat: SOUTH_AFRICA.lat,
                    endLng: SOUTH_AFRICA.lng,

                }])

                .arcColor(() => "#20D68A")

                .arcStroke(0.8)

                .arcAltitude(0.25)

                .arcDashLength(0.45)

                .arcDashGap(0.25)

                .arcDashAnimateTime(1800)

                // ------------------------------------
                // COUNTRY MARKERS
                // ------------------------------------

                .pointsData([
                    INDIA,
                    SOUTH_AFRICA
                ])

                .pointLat(d => d.lat)

                .pointLng(d => d.lng)

                .pointColor(() => "#42E6A0")

                .pointRadius(0.65)

                .pointAltitude(0.025)

                .pointResolution(16)

                // ------------------------------------
                // COUNTRY LABELS
                // ------------------------------------

                .labelsData([
                    INDIA,
                    SOUTH_AFRICA
                ])

                .labelLat(d => d.lat)

                .labelLng(d => d.lng)

                .labelText(d => d.name)

                .labelSize(1.4)

                .labelColor(() => "#FFFFFF")

                .labelDotRadius(0.4)

                .labelAltitude(0.04)

                .labelResolution(3);

            // ----------------------------------------
            // GLOBE CAMERA AND ROTATION
            // ----------------------------------------

            globe.pointOfView({

                lat: 8,
                lng: 55,
                altitude: 1.8

            }, 0);

            const controls = globe.controls();

            controls.autoRotate = true;

            controls.autoRotateSpeed = speed;

            controls.enableDamping = true;

            controls.dampingFactor = 0.08;

            controls.enableZoom = true;

            // ----------------------------------------
            // RENDER QUALITY
            // ----------------------------------------

            globe.renderer().setPixelRatio(
                Math.min(window.devicePixelRatio || 1, 1.5)
            );

            globe.renderer().setClearColor("#07130F", 1);

            // ----------------------------------------
            // INITIALISE
            // ----------------------------------------

            loading.style.display = "none";

            // ----------------------------------------
            // PAUSE / RESUME
            // ----------------------------------------

            pauseButton.addEventListener("click", () => {

                running = !running;

                controls.autoRotate = running;

                pauseButton.textContent = running
                    ? "Ⅱ PAUSE"
                    : "▶ RESUME";

                status.textContent = running
                    ? "GLOBE ACTIVE"
                    : "ROTATION PAUSED";

            });

            // ----------------------------------------
            // ROTATION SPEED
            // ----------------------------------------

            speedSlider.addEventListener("input", event => {

                speed = Number(event.target.value);

                controls.autoRotateSpeed = speed;

                status.textContent = speed === 0
                    ? "ROTATION STOPPED"
                    : "GLOBE ACTIVE";

            });

            // ----------------------------------------
            // RESET CAMERA
            // ----------------------------------------

            document.getElementById("reset")
                .addEventListener("click", () => {

                    globe.pointOfView({

                        lat: 8,
                        lng: 55,
                        altitude: 1.8

                    }, 700);

                    speedSlider.value = 0.42;

                    speed = 0.42;

                    controls.autoRotateSpeed = speed;

                    running = true;

                    controls.autoRotate = true;

                    pauseButton.textContent = "Ⅱ PAUSE";

                    status.textContent = "GLOBE ACTIVE";

                });

            // ----------------------------------------
            // RESPONSIVE RESIZING
            // ----------------------------------------

            const resizeObserver = new ResizeObserver(() => {

                globe
                    .width(container.clientWidth)
                    .height(container.clientHeight);

            });

            resizeObserver.observe(container);

            // ----------------------------------------
            // FPS MONITOR
            // ----------------------------------------

            function monitorFPS() {

                requestAnimationFrame(monitorFPS);

                frameCount++;

                const now = performance.now();

                if (now - previousFPS >= 1000) {

                    const actualFPS = Math.round(
                        frameCount * 1000 / (now - previousFPS)
                    );

                    fpsElement.textContent =
                        "FPS: " + actualFPS;

                    frameCount = 0;

                    previousFPS = now;

                }

            }

            requestAnimationFrame(monitorFPS);

            // ----------------------------------------
            // FINAL STATUS
            // ----------------------------------------

            status.textContent = "GLOBE ACTIVE";

        }

        catch(error) {

            loading.innerHTML =
                '<div id="error">' +
                'EARTH INITIALISATION FAILED<br><br>' +
                error.message +
                '<br><br>Check your internet connection and reload.' +
                '</div>';

            console.error(error);

        }

    })();

    </script>

    </body>
    </html>
    """

    components.html(
        html,
        height=760,
        scrolling=False
    )


# ============================================================
# END OF ANIMATED INTERACTIVE GLOBE
# ============================================================



# ============================================================
# 5. PROFESSIONAL DASHBOARD HEADER
# ============================================================


# ============================================================
# PROFESSIONAL BRITANNIA HEADER - NATIVE STREAMLIT
# No HTML rendering required
# ============================================================

header_left, header_right = st.columns([3, 1])

with header_left:
    st.markdown(
        "## :green[◇ BRITANNIA]"
    )

    st.caption(
        "GLOBAL MARKET INTELLIGENCE SYSTEM"
    )

with header_right:
    st.markdown(
        "**:green[● INTELLIGENCE MONITOR]**"
    )

    st.markdown(
        "INDIA → SOUTH AFRICA"
    )

st.markdown("---")


# ============================================================
# 6. NAVIGATION
# ============================================================

pages = [
    "Overview",
    "Country & Trade",
    "Risk Intelligence",
    "Market Opportunity",
    "Segmentation & STP",
    "Entry Strategy"
]

selected = st.radio(
    "NAVIGATION",
    pages,
    horizontal=True,
    label_visibility="collapsed"
)

st.markdown("---")


# ============================================================
# 7. OVERVIEW
# ============================================================

if selected == "Overview":

    st.markdown(
        '<div class="status">GLOBAL MARKET MONITORING / EXECUTIVE VIEW</div>',
        unsafe_allow_html=True
    )

    st.title("South Africa | Market Intelligence")

    st.caption(
        "Britannia Industries · International Expansion Analysis · CIA I"
    )

    c1, c2, c3, c4 = st.columns(4)

    c1.metric("POPULATION", "63 Million")
    c2.metric("NOMINAL GDP", "$401 Billion")
    c3.metric("BISCUIT MARKET", "ZAR 4.70B")
    c4.metric("MARKET RISK", "2.8 / 5")

    st.write("")

    left, centre, right = st.columns(
        [0.85, 3.5, 0.85],
        gap="medium"
    )

    # LEFT PANEL

    with left:

        st.markdown(
            '<div class="panel-title">BRITANNIA PROFILE</div>',
            unsafe_allow_html=True
        )

        st.markdown(
            '<div class="big-number">1892</div>',
            unsafe_allow_html=True
        )

        st.caption("Year of establishment")

        st.markdown(
            '<div class="big-number">80+</div>',
            unsafe_allow_html=True
        )

        st.caption("Countries served")

        st.divider()

        st.markdown(
            '<div class="panel-title">LEAD PRODUCT</div>',
            unsafe_allow_html=True
        )

        st.subheader("Marie Gold")

        st.caption("Plain tea-time biscuit")

        st.success("Recommended launch product")

        st.divider()

        st.markdown(
            '<div class="panel-title">COUNTRY INDICATORS</div>',
            unsafe_allow_html=True
        )

        st.write("Unemployment")
        st.markdown("**32.7%**")

        st.write("Inflation")
        st.markdown("**3.1%**")


    # CENTRE PANEL

    with centre:

        st.markdown(
            '<div class="panel-title">GLOBAL MARKET CONNECTIVITY</div>',
            unsafe_allow_html=True
        )

        display_animated_globe()

        st.caption(
            "Animated geographic globe · Drag to rotate · "
            "Scroll to zoom · Adjust rotation speed or pause."
        )

        st.markdown("""
        <div style="
        display:flex;
        justify-content:center;
        gap:20px;
        flex-wrap:wrap;
        font-size:10px;
        color:#91A99C;
        padding:8px;
        ">

        <span style="color:#42E6A0;">
        ● INDIA · HOME MARKET
        </span>

        <span style="color:#20D68A;">
        ● SOUTH AFRICA · TARGET MARKET
        </span>

        <span style="color:#42E6A0;">
        ━ TRADE CONNECTION
        </span>

        </div>
        """, unsafe_allow_html=True)


    # RIGHT PANEL

    with right:

        st.markdown(
            '<div class="panel-title">MARKET PERFORMANCE</div>',
            unsafe_allow_html=True
        )

        st.metric("TARGET SEGMENT SCORE", "3.9 / 5")

        st.metric("INDIA–SA TRADE", "$18 Billion")

        st.metric("TRADE / GDP", "61.6%")

        st.divider()

        st.markdown(
            '<div class="panel-title">STRATEGIC DECISION</div>',
            unsafe_allow_html=True
        )

        st.success("ENTER IN PHASES")

        st.caption(
            "Recommended entry: Local importer-distributor"
        )

        st.caption(
            "Initial target: Indian-origin households"
        )


    # MARKET ANALYTICS

    st.divider()

    st.subheader("MARKET ANALYTICS")

    chart1, chart2 = st.columns(2)

    with chart1:

        st.markdown(
            '<div class="panel-title">SOUTH AFRICA BISCUIT MARKET GROWTH</div>',
            unsafe_allow_html=True
        )

        fig = px.area(
            market,
            x="Year",
            y="Market Size",
            markers=True
        )

        fig.update_traces(
            line_color=GREEN,
            fillcolor="rgba(32,214,138,0.14)",
            marker_color=GLOW
        )

        show_chart(fig)

        st.caption(
            "2023 reported baseline; later years are illustrative estimates."
        )

    with chart2:

        st.markdown(
            '<div class="panel-title">COUNTRY RISK DISTRIBUTION</div>',
            unsafe_allow_html=True
        )

        fig = px.bar(
            risk.sort_values("Score"),
            x="Score",
            y="Factor",
            orientation="h",
            range_x=[0, 5]
        )

        fig.update_traces(marker_color=GREEN)

        show_chart(fig)

        st.caption(
            "Qualitative risk scores from the project dataset."
        )


# ============================================================
# 8. COUNTRY & TRADE
# ============================================================

elif selected == "Country & Trade":

    st.title("Country & Trade Intelligence")

    st.caption(
        "South Africa · Economic and cultural environment"
    )

    a, b, c, d = st.columns(4)

    a.metric("GDP PER CAPITA", "$6,253")
    b.metric("UNEMPLOYMENT", "32.7%")
    c.metric("INFLATION", "3.1%")
    d.metric("TRADE / GDP", "61.6%")

    st.subheader("India–South Africa Bilateral Trade")

    fig = px.bar(
        trade,
        x="Trade Flow",
        y="Value"
    )

    fig.update_traces(marker_color=GREEN)

    show_chart(fig)

    st.caption(
        "Trade values retained from the supplied project dataset; "
        "confirm unit and reporting year."
    )

    st.subheader("Cultural Comparison")

    culture = pd.DataFrame({
        "Dimension": [
            "Power Distance",
            "Individualism",
            "Uncertainty Avoidance"
        ],
        "India": [77, 48, 40],
        "South Africa": [49, 65, 49]
    })

    cultural = culture.melt(
        id_vars="Dimension",
        var_name="Country",
        value_name="Score"
    )

    fig = px.bar(
        cultural,
        x="Dimension",
        y="Score",
        color="Country",
        barmode="group",
        color_discrete_map={
            "India": GREEN,
            "South Africa": "#648B76"
        }
    )

    show_chart(fig)

    st.caption(
        "Cultural values retained from the supplied project dataset."
    )


# ============================================================
# 9. RISK INTELLIGENCE
# ============================================================

elif selected == "Risk Intelligence":

    st.title("International Risk Intelligence")

    st.metric(
        "AVERAGE RISK SCORE",
        f"{risk['Score'].mean():.1f} / 5"
    )

    selected_risks = st.multiselect(
        "Select risk categories",
        risk["Factor"].tolist(),
        default=risk["Factor"].tolist()
    )

    filtered = risk[
        risk["Factor"].isin(selected_risks)
    ]

    if not filtered.empty:

        fig = px.bar(
            filtered,
            x="Score",
            y="Factor",
            orientation="h",
            range_x=[0, 5]
        )

        fig.update_traces(marker_color=GREEN)

        show_chart(fig)

        st.dataframe(
            filtered,
            use_container_width=True,
            hide_index=True
        )

    else:

        st.warning(
            "Select at least one risk category."
        )

    st.caption(
        "Scores are qualitative team assessments. "
        "A score of 5 represents higher risk."
    )


# ============================================================
# 10. MARKET OPPORTUNITY
# ============================================================

elif selected == "Market Opportunity":

    st.title("Market Opportunity Intelligence")

    st.caption(
        "Interactive scenario analysis using the 2023 market baseline."
    )

    growth = st.slider(
        "Annual market growth assumption (%)",
        0.0,
        12.0,
        6.0,
        0.5
    )

    share = st.slider(
        "Illustrative Britannia market share (%)",
        0.1,
        3.0,
        0.5,
        0.1
    )

    year = st.selectbox(
        "Forecast year",
        [2023, 2024, 2025, 2026, 2027, 2028],
        index=3
    )

    market_size = (
        4.70 *
        (1 + growth / 100) ** (year - 2023)
    )

    estimated_sales = market_size * share / 100

    a, b, c = st.columns(3)

    a.metric(
        "PROJECTED MARKET",
        f"ZAR {market_size:.2f}B"
    )

    b.metric(
        "ILLUSTRATIVE SALES",
        f"ZAR {estimated_sales * 1000:.2f}M"
    )

    c.metric(
        "MARKET SHARE",
        f"{share:.1f}%"
    )

    forecast = pd.DataFrame({
        "Year": range(2023, 2029)
    })

    forecast["Market Size"] = (
        4.70 *
        (1 + growth / 100) **
        (forecast["Year"] - 2023)
    )

    fig = px.line(
        forecast,
        x="Year",
        y="Market Size",
        markers=True
    )

    fig.update_traces(
        line_color=GREEN,
        marker_color=GLOW
    )

    show_chart(fig)

    st.caption(
        "Scenario calculation, not actual Britannia revenue or sales."
    )


# ============================================================
# 11. SEGMENTATION & STP
# ============================================================

elif selected == "Segmentation & STP":

    st.title("Customer Segmentation Intelligence")

    st.caption(
        "Customer segment evaluation through weighted scoring."
    )

    fig = px.bar(
        segments.sort_values("Score"),
        x="Score",
        y="Segment",
        orientation="h",
        range_x=[0, 5]
    )

    fig.update_traces(marker_color=GREEN)

    show_chart(fig)

    st.subheader("Weighted Evaluation Matrix")

    criteria = [
        "Segment size",
        "Affordability",
        "Channel reach",
        "Brand awareness",
        "Competition",
        "Profit potential"
    ]

    weights = [20, 20, 20, 20, 10, 10]

    scores = {

        "Indian-origin households": [2, 4, 5, 5, 4, 3],

        "Price-sensitive mass market": [5, 5, 3, 1, 2, 2],

        "Young urban professionals": [3, 3, 4, 2, 2, 3],

        "Health-conscious families": [3, 2, 3, 1, 2, 3],

        "Lunchbox and school-snack parents": [4, 4, 4, 4, 2, 3]

    }

    custom_weights = []

    cols = st.columns(3)

    for i, criterion in enumerate(criteria):

        with cols[i % 3]:

            value = st.number_input(
                criterion,
                min_value=0,
                max_value=100,
                value=weights[i],
                step=5,
                key=f"weight_{i}"
            )

            custom_weights.append(value)

    total = sum(custom_weights)

    if total > 0:

        results = []

        for name, values in scores.items():

            score = sum(
                v * w
                for v, w in zip(values, custom_weights)
            ) / total

            results.append({
                "Segment": name,
                "Weighted Score": score
            })

        result_df = pd.DataFrame(
            results
        ).sort_values(
            "Weighted Score",
            ascending=False
        )

        st.success(
            "Highest ranked segment: " +
            str(result_df.iloc[0]["Segment"])
        )

        st.dataframe(
            result_df.style.format({
                "Weighted Score": "{:.2f}"
            }),
            use_container_width=True,
            hide_index=True
        )

    else:

        st.warning(
            "At least one criterion weight must be positive."
        )

    st.subheader("Recommended Positioning")

    st.info(
        "The light, trusted tea-time biscuit from India "
        "that feels like home."
    )


# ============================================================
# 12. ENTRY STRATEGY
# ============================================================

elif selected == "Entry Strategy":

    st.title("International Market Entry Strategy")

    phases = [

        {
            "Phase": "PHASE 01",
            "Timeline": "0–12 Months",
            "Strategy": "Community Launch",
            "Detail": (
                "Local importer-distributor and "
                "Indian grocery stores."
            )
        },

        {
            "Phase": "PHASE 02",
            "Timeline": "12–24 Months",
            "Strategy": "Supermarket Expansion",
            "Detail": (
                "Target lunchbox parents and larger family packs."
            )
        },

        {
            "Phase": "PHASE 03",
            "Timeline": "24–36 Months",
            "Strategy": "Localisation",
            "Detail": (
                "Evaluate contract manufacturing "
                "and regional expansion."
            )
        }

    ]

    for phase in phases:

        with st.container(border=True):

            st.markdown(
                f"<h3 style='color:{GLOW};'>"
                f"{phase['Phase']}</h3>",
                unsafe_allow_html=True
            )

            st.caption(phase["Timeline"])

            st.subheader(phase["Strategy"])

            st.write(phase["Detail"])

    st.subheader("Marketing Mix · 4Ps")

    a, b = st.columns(2)

    with a:

        st.markdown("**PRODUCT**")

        st.write(
            "Marie Gold with suitable local labelling, "
            "halal certification where required "
            "and suitable pack sizes."
        )

        st.markdown("**PRICE**")

        st.write(
            "Value pricing based on landed cost, "
            "duties, freight and retailer margins."
        )

    with b:

        st.markdown("**PLACE**")

        st.write(
            "Importer-distributor, Indian grocery stores, "
            "supermarkets and online grocery."
        )

        st.markdown("**PROMOTION**")

        st.write(
            "Community events, sampling and "
            "tea-time social campaigns."
        )


# ============================================================
# 13. FOOTER
# ============================================================

st.markdown("---")

st.markdown(f"""
<div style="
text-align:center;
color:{MUTED};
font-size:10px;
letter-spacing:1px;
">

BRITANNIA GLOBAL MARKET INTELLIGENCE SYSTEM

<br><br>

CIA I · INTERNATIONAL MARKETING · SOUTH AFRICA

<br><br>

RESEARCH SNAPSHOT · NOT A LIVE DATA FEED

</div>
""", unsafe_allow_html=True)
