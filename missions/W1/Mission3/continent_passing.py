import requests
from bs4 import BeautifulSoup
import pandas as pd

continent_url = "https://en.wikipedia.org/wiki/List_of_countries_and_territories_by_the_United_Nations_geoscheme"
r_continent = requests.get(continent_url)
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
                if len(con_cols)>1:
                    region = con_cols[1].text.strip().replace(',', '')  # 콤마 제거
                    con_lst.append((con_country,region))


# 결과 출력
print(con_lst)

# 데이터프레임 생성 및 출력
pd.set_option('display.max_rows', None)
df_continent = pd.DataFrame(con_lst, columns=['Country', 'Region'])
print(df_continent)
