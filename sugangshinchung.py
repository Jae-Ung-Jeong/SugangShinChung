from selenium import webdriver
from selenium.common import exceptions
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By


import sys
import time

#### temp_id, temp_pw, temp_std_num#####
TEMP_STD_NUM = '2018112874'  # 자신의 학번을 입력하세요
TEMP_STD_ID = 'qkrrjsgk79'  # 자신의 아이디를 입력하세요
TEMP_STD_PW = '@pk3721204'  # 자신의 비밀번호를 입력하세요

# 예를 들어 수꾸목록의 첫번째, 세번째 과목을 수강신청해야하면 [1,3] 같이 써주시면 됩니다. ++8까지 가능합니다.
select_sukku_num = [1, 2, 3, 4]
refresh_limit = 100  # 새로고침횟수 제한

# 카운터 변수
web_repeated = 1
refresh_cnt = 1

# params : 성능 조절 파라미터
POLL_FREQ = 0.01

# webdriver option params
options = webdriver.ChromeOptions()
prefs = {'profile.default_content_setting_values': {'cookies': 2, 'images': 2,
                                                    'plugins': 2, 'popups': 2, 'geolocation': 2,
                                                    'notifications': 2, 'auto_select_certificate': 2,
                                                    'fullscreen': 2,
                                                    'mouselock': 2, 'mixed_script': 2,
                                                    'media_stream': 2,
                                                    'media_stream_mic': 2, 'media_stream_camera': 2,
                                                    'protocol_handlers': 2,
                                                    'ppapi_broker': 2, 'automatic_downloads': 2,
                                                    'midi_sysex': 2,
                                                    'push_messaging': 2, 'ssl_cert_decisions': 2,
                                                    'metro_switch_to_desktop': 2,
                                                    'protected_media_identifier': 2, 'app_banner': 2,
                                                    'site_engagement': 2,
                                                    'durable_storage': 2}}
options.add_experimental_option('prefs', prefs)
options.add_argument('headless')
options.add_argument("start-maximized")
options.add_argument("disable-infobars")
options.add_argument("--disable-extensions")
options.add_argument('window-size=1920x1080')
options.add_argument("disable-gpu")
options.add_experimental_option("excludeSwitches", ["enable-logging"])

# 수강인원 비었는지 체크


def check_empty(driver, skku_num):
    limit_personnel = WebDriverWait(driver, timeout=10, poll_frequency=POLL_FREQ).until(
        EC.presence_of_element_located(
            (By.XPATH, '/html/body/div[3]/div[1]/div[5]/div[2]/div/table/tbody/tr[%d]/td[11]' % (skku_num)))
    ).get_attribute('innerText')
    sugang_personnel, sub_name = driver.find_element(
        By.XPATH, '/html/body/div[3]/div[1]/div[5]/div[2]/div/table/tbody/tr[%d]/td[12]' % (skku_num)).get_attribute('innerText'), driver.find_element(
        By.XPATH, '/html/body/div[3]/div[1]/div[5]/div[2]/div/table/tbody/tr[%d]/td[4]' % (skku_num)).get_attribute('innerText')
    print(sub_name + "\t[ 제한인원 :" + limit_personnel +
          "\t수강인원 :" + sugang_personnel + ']')
    if limit_personnel <= sugang_personnel:
        print("신청할 수 있는 수강꾸러미가 없습니다.")
        return False
    else:
        return True


# 수강신청 처리
def submit(driver, _xpath, skku_num):
    submit_element = WebDriverWait(driver, timeout=600, poll_frequency=POLL_FREQ).until(
        EC.presence_of_element_located(
            (By.XPATH, str(_xpath))))
    submit_element.click()
    try:
        # alert메세지가 올 때까지 최대 600초까지 기다림.
        alert_element = WebDriverWait(driver, timeout=600, poll_frequency=POLL_FREQ).until(
            EC.alert_is_present())
        # 신청하시겠습니까 : 예
        alert_element.accept()
        # 다음 alert 메세지 대기.
        alert_element = WebDriverWait(
            driver, timeout=600, poll_frequency=0.2).until(EC.alert_is_present())
        print(alert_element.text)  # 객체를 받으면 text를 반환, 받지 못하면 예외처리
        if "신청되었습" in alert_element.text:
            print("신청성공\n")
            select_sukku_num.remove(skku_num)
        else:
            print("신청실패\n")
        alert_element.accept()
        return
    except:
        print("사이트가 응답하지 않습니다.\n")


if __name__ == '__main__':
    # webdriver 실행
    # driver = webdriver.Chrome(executable_path='chromedriver')
    driver = webdriver.Chrome(executable_path='chromedriver', options=options)
    driver.get("https://sugang.knu.ac.kr/login.knu")
    driver.implicitly_wait(1)
    now = time.time()
    while True:
        # 웹 로드 후 로그인 시도
        print("로그인")
        std_num_element = WebDriverWait(driver, timeout=10, poll_frequency=POLL_FREQ).until(
            EC.presence_of_element_located(
                (By.XPATH, '/html/body/div[3]/div/div/div[1]/div/div[2]/div[1]/input'))
        )
        std_num_element.send_keys(TEMP_STD_NUM)  # 사이트에 학번 입력 + 로딩
        driver.find_element(
            By.XPATH, '/html/body/div[3]/div/div/div[1]/div/div[2]/div[2]/input').send_keys(TEMP_STD_ID)  # 사이트에 아이디 입력
        driver.find_element(
            By.XPATH, '/html/body/div[3]/div/div/div[1]/div/div[2]/div[3]/input').send_keys(TEMP_STD_PW)  # 사이트에 비밀번호 입력
        driver.find_element(
            By.XPATH, '/html/body/div[3]/div/div/div[1]/div/div[2]/div[5]/div/input').click()  # 로그인 블럭 클릭

        try:
            for _ in range(refresh_limit):  # 반복횟수 조절 가능 ,
                kkurumi = WebDriverWait(driver, timeout=10, poll_frequency=POLL_FREQ).until(
                    EC.presence_of_element_located(
                        (By.XPATH, '/html/body/div[3]/div[1]/div[4]/ul/li[2]/a'))
                ).click()
                for skku_num in select_sukku_num:
                    print(skku_num)
                    if(check_empty(driver, skku_num)):
                        submit(
                            driver, '//*[@id="grid01"]/tr[%d]/td[2]' % (skku_num), skku_num)
                print("현재 반복 : %d\n" % (refresh_cnt))
                refresh_cnt = refresh_cnt+1
                driver.refresh()
            driver.find_element(
                By.XPATH, '/html/body/div[2]/div[1]/div/div/div/ul/li[4]/a').click()  # 로그아웃
        except exceptions.ElementClickInterceptedException:
            print("웹 컴포넌트 에러")
            driver.refresh()
        except exceptions.UnexpectedAlertPresentException:
            driver.refresh()
        except KeyboardInterrupt:
            print("강제종료")
            print("크롬드라이버 종료..")
            break

        last = time.time()
        gap = float(last) - float(now)
        print("%f초 지난 후 다시 로그인했습니다.\n\n" % (gap))
        print("현재 로그인 횟수 : %d" % (web_repeated))
        web_repeated = web_repeated+1

    print("---종료---")
    print("프로세싱 시간 : %f \n\n" % (float(time.time()-float(now))))
    print("총 로그인 횟수 : " + str(web_repeated))
    print("총 새로고침 횟수 : " + str(refresh_cnt))
    driver.quit()
    sys.exit()

    # from selenium.webdriver.common.keys import Keys
    # alert메세지가 올 때까지 최대 0.6초까지 기다림.
    # login_alert_element = WebDriverWait(
    #     driver, timeout=1, poll_frequency=0.01).until(EC.alert_is_present())

    # if login_alert_element != None:
    #     print(login_alert_element.text)  # 객체를 받으면 text를 반환, 받지 못하면 예외처리
    #     print("로그인실패\n")
    #     break
    # else:
    #     print("로그인성공\n")

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


# 서버시간 판단
# month = {'Jan': '01', 'Feb': '02', 'Mar': '03', 'Apr': '04', 'May': '05', 'Jun': '06',
#          'Jul': '07', 'Aug': '08', 'Sep': '09', 'Oct': '10', 'Nov': '11', 'Dec': '12'}


# def time_small():
#     return random.random()/10+0.01


# # 팝업 윈도우 닫고 원래 창으로 포커스 옮기기
# for i in range(len(driver.window_handles)) :
#     if(i>=1) :
#         driver.switch_to.window(driver.window_handles[i])
#         driver.close()
# driver.switch_to.window(driver.window_handles[0])

# # 경고창 확인
# status = False  # False이면 Alert 메세지가 없음
# if status:  # AlertText가 있을 경우 종료.
#     print("로그인 실패 : exit")
#     driver.quit()
#     sys.exit()
# else:  # 없을 경우 로그인
#     print("로그인 성공 : Login")
    # driver.execute_script("arguments[0].click();", submit_element)
