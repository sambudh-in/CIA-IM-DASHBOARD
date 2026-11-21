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
# Updated to match the revised CIA 1 report (21/11/2026)
# ============================================================

# Sweet biscuit market, ZAR billion
# 2023 published (GlobalData); 2024-2028 author's estimate at 6% growth
market = pd.DataFrame({
    "Year": [2023, 2024, 2025, 2026, 2027, 2028],
    "Market Size": [4.70, 4.98, 5.28, 5.60, 5.93, 6.29]
})

# Risk register: likelihood (L) x impact (I), each 1-5
risk = pd.DataFrame({
    "Factor": [
        "Competition from local incumbents and low-cost importers",
        "Import duty, no preferential access (21%)",
        "Ocean freight and shipping disruption",
        "Currency risk (rand volatility)",
        "Payment and counterparty risk",
        "Raw material prices (wheat, sugar, palm oil)",
        "Port and logistics inefficiency",
        "Labelling and regulatory compliance",
        "Weak consumer demand (growth about 1%)"
    ],
    "L": [5, 5, 4, 4, 3, 4, 3, 3, 3],
    "I": [4, 4, 4, 3, 4, 3, 3, 3, 3],
    "Response": [
        "Price-pack architecture; cream, wafer and rusk formats; distributor incentives",
        "Price from landed cost; follow SACU talks; assess local co-packing",
        "Contracted freight, Durban and Cape Town options, buffer stock",
        "Invoice in US$ or hedge; price-review clause",
        "Letters of credit, credit insurance, staged terms",
        "Index-linked price clauses; forward cover",
        "Clearing agent; bonded buffer stock",
        "Pre-clear artwork; verify rules before launch",
        "Entry price packs; trade promotions"
    ]
})

risk["Score"] = risk["L"] * risk["I"]


def risk_level(score):
    if score >= 15:
        return "High"
    if score >= 8:
        return "Medium"
    return "Low"


risk["Level"] = risk["Score"].apply(risk_level)

AVG_RISK = risk["Score"].mean()   # 13.2 out of 25

# Segmentation: five route-to-customer segments
criteria = [
    "Segment size",
    "Growth outlook",
    "Ease of access (listing, duty)",
    "Competitive intensity",
    "Margin potential",
    "Fit with Britannia capability"
]

base_weights = [25, 20, 20, 15, 10, 10]

# Growth-heavy sensitivity case: growth 35%, size 10%
growth_weights = [10, 35, 20, 15, 10, 10]

segment_scores = {
    "A. Modern grocery chains":        [5, 3, 2, 2, 2, 4],
    "B. Wholesale and cash-and-carry": [4, 3, 4, 3, 2, 4],
    "C. Informal trade and spaza":     [4, 3, 3, 2, 3, 5],
    "D. Indian-diaspora grocers":      [2, 2, 5, 4, 4, 5],
    "E. E-commerce and quick commerce": [2, 5, 4, 3, 3, 3]
}


def weighted(values, weights):
    total_w = sum(weights)
    return sum(v * w for v, w in zip(values, weights)) / total_w


segments = pd.DataFrame({
    "Segment": list(segment_scores.keys()),
    "Score": [
        weighted(v, base_weights) for v in segment_scores.values()
    ]
})

# India - South Africa trade, US$ billion
trade_total = pd.DataFrame({
    "Period": ["FY2024-25", "FY2025-26"],
    "Value": [18.00, 15.56]
})

trade_flow = pd.DataFrame({
    "Trade Flow": [
        "Indian exports to South Africa",
        "Indian imports from South Africa"
    ],
    "Value": [7.00, 8.56]
})

# South African HS 1905 imports by supplier, 2023 (share of value, %)
suppliers = pd.DataFrame({
    "Supplier": [
        "India", "Bahrain", "Malaysia", "United Kingdom", "Poland",
        "Spain", "Canada", "Netherlands", "Germany", "Belgium"
    ],
    "Share": [12.9, 11.1, 10.8, 7.0, 6.5, 5.5, 3.7, 3.5, 3.1, 2.9]
})

# Landed cost multiplier: 21% duty, then 15% VAT on duty-paid value
DUTY = 0.21
VAT = 0.15
LANDED_MULTIPLE = (1 + DUTY) * (1 + VAT)   # about 1.39


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
# 5. PROFESSIONAL BRITANNIA HEADER - NATIVE STREAMLIT
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

    c1.metric("POPULATION", "63.5 Million")
    c2.metric("NOMINAL GDP", "$426.4 Billion")
    c3.metric("BISCUIT MARKET", "ZAR 4.70B")
    c4.metric("MARKET RISK", f"{AVG_RISK:.1f} / 25")

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

        st.markdown(
            '<div class="big-number">₹18,858 Cr</div>',
            unsafe_allow_html=True
        )

        st.caption("Consolidated sales, FY26")

        st.divider()

        st.markdown(
            '<div class="panel-title">LEAD PRODUCT</div>',
            unsafe_allow_html=True
        )

        st.subheader("Marie Gold")

        st.caption("Plain tea-time biscuit (HS 1905.31)")

        st.success("Recommended launch product")

        st.divider()

        st.markdown(
            '<div class="panel-title">COUNTRY INDICATORS</div>',
            unsafe_allow_html=True
        )

        st.write("Unemployment")
        st.markdown("**33.6%**")

        st.write("Inflation")
        st.markdown("**4.5%**")


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

        st.metric("TARGET SEGMENT SCORE", "3.45 / 5")

        st.metric("INDIA–SA TRADE", "$15.56 Billion")

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
            "Initial target: Wholesale buyers and "
            "Indian-diaspora grocers"
        )


    # MARKET ANALYTICS

    st.divider()

    st.subheader("MARKET ANALYTICS")

    chart1, chart2 = st.columns(2)

    with chart1:

        st.markdown(
            '<div class="panel-title">SOUTH AFRICA SWEET BISCUIT MARKET GROWTH</div>',
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
            "2023 from GlobalData (ZAR billion); 2024 to 2028 are "
            "the author's estimate at 6% growth."
        )

    with chart2:

        st.markdown(
            '<div class="panel-title">RISK REGISTER SCORES</div>',
            unsafe_allow_html=True
        )

        fig = px.bar(
            risk.sort_values("Score"),
            x="Score",
            y="Factor",
            orientation="h",
            range_x=[0, 25]
        )

        fig.update_traces(marker_color=GREEN)

        fig.update_layout(yaxis_title=None)

        show_chart(fig)

        st.caption(
            "Likelihood × impact, out of 25. High risk is 15 or more. "
            "Scores are the author's judgement."
        )


# ============================================================
# 8. COUNTRY & TRADE
# ============================================================

elif selected == "Country & Trade":

    st.title("Country & Trade Intelligence")

    st.caption(
        "South Africa · Economic, trade and cultural environment"
    )

    a, b, c, d = st.columns(4)

    a.metric("INFLATION (SEP 2026)", "4.5%")
    b.metric("UNEMPLOYMENT (Q2 2026)", "33.6%")
    c.metric("REPO RATE", "7.25%")
    d.metric("TRADE / GDP", "61.6%")

    e, f, g, h = st.columns(4)

    e.metric("REAL GDP GROWTH (2025)", "1.1%")
    f.metric("YOUTH UNEMPLOYMENT", "62.8%")
    g.metric("BELOW US$3.65 A DAY", "34%")
    h.metric("RAND PER US$", "≈ 16.5")

    st.caption(
        "Population 63.52 million (mid-2026) · Urban population 69.3% · "
        "Nominal GDP US$426.4 billion (2025). "
        "Re-check these figures before submission."
    )

    st.subheader("India–South Africa Bilateral Trade")

    t1, t2 = st.columns(2)

    with t1:

        fig = px.bar(
            trade_total,
            x="Period",
            y="Value"
        )

        fig.update_traces(marker_color=GREEN)

        fig.update_layout(yaxis_title="US$ billion")

        show_chart(fig)

        st.caption(
            "Bilateral trade fell 13.6% from US$18.0 billion "
            "in FY2024–25 to US$15.56 billion in FY2025–26."
        )

    with t2:

        fig = px.bar(
            trade_flow,
            x="Trade Flow",
            y="Value"
        )

        fig.update_traces(marker_color=GREEN)

        fig.update_layout(yaxis_title="US$ billion")

        show_chart(fig)

        st.caption(
            "FY2025–26: Indian exports US$7.00 billion, imports "
            "US$8.56 billion, a deficit of about US$1.56 billion "
            "for India."
        )

    st.subheader("Duty and Landed Cost")

    d1, d2, d3, d4 = st.columns(4)

    d1.metric("GENERAL IMPORT DUTY", "21%")
    d2.metric("VAT ON DUTY-PAID VALUE", "15%")
    d3.metric("COST VS IMPORT VALUE", f"{LANDED_MULTIPLE:.2f}x")
    d4.metric("INDIA PREFERENCE", "None yet")

    st.caption(
        "Sweet biscuits (HS 1905.31) face a 21% general duty, while EU, "
        "UK and SADC suppliers enter duty-free. India and SACU signed "
        "Terms of Reference for a preferential trade agreement on "
        "12 August 2026, but negotiations have only begun. "
        "Confirm the duty in the SARS tariff book before costing."
    )

    st.subheader("Import Competition: HS 1905 Bakery Products, 2023")

    fig = px.bar(
        suppliers,
        x="Supplier",
        y="Share"
    )

    fig.update_traces(marker_color=GREEN)

    fig.update_layout(yaxis_title="Share of import value (%)")

    show_chart(fig)

    st.caption(
        "South Africa imported US$100.5 million of HS 1905 products in "
        "2023, of which sweet biscuits were US$46.8 million (46.6%). "
        "India was the largest supplier at 12.9% (US$13.0 million), "
        "ahead of Bahrain (11.1%) and Malaysia (10.8%)."
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
        "Hofstede scores (0–100). South Africa is less hierarchical "
        "and more individualistic than India, so single-serve packs and "
        "'treat yourself' messages fit, and reviews and in-store "
        "sampling persuade more than celebrity endorsement."
    )

    st.info(
        "Language: English-led packaging is practical. "
        "Religion and diet: halal certification matters to Muslim "
        "consumers and vegetarian labelling helps Indian-origin "
        "shoppers. Brand relationship: most South Africans know "
        "Britannia far less than Indian shoppers do, so it must earn "
        "trust through sampling and visibility."
    )


# ============================================================
# 9. RISK INTELLIGENCE
# ============================================================

elif selected == "Risk Intelligence":

    st.title("International Risk Intelligence")

    m1, m2, m3, m4 = st.columns(4)

    m1.metric("AVERAGE RISK SCORE", f"{AVG_RISK:.1f} / 25")
    m2.metric("OVERALL LEVEL", risk_level(AVG_RISK))
    m3.metric("HIGH RISKS", int((risk["Level"] == "High").sum()))
    m4.metric("MEDIUM RISKS", int((risk["Level"] == "Medium").sum()))

    selected_risks = st.multiselect(
        "Select risks",
        risk["Factor"].tolist(),
        default=risk["Factor"].tolist()
    )

    filtered = risk[
        risk["Factor"].isin(selected_risks)
    ]

    if not filtered.empty:

        fig = px.bar(
            filtered.sort_values("Score"),
            x="Score",
            y="Factor",
            orientation="h",
            range_x=[0, 25],
            color="Level",
            color_discrete_map={
                "High": "#C4524F",
                "Medium": "#E0A030",
                "Low": GREEN
            }
        )

        fig.update_layout(yaxis_title=None)

        fig.add_vline(
            x=15,
            line_dash="dash",
            line_color=MUTED,
            annotation_text="High threshold (15)",
            annotation_font_color=MUTED
        )

        show_chart(fig, height=420)

        st.dataframe(
            filtered[
                ["Factor", "L", "I", "Score", "Level", "Response"]
            ],
            use_container_width=True,
            hide_index=True
        )

    else:

        st.warning(
            "Select at least one risk."
        )

    st.caption(
        "Each risk is scored for likelihood (L) and impact (I) from 1 to 5; "
        "score = L × I. High is 15 or more, Medium 8–14, Low below 8. "
        "Scores are the author's judgement from the evidence in the report."
    )

    st.info(
        "In PESTEL terms, duty and labelling are legal-political risks; "
        "rand, demand and raw materials are economic; freight and port "
        "delays are logistics risks. Cultural risk is low. Freight "
        "deserves extra weight because West Asia tensions already "
        "disrupted Britannia's international supply chain."
    )


# ============================================================
# 10. MARKET OPPORTUNITY
# ============================================================

elif selected == "Market Opportunity":

    st.title("Market Opportunity Intelligence")

    st.caption(
        "Interactive scenario analysis using the 2023 sweet biscuit "
        "market baseline (ZAR 4.70 billion, GlobalData)."
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

    rand_rate = st.slider(
        "Rand per US dollar",
        14.0,
        20.0,
        16.5,
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

    sales_zar_m = estimated_sales * 1000

    sales_usd_m = sales_zar_m / rand_rate

    a, b, c, d = st.columns(4)

    a.metric(
        "PROJECTED MARKET",
        f"ZAR {market_size:.2f}B"
    )

    b.metric(
        "ILLUSTRATIVE SALES",
        f"ZAR {sales_zar_m:.1f}M"
    )

    c.metric(
        "IN US DOLLARS",
        f"US$ {sales_usd_m:.2f}M"
    )

    d.metric(
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

    fig.update_layout(yaxis_title="ZAR billion")

    show_chart(fig)

    st.caption(
        "Report case: 6% growth gives about ZAR 5.60 billion in 2026; "
        "a 0.5% share is roughly ZAR 28 million, or about US$1.7 million "
        "at 16.5 rand per dollar. This is the author's estimate, "
        "not a published figure or actual Britannia revenue."
    )

    st.subheader("Product Choice: Britannia Marie Gold")

    p1, p2 = st.columns(2)

    with p1:

        st.markdown("**Why Marie Gold**")

        st.write(
            "South Africa has a growing sweet biscuit category, a "
            "tea-time use occasion that matches the product, and a gap "
            "for affordable, familiar plain biscuits. Marie Gold is "
            "vegetarian and already sold online in South Africa "
            "(248 g at R107, about R43 per 100 g, a cross-border "
            "retail price). Good Day and NutriChoice suit later phases."
        )

        st.markdown("**Gap in the market**")

        st.write(
            "Local leaders compete on cream, chocolate and branded "
            "cookies. A plain, low-fat, vitamin-fortified tea biscuit "
            "at an everyday price is underserved outside Indian "
            "grocery stores."
        )

    with p2:

        st.markdown("**Market indicators**")

        st.write(
            "Wider bakery market: US$2.46 billion in 2025, rising to "
            "US$3.22 billion by 2034 (about 2.95% a year, IMARC). "
            "Hypermarkets and supermarkets hold the highest share of "
            "sweet biscuit sales. Local leaders include Bakers "
            "(the most scanned biscuit brand) and Eet-Sum-Mor."
        )

        st.markdown("**Threats**")

        st.write(
            "Supermarket private labels, local price wars and demand "
            "for lower-sugar products."
        )


# ============================================================
# 11. SEGMENTATION & STP
# ============================================================

elif selected == "Segmentation & STP":

    st.title("Customer Segmentation Intelligence")

    st.caption(
        "Five route-to-customer segments evaluated through weighted "
        "scoring. Scores run from 1 (poor) to 5 (excellent)."
    )

    seg_base = pd.DataFrame({
        "Segment": list(segment_scores.keys()),
        "Base weights": [
            weighted(v, base_weights) for v in segment_scores.values()
        ],
        "Growth-heavy weights": [
            weighted(v, growth_weights) for v in segment_scores.values()
        ]
    })

    seg_long = seg_base.melt(
        id_vars="Segment",
        var_name="Weighting",
        value_name="Weighted Score"
    )

    fig = px.bar(
        seg_long,
        x="Segment",
        y="Weighted Score",
        color="Weighting",
        barmode="group",
        range_y=[0, 5],
        color_discrete_map={
            "Base weights": GREEN,
            "Growth-heavy weights": "#648B76"
        }
    )

    show_chart(fig, height=380)

    st.caption(
        "Wholesale leads on base weights (3.45); e-commerce leads on "
        "growth-heavy weights (3.80, with growth at 35% and size at 10%). "
        "The ranking depends on the weights, and the top three segments "
        "are close under base weights."
    )

    st.subheader("Segmentation Bases")

    bases = pd.DataFrame({
        "Base": [
            "Geographic",
            "Demographic",
            "Psychographic",
            "Behavioural"
        ],
        "Variables used": [
            "Province and urban or township setting; Gauteng, "
            "KwaZulu-Natal and Western Cape are the main metros",
            "Income level, household type and community background, "
            "including the Indian-origin community (about 2.6% of "
            "the population)",
            "Price consciousness, health attitude, comfort with "
            "imported brands",
            "Purchase channel, pack size bought, tea-time use, "
            "brand loyalty"
        ]
    })

    st.dataframe(
        bases,
        use_container_width=True,
        hide_index=True
    )

    st.subheader("Weighted Evaluation Matrix")

    custom_weights = []

    cols = st.columns(3)

    for i, criterion in enumerate(criteria):

        with cols[i % 3]:

            value = st.number_input(
                criterion,
                min_value=0,
                max_value=100,
                value=base_weights[i],
                step=5,
                key=f"weight_{i}"
            )

            custom_weights.append(value)

    total = sum(custom_weights)

    if total > 0:

        results = []

        for name, values in segment_scores.items():

            score = weighted(values, custom_weights)

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

        if total != 100:

            st.caption(
                f"Weights currently add up to {total}%. Scores are "
                "normalised by the total, so rankings stay comparable."
            )

    else:

        st.warning(
            "At least one criterion weight must be positive."
        )

    st.caption(
        "Default weights: size 25%, growth 20%, access 20%, competitive "
        "intensity 15%, margin 10%, capability fit 10%. Competitive "
        "intensity is scored so that higher means less intense."
    )

    st.subheader("Segments")

    segment_table = pd.DataFrame({
        "Segment": [
            "A. Modern grocery chains",
            "B. Wholesale and cash-and-carry",
            "C. Informal trade and spaza shops",
            "D. Indian-diaspora and ethnic grocers",
            "E. E-commerce and quick commerce"
        ],
        "Who they are": [
            "National supermarket groups (Shoprite, Pick n Pay, Spar); "
            "want category fit, margin and promotion funding",
            "Wholesalers supplying spaza shops, caterers and small "
            "retailers; want bulk packs, low prices and reliable supply",
            "Township and rural traders buying small quantities for "
            "cash; price-sensitive",
            "Indian-origin households, mainly in KwaZulu-Natal and "
            "Gauteng; want a familiar taste from home",
            "Younger urban shoppers who value convenience and discovery"
        ],
        "How Britannia reaches them": [
            "Direct listings, usually after a distributor proves "
            "sell-through",
            "Importer-distributor",
            "Wholesalers and van distributors",
            "Specialist importers and community stores",
            "Online marketplaces and grocery apps"
        ]
    })

    st.dataframe(
        segment_table,
        use_container_width=True,
        hide_index=True
    )

    st.info(
        "Decision: target wholesale buyers and diaspora grocers "
        "together in Phase 1, using the diaspora segment to build brand "
        "awareness. Add e-commerce in Phase 2 and approach grocery "
        "chains once sell-through is proven."
    )

    st.subheader("Targeting")

    st.write(
        "Phase 1 uses concentrated targeting: two trade segments "
        "reached through one importer-distributor, which keeps the "
        "budget small. Phase 2 moves to differentiated targeting by "
        "adding e-commerce listings and larger family packs for "
        "grocery chains."
    )

    st.subheader("Recommended Positioning")

    st.info(
        "The light, trusted tea-time biscuit from India that feels "
        "like home."
    )

    st.markdown("**Positioning statement**")

    st.write(
        "For families and tea drinkers in South Africa who want a "
        "familiar taste of home, Britannia Marie Gold is the light, "
        "trusted tea biscuit that a generation grew up with, unlike "
        "local cream and chocolate biscuits that compete on "
        "indulgence rather than everyday habit."
    )

    st.markdown("**Proposed tagline:** \"Tea-time, the way you know it.\"")

    st.markdown("**Points of differentiation**")

    st.write(
        "1. Heritage and trust: a brand founded in 1892 that is part "
        "of Indian family life, which local brands cannot copy."
    )
    st.write(
        "2. Light taste for dipping: a crisp plain biscuit made for "
        "tea, in contrast to heavily flavoured options."
    )
    st.write(
        "3. Range depth: Good Day, Tiger and NutriChoice let Britannia "
        "trade shoppers up later, which a single-product importer "
        "cannot."
    )

    st.caption(
        "Perceptual map: on price and heritage axes, Marie Gold should "
        "sit in the mid-price, high-heritage corner, a space local "
        "brands and premium imports leave largely empty (qualitative "
        "author judgement)."
    )


# ============================================================
# 12. ENTRY STRATEGY
# ============================================================

elif selected == "Entry Strategy":

    st.title("International Market Entry Strategy")

    st.caption(
        "Enter through a local importer-distributor, scale in three "
        "phases, and commit to local production only once demand "
        "is proven."
    )

    st.subheader("Entry Mode Evaluation")

    entry_modes = pd.DataFrame({
        "Entry mode": [
            "Export through a local importer-distributor",
            "Contract manufacturing in South Africa",
            "Joint venture with a local food company",
            "Own subsidiary and plant"
        ],
        "Capital and risk": [
            "Low",
            "Medium",
            "Medium to high",
            "High"
        ],
        "Control": [
            "Medium",
            "Medium",
            "Shared",
            "High"
        ],
        "Verdict": [
            "Chosen for Phase 1",
            "Option for Phase 3 to avoid the 21% duty and cut "
            "currency exposure",
            "Considered once volumes justify it",
            "Too risky before demand is proven"
        ]
    })

    st.dataframe(
        entry_modes,
        use_container_width=True,
        hide_index=True
    )

    st.subheader("Phased Roadmap")

    phases = [

        {
            "Phase": "PHASE 01",
            "Timeline": "0–12 Months",
            "Strategy": "Wholesale and Community Launch",
            "Detail": (
                "Appoint an importer-distributor, supply wholesalers "
                "and diaspora grocers in KwaZulu-Natal and Gauteng. "
                "Gate: repeat orders and a clear landed-cost margin."
            )
        },

        {
            "Phase": "PHASE 02",
            "Timeline": "12–24 Months",
            "Strategy": "Online and Chains",
            "Detail": (
                "Add e-commerce listings and pilot one national chain "
                "with family packs. "
                "Gate: sell-through at or above the category average."
            )
        },

        {
            "Phase": "PHASE 03",
            "Timeline": "24–36 Months",
            "Strategy": "Localisation",
            "Detail": (
                "Explore contract manufacturing or a partnership if no "
                "trade preference has arrived, add a lower-sugar "
                "variant, and use Britannia's Kenya unit as a "
                "reference for African production."
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

    st.caption(
        "Targets are proposals for management to adjust."
    )

    st.subheader("Marketing Mix · 4Ps (Phase 1)")

    a, b = st.columns(2)

    with a:

        st.markdown("**PRODUCT**")

        st.write(
            "Marie Gold with English labelling, halal certification "
            "where needed, and a larger family pack. Recipe and name "
            "stay standard; labels, pack sizes and promotions adapt "
            "locally."
        )

        st.markdown("**PRICE**")

        st.write(
            "Everyday-value pricing set against local tea biscuits "
            "after a full landed-cost calculation including duty, VAT "
            "and freight. The R107 online price is a ceiling to beat."
        )

    with b:

        st.markdown("**PLACE**")

        st.write(
            "Importer-distributor, wholesalers and diaspora grocers, "
            "then online grocery and chains."
        )

        st.markdown("**PROMOTION**")

        st.write(
            "Distributor trade incentives, in-store sampling, Diwali "
            "and community events, and a \"tea-time\" social media "
            "theme."
        )

    st.subheader("Risk Controls")

    st.info(
        "Agree rand or US-dollar pricing with the distributor for "
        "fixed periods, hold limited stock, plan shipping with buffer "
        "time, use credit protection with new buyers, and track "
        "margins monthly."
    )

    st.subheader("Next Step")

    st.success(
        "Confirm duty, halal and labelling rules, then build the "
        "landed-cost model before approaching distributors."
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
