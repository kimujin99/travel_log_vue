import requests
import csv

# Geonames API에 접근하는 함수
def get_all_cities_from_geonames():
    username = 'your_geonames_username'  # Geonames 사용자 이름을 여기에 입력
    country_code = 'KR'  # 한국의 국가 코드
    cities = []
    start_row = 0  # 데이터 시작 위치
    max_rows = 1000  # 한 번에 가져올 최대 도시 수

    while True:
        url = f'http://api.geonames.org/citiesJSON?lang=ko&country={country_code}&maxRows={max_rows}&startRow={start_row}&username={username}'
        response = requests.get(url)
        
        if response.status_code == 200:
            data = response.json()
            cities_data = data.get('geonames', [])
            if not cities_data:
                break  # 데이터가 더 이상 없으면 종료
            cities.extend(cities_data)
            start_row += max_rows  # 다음 페이지로 이동
        else:
            print("API 요청 실패")
            break
    return cities

# 데이터를 CSV로 저장하는 함수
def save_to_csv(cities, filename='cities.csv'):
    with open(filename, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['city_name', 'country_sn'])  # 헤더 작성
        
        for city in cities:
            city_name = city['name']
            country_sn = 1  # 한국의 경우 country_sn이 1로 설정 (예시로 사용)
            writer.writerow([city_name, country_sn])

# 메인 실행
if __name__ == '__main__':
    cities = get_all_cities_from_geonames()  # API에서 모든 도시 목록 가져오기
    if cities:
        save_to_csv(cities)  # CSV 파일로 저장
        print("CSV 파일 저장 완료!")
    else:
        print("도시 데이터가 없습니다.")