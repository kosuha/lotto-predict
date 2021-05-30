#-*- coding: utf-8 -*-

from selenium import webdriver    # 라이브러리에서 사용하는 모듈만 호출
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys    # 키보드 사용
from selenium.webdriver.support.ui import WebDriverWait   # 해당 태그를 기다림
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException    # 태그가 없는 예외 처리
import pandas as pd
import time
import urllib
import random

chromedriver = '/Users/seonhokim/lotto-predict/chromedriver'
options = webdriver.ChromeOptions()
options.add_argument('headless')    # headless chrome 옵션 적용
options.add_argument('disable-gpu')    # GPU 사용 안함
options.add_argument('lang=ko_KR')    # 언어 설정
driver = webdriver.Chrome(chromedriver, options=options) # 옵션 적용

total_list = []

def get_num_win_txt():
    with open('numbers.txt', 'r') as f:
        data = f.read()

    num_list = data.splitlines()

    result = []
    for n in num_list:
        result.append(list(map(int, n.split("\t"))))

    result.reverse()

    return result

def get_lastest():
    url = "https://dhlottery.co.kr/gameResult.do?method=byWin"
    driver.get(url) # 크롤링할 사이트 호출
    print(url)

    lastest = driver.find_element_by_css_selector("#dwrNoList > option:nth-child(1)").text
    return int(lastest)

def get_num_win(num):
    url = f"https://dhlottery.co.kr/gameResult.do?method=byWin&drwNo={num}"
    driver.get(url) # 크롤링할 사이트 호출

    win_num_tag = "#article > div:nth-child(2) > div > div.win_result > div > div.num.win > p > span"
    bonus_num_tag = "#article > div:nth-child(2) > div > div.win_result > div > div.num.bonus > p > span"

    # 3초간 로딩 대기
    element = WebDriverWait(driver, 3).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "#article > div:nth-child(2) > div > div.win_result"))
    )

    win_num_list = []
    win_num_tag_list = driver.find_elements_by_css_selector(win_num_tag)
    for t in win_num_tag_list:
        win_num_list.append(int(t.text))

    bonus_num = driver.find_element_by_css_selector(bonus_num_tag).text
    win_num_list.append(int(bonus_num))

    time.sleep(2)

    return win_num_list

def add_stat(win_num):
    global total_list
    total_list = total_list + win_num

def get_my_num():
    stat = []
    for i in range(1, 46):
        c = total_list.count(i)
        if c != 0:
            stat.append([i, c])
    
    if len(stat) >= 6:
        stat.sort(key=lambda x:-x[1])
        my_num = []
        for s in stat[:2]:  # 추천 몇 개
            my_num.append(s[0])
        
        while True:
            r = random.randrange(1, 46)
            if r in my_num or r in stat[-10:]: # 중복 제거, 확률 낮은 것 제외한 랜덤
                continue
            
            if len(my_num) > 5:
                break
            else:
                my_num.append(r)
            
        return my_num
    else:
        return [1,2,3,4,5,6]
    

def main():
    total_score = 0
    win = {
        1: 0,
        2: 0,
        3: 0,
        4: 0,
        5: 0
    }

    win_num_list = get_num_win_txt()
    lastest = len(win_num_list)

    for i in range(1, lastest + 1):
        print(i)
        win_num = win_num_list[i - 1]
        print(win_num)
        my_num = get_my_num()
        print(my_num)
        score = 0
        same_num = 0
        bouns = 0
        for m in my_num:
            if m in win_num[:6]:
                same_num += 1
            if m == win_num[-1]:
                bouns = 1

        if same_num == 6:
            score = 5
            win[1] = win[1] + 1
        elif same_num == 5 and bouns == 1:
            score = 4
            win[2] = win[2] + 1
        elif same_num == 5:
            score = 3
            win[3] = win[3] + 1
        elif same_num == 4:
            score = 2
            win[4] = win[4] + 1
        elif same_num == 3:
            score = 1
            win[5] = win[5] + 1

        total_score = total_score + score
        add_stat(win_num)

    print(win)
    print(total_score)

main()
driver.quit()
