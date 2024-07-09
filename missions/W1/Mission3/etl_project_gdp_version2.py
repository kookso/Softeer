import requests
from bs4 import BeautifulSoup
import pandas as pd
from IPython.display import display, Markdown
import logging
import sqlite3
import json

#로그파일 만들기 
logging.basicConfig(
    filename='elt_project_log.txt', # 로그 파일 이름
    format='%(asctime)s, %(message)s', # 로그 형식
    datefmt='%Y-%b-%d-%H-%M-%S', # 날짜 표기 형식
    level=logging.INFO
    )

def web_scrapping(GDP_url):
    url = GDP_url
    r = requests.get(url)

    # 로그 기록, 추출
    logging.info('Extract start')

    #나라 - GDP 데이터 추출하기
    soup = BeautifulSoup(r.content,'html.parser')
    data = soup.find_all('table',class_ = 'wikitable sortable sticky-header-multi static-row-numbers jquery-tablesorter'.split())
    lst = []
    logging.info('Transform Start : GDP')
    for table in data:
        rows = table.find_all('tr')
        for row in rows:
            cols = row.find_all('td')
            if cols:
                name  = cols[0].find('a')
                if name :
                    country = name.text.strip()
                    if len(cols)>1:
                        gdp_value = cols[1].text.strip().replace(',', '')  # 콤마 제거
                        
                    if len(cols)>3:
                        year = cols[2].text.strip()
                        if gdp_value == '—': 
                            year = '—'
                        lst.append((country,gdp_value,year))
    logging.info('Extract end')
    print('e_end')
    return lst

def transform_to_pd(lst):
    logging.info('Transform start')
    #대륙 - 나라 데이터 추출하기
    continent_url = "https://en.wikipedia.org/wiki/List_of_countries_and_territories_by_the_United_Nations_geoscheme"
    r_continent = requests.get(continent_url)
    logging.info('Extract:Region') #추출로그
    con_soup = BeautifulSoup(r_continent.content,'html.parser')
    con_data = con_soup.find('table',class_ = 'wikitable nowrap sortable mw-datatable jquery-tablesorter'.split())


    con_lst=[]
    if con_data:
        con_datas = con_data.find('tbody')
        con_rows = con_datas.find_all('tr')
        for con_row in con_rows:
            con_cols = con_row.find_all('td')
            if con_cols :
                con_name = con_cols[0].find('a')
                if con_name:
                    con_country = con_name.text.strip()
                    if len(con_cols)>3:
                        region = con_cols[3].text.strip().replace(',', '')  # 콤마 제거
                        con_lst.append((con_country,region))

    # 대륙 - 나라 데이터프레임 생성 및 출력
    df_continent = pd.DataFrame(con_lst, columns=['Country', 'Region'])
    #pd.set_option('display.max_rows', None)
    #print(df_continent)

    #나라 - GDP 데이터프레임 
    df = pd.DataFrame(lst,columns = ['Country','GDP','Year']) #나라이름, gdp, 연도값을 저장한 lst을 데이터 프레임으로 변환
    df['GDP'] = pd.to_numeric(df['GDP'], errors='coerce')/1000 # GDP 값 빌리언 기준으로 바꾸고 숫자로 변환
    df = df.sort_values(by='GDP', ascending=False) # GDP 값 기준으로 내림차순 정렬
    df['GDP'] = df['GDP'].map(lambda x : f'{x:.2f}') #소수점 두자리로 변환

    #대륙-나라-GDP-Year left join해서 데이터 프레임 합치기
    df_Total = pd.merge(df, df_continent, left_on='Country', right_on='Country', how='left')
    pd.set_option('display.max_rows', None) #생략없이 모든 행 출력하기


    #대륙페이지와 GDP 페이지에서 나라 이름이 다르게 표기된 것 추가로 수정
    #pandas로 테이블 만들어서 csv파일로 저장 -> 현재 파일에서 해당 csv파일을 가져와서 판다스 형식을 데이터 프레임으로 가져와서 비교하고 값 넣기,,,,?

    # JSON 파일 불러오기
    with open('add_country_region.json', 'r', encoding='utf-8') as json_file:
        country_region_dict = json.load(json_file)
    # JSON 딕셔너리에서 값 가져와서 업데이트
    for country, region in country_region_dict.items():
        df_Total.loc[df_Total['Country'] == country, 'Region'] = region
    print(df_Total)
    return df_Total

def load_ro_db(df_Total):
    logging.info('saved_json_file')
    #GDP 데이터 프레임 json으로 저장하기
    df_Total.to_json('Countries_by_GDP.json',orient = 'columns')
    logging.info('Load to DB start')
    #추출한 데이터를 데이터베이스에 저장하기
    conn = sqlite3.connect('World_Economies.db') #SQLite3 데이터베이스에 연결 (해당 db가 없으면 새로 생성함)
    cursor = conn.cursor()
    # 'Countries_by_GDP' 테이블 생성
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Countries_by_GDP(
            Country TEXT,
            GDP_USD_billion REAL,
            Region TEXT,
            Year TEXT           
        )
    ''')
    df_Total = df_Total.rename(columns={'GDP':'GDP_USD_billion'}) # 데이터프레임의 열 이름을 데이터베이스에 맞게 변경
    df_Total.to_sql('Countries_by_GDP',conn,if_exists='replace',index=False) # 데이터프레임을 데이터베이스에 저장, 이미 있으면 덮어쓰기
    conn.close() # 데이터베이스 연결 종료
    logging.info('Load to DB end')
    logging.info('Load to World_Economies.db')

def example():
    conn = sqlite3.connect('World_Economies.db')
    cursor = conn.cursor()
    #GDP가 100B USD이상이 되는 국가만 출력
    query1 = '''
        SELECT * 
        FROM Countries_by_GDP 
        WHERE GDP_USD_billion >= 100
    '''
    example1 = pd.read_sql_query(query1,conn)
    print(' ')
    print('#추가 요구 사항 예제 1 : GDP가 100B USD이상이 되는 국가')
    print(example1)

    # 각 Region별로 상위 5개 국가의 GDP 평균 구하기
    query2 = '''
    WITH RankedCountries AS (
        SELECT *,ROW_NUMBER() OVER (PARTITION BY Region ORDER BY GDP_USD_billion DESC) AS rank
        FROM Countries_by_GDP
    )
    SELECT Region, AVG(GDP_USD_billion) as Avg_Top5_GDP
    FROM RankedCountries
    WHERE rank <= 5
    GROUP BY Region
    '''
    example2 = pd.read_sql_query(query2, conn)
    print(' ')
    print('#추가 요구 사항 예제 2 : 각 Region별로 상위 5개 국가의 GDP 평균')
    print(example2)

    conn.close()

if __name__ == '__main__':
    GDP_url = "https://en.wikipedia.org/wiki/List_of_countries_by_GDP_%28nominal%29"
    #Extract
    e_result = web_scrapping(GDP_url)
    t_result = transform_to_pd(e_result)
    load_ro_db(t_result)
    example()