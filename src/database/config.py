import streamlit as st

from supabase import create_client ,Client

supabase: Client = create_client(
    st.secrets["supabase_url"],
    st.secrets["superbase_key"]
)