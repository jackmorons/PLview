import streamlit as st

st.markdown('<div class="hero-title">Powerlifting,<br>Visualized.</div>', unsafe_allow_html=True)
st.markdown('<div class="hero-subtitle">Explore athletes, records, and data from the world of powerlifting, all in one place.</div>', unsafe_allow_html=True)



#col1, col2, col3 = st.columns([1, 1, 1])
#with col2:
#    st.markdown("""
#        <style>
#        div[data-testid="stElementContainer"]:has(.athlete-btn-marker) + div[data-testid="stElementContainer"] button {
#            background-color: rgba(211, 47, 47, 0.1);
#            border: 1px solid #d32f2f;
#            color: #ef5350;
#            transition: all 0.2s ease;
#        }
#        div[data-testid="stElementContainer"]:has(.athlete-btn-marker) + div[data-testid="stElementContainer"] button:hover {
#            background-color: #d32f2f;
#            color: #ffffff;
#            border: 1px solid #d32f2f;
#        }
#        </style>
#        <div class="athlete-btn-marker"></div>
#    """, unsafe_allow_html=True)
#    if st.button("Browse Athletes", type="primary", use_container_width=True):
#        st.switch_page("pages/athletes.py")

#col4, col5, col6 = st.columns([1, 1, 1])
#with col5:
#    st.markdown("""
#        <style>
#        div[data-testid="stElementContainer"]:has(.record-btn-marker) + div[data-testid="stElementContainer"] button {
#            background-color: rgba(25, 118, 210, 0.1);
#            border: 1px solid #1976d2;
#            color: #64b5f6;
#            transition: all 0.2s ease;
#        }
#        div[data-testid="stElementContainer"]:has(.record-btn-marker) + div[data-testid="stElementContainer"] button:hover {
#            background-color: #1976d2;
#            color: #ffffff;
#            border: 1px solid #1976d2;
#        }
#        </style>
#        <div class="record-btn-marker"></div>
#    """, unsafe_allow_html=True)
#    if st.button("Browse Records", type="primary", use_container_width=True):
#        st.switch_page("pages/record.py")

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
    st.image("https://www.repelbullies.com/cdn/shop/articles/ed_coan_1024x1024.jpg?v=1604244278")
    st.markdown("Ed Coan", text_alignment="center")
    st.image("https://i.vimeocdn.com/video/677094309-127c02ce090a4117d20683950924113a4e21a27cfeefc4c750ffa111fa1f50b4-d")
    st.markdown("Konstantīns Konstantinovs", text_alignment="center")
with gallery[3]:
    st.image("https://i0.wp.com/www.muscleandfitness.com/wp-content/uploads/2018/06/andrey-1109.jpg?quality=86&strip=all")
    st.markdown("Andrey Malanichev", text_alignment="center")
    st.image("https://www.ironcompany.com/media/magefan_blog/2018/04/Larry-Pacifico-Squat.jpg")
    st.markdown("Larry Pacifico", text_alignment="center")

