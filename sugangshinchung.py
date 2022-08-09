# version 0.2
## last update 220810 04:10
### seunmul

from selenium import webdriver
from selenium.common import exceptions
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

from __sugang__ import *

import sys
import time

#### temp_id, temp_pw, temp_std_num#####
TEMP_STD_NUM = '2018112874'  # 자신의 학번을 입력하세요
TEMP_STD_ID = 'qkrrjsgk79'  # 자신의 아이디를 입력하세요
TEMP_STD_PW = '@pk3721204'  # 자신의 비밀번호를 입력하세요

## 2022.08.09 수강신청 사이트 변경 이후로 수강신청횟수에 따라 테이블이 재정렬 됩니다.
## 이에 따라 수강 꾸러미에 담긴 과목 개수를 적어주시기 바라며,
## 프로세스가 지속되는 동안에는 리스트가 최신화되나, 
## 실행 프로세스가 종료되었을 때 신청된 과목이 있다면, 수강꾸러미 내 과목 숫자를 다시 확인하고 입력해주시기 바랍니다.
## 안그러면 실행은 될 수 있으나 제대로 돌아가지 않습니다.
sukku_list_num = 3 # 수강꾸러미에 대학글쓰기, 논리와 비판적 사고, 캠핑 3과목이 있으면 '3'을 입력해주시면 됩니다.

# 새로고침횟수 제한
## 컴퓨터 환경에 따라 한 세션에 머무를 새로고침횟수를 적어주시면 됩니다.
refresh_limit = 2000

# 카운터 변수
login_cnt = 1
refresh_cnt = 1

# params : 성능 조절 파라미터
## 성능 조절 파라미터로, POLL_FREQ는 웹 컴포넌트들이 로드되는 풀링 시간을 조절하는 파라미터입니다.
## CLK_BTN_FRQ는 수강신청 버튼을 누르기 전에 time.sleep하는 시간입니다
## 컴퓨터 성능, 네트워크 상황에따라 선택하시면 됩니다..만 사양이 다들 다르니
## CLK_BTN_FRQ는 안정성을 위해 0.25 이상의 값을 넣어주세요
## POLL_FREQ는 작을수록 좋지만, 본인 CPU가 좋지 않다면 성능이 안따라주니 테스트 해보시고
## 에러가 발생하면 값을 올려주시면 되겠습니다
## 참고로 테스트 환경은 i5-1135G 인텔 11세대 노트북 프로세서 / 자취방 공유기 인터넷 속도 100Mb/s입니다. 
## 기본 값은 0.001 / 0.1 입니다. 에러가 발생해서 자꾸 창이 재실행되면 숫자를 올려주세요.
POLL_FREQ = 0.001
CLK_BTN_FRQ = 0.1

# 사이트 url
## 사이트 주소 바뀌면 업데이트 ㄱㄱ
url = "https://sugang.knu.ac.kr/login.knu"



#### -----------program codes-------------- ####
def check_empty(driver, skku_num):  # 수강인원 비었는지 체크
    limit_personnel, sugang_personnel, sub_name = \
        WebDriverWait(driver, timeout=10, poll_frequency=POLL_FREQ).until(
            EC.presence_of_element_located(
                (By.XPATH, '/html/body/div[3]/div[1]/div[5]/div[2]/div/table/tbody/tr[%d]/td[11]' % (skku_num)))
        ).get_attribute('innerText'),\
        driver.find_element(
            By.XPATH, '/html/body/div[3]/div[1]/div[5]/div[2]/div/table/tbody/tr[%d]/td[12]' % (skku_num)).get_attribute('innerText'),\
        driver.find_element(
            By.XPATH, '/html/body/div[3]/div[1]/div[5]/div[2]/div/table/tbody/tr[%d]/td[4]' % (skku_num)).get_attribute('innerText')
    print(sub_name + "\t[ 제한인원 :" + limit_personnel +
          "\t수강인원 :" + sugang_personnel + ' ]', end=" ")
    
    if limit_personnel <= sugang_personnel:
        print(": 신청불가")
        return False
    else:
        print(": 신청가능")
        return True


def submit(driver, _xpath, skku_num):  # 수강신청 처리
    print("신청시도 : ", end=" ")
    submit_element = WebDriverWait(driver, timeout=600, poll_frequency=POLL_FREQ).until(
        EC.presence_of_element_located(
            (By.XPATH, str(_xpath))))
    time.sleep(CLK_BTN_FRQ)
    print("클릭")
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
            sukku_list.pop()
        else:
            print("신청실패\n")
        alert_element.accept()
    except Exception as e:
        print(e)
        raise SUBMIT_ERROR()
    finally:
        return


def login():  # 로그인
    try:
        std_num_element, std_id_element, std_pw_element = \
            WebDriverWait(driver, timeout=10, poll_frequency=POLL_FREQ).until(
                EC.presence_of_element_located(
                    (By.XPATH, '/html/body/div[3]/div/div/div[1]/div/div[2]/div[1]/input'))
            ),\
            WebDriverWait(driver, timeout=10, poll_frequency=POLL_FREQ).until(
                EC.presence_of_element_located(
                    (By.XPATH, '/html/body/div[3]/div/div/div[1]/div/div[2]/div[2]/input'))
            ),\
            WebDriverWait(driver, timeout=10, poll_frequency=POLL_FREQ).until(
                EC.presence_of_element_located(
                    (By.XPATH, '/html/body/div[3]/div/div/div[1]/div/div[2]/div[3]/input'))
            )
        std_num_element.send_keys(TEMP_STD_NUM)  # 사이트에 학번 입력 + 로딩
        std_id_element.send_keys(TEMP_STD_ID)  # 사이트에 아이디 입력 + 로딩
        std_pw_element.send_keys(TEMP_STD_PW)  # 사이트에 비밀번호 입력 + 로딩
        driver.find_element(
            By.XPATH, '/html/body/div[3]/div/div/div[1]/div/div[2]/div[5]/div/input').click()  # 로그인 블럭 클릭
    except Exception as e:
        print(e)
        raise LOGIN_ERROR()
    finally:
        return


def restart(driver, options, url):
    driver.quit()
    driver = webdriver.Chrome(
        executable_path='chromedriver', options=options)
    print("드라이버 재실행 및 세션 재시작\n")
    driver.get(str(url))
    return driver


if __name__ == '__main__':
    
    now = time.time()
    sukku_list = []
    for i in range(1,sukku_list_num+1) :
        
        sukku_list.append(i) 
    # webdriver 실행
    driver = webdriver.Chrome(
        executable_path='chromedriver', options=options)
    driver.get(str(url))
    while True:
        start = time.time()
        # 수꾸 리스트 개수 확인
        print("현재 수꾸 리스트 %s" % (sukku_list))
        
        if(sukku_list.__len__() == 0):
            break
        try:
            print("로그인")
            login()  # 웹 로드 후 로그인 시도
            for _ in range(refresh_limit):  # 새로고침 하면서 수강신청 시도 : 리프레시 리밋 커스텀 가능
                # 꾸러미 신청목록 클릭
                kkurumi_element = WebDriverWait(driver, timeout=10, poll_frequency=POLL_FREQ).until(
                    EC.presence_of_element_located(
                        (By.XPATH, '/html/body/div[3]/div[1]/div[4]/ul/li[2]/a'))
                ).click()
                # 꾸러미 수강인원 체크 및 신청 시도
                for skku_num in sukku_list:
                    if(check_empty(driver, skku_num)):
                        submit(
                            driver, '//*[@id="grid01"]/tr[%d]/td[2]' % (skku_num), skku_num)
                print("현재 반복 : %d\n" % (refresh_cnt))
                refresh_cnt = refresh_cnt+1
                driver.refresh()
            # 리프레쉬 리밋 => 로그아웃
            driver.find_element(
                By.XPATH, '/html/body/div[2]/div[1]/div/div/div/ul/li[4]/a').click()
            # 드라이버 종료 및 재시작
            driver = restart(driver, options, url)

        except KeyboardInterrupt:
            print("강제종료")
            print("크롬드라이버 종료..")
            driver.quit()
            break
        except LOGIN_ERROR:
            print("로그인 에러")
            driver.quit()
            print("세션종료중...")
            break
        except SUBMIT_ERROR:
            print("수강신청 중 에러 발생")
            driver.quit()
            print("세션종료중...")
            break
        except exceptions.ElementClickInterceptedException:
            print("웹 컴포넌트 로딩 에러")
            driver.refresh()
            driver.find_element(
                By.XPATH, '/html/body/div[2]/div[1]/div/div/div/ul/li[4]/a').click()  # 로그아웃
            continue
        except exceptions.UnexpectedAlertPresentException as e:
            print("경고창 에러")
            print(e)
            driver = restart(driver, options, url)
            continue
        except Exception as e:
            print("언노운 에러")
            print(e)
            driver = restart(driver, options, url)
            continue

        # 한 사이클 종료 시 실행
        last = time.time()
        gap = float(last) - float(start)
        print("%f초 지난 후 다시 로그인했습니다.\n\n" % (gap))
        print("현재 로그인 횟수 : %d" % (login_cnt))
        login_cnt = login_cnt+1

    # 프로그램 종료
    print("---종료---")
    print("프로세싱 시간 : %f \n\n" % (float(time.time()-float(now))))
    print("총 로그인 횟수 : " + str(login_cnt))
    print("총 새로고침 횟수 : " + str(refresh_cnt))
    sys.exit()
