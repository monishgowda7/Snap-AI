import streamlit as st


def footer_home():          # created ❤️ in home page

    st.markdown(f"""
    <div style="
        margin-top: 2rem;
        display: flex;
        gap: 6px;
        justify-content: center;
        align-items: center;
    ">
        <p style="
            font-weight: bold;
            color: white;
            margin: 0;
        ">
            Created with ❤️ by
            <span style="
                font-weight: bold;
                color: #ffe312;
            ">
                  Monish Gowda
            </span>
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    
def footer_dashboard():          # created ❤️ in home page

    st.markdown(f"""
    <div style="
        margin-top: 2rem;
        display: flex;
        gap: 6px;
        justify-content: center;
        align-items: center;
    ">
        <p style="
            font-weight: bold;
            color: black;
            margin: 0;
        ">
            Created with ❤️ by
            <span style="
                font-weight: bold;
                color: #ffe312;
            ">
                  Monish Gowda
            </span>
        </p>
    </div>
    """, unsafe_allow_html=True)