# mobile_styles.py - Mobile optimization and responsive design
import streamlit as st

def add_mobile_optimization():
    """Add mobile optimization CSS"""
    
    mobile_css = """
    <style>
    /* Mobile-first responsive design */
    @media screen and (max-width: 768px) {
        /* Main container adjustments */
        .main .block-container {
            padding: 1rem 0.5rem;
            max-width: 100%;
        }
        
        /* Header adjustments */
        .main-header {
            padding: 1rem 0.5rem;
            margin-bottom: 1rem;
        }
        
        .main-header h1 {
            font-size: 1.8rem;
            line-height: 1.2;
        }
        
        .main-header p {
            font-size: 1rem;
            margin-top: 0.5rem;
        }
        
        /* Metric cards responsive */
        .metric-card {
            padding: 1rem;
            margin: 0.5rem 0;
        }
        
        .metric-value {
            font-size: 1.5rem;
        }
        
        .metric-label {
            font-size: 0.8rem;
        }
        
        /* Button adjustments */
        .stButton > button {
            width: 100%;
            margin: 0.25rem 0;
            padding: 0.75rem 1rem;
            font-size: 1rem;
        }
        
        /* Form elements */
        .stTextInput > div > div > input,
        .stTextArea > div > div > textarea,
        .stSelectbox > div > div > select {
            font-size: 16px; /* Prevents zoom on iOS */
        }
        
        /* Slider adjustments */
        .stSlider > div > div > div > div {
            height: 8px;
        }
        
        /* Tab adjustments */
        .stTabs [data-baseweb="tab"] {
            padding: 0.5rem;
            font-size: 0.9rem;
        }
        
        /* Sidebar adjustments */
        .sidebar .sidebar-content {
            padding: 1rem 0.5rem;
        }
        
        .sidebar .sidebar-content .element-container {
            margin-bottom: 1rem;
        }
        
        /* Chart responsiveness */
        .plotly-graph-div {
            height: 300px !important;
        }
        
        /* Table responsiveness */
        .stDataFrame {
            font-size: 0.8rem;
        }
        
        .stDataFrame table {
            width: 100%;
            overflow-x: auto;
        }
        
        /* Hide non-essential elements on mobile */
        .hide-mobile {
            display: none !important;
        }
        
        /* Show mobile-specific elements */
        .show-mobile {
            display: block !important;
        }
        
        /* Show mobile nav on mobile devices */
        @media (max-width: 768px) {
            .mobile-nav {
                display: flex !important;
            }
        }
        
        /* Mobile navigation */
        .mobile-nav {
            position: fixed;
            bottom: 0;
            left: 0;
            right: 0;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 0.75rem;
            z-index: 1000;
            display: flex;
            justify-content: space-around;
            align-items: center;
            box-shadow: 0 -4px 20px rgba(0,0,0,0.1);
        }
        
        .mobile-nav button {
            background: transparent;
            border: none;
            color: white;
            padding: 0.75rem 0.5rem;
            border-radius: 12px;
            font-size: 0.8rem;
            text-align: center;
            transition: all 0.3s ease;
            min-width: 70px;
            display: flex;
            flex-direction: column;
            align-items: center;
            gap: 0.25rem;
        }
        
        .mobile-nav button:hover {
            background: rgba(255,255,255,0.1);
            transform: translateY(-2px);
        }
        
        .mobile-nav button.active {
            background: rgba(255, 255, 255, 0.2);
        }
        
        /* Touch-friendly spacing */
        .touch-target {
            min-height: 44px;
            min-width: 44px;
            padding: 12px;
        }
        
        /* Mobile-specific layouts */
        .mobile-columns {
            display: flex;
            flex-direction: column;
            gap: 1rem;
        }
        
        /* Responsive text */
        .responsive-text {
            font-size: clamp(0.8rem, 2.5vw, 1.1rem);
            line-height: 1.5;
        }
        
        /* Mobile-optimized cards */
        .mobile-card {
            background: white;
            border-radius: 12px;
            padding: 1rem;
            margin: 0.5rem 0;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
            border-left: 4px solid var(--primary-color);
        }
        
        /* Swipe indicators */
        .swipe-indicator {
            text-align: center;
            color: #666;
            font-size: 0.8rem;
            margin: 0.5rem 0;
        }
        
        /* Mobile charts */
        .mobile-chart {
            height: 250px;
            overflow: hidden;
        }
        
        /* Compact metrics */
        .compact-metric {
            text-align: center;
            padding: 0.5rem;
            background: #f8f9fa;
            border-radius: 8px;
            margin: 0.25rem;
        }
        
        .compact-metric .value {
            font-size: 1.2rem;
            font-weight: bold;
            color: var(--primary-color);
        }
        
        .compact-metric .label {
            font-size: 0.7rem;
            color: #666;
            text-transform: uppercase;
        }
    }
    
    /* Tablet adjustments */
    @media screen and (min-width: 769px) and (max-width: 1024px) {
        .main .block-container {
            padding: 2rem 1rem;
        }
        
        .main-header h1 {
            font-size: 2.2rem;
        }
        
        .metric-card {
            padding: 1.5rem;
        }
        
        .plotly-graph-div {
            height: 400px !important;
        }
    }
    
    /* Desktop optimizations */
    @media screen and (min-width: 1025px) {
        .main .block-container {
            padding: 2rem;
        }
        
        .mobile-nav {
            display: none;
        }
        
        .show-mobile {
            display: none !important;
        }
    }
    
    /* High DPI displays */
    @media (-webkit-min-device-pixel-ratio: 2), (min-resolution: 192dpi) {
        .main-header {
            background-image: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        }
        
        .metric-card {
            border: 1px solid rgba(0,0,0,0.05);
        }
    }
    
    /* Dark mode support */
    @media (prefers-color-scheme: dark) {
        .main {
            background-color: #1a1a1a;
            color: #ffffff;
        }
        
        .metric-card {
            background-color: #2d2d2d;
            color: #ffffff;
            border-left-color: #4a9eff;
        }
        
        .mobile-card {
            background-color: #2d2d2d;
            color: #ffffff;
        }
    }
    
    /* Accessibility improvements */
    @media (prefers-reduced-motion: reduce) {
        * {
            animation-duration: 0.01ms !important;
            animation-iteration-count: 1 !important;
            transition-duration: 0.01ms !important;
        }
    }
    
    /* High contrast mode */
    @media (prefers-contrast: high) {
        .main-header {
            background: #000000;
            color: #ffffff;
        }
        
        .metric-card {
            border: 2px solid #000000;
            background: #ffffff;
            color: #000000;
        }
        
        .stButton > button {
            border: 2px solid #000000;
        }
    }
    
    /* Landscape mobile orientation */
    @media screen and (max-width: 768px) and (orientation: landscape) {
        .main-header {
            padding: 0.5rem;
        }
        
        .main-header h1 {
            font-size: 1.5rem;
        }
        
        .mobile-nav {
            display: none;
        }
        
        .plotly-graph-div {
            height: 200px !important;
        }
    }
    </style>
    """
    
    st.markdown(mobile_css, unsafe_allow_html=True)

def show_mobile_navigation():
    """Show mobile navigation bar with clear labels"""
    mobile_nav = """
    <div class="mobile-nav hide-mobile">
        <button onclick="scrollToSection('knowledge')" class="touch-target">
            🔬<br><span style="font-size: 0.7rem;">Knowledge</span>
        </button>
        <button onclick="scrollToSection('reactor')" class="touch-target">
            ⚛️<br><span style="font-size: 0.7rem;">Reactor</span>
        </button>
        <button onclick="scrollToSection('policy')" class="touch-target">
            🌍<br><span style="font-size: 0.7rem;">Policy</span>
        </button>
        <button onclick="scrollToSection('realtime')" class="touch-target">
            🌐<br><span style="font-size: 0.7rem;">Live Data</span>
        </button>
    </div>
    
    <script>
    function scrollToSection(section) {
        const element = document.querySelector('[data-testid="stTabs"]');
        if (element) {
            element.scrollIntoView({ behavior: 'smooth' });
        }
    }
    
    // Add touch event listeners for mobile
    document.addEventListener('DOMContentLoaded', function() {
        // Add swipe gestures for mobile
        let startX = 0;
        let startY = 0;
        
        document.addEventListener('touchstart', function(e) {
            startX = e.touches[0].clientX;
            startY = e.touches[0].clientY;
        });
        
        document.addEventListener('touchmove', function(e) {
            if (!startX || !startY) return;
            
            let endX = e.touches[0].clientX;
            let endY = e.touches[0].clientY;
            
            let diffX = startX - endX;
            let diffY = startY - endY;
            
            if (Math.abs(diffX) > Math.abs(diffY)) {
                if (diffX > 0) {
                    // Swipe left - next tab
                    console.log('Swipe left detected');
                } else {
                    // Swipe right - previous tab
                    console.log('Swipe right detected');
                }
            }
            
            startX = 0;
            startY = 0;
        });
    });
    </script>
    """
    
    st.markdown(mobile_nav, unsafe_allow_html=True)

def create_mobile_friendly_metrics(data, title="Metrics"):
    """Create mobile-friendly metrics display"""
    if not data:
        return
    
    st.markdown(f"### 📊 {title}")
    
    # Create responsive grid
    cols = st.columns(min(len(data), 4))
    
    for i, (key, value) in enumerate(data.items()):
        with cols[i % len(cols)]:
            st.markdown(f"""
            <div class="compact-metric">
                <div class="value">{value}</div>
                <div class="label">{key}</div>
            </div>
            """, unsafe_allow_html=True)

def create_mobile_chart(fig, title="Chart"):
    """Create mobile-optimized chart"""
    st.markdown(f"### 📈 {title}")
    st.markdown('<div class="mobile-chart">', unsafe_allow_html=True)
    st.plotly_chart(fig, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

def show_mobile_swipe_instructions():
    """Show swipe instructions for mobile users"""
    st.markdown("""
    <div class="swipe-indicator show-mobile">
        ← Swipe left/right to navigate between tabs →
    </div>
    """, unsafe_allow_html=True)

def optimize_for_mobile():
    """Main function to optimize the entire app for mobile"""
    add_mobile_optimization()
    
    # Add viewport meta tag for mobile
    st.markdown("""
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    """, unsafe_allow_html=True)
    
    # Add mobile-specific JavaScript
    mobile_js = """
    <script>
    // Detect mobile device
    function isMobile() {
        return /Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(navigator.userAgent);
    }
    
    // Add mobile class to body
    if (isMobile()) {
        document.body.classList.add('mobile-device');
        
        // Optimize for mobile performance
        const images = document.querySelectorAll('img');
        images.forEach(img => {
            img.style.maxWidth = '100%';
            img.style.height = 'auto';
        });
        
        // Add touch feedback
        const buttons = document.querySelectorAll('.stButton button');
        buttons.forEach(button => {
            button.addEventListener('touchstart', function() {
                this.style.transform = 'scale(0.95)';
            });
            
            button.addEventListener('touchend', function() {
                this.style.transform = 'scale(1)';
            });
        });
    }
    
    // Handle orientation change
    window.addEventListener('orientationchange', function() {
        setTimeout(function() {
            window.dispatchEvent(new Event('resize'));
        }, 100);
    });
    </script>
    """
    
    st.markdown(mobile_js, unsafe_allow_html=True)
