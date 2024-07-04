#Web Scraping tutorial practice

import requests

# Base URL   
base_url = 'https://books.toscrape.com'

# Send GET request to the base URL   
response = requests.get(base_url)

# Get the HTML content   
html_content = response.text

# Print the HTML content   
print(html_content)  


from selenium import webdriver 
# Set up the webdriver.  
# In this example, we're using the Chrome driver.  
# Replace with the path to your chromedriver  
driver = webdriver.Chrome(executable_path='https://books.toscrape.com')

# Navigate to the website   
driver.get("https://quotes.toscrape.com/js/")
# Get the HTML source   
html_source = driver.page_source
print("HTML source of the website:", html_source)
# Close the browser to free up resources  
driver.close() 

import requests
#requests 라이브러리를 사용해서 get함수를 사용하여 특정 url주소로 요청을 보내고 응답을 받아옴 
r = requests.get('https://www.geeksforgeeks.org/python-programming-language/')
#r은 연결 응답 메세지
print(r)
#r.content는 해당 연결된 웹페이지의 정보
print(r.content)

#beautifulsoup 라이브러리
# 구문 분석 트리,,? 를 안내고 검색하고 변경하기 위한 방법을 제공하는 라이브러리,,/
import requests  #HTTP 요청을 만들기 위한 요청 라이브러리
from bs4 import BeautifulSoup #HTML 구문 분석을 위한 bs4 라이브버리의 BeautifulSoup 클래스
#특정 url에 GET요청을 보내고 응답을 변수 r로 저장
r = requests.get('https://www.geeksforgeeks.org/python-programming-language/')
#응답의 상태 코드 확인
print(r)
#응답의 HTML 내용은 BeautifulSoup를 사용하여 구문 분석됨. soup 변수에 내용 저장.
soup = BeautifulSoup(r.content,'html.parser')

#구문 분석된 HTMP 내용의 미리 정의된 버전을 출력 (보기 쉽게 개발자 도구 페이지처럼 출력)
#print(soup.prettify())

#전제 HTML내용에서 원하는 데이터만 추출 -> 웹페이지에서 원하는 정보가 어디에 있는지 개발자 도구를 통해 탐색
#beautifulsoup의 findall클래스를 활용하여 해당 위치를 찾음
s = soup.find('div',class_='entry-content') #find 함수를 통해 해당 되는 위치 검색
content = s.find_all('p') #find_all 함수를 사용해 모든 p태그 검색
print(content)

#정적 페이지가 아닌 동적페이지에서 정보를 가져올때는 다른 라이브러리 사용 => selenium
#selenium은 크롬, 파이어폭스, 사파리,엣지 등 당야한 브라우저 지원 가능

#크롬의 경우
from selenium import webdriver
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

#resultant list
element_list = []

for page in range(1,3,1):
    page_url = "https://webscraper.io/test-sites/e-commerce/static/computers/laptops?page=" + str(page)
    driver = webdriver.Chrome() #selenium이 업데이트 되서 이제 아무것도 안넣어도 가능하다는데 
    driver.get(page_url)
    title = driver.find_elements(By.CLASS_NAME,"title")
    price = driver.find_elements(By.CLASS_NAME,"price")
    description = driver.find_elements(By.CLASS_NAME,"description")
    rating = driver.find_elements(By.CLASS_NAME,'ratings')

    for i in range(len(title)):
        element_list.append([title[i].text,price[i].text,description[i].text,rating[i].text])
    
print(element_list)
#driver.close()

from selenium import webdriver   
   
# Set up the webdriver.  
# In this example, we're using the Chrome driver.  
# Replace with the path to your chromedriver  
driver = webdriver.Chrome() 
   
# Navigate to the website   
driver.get("https://quotes.toscrape.com/js/")   
   
# Get the HTML source   
html_source = driver.page_source   
print("HTML source of the website:", html_source)   
   
# Close the browser to free up resources  
driver.close()   
