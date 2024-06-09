import pandas as pd

def filter_movies_by_criteria(file_path, output_file_path):
    # CSV 파일을 읽어옵니다.
    df = pd.read_csv(file_path)

    # release_date를 datetime 형식으로 변환합니다.
    df['release_date'] = pd.to_datetime(df['release_date'], errors='coerce')

    # 유효한 연령 등급 목록
    valid_ratings = ['12', '15', '12세 이상 관람가', '12이상 관람가','12세 관람가','15세 이상 관람가','15세이상관람가','15세 관람가','ALL','전체관람가','전체 관람가']

    # release_date가 2023-12-01 이후, vote_average가 7점 이상,
    # 그리고 연령 등급이 유효한 값 중 하나인 데이터를 필터링합니다.
    filtered_df = df[
        (df['release_date'] > '2022-01-01') &
        (df['vote_average'] >= 7) &
        (df['kr_rating'].isin(valid_ratings))
    ]

    # 필터링된 데이터를 새로운 CSV 파일로 저장합니다.
    filtered_df.to_csv(output_file_path, index=False)

# 사용 예시
file_path = 'movies.csv'  # 입력 CSV 파일 경로
output_file_path = 'filtered_movies.csv'  # 출력 CSV 파일 경로
filter_movies_by_criteria(file_path, output_file_path)
