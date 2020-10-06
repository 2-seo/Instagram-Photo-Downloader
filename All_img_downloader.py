import dload
from bs4 import BeautifulSoup
from selenium import webdriver
import time
import os

# 인스타그램 아이디 받기
instagramID = input('ID: ')
url = 'https://www.instagram.com/'

# id로 폴더 생성
path = './img/' + instagramID
os.makedirs(path, exist_ok=True)

# 웹드라이버 파일의 경로
driver = webdriver.Chrome('./chromedriver')
driver.get(url + instagramID)


def scroll():
    # 무한 스크롤
    SCROLL_PAUSE_TIME = 1

    # Get scroll height
    last_height = driver.execute_script("return document.body.scrollHeight")

    while True:
        # Scroll down to bottom
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        # Wait to load page
        time.sleep(SCROLL_PAUSE_TIME)
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight-50);")
        time.sleep(SCROLL_PAUSE_TIME)

        # Calculate new scroll height and compare with last scroll height
        new_height = driver.execute_script("return document.body.scrollHeight")

        if new_height == last_height:
            break

        last_height = new_height


scroll()
# 무한 스크롤 끝 까지 내려간 후 req와 soup설정하기
req = driver.page_source
soup = BeautifulSoup(req, 'html.parser')

# 만약 버튼이 스크롤을 막고 있다면 버튼을 클릭 후 다시 스크
if str(type(soup.select_one('.tCibT'))) != "<class 'NoneType'>":
    driver.find_element_by_css_selector('.tCibT').click()
    scroll()
    req = driver.page_source
    soup = BeautifulSoup(req, 'html.parser')

# 1. 메인 그리드 세부 사진 링크 가져오기
links = soup.select('.v1Nh3')
mainGridImgUrls = []
for link in links:
    tmp = link.select_one('a')['href']
    mainGridImgUrls.append(tmp)

# 세부링크 들어가서 큰 사진 사이즈 링크 구하기
i = 1
for mainGridImgUrl in mainGridImgUrls:
    driver.get('https://www.instagram.com' + mainGridImgUrl)
    req = driver.page_source
    soup = BeautifulSoup(req, 'html.parser')

    links = soup.select('div.pR7Pc > div > div > div > div > ul > li')

    for link in links:
        tmp = link.select_one('.Ckrof > div > div > div > div > img')
        if str(type(tmp)) == "<class 'NoneType'>":
            continue
        imgSrc = tmp['src']

        dload.save(imgSrc, f'img/{instagramID}/{i}.jpeg')
        i += 1

print(i, "개의 이미지 다운로드 완료")
driver.quit()
