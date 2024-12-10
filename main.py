import os
import streamlit as st
from functions import get_links

url = st.text_input("브로슈어를 만들 회사의 URL을 입력하세요.")

if url:
    st.write(get_links(url))
