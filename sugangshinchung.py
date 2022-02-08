from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import sys
import time
import random

#### temp_id, temp_pw, temp_std_num#####

temp_id = 'qkrrjsgk79'  ##자신의 아이디를 입력하세요
temp_pw = '@pk3721204'  ##자신의 비밀번호를 입력하세요
temp_std_num = '2018112874'  ##자신의 학번을 입력하세요
select_sukku_num = [1,2,3,4]  ##예를 들어 수꾸목록의 첫번째, 세번째 과목을 수강신청해야하면 [1,3] 같이 써주시면 됩니다. ++8까지 가능합니다.
refresh_limit = 10

# 시간반환 함수
def time_small():
    return random.random()/10+0.01

# 수강인원 비었는지 체크
def check_empty(driver, grid_num):
    try:
        a = driver.find_element_by_id(grid_num).find_element_by_class_name('lect_quota').get_attribute('currentvalue')
        b = driver.find_element_by_id(grid_num).find_element_by_class_name('lect_req_cnt').get_attribute('currentvalue')
        sub_name = driver.find_element_by_id(grid_num).find_element_by_class_name('subj_nm').get_attribute('currentvalue')
        print(sub_name + "\t[ 제한인원 :" + a + "\t수강인원 :" + b + ']')
        if a<=b:
            return False
        else:
            return True
    except:
        print("신청할 수 있는 수강꾸러미가 없습니다.")
        return False
    
# 수강신청 처리
def submit(_xpath):
    try :
        driver.find_element_by_xpath(str(_xpath)).click()     
        element = WebDriverWait(driver, 600).until(EC.alert_is_present()) ## alert메세지가 올 때까지 최대 600초까지 기다림.
        print(element.text) # 객체를 받으면 text를 반환, 받지 못하면 예외처리 
        if "신청되었습" in element.text :
            print("신청성공\n")    
        else :
            print("신청실패\n")
        element.accept()
    except : 
        print("사이트가 응답하지 않습니다.\n")
    
### webdriver 실행

driver=webdriver.Chrome(executable_path='chromedriver')
driver.get("https://sugang.knu.ac.kr/Sugang/comm/support/login/loginForm.action?redirUrl=%2FSugang%2Fcour%2FlectReq%2FonlineLectReq%2Flist.action")

grid_name = ['lectPackReqGrid_0', 'lectPackReqGrid_1','lectPackReqGrid_2','lectPackReqGrid_3','lectPackReqGrid_4','lectPackReqGrid_5','lectPackReqGrid_6', 'lectPackReqGrid_7']

web_repeated=1
clicked_cnt=1
try:
    while(1):
        # 웹 로드까지 대기
        driver.implicitly_wait(time_to_wait=1) 
        # 팝업 윈도우 닫고 원래 창으로 포커스 옮기기
        for i in range(len(driver.window_handles)) :
            if(i>=1) :
                driver.switch_to.window(driver.window_handles[i]) 
                driver.close()
        driver.switch_to.window(driver.window_handles[0])
        # 웹 로드 후 로그인 시도
        now = time.time()
        driver.find_element_by_xpath('//*[@id="user.stu_nbr"]').send_keys(temp_std_num) #사이트에 학번 입력
        time.sleep(time_small())
        driver.find_element_by_xpath('//*[@id="user.usr_id"]').send_keys(temp_id) #사이트에 아이디 입력
        time.sleep(time_small())
        driver.find_element_by_xpath('//*[@id="user.passwd"]').send_keys(temp_pw) #사이트에 비밀번호 입력
        time.sleep(time_small())
        driver.find_element_by_xpath('//*[@id="loginForm"]/table/tbody/tr[4]/td/button[1]').click() #로그인 블럭 클릭

        ## 경고창 확인
        status = False # False이면 Alert 메세지가 없음
        try : 
            element = WebDriverWait(driver, 0.6).until(EC.alert_is_present()) ## alert메세지가 올 때까지 최대 0.6초까지 기다림.
            print(element.text) # 객체를 받으면 text를 반환, 받지 못하면 예외처리 
            status = True
            print("Yes alert") #alert가 있으면 yes alert 출력
        except : 
            status = False
            print("No alert") #alert 없으면 no alert 출력

        if  status: #AlertText가 있을 경우 종료.
            print("로그인 실패 : exit")
            time.sleep(1)
            driver.quit()
            sys.exit()
        else : #없을 경우 로그인
            print("로그인 성공 : Login")

        ## 여기까지 로그인 ##
        #lectPackReqGrid_0, lectPackReqGrid_1,  lectPackReqGrid_2 ...

            for _ in range(refresh_limit): ## 반복횟수 조절 가능 , 
                time.sleep(0.5)
                for skku_num in select_sukku_num:
                    if skku_num == 1:
                        if(check_empty(driver, grid_name[skku_num-1])):
                            submit('//*[@id="lectPackReqGrid_0"]/td[11]/a')
                    elif skku_num == 2:
                        if (check_empty(driver, grid_name[skku_num - 1])):
                            submit('//*[@id="lectPackReqGrid_1"]/td[11]/a')
                    elif skku_num == 3:
                        if (check_empty(driver, grid_name[skku_num - 1])):
                            submit('//*[@id="lectPackReqGrid_2"]/td[11]/a')
                    elif skku_num == 4:
                        if (check_empty(driver, grid_name[skku_num - 1])):
                            submit('//*[@id="lectPackReqGrid_3"]/td[11]/a')
                    elif skku_num == 5:
                        if (check_empty(driver, grid_name[skku_num - 1])):
                            submit('//*[@id="lectPackReqGrid_4"]/td[11]/a')
                    elif skku_num == 6:
                        if (check_empty(driver, grid_name[skku_num - 1])):
                            submit('//*[@id="lectPackReqGrid_5"]/td[11]/a')
                    elif skku_num == 7:
                        if (check_empty(driver, grid_name[skku_num - 1])):
                            submit('//*[@id="lectPackReqGrid_6"]/td[11]/a')
                    elif skku_num == 8:
                        if (check_empty(driver, grid_name[skku_num - 1])):
                            submit('//*[@id="lectPackReqGrid_7"]/td[11]/a')
                print("현재 반복 : {}".format(clicked_cnt))
                clicked_cnt=clicked_cnt+1 
                driver.refresh()



            driver.find_element_by_xpath('//*[@id="logout"]/button[1]').click()
            time.sleep(3)
            last = time.time()
            gap = float(last) - float(now)
            print("{}초 지난 후 다시 로그인했습니다.\n\n".format(gap))
            print("현재 로그인 횟수 : " + str(web_repeated))
            web_repeated=web_repeated+1
                
except :
    print("총 로그인 횟수 : " +str(web_repeated))
    print("총 클릭 횟수 : " +str(clicked_cnt))    
    driver.quit()
    sys.exit()
