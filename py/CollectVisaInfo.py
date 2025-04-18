import requests
from bs4 import BeautifulSoup
import csv

# 대상 웹사이트 URL
url = "https://overseas.mofa.go.kr/ru-ko/brd/m_7327/view.do?seq=1341531"

# HTTP 요청 보내기
response = requests.get(url)
response.encoding = "utf-8"  # 한글 깨짐 방지

# 응답이 성공적인지 확인
if response.status_code == 200:
    soup = BeautifulSoup(response.text, "html.parser")
    
    # 테이블 선택
    tbody = soup.select_one("div.datatbl_box table tbody")
    rows = tbody.find_all("tr")[2:]  # 세 번째 행부터 선택
    
    data = []
    for row in rows:
        cols = row.find_all("td")
        if len(cols) >= 2:
            korean_name = cols[0].find("p").find("span").get_text(strip=True)
            VisaRequirement = cols[1].find("p").find("span").get_text(strip=True)
            data.append([korean_name, VisaRequirement])
    
    # CSV 파일로 저장
    with open("visa_info.csv", "w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["KoreanName", "VisaRequirement"])
        writer.writerows(data)
    
    print("CSV 파일 저장 완료!")
else:
    print("페이지 요청 실패:", response.status_code)