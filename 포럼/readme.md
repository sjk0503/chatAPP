
원래 하나의 파일에 작성했던 코드를 Dami/Dami_generator/functions 3개로 나누었습니다. 

1. Dami.py는 실제로 코드를 실행하는 메인 함수가 있습니다. API_KEY 입력해주세요
2. Dami_gnerator.py는 어시스턴스 id를 생성하는 instructions가 있는 파일입니다. API_KEY 입력해주세요
3. functions.py는 실제로 실행할 함수가 포함되어 있습니다.
4. TMDB2.py는 db구성하는 코드입니다. 수정해서 데이터 수집하는데 시간 이제 오래 안걸립니다. 그런데 수집한 정보의 질이 안좋다는 문제는 해결 못했습니다... 한번 실행하면 1000개의 영화를 가져옵니다. 만약 이 이상의 영화를 한번에 가져오길 원하시면
   ```
   MOVIE_NUMBER=50
   ```
   여기서 50의 숫자를 변경하시면 됩니다. 1 증가 == 영화 20개 증가 입니다. 이때 250이상으로 하면 데이터베이스가 닫혀버리더라구요 여러번 나눠서 해야하는데
   ```
     for page in range(1, count + 1):
        print(f"Selected page: {page}")

        response = requests.get(f"{BASE_URL}/discover/movie", params={
            'api_key': api_key,
            'sort_by': 'vote_count.desc,vote_average.desc',
            'page': page
        })
            
        if response.status_code == 200:
            movies = response.json().get('results', [])
            movie_ids.extend([movie['id'] for movie in movies])
        else:
            print(f"Error: Unable to fetch data from page {page} (status code: {response.status_code})")
    
    return movie_ids
   ```

   여러번 하실땐 여기 range에 (1, count+1) 을 수정해주시면 됩니다.
   예를 들어 MOVIE_NUMBER를 100으로 해서 두번 실행하시면(총 2000개 영화)
   처음엔 (1, count+1), 두번째 돌릴땐 (101, count+101) 로 해주셔야 합니다. 그냥 돌리면 똑같은 영화 다시 가져오는게 됨
