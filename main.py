import os
import streamlit as st
from functions import create_brochure, create_translation_brochure

company_name = st.text_input("브로슈어를 만들 회사의 이름을 입력하세요.")
url = st.text_input("브로슈어를 만들 회사의 URL을 입력하세요.")

if url and company_name:
    brochure = create_brochure(company_name, url)
    st.markdown(brochure)

    language = st.text_input("브로슈어의 번역이 필요한 경우 언어를 입력해주세요.")
    if language:
        trans_brochure = create_translation_brochure(brochure, language)
        st.markdown(trans_brochure)
