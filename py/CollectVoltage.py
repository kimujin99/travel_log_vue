import requests
from bs4 import BeautifulSoup
import csv

# 1. 웹페이지 요청
url = "https://www.tenso.com/kr/static/guide_advice_voltage"
headers = {"User-Agent": "Mozilla/5.0"}  # User-Agent 설정
response = requests.get(url, headers=headers)
response.raise_for_status()

# 2. HTML 파싱
soup = BeautifulSoup(response.text, "html.parser")

# 3. 데이터 추출 (모든 <section> 태그에서 테이블 row 정보 가져오기)
data = []
for section in soup.find_all("section"):
    table = section.find("table")  # 각 section 내 table 찾기
    if table:
        for row in table.find("tbody").find_all("tr"):
            tds = row.find_all("td")
            if len(tds) >= 4:  # 최소한 두 개의 td가 있는지 확인
                COUNTRY_KR_NAME = tds[0].get_text(strip=True)  # 첫 번째 td (국가명)
                VOLTAGE = tds[1].get_text(strip=True)  # 두 번째 td (전압)
                PLUG_TYPE = tds[3].get_text(strip=True)  # 네 번째 td (콘센트타입)
                data.append([COUNTRY_KR_NAME, VOLTAGE, PLUG_TYPE])

# 4. CSV 파일로 저장
csv_filename = "voltage_data.csv"

with open(csv_filename, mode="w", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)
    writer.writerow(["COUNTRY_KR_NAME", "VOLTAGE", "PLUG_TYPE"])  # 헤더 추가
    writer.writerows(data)  # 데이터 저장

print(f"데이터가 {csv_filename} 파일로 저장되었습니다.")