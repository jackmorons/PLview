import streamlit as st
from style_utils import inject_custom_css

inject_custom_css()

st.markdown('<div class="hero-title">Powerlifting,<br>Visualized.</div>', unsafe_allow_html=True)

st.markdown('<div style="margin-top: 2rem;"></div>', unsafe_allow_html=True)

st.markdown('<div class="hero-subtitle">Powerlifting is not just about lifting weights, it is about pushing yourself to the limit.</div>', unsafe_allow_html=True)
st.markdown('<div class="hero-subtitle">Explore athletes, records, and data from the world of powerlifting, all in one place.</div>', unsafe_allow_html=True)

st.markdown("---")

# Feature Cards
featureCards = st.columns([0.2, 0.2, 3, 3, 3, 0.2, 0.2])

with featureCards[2]:
    st.page_link("pages/athletes.py", label="**Athletes**", icon="🏋️")
    st.write("Search and explore athlete profiles, competition history, and personal bests.")

with featureCards[3]:
    st.page_link("pages/record.py", label="**Records**", icon="🏆")
    st.write("Discover all-time records across weight classes, federations, and events.")

with featureCards[4]:
    st.page_link("pages/tools.py", label="**Tools**", icon="⚙️")
    st.write("Tools for data analysis and visualization built for coaches and athletes.")

st.markdown("---")
st.markdown("## Gallery", text_alignment="center")
st.markdown('<div style="margin-top: 2rem;"></div>', unsafe_allow_html=True)

# Gallery Grid
gallery = st.columns([0.6, 5, 0.2, 5, 0.4])
with gallery[1]:
    # first
    st.image("https://www.repelbullies.com/cdn/shop/articles/ed_coan_1024x1024.jpg?v=1604244278")
    st.markdown("Ed Coan", text_alignment="center")
    # second
    st.image("https://i.vimeocdn.com/video/677094309-127c02ce090a4117d20683950924113a4e21a27cfeefc4c750ffa111fa1f50b4-d")
    st.markdown("Konstantīns Konstantinovs", text_alignment="center")
    # third
    st.image("https://i.ytimg.com/vi/Q1uwqvNjJQk/maxresdefault.jpg")
    st.markdown("Austin Perkins", text_alignment="center")



with gallery[3]:
    # first
    st.image("https://i0.wp.com/www.muscleandfitness.com/wp-content/uploads/2018/06/andrey-1109.jpg?quality=86&strip=all")
    st.markdown("Andrey Malanichev", text_alignment="center")
    # second
    st.image("https://www.ironcompany.com/media/magefan_blog/2018/04/Larry-Pacifico-Squat.jpg")
    st.markdown("Larry Pacifico", text_alignment="center")
    # third
    st.image("https://i.ytimg.com/vi/pV-hG2tO8LQ/maxresdefault.jpg")
    st.markdown("Jesus Olivares", text_alignment="center")