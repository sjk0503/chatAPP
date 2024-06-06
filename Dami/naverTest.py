from bs4 import BeautifulSoup as bs 
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

import sqlite3

# 데이터베이스 연결 (파일로 저장, 메모리에 저장할 수도 있음)


# Chrome 옵션 설정 (비표시 모드)
options = webdriver.ChromeOptions()
options.add_argument('--headless')  # 브라우저를 표시하지 않음
options.add_argument('--disable-gpu')  # GPU 비활성화 (일부 시스템에서 필요)
options.add_argument('--no-sandbox')  # 샌드박스 비활성화 (리눅스에서 필요할 수 있음)
options.add_argument('window-size=1920x1080')  # 창 크기 설정 (해상도 문제 방지)
options.add_argument('--ignore-certificate-errors') #에러 무시
options.add_argument('--ignore-ssl-errors')
driver=webdriver.Chrome(options=options)



screening_list=[]
forthcoming_list=[]


def screening():
    conn = sqlite3.connect('movies.db')
    c = conn.cursor()

    c.execute('DROP TABLE IF EXISTS movies')
    conn.commit()


    # 테이블 생성
    c.execute('''
            CREATE TABLE IF NOT EXISTS movies
            (id INTEGER PRIMARY KEY AUTOINCREMENT, 
            title TEXT, 
            release_date TEXT, )
            ''')
    conn.commit()

    # 네이버 영화 검색 페이지 열기
    driver.get('https://search.naver.com/search.naver?query=현재상영영화')

    # 페이지 로딩 대기
    wait = WebDriverWait(driver, 10)
    while True:
        # 페이지 소스 가져오기
        soup = bs(driver.page_source, 'html.parser')
        
        # 영화 정보 크롤링
        data2 = soup.find('div', {'class': 'card_area _panel'})
        if data2:
            cards = data2.findAll('div', {'class': 'card_item'})
            
            for card in cards:
                title = card.find('a', {'class': 'this_text _text'}).text.replace('\n', '')
                Info= card.find('dl', {'class': 'info_group type_visible'})              
                ReleaseDate=Info.find('dd')
                if ReleaseDate==None: ReleaseDate="미정"
                else: ReleaseDate=ReleaseDate.text.strip()
                
                rating=Info.find('span',{'class':"num"})
                if rating==None: rating="0"
                else: rating=rating.text.strip()

                screening_list.append({'title': title, 'ReleaseDate': ReleaseDate, 'rating':rating})

        
        # 다음 버튼 찾기
        try:
            next_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'a.pg_next._next.on')))
            
            # aria-disabled 속성 확인
            aria_disabled = next_button.get_attribute('aria-disabled')
            if aria_disabled == 'true':
                print("마지막 페이지에 도달했습니다.")
                break
            
            # 다음 버튼 클릭
            next_button.click()
            
            # 페이지가 로드될 시간을 기다리기 위해 잠시 대기
            time.sleep(1)

        except Exception as e:
            print(e)
            break
        
    for movie in screening_list:
        c.execute('''
              INSERT INTO movies (title, release_date, dday)
              VALUES (?, ?, ?)
              ''', (movie['title'], movie['ReleaseDate'], movie['rating']))
        conn.commit()
    
    # 연결 종료
    conn.close()



    # # 크롤링한 영화 정보 출력
    # for movie in screening_list:
    #     print(f"Title: {movie['title']}, Relase Date: {movie['ReleaseDate']}, rating: {movie['rating']}")

    # 브라우저 닫기
    driver.quit()
    
    
    
def forthcoming():
    conn = sqlite3.connect('forthcomming.db')
    c = conn.cursor()

    c.execute('DROP TABLE IF EXISTS forthcomming')
    conn.commit()


    # 테이블 생성
    c.execute('''
            CREATE TABLE IF NOT EXISTS forthcomming
            (id INTEGER PRIMARY KEY AUTOINCREMENT, 
            title TEXT, 
            release_date TEXT, 
            dday INTEGER)
            ''')
    conn.commit()

    # 네이버 영화 검색 페이지 열기
    driver.get('https://search.naver.com/search.naver?query=개봉예정영화')

    # 페이지 로딩 대기
    wait = WebDriverWait(driver, 10)
    while True:
        # 페이지 소스 가져오기
        soup = bs(driver.page_source, 'html.parser')
        
        # 영화 정보 크롤링
        data2 = soup.find('div', {'class': 'card_area _panel'})
        if data2:
            cards = data2.findAll('div', {'class': 'card_item'})
            
            for card in cards:
                dday=card.find('span', class_='icon_dday')
                if dday==None: dday="미정"
                else: dday=dday.text.strip()
                title = card.find('a', {'class': 'this_text _text'}).text
                title=title.replace("\n", "")
                ReleaseDate = card.find('dl', {'class': 'info_group type_visible'}).text
                ReleaseDate=ReleaseDate.replace("\n", "")
                
                
                forthcoming_list.append({'title': title, 'ReleaseDate': ReleaseDate,'dday': dday })
        
        
        # 다음 버튼 찾기
        try:
            next_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'a.pg_next._next.on')))
            
            # aria-disabled 속성 확인
            aria_disabled = next_button.get_attribute('aria-disabled')
            if aria_disabled == 'true':
                print("마지막 페이지에 도달했습니다.")
                break
            
            # 다음 버튼 클릭
            next_button.click()
            
            # 페이지가 로드될 시간을 기다리기 위해 잠시 대기
            time.sleep(1)

        except Exception as e:
            print(e)
            break

    # # 크롤링한 영화 정보 출력
    # print("\n모든 영화 정보:")
    # for movie in forthcoming_list:
    #     print(f"Title: {movie['title']}, Relase Date: {movie['ReleaseDate']}, D-day: {movie['dday']}")
    
    for movie in forthcoming_list:
        c.execute('''
              INSERT INTO forthcomming (title, release_date, dday)
              VALUES (?, ?, ?)
              ''', (movie['title'], movie['ReleaseDate'], movie['dday']))
        conn.commit()
    
    # 연결 종료
    conn.close()

    # 브라우저 닫기
    driver.quit()

forthcoming()