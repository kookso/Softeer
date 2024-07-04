import requests
from bs4 import BeautifulSoup
import pandas as pd
from IPython.display import display, Markdown
import logging
import sqlite3

#로그파일 만들기 
logging.basicConfig(
    filename='elt_project_log.txt', # 로그 파일 이름
    format='%(asctime)s, %(message)s', # 로그 형식
    datefmt='%Y-%b-%d-%H-%M-%S', # 날짜 표기 형식
    level=logging.INFO
    )

url = "https://en.wikipedia.org/wiki/List_of_countries_by_GDP_%28nominal%29"
r = requests.get(url)

 # 로그 기록, 추출
logging.info('Extract:GDP')

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

#나라 - GDP 데이터프레임 
df = pd.DataFrame(lst,columns = ['Country','GDP','Year']) #나라이름, gdp, 연도값을 저장한 lst을 데이터 프레임으로 변환
df['GDP'] = pd.to_numeric(df['GDP'], errors='coerce')/1000 # GDP 값 빌리언 기준으로 바꾸고 숫자로 변환
df = df.sort_values(by='GDP', ascending=False) # GDP 값 기준으로 내림차순 정렬
df['GDP'] = df['GDP'].map(lambda x : f'{x:.2f}') #소수점 두자리로 변환

#웹페이지에서 가져온 데이터를 가공하여 데이터 프레임으로 변환 완료 로그
logging.info('Transform End GDP')


#대륙 - 나라 데이터 추출하기
continent_url = "https://en.wikipedia.org/wiki/List_of_countries_and_territories_by_the_United_Nations_geoscheme"
r_continent = requests.get(continent_url)
logging.info('Extract:Region') #추출로그
con_soup = BeautifulSoup(r_continent.content,'html.parser')
con_data = con_soup.find('table',class_ = 'wikitable nowrap sortable mw-datatable jquery-tablesorter'.split())

logging.info('Transform Start Region')
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

#대륙-나라-GDP-Year left join해서 데이터 프레임 합치기
df_Total = pd.merge(df, df_continent, left_on='Country', right_on='Country', how='left')
pd.set_option('display.max_rows', None) #생략없이 모든 행 출력하기

#대륙페이지와 GDP 페이지에서 나라 이름이 다르게 표기된 것 추가로 수정
country_name = ['United States','United Kingdom','Russia','South Korea','Turkey','Taiwan','Vietnam','Iran','Hong Kong','Czech Republic','Venezuela','Ivory Coast','Tanzania','DR Congo','Myanmar','Macau','Bolivia','Palestine','Moldova','Brunei','Congo','Laos','North Korea','Kosovo','Syria','Eswatini','Cape Verde','Zanzibar','East Timor','Sint Maarten','São Tomé and Príncipe','Micronesia']
region_name = ['Americas','Europe','Europe','Asia','Asia','Asia','Asia','Asia','Asia','Europe','Americas','Africa','Africa','Africa','Asia','Asia','Americas','Asia','Europe','Asia','Africa','Asia','Asia','Europe','Asia','Africa','Africa','Africa','Asia','Americas','Africa','Oceania']
for i in range(len(country_name)):
    df_Total.loc[df_Total['Country'] == country_name[i], 'Region'] = region_name[i]

logging.info('Transform End Region') 

pd.set_option('display.max_rows', None)
#print(df_Total)

#화면 출력 예제 1
print(' ')
print('#화면 출력 예제 1 : GDP가 100B USD이상이 되는 국가')
threshold = 100
filtered_df = df_Total[df_Total['GDP'].astype(float) >= threshold] #GDP가 100B USD이상이 되는 국가만 출력
print(filtered_df)

#화면 출력 예제 2
print(' ')
print('#화면 출력 예제 2 : 각 Region별로 상위 5개 국가의 GDP 평균')
df_Total['GDP'] = pd.to_numeric(df_Total['GDP'], errors='coerce')
region_top5_avg = df_Total.groupby('Region').apply(lambda x: x.nlargest(5, 'GDP')['GDP'].mean()) #각 Region별로 상위 5개 국가의 GDP 평균 계산
print(region_top5_avg)


#GDP 데이터 프레임 json으로 저장하기
df_Total.to_json('Countries_by_GDP.json',orient = 'columns')

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
logging.info('Load to World_Economies.db')

#추가 요구사항 출력하기
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