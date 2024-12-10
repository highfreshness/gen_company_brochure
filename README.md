# 회사 브로슈어 생성기
회사 이름과 URL을 입력하면 URL에 존재하는 링크를 해석해 회사의 간단한 브로슈어를 마크다운 형태로 제작


## 사전 준비
1. 가상 환경 생성(conda 또는 venv)
2. 의존성 설치(`pip install -r requirements.txt`)
3. .env 파일 생성 후 OPENAI API KEY 등록(`OPENAI_API_KEY=sk-proj...`)
4. Streamlit 실행 (`streamlit run main.py`)
5. [localhost](http://localhost:8501) 접속

## 실행 화면
- 메인 페이지
![main_page](/media/llm.png)
<br>
- 브로슈어 생성 
  
![create_brochure](/media/llm2.png)
<br>
- 브로슈어 번역

![translation](/media/llm3.png)