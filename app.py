import streamlit as st
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import time

# Page configuration
st.set_page_config(
    page_title="🌹 Beautiful Rose for Yatakshi",
    page_icon="🌹",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for romantic styling
st.markdown("""
<style>
    .main-header {
        text-align: center;
        color: #FF69B4;
        font-size: 2.5rem;
        font-weight: bold;
        margin-bottom: 1rem;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
    }
    .subtitle {
        text-align: center;
        color: #FFB6C1;
        font-size: 1.2rem;
        font-style: italic;
        margin-bottom: 2rem;
    }
    .romantic-quote {
        text-align: center;
        color: #E6E6FA;
        font-size: 1rem;
        font-style: italic;
        margin-top: 1rem;
        padding: 1rem;
        background: linear-gradient(45deg, rgba(255,182,193,0.1), rgba(255,105,180,0.1));
        border-radius: 10px;
        border: 1px solid rgba(255,182,193,0.3);
    }
    .stSelectbox > div > div {
        background-color: rgba(255,182,193,0.1);
    }
    .gif-container {
        display: flex;
        justify-content: center;
        align-items: center;
        padding: 2rem;
        background: radial-gradient(circle, rgba(25,0,25,0.8), rgba(0,0,0,0.9));
        border-radius: 15px;
        margin: 1rem 0;
    }
    .gif-container img {
        max-width: 100%;
        height: auto;
        border-radius: 10px;
        box-shadow: 0 10px 30px rgba(255,105,180,0.3);
    }
</style>
""", unsafe_allow_html=True)
def create_plotly_rose(bloom_factor=1.0, view_angle=45):
    """Create a natural-looking rose using Mesh3d with gradient shading."""
    fig = go.Figure()

    # Add petals as Mesh3d with gradient intensity
    for x, y, z, ptype in create_optimized_rose(bloom_factor):
        # Compute per-vertex intensity from distance to petal base for subtle color gradient
        envelope = ((np.arctan2(np.sqrt(x**2 + y**2), z) / np.pi) * 0.5 + 0.5).flatten()
        color_base = get_rose_colors(ptype, bloom_factor)
        # dark base tone
        dark = color_base
        light = '#FFD1DC' if ptype=='outer' else '#FFF5F7'
        fig.add_trace(go.Mesh3d(
            x=x.flatten(), y=y.flatten(), z=z.flatten(),
            intensity=envelope,
            colorscale=[[0, dark], [1, light]],
            showscale=False,
            lighting=dict(
                ambient=0.6,
                diffuse=0.7,
                specular=0.1,
                roughness=0.7,
                fresnel=0.1
            ),
            hoverinfo='skip'
        ))

    # Stem and thorns
    (sX, sY, sZ), thorns = create_realistic_stem()
    fig.add_trace(go.Mesh3d(
        x=sX.flatten(), y=sY.flatten(), z=sZ.flatten(),
        color='#2F4F2F',
        lighting=dict(ambient=0.5, diffuse=0.6, specular=0.05, roughness=0.8),
        hoverinfo='skip'
    ))
    for Xth, Yth, Zth in thorns:
        fig.add_trace(go.Mesh3d(
            x=Xth.flatten(), y=Yth.flatten(), z=Zth.flatten(),
            color='#8B4513',
            lighting=dict(ambient=0.5, diffuse=0.6, specular=0.05, roughness=0.8),
            hoverinfo='skip'
        ))

    # Leaves
    leaf_cols = ['#2E8B57', '#3CB371', '#66CDAA']
    for i, (lx, ly, lz) in enumerate(create_elegant_leaves()):
        fig.add_trace(go.Mesh3d(
            x=lx.flatten(), y=ly.flatten(), z=lz.flatten(),
            color=leaf_cols[i],
            opacity=0.9,
            lighting=dict(ambient=0.5, diffuse=0.7, specular=0.05, roughness=0.8),
            hoverinfo='skip'
        ))

    # Layout for realistic look
    fig.update_layout(
        scene=dict(
            xaxis=dict(showticklabels=False, showgrid=False, zeroline=False, showbackground=False),
            yaxis=dict(showticklabels=False, showgrid=False, zeroline=False, showbackground=False),
            zaxis=dict(showticklabels=False, showgrid=False, zeroline=False, showbackground=False),
            bgcolor='rgba(5,5,5,1)',
            camera=dict(
                eye=dict(x=2*np.cos(np.radians(view_angle)), y=2*np.sin(np.radians(view_angle)), z=2),
                up=dict(x=0, y=0, z=1)
            )
        ),
        paper_bgcolor='rgba(5,5,5,1)',
        margin=dict(l=0, r=0, t=50, b=0)
    )

    return fig

GITHUB_RAW_BASE = "https://raw.githubusercontent.com/AtharvVatsal/Rose-For-Yatakshi/main"
GITHUB_GIF_URL = f"{GITHUB_RAW_BASE}/rose.gif"

# Main Streamlit App
def main():
    # Header
    st.markdown('<h1 class="main-header">🌹✨ Interactive Rose for Yatakshi (Niggi) ✨🌹</h1>', unsafe_allow_html=True)
    st.markdown('<p class="subtitle">A digital rose as beautiful and beloved as you! 💖</p>', unsafe_allow_html=True)
    
    # Sidebar controls
    st.sidebar.markdown("### 🌹 Rose Display Options")
    
    # Display mode selection
    display_mode = st.sidebar.selectbox(
        "🎭 Choose Display Mode",
        options=["Interactive 3D Rose", "Animated GIF"],
        help="Select how you'd like to view the rose"
    )
    
    if display_mode == "Interactive 3D Rose":
        # Interactive 3D Rose Controls
        st.sidebar.markdown("### 🌸 3D Rose Controls")
        
        # Bloom factor slider
        bloom_factor = st.sidebar.slider(
            "🌸 Bloom Stage",
            min_value=0.1,
            max_value=1.5,
            value=1.0,
            step=0.1,
            help="Control how much the rose has bloomed"
        )
        
        # Sparkles toggle
        show_sparkles = st.sidebar.checkbox("✨ Show Sparkles", value=True)
        
        # View angle
        view_angle = st.sidebar.slider(
            "👁️ Initial View Angle",
            min_value=0,
            max_value=360,
            value=45,
            step=5,
            help="Set initial view angle (you can rotate interactively!)"
        )
        
        # Interactive controls info
        st.sidebar.markdown("### 🎮 Interactive Controls")
        st.sidebar.markdown("""
        **Mouse Controls:**
        - 🖱️ **Drag** to rotate the rose
        - 🎯 **Scroll** to zoom in/out
        - 📱 **Double-click** to reset view
        - 🎨 **Hover** over elements for details
        """)
        
        # Display the interactive rose
        fig = create_plotly_rose(bloom_factor, show_sparkles, view_angle)
        
        # Dynamic title based on bloom stage
        if bloom_factor < 0.3:
            title = "A budding rose for Yatakshi"
        elif bloom_factor < 0.6:
            title = "Blossoming beautifully"
        elif bloom_factor < 0.9:
            title = "Almost in full bloom"
        else:
            title = "For Yatakshi (Niggi) - A Rose as Beautiful and Beloved as You"
        
        fig.update_layout(title=dict(
            text=title,
            x=0.5,
            font=dict(size=16, color='#FFB6C1', family="Arial Black")
        ))
        
        # Display the interactive rose
        st.plotly_chart(fig, use_container_width=True, config={
            'displayModeBar': True,
            'modeBarButtonsToRemove': ['pan2d', 'lasso2d'],
            'displaylogo': False,
            'toImageButtonOptions': {
                'format': 'png',
                'filename': 'beautiful_rose_for_yatakshi',
                'height': 800,
                'width': 1200,
                'scale': 1
            }
        })
        
        # Stats and info for 3D mode
        st.sidebar.markdown("---")
        st.sidebar.markdown("### 📊 Rose Stats")
        st.sidebar.metric("Bloom Percentage", f"{bloom_factor * 100:.1f}%")
        st.sidebar.metric("Petals Rendered", f"{len(create_optimized_rose(bloom_factor))}")
        st.sidebar.metric("Beauty Level", "∞ (Infinite)")
        st.sidebar.metric("Smoothness", "🚀 Ultra Smooth!")
        
    else:  # Animated GIF mode
         st.markdown("### 🌹 Animated Rose GIF")
        # Display the GIF directly from GitHub
         st.markdown(f"""
        <div class="gif-container">
            <img src="{GITHUB_GIF_URL}" alt="Rose GIF">
        </div>
        """, unsafe_allow_html=True)
    
    # Romantic quote (common for both modes)
    quotes = [
        "Like a rose in full bloom, you bring beauty and joy to my world",
        "Every petal represents a reason why you're special to me",
        "This digital rose will never wilt, just like my appreciation for you",
        "In a garden of friends, you'd be the most beautiful rose",
        "Your smile is more radiant than any flower could ever be"
    ]
    
    if display_mode == "Interactive 3D Rose":
        quote_index = int(bloom_factor * len(quotes)) % len(quotes)
    else:
        quote_index = 0  # Use first quote for GIF mode
    
    st.markdown(f'<div class="romantic-quote">"{quotes[quote_index]}" 💕</div>', unsafe_allow_html=True)
    
    # Footer
    st.markdown("---")
    col1, col2, col3 = st.columns([2, 4, 2])
    with col2:
        st.markdown(
            "<div style='text-align: center; color: #FFB6C1; font-style: italic;'>"
            "Made with 💖 for the most wonderful Yatakshi (Niggi)<br>"
            "🌹 May this rose bring joy to your beautiful face 🌹<br>"
            f"<small>✨ Displaying: {'Interactive 3D Rose' if display_mode == 'Interactive 3D Rose' else 'Animated GIF'} ✨</small>"
            "</div>",
            unsafe_allow_html=True
        )

if __name__ == "__main__":
    main()
