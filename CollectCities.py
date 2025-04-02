import requests
import csv

# 🔹 1. 국가 코드 목록 CSV 파일 읽기
country_codes = []
with open("countries.csv", mode="r", encoding="utf-8") as file:
    reader = csv.DictReader(file)
    for row in reader:
        country_codes.append(row["isoAlpha2"])

# 🔹 2. CSV 파일 준비
output_filename = "all_cities.csv"

# CSV 파일 헤더 정의
header = ["countryCode", "name", "toponymName"]

with open(output_filename, mode="w", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)
    writer.writerow(header)  # 헤더 추가

# 🔹 3. 국가별 도시 목록 가져와서 CSV 파일에 추가
USERNAME = ""  # Geonames 사용자 이름

def fetch_and_save_cities(country_code):
    url = f"http://api.geonames.org/searchJSON?country={country_code}&featureClass=A&featureCode=ADM1&&maxRows=1000&lang=ko&username={USERNAME}"
    
    response = requests.get(url)
    data = response.json()

    if "geonames" not in data:
        print(f"⚠️ {country_code} 데이터 없음")
        return []

    # 🔹 4. 필요한 데이터 추출
    rows = []
    for city in data["geonames"]:
        rows.append([city["countryCode"], city["name"], city["toponymName"]])

    return rows

# 🔹 5. 모든 국가 코드에 대해 실행하고 파일에 추가 저장
with open(output_filename, mode="a", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)
    
    for country_code in country_codes:
        city_data = fetch_and_save_cities(country_code)
        writer.writerows(city_data)  # CSV 파일에 추가 저장
        print(f"✅ {country_code} 데이터 저장 완료")

print(f"🚀 모든 국가의 도시 데이터를 {output_filename} 파일에 저장 완료!")