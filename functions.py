import os
import json
import requests
from openai import OpenAI
from bs4 import BeautifulSoup
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
MODEL = "gpt-4o-mini"
openai = OpenAI()

########################### 회사 웹사이트 파싱 및 링크 정리

link_system_prompt = "웹페이지에서 찾을 수 있는 링크 목록이 제공됩니다. \
    다음 중 회사에 관한 브로셔에 포함시킬 링크 중 가장 관련성이 높은 링크를 결정할 수 있습니다\
    정보 페이지, 회사 페이지 또는 경력/일자리 페이지 링크와 같은 링크입니다.\n"
link_system_prompt += "응답은 아래의 예시처럼 JSON 형태로 응답해야만 한다.:"
link_system_prompt += """
{
    "links": [
        {"type": "about page", "url": "https://full.url/goes/here/about"},
        {"type": "careers page": "url": "https://another.full.url/careers"}
    ]
}
"""


class Website:
    def __init__(self, url):
        self.url = url
        response = requests.get(url)
        self.body = response.content
        soup = BeautifulSoup(self.body, "html.parser")
        self.title = soup.title.string if soup.title else "No title found"
        if soup.body:
            for irrelevant in soup.body(
                ["script", "style", "img", "input"]
            ):  # 불필요 태그 자료 삭제
                irrelevant.decompose()
            self.text = soup.body.get_text(
                separator="\n", strip=True
            )  # HTML 태그 제거 후 모든 텍스트 추출
        else:
            self.text = ""
        links = [link.get("href") for link in soup.find_all("a")]
        self.links = [link for link in links if link]

    def get_contents(self):

        return f"Webpage Title:\n{self.title}\nWebpage Contents:\n{self.text}\n\n"


def get_links_user_prompt(website):
    user_prompt = f"{website.url} 사이트의 링크 목록입니다 - "
    user_prompt += "이 중 회사 브로셔에 적합한 웹 링크를 선택해주세요. 이용 약관, 개인정보 보호정책, 이메일 링크는 포함하지 마세요. 응답은 JSON 형식으로 https URL을 포함해주세요.\n"
    user_prompt += "링크 목록 (일부는 상대 링크일 수 있습니다):\n"
    user_prompt += "\n".join(website.links)
    return user_prompt


def get_links(url):
    website = Website(url)
    response = openai.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": link_system_prompt},
            {"role": "user", "content": get_links_user_prompt(website)},
        ],
        response_format={"type": "json_object"},
    )
    result = response.choices[0].message.content
    return json.loads(result)


########################### 회사 브로셔 제작
system_prompt = "너는 회사 웹사이트의 여러 관련 페이지의 내용을 분석하고, \
    잠재 고객, 투자자 및 채용자를 위한 회사의 짧은 브로셔를 작성하는 도우미다. \
    마크다운 형식으로 응답하라. 회사 문화, 고객 및 채용/직무에 대한 정보가 있다면 포함시키세요."


def get_all_details(url):
    result = "Landing page:\n"
    result += Website(url).get_contents()
    links = get_links(url)
    print("Found links:", links)
    for link in links["links"]:
        result += f"\n\n{link['type']}\n"
        result += Website(link["url"]).get_contents()
    return result


def get_brochure_user_prompt(company_name, url):
    user_prompt = f"너는 {company_name}라는 회사를 보고 있다.\n"
    user_prompt += f"여기 랜딩 페이지와 기타 관련 페이지의 내용이 있습니다. 이 정보를 사용하여 회사의 짧은 브로셔를 마크다운 형식으로 작성하세요.\n"
    user_prompt += get_all_details(url)
    user_prompt = user_prompt[:20_000]  # 20,000 글자 이상 자르기
    return user_prompt


def create_brochure(company_name, url):
    response = openai.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": get_brochure_user_prompt(company_name, url)},
        ],
    )
    result = response.choices[0].message.content
    return result


########################### 회사 브로셔 번역
translation_system_prompt = (
    "너는 마크다운으로 작성된 회사의 브로슈어를 번역하는 번역기이다."
)


def translation_user_prompt(brochure, language):
    user_prompt = f"여기 작성된 브로슈어를 {language}로 번역해주세요.\n"
    user_prompt += brochure
    return user_prompt


def create_translation_brochure(brochure, language):
    response = openai.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": translation_system_prompt},
            {"role": "user", "content": translation_user_prompt(brochure, language)},
        ],
    )
    result = response.choices[0].message.content
    return result
