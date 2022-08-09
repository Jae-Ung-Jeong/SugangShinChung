from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import urllib.request
import sys
import time
import random


#### temp_id, temp_pw, temp_std_num#####

temp_std_num = ''  # 자신의 학번을 입력하세요
temp_id = ''  # 자신의 아이디를 입력하세요
temp_pw = ''  # 자신의 비밀번호를 입력하세요
# 예를 들어 수꾸목록의 첫번째, 세번째 과목을 수강신청해야하면 [1,3] 같이 써주시면 됩니다. ++8까지 가능합니다.
select_sukku_num = [1, 2, 3, 4]
refresh_limit = 1000  # 새로고침횟수 제한

# 카운터 변수
web_repeated = 1
refresh_cnt = 1

# 서버시간 판단
month = {'Jan': '01', 'Feb': '02', 'Mar': '03', 'Apr': '04', 'May': '05', 'Jun': '06',
         'Jul': '07', 'Aug': '08', 'Sep': '09', 'Oct': '10', 'Nov': '11', 'Dec': '12'}


def time_small():
    return random.random()/10+0.01

# 수강인원 비었는지 체크


def check_empty(driver, grid_num):
    driver.implicitly_wait(time_to_wait=10)
    limit_personnel = driver.find_element(
        By.XPATH, '/html/body/div[3]/div[1]/div[5]/div[2]/div/table/tbody/tr[%d]/td[11]' % (grid_num)).get_attribute('innerText')
    sugang_personnel = driver.find_element(
        By.XPATH, '/html/body/div[3]/div[1]/div[5]/div[2]/div/table/tbody/tr[%d]/td[12]' % (grid_num)).get_attribute('innerText')
    sub_name = driver.find_element(
        By.XPATH, '/html/body/div[3]/div[1]/div[5]/div[2]/div/table/tbody/tr[%d]/td[4]' % (grid_num)).get_attribute('innerText')
    print(sub_name + "\t[ 제한인원 :" + limit_personnel +
          "\t수강인원 :" + sugang_personnel + ']')
    if limit_personnel <= sugang_personnel:
        print("신청할 수 있는 수강꾸러미가 없습니다.")
        return False
    else:
        return True
    


# 수강신청 처리
def submit(_xpath, skku_num):
    # print(_xpath)
    driver.find_element(By.XPATH, str(_xpath)).click()
    try:
        # alert메세지가 올 때까지 최대 600초까지 기다림.
        element = WebDriverWait(driver, 600).until(EC.alert_is_present())
        element.accept()  # 신청하시겠습니까 : 예
        element = WebDriverWait(driver, 600).until(EC.alert_is_present())
        print(element.text)  # 객체를 받으면 text를 반환, 받지 못하면 예외처리
        if "신청되었습" in element.text:
            print("신청성공\n")
            select_sukku_num.remove(skku_num)
        else:
            print("신청실패\n")
        element.accept()
    except:
        print("사이트가 응답하지 않습니다.\n")

options = webdriver.ChromeOptions()
options.add_argument('headless')
options.add_argument('window-size=1920x1080')
options.add_argument("disable-gpu")
# UserAgent값을 바꿔줍시다!
options.add_argument("user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36")
# webdriver 실행
driver = webdriver.Chrome(executable_path='chromedriver',chrome_options=options)
driver.get("https://sugang.knu.ac.kr/login.knu")


try:
    while(1):
        # 웹 로드까지 대기
        driver.implicitly_wait(time_to_wait=1)

        # # 팝업 윈도우 닫고 원래 창으로 포커스 옮기기
        # for i in range(len(driver.window_handles)) :
        #     if(i>=1) :
        #         driver.switch_to.window(driver.window_handles[i])
        #         driver.close()
        # driver.switch_to.window(driver.window_handles[0])

        # 웹 로드 후 로그인 시도
        now = time.time()
        driver.find_element(
            By.XPATH, ('/html/body/div[3]/div/div/div[1]/div/div[2]/div[1]/input')).send_keys(temp_std_num)  # 사이트에 학번 입력
        driver.find_element(
            By.XPATH, ('/html/body/div[3]/div/div/div[1]/div/div[2]/div[2]/input')).send_keys(temp_id)  # 사이트에 아이디 입력
        driver.find_element(
            By.XPATH, ('/html/body/div[3]/div/div/div[1]/div/div[2]/div[3]/input')).send_keys(temp_pw)  # 사이트에 비밀번호 입력
        driver.find_element(
            By.XPATH, ('/html/body/div[3]/div/div/div[1]/div/div[2]/div[5]/div/input')).click()  # 로그인 블럭 클릭

        # 경고창 확인
        status = False  # False이면 Alert 메세지가 없음

        if status:  # AlertText가 있을 경우 종료.
            print("로그인 실패 : exit")
            time.sleep(1)
            driver.quit()
            sys.exit()
        else:  # 없을 경우 로그인
            print("로그인 성공 : Login")
        try:
            ## 여기까지 로그인 ##
            for _ in range(refresh_limit):  # 반복횟수 조절 가능 ,
                driver.implicitly_wait(time_to_wait=10)
                driver.find_element(
                    By.XPATH, ('/html/body/div[3]/div[1]/div[4]/ul/li[2]/a')).click()  # 꾸러미 신청목록 찾기
                for skku_num in select_sukku_num:
                    if skku_num == 1:
                        if(check_empty(driver, skku_num)):
                            submit(
                                '/html/body/div[3]/div[1]/div[5]/div[2]/div/table/tbody/tr[%d]/td[2]/a' % (skku_num), skku_num)
                    elif skku_num == 2:
                        if (check_empty(driver, skku_num)):
                            submit(
                                '/html/body/div[3]/div[1]/div[5]/div[2]/div/table/tbody/tr[%d]/td[2]/a' % (skku_num), skku_num)
                    elif skku_num == 3:
                        if (check_empty(driver, skku_num)):
                            submit(
                                '/html/body/div[3]/div[1]/div[5]/div[2]/div/table/tbody/tr[%d]/td[2]/a' % (skku_num), skku_num)
                    elif skku_num == 4:
                        if (check_empty(driver, skku_num)):
                            submit(
                                '/html/body/div[3]/div[1]/div[5]/div[2]/div/table/tbody/tr[%d]/td[2]/a' % (skku_num), skku_num)
                    elif skku_num == 5:
                        if (check_empty(driver, skku_num)):
                            submit(
                                '/html/body/div[3]/div[1]/div[5]/div[2]/div/table/tbody/tr[%d]/td[2]/a' % (skku_num), skku_num)
                    elif skku_num == 6:
                        if (check_empty(driver, skku_num)):
                            submit(
                                '/html/body/div[3]/div[1]/div[5]/div[2]/div/table/tbody/tr[%d]/td[2]/a' % (skku_num), skku_num)
                    elif skku_num == 7:
                        if (check_empty(driver, skku_num)):
                            submit(
                                '/html/body/div[3]/div[1]/div[5]/div[2]/div/table/tbody/tr[%d]/td[2]/a' % (skku_num), skku_num)
                    elif skku_num == 8:
                        if (check_empty(driver, skku_num)):
                            submit(
                                '/html/body/div[3]/div[1]/div[5]/div[2]/div/table/tbody/tr[%d]/td[2]/a' % (skku_num), skku_num)
                print("현재 반복 : {}".format(refresh_cnt))
                refresh_cnt = refresh_cnt+1
                driver.refresh()
            driver.find_element(
                By.XPATH, ('/html/body/div[2]/div[1]/div/div/div/ul/li[4]/a')).click()  # 로그아웃

        except KeyboardInterrupt:
            print("강제종료")

        last = time.time()
        gap = float(last) - float(now)
        print("{}초 지난 후 다시 로그인했습니다.\n\n".format(gap))
        print("현재 로그인 횟수 : " + str(web_repeated))
        web_repeated = web_repeated+1

except KeyboardInterrupt:
    print("강제종료")
    print("총 로그인 횟수 : " + str(web_repeated))
    print("총 새로고침 횟수 : " + str(refresh_cnt))
    driver.quit()
    sys.exit()
# finally:
#     driver.quit()
#     sys.exit()


# legacy
# def get_severtime(url) :
#     date = urllib.request.urlopen(url).headers['Date'][5:-4]
#     d, m, y, hour, min, sec = date[:2], month[date[3:6]], date[7:11], date[12:14], date[15:17], date[18:]
#     print(f'[{url}]의 서버시간\n{y}년 {m}월 {d}일 {hour}시 {min}분 {sec}초')
#     #date = urllib.request.urlopen('http://www.google.com').headers['Date']
#     #print(date)
#     #now = time.strptime(date, '%a, %d %,"b %Y %H:%M:%S %Z')
#     #print(now)
#     return {"hour":hour,"min":min,"sec":sec}

# 서버타임 확인
    # serverTime=get_severtime("https://sugang.knu.ac.kr/login.knu")
    # print(str(serverTime))
    # print(serverTime["hour"])
    # if(int(serverTime["hour"])==9) :
    #     left_min=60-int(serverTime["min"])
    #     left_sec=60-int(serverTime["sec"])
    #     print(f'접속까지 대기시간 : {left_min}분 {left_sec}초')
    #     time.sleep(60*left_min+left_sec)

# try :
    #     element = WebDriverWait(driver, 0.6).until(EC.alert_is_present()) ## alert메세지가 올 때까지 최대 0.6초까지 기다림.
    #     print(element.text) # 객체를 받으면 text를 반환, 받지 못하면 예외처리
    #     status = True
    #     print("Yes alert") #alert가 있으면 yes alert 출력
    # except :
    #     status = False
    #     print("No alert") #alert 없으면 no alert 출력
