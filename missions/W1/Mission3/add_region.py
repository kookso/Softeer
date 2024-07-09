import json

# 두 개의 리스트
country_name = ['United States','United Kingdom','Russia','South Korea','Turkey','Taiwan','Vietnam','Iran','Hong Kong','Czech Republic','Venezuela','Ivory Coast','Tanzania','DR Congo','Myanmar','Macau','Bolivia','Palestine','Moldova','Brunei','Congo','Laos','North Korea','Kosovo','Syria','Eswatini','Cape Verde','Zanzibar','East Timor','Sint Maarten','São Tomé and Príncipe','Micronesia']
region_name = ['Americas','Europe','Europe','Asia','Asia','Asia','Asia','Asia','Asia','Europe','Americas','Africa','Africa','Africa','Asia','Asia','Americas','Asia','Europe','Asia','Africa','Asia','Asia','Europe','Asia','Africa','Africa','Africa','Asia','Americas','Africa','Oceania']

# 딕셔너리 생성
country_region_dict = dict(zip(country_name, region_name))

# 딕셔너리를 JSON 파일로 저장
with open('add_country_region.json', 'w', encoding='utf-8') as json_file:
    json.dump(country_region_dict, json_file, ensure_ascii=False, indent=4)

print("JSON 파일이 성공적으로 생성되었습니다.")
