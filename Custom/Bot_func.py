import os
import json
import requests
from bs4 import BeautifulSoup
import pytz
from datetime import datetime


Google_SEARCH_ENGINE_ID="063384971a7b946ac"
Google_API_KEY=" AIzaSyDLftoBTzRrELTssUKamWyGTo4Ntvuo9Bo"


#함수 실행 목록. 모든 함수들은 return 값을 가진다.

#=====================================================================================================================
#정보 업데이트
def update_information(key_name, value):
    file_path = 'character_info.json'
    
    single_values_keys = ["name", "gender", "age"]
    
    # 기존 정보를 읽어옵니다.
    if os.path.exists(file_path):
        with open(file_path, 'r', encoding='utf-8') as f:
            user_data = json.load(f)
    else:
        return "error"

    if key_name in single_values_keys:

        if isinstance(user_data[key_name], str):
            user_data[key_name] = user_data[key_name].split(',')

        #이름/성별/나이의 경우 키워드업데이트(교체)
        user_data[key_name] = value
        save_user_data(file_path, user_data)
        return ""
    else:

        #나머지 키워드
        if value in user_data[key_name]:
            #키워드 중복
            return ""
        
        else:
            #키워드 업데이트(추가)
            values = value.split(',')
            for val in values:
                if val not in user_data[key_name]:
                    user_data[key_name].append(val)                
            save_user_data(file_path, user_data)
            return ""


def save_user_data(file_path, user_data):
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(user_data, f, ensure_ascii=False, indent=4)


#=====================================================================================================================


#=====================================================================================================================

#=====================================================================================================================
# 웹 검색
def do_WebSearch(query):
    current_date, current_time=get_time()
    api_key = Google_API_KEY  # 여기에 실제 API 키를 넣으세요
    search_url = "https://www.googleapis.com/customsearch/v1"
    params = {
        "key": api_key,
        "cx":Google_SEARCH_ENGINE_ID,
        "q": query,
        "lowRange":0,
        "highRange":20
    }
    response = requests.get(search_url, params=params)
    results = response.json()

    return current_date, current_time,results



#=====================================================================================================================

#=====================================================================================================================

#=====================================================================================================================
#날씨 정보

def get_temperature():
    url = "https://search.naver.com/search.naver?sm=tab_hty.top&where=nexearch&ssc=tab.nx.all&query=%EC%96%91%EC%82%B0+%EB%82%A0%EC%94%A8&oquery=%EC%96%91%EC%82%B0+%EB%AF%B8%EC%84%B8%EB%A8%BC%EC%A7%80&tqi=iQoHbwqo1SCssZQRYu4ssssss6w-439288"

    # HTTP GET 요청
    response = requests.get(url)

    # 응답 코드가 200(성공)인 경우에만 진행
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'lxml')

        # 오늘의 날씨
        today_weather = soup.find('div', class_='temperature_text').text

        # 미세먼지 및 초미세먼지
        dust_info = soup.find_all('li', class_='item_today level2')
        micro_dust = dust_info[0].find('span').text.strip()
        ultra_micro_dust = dust_info[1].find('span').text.strip()
        
    return today_weather, micro_dust, ultra_micro_dust
    

#=====================================================================================================================
# 시간 정보
def get_time():
    korea_tz = pytz.timezone('Asia/Seoul')
    
    # 현재 UTC 시간 가져오기
    now_utc = datetime.now(pytz.utc)
    
    # 한국 시간으로 변환
    now_korea = now_utc.astimezone(korea_tz)
    
    # 날짜와 시간 포맷팅
    current_date = now_korea.strftime("%Y-%m-%d")
    current_time = now_korea.strftime("%H:%M:%S")
    
    return current_date, current_time




