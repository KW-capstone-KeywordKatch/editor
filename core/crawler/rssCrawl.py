from bs4 import BeautifulSoup
import requests
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from datetime import datetime



def print_articles(entries, company, get_encoding):
    for entry in entries:
        title = entry["title"]
        link = entry["link"]
        try:
            date = entry["published"]
        except:
            date = "date없음"
        print(title)
        print(link)
        print(date)

        request_headers = {
            'User-Agent': ('Mozilla/5.0 (Windows NT 10.0;Win64; x64)\
                    AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98\
                    Safari/537.36'), }
        article_res = requests.get(link, headers=request_headers)
        article_res.encoding = get_encoding
        soup = BeautifulSoup(article_res.text, "html.parser")


        #### 조선일보 본문 ####
        if company == "chosun":
            # 조선일보의 [뉴스q]는 제외 (중복이다)
            if "뉴스Q" in title:
                continue

            options = webdriver.ChromeOptions()
            options.add_argument('--headless')
            driver = webdriver.Chrome(options=options)
            driver.get(link)
            element = WebDriverWait(driver, 3) \
                .until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'section.article-body')))
            body = driver.find_element(By.CSS_SELECTOR, 'section.article-body')
            body = body.text
            print(body)
            continue


        #### jtbc 본문 ####
        if company == "jtbc" :
            content = soup.find("div", attrs={"class": "article_content"})

        #### 국민일보, 매일경제, 머니투데이, 헤럴드경제, 이데일리, mbn, 동아일보 본문 ####
        elif company in ["kukmin", "maeil", "moneytoday", "herald", "edaily", "mbn", "donga"] :
            content = soup.find("div", attrs={"itemprop": "articleBody"})

            if company == "donga":
                # 동아일보 본문만 남기고 좋아요 구독 같은 거 없애줌
                content.find(attrs={"class": "article_footer"}).decompose()

        #### 한국경제, 경향신문 본문 ####
        elif company == "hankyung" or company == "kyunghyang":
            content = soup.find("div", attrs={"itemprop": "articleBody"})

        #### sbs 본문 ####
        elif company == "sbs":
            content = soup.find("div", attrs={"class": "article_cont_area"})

        #### 한겨래 본문 ####
        elif company == "hankyoreh":
            content = soup.find("div", attrs={"class": "text"})

        #### 파이낸셜 본문 ####
        elif company == "financial":
            content = soup.find("div", attrs={"id": "article_content"})
            if content == None:
                content = soup.find("div", attrs={"itemprop": "articleBody"})

        try:
            print(content.getText().strip())
        except:
            print(title + "     본문 출력 오류남     " + link)

        print()


def save_articles(entries, company, get_encoding):
    # 경로 조정 필요
    file_path = "/Users/hyung/articles/" + company + "/"
    count = 0
    for entry in entries:
        # id 생성
        now = datetime.now()
        id = now.strftime('%Y%m%d%H%M%S')
        id += str(now.microsecond)

        title = entry["title"]
        link = entry["link"]
        try:
            date = entry["published"]
        except:
            date = "date없음"

        try:
            f = open(file_path+company+'-'+id, 'w', encoding=get_encoding)
        except:
            print(file_path+company+'-'+id + "       제목: " + title + "    file open 오류발생")
            continue

        request_headers = {
            'User-Agent': ('Mozilla/5.0 (Windows NT 10.0;Win64; x64)\
                            AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98\
                            Safari/537.36'), }
        try:
            article_res = requests.get(link, headers=request_headers)
            article_res.encoding = get_encoding
            soup = BeautifulSoup(article_res.text, "html.parser")
        except:
            print(title + "      requests.get() 오류발생")
            continue


        #### jtbc 본문 ####
        if company == "jtbc" :
            content = soup.find("div", attrs={"class": "article_content"})

        #### 국민일보, 매일경제, 머니투데이, 헤럴드경제, 이데일리, mbn, 동아일보 본문 ####
        elif company in ["kukmin", "maeil", "moneytoday", "herald", "edaily", "mbn", "donga"] :
            content = soup.find("div", attrs={"itemprop": "articleBody"})

            if company == "donga":
                # 동아일보 본문만 남기고 좋아요 구독 같은 거 없애줌
                content.find(attrs={"class": "article_footer"}).decompose()

        #### 한국경제, 경향신문 본문 ####
        elif company == "hankyung" or company == "kyunghyang":
            content = soup.find("div", attrs={"itemprop": "articleBody"})

        #### sbs 본문 ####
        elif company == "sbs":
            content = soup.find("div", attrs={"class": "article_cont_area"})

        #### 한겨래 본문 ####
        elif company == "hankyoreh":
            content = soup.find("div", attrs={"class": "text"})

        #### 파이낸셜 본문 ####
        elif company == "financial":
            content = soup.find("div", attrs={"id": "article_content"})
            if content == None:
                content = soup.find("div", attrs={"itemprop": "articleBody"})

        try:
            f.write(title + '\n' + content.getText().strip())
            f.close()
            count += 1
        except:
            print(title + "      저장 오류       " + link)

    return count