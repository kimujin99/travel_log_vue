import requests
import csv

# REST Countries API 호출
url = "https://restcountries.com/v3.1/all"
response = requests.get(url)
countries = response.json()

# CSV 파일로 데이터 저장
with open('countries.csv', 'w', newline='', encoding='utf-8') as csvfile:
    fieldnames = ['isoAlpha2', 'isoAlpha3', 'englishName', 'koreanName']  # CSV의 헤더 이름
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

    writer.writeheader()  # 헤더 작성

    for country in countries:
        isoAlpha2 = country.get("cca2", "")
        isoAlpha3 = country.get("cca3", "")
        englishName = country.get("name", {}).get("common", "")
        koreanName = country.get("translations", {}).get("kor", {}).get("common", "")

        # 데이터 한 줄씩 작성
        writer.writerow({
            'isoAlpha2': isoAlpha2,
            'isoAlpha3': isoAlpha3,
            'englishName': englishName,
            'koreanName': koreanName
        })

print("CSV 파일로 저장 완료!")