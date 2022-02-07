from selenium import webdriver
import time
import random

def time_small():
    return random.random()/10+0.01

def check_empty(driver, grid_num):
    a = driver.find_element_by_id(grid_num).find_element_by_class_name('lect_quota').get_attribute('currentvalue')
    b = driver.find_element_by_id(grid_num).find_element_by_class_name('lect_req_cnt').get_attribute('currentvalue')
    sub_name = driver.find_element_by_id(grid_num).find_element_by_class_name('subj_nm').get_attribute('currentvalue')
    print(sub_name + "\t[ 제한인원 :" + a + "\t수강인원 :" + b + ']')
    if a==b:
        return False
    else:
        return True

##### temp_id, temp_pw, temp_std_num#####

driver=webdriver.Chrome('C:\chromedriver.exe')
driver.get("https://sugang.knu.ac.kr/Sugang/comm/support/login/loginForm.action?redirUrl=%2FSugang%2Fcour%2FlectReq%2FonlineLectReq%2Flist.action")

temp_id = ''  ##자신의 아이디를 입력하세요
temp_pw = '!!'  ##자신의 비밀번호를 입력하세요
temp_std_num = ''  ##자신의 학번을 입력하세요
select_sukku_num = [1,2]  ##예를 들어 수꾸목록의 첫번째, 세번째 과목을 수강신청해야하면 [1,3] 같이 써주시면 됩니다. ++8까지 가능합니다.

grid_name = ['lectPackReqGrid_0', 'lectPackReqGrid_1','lectPackReqGrid_2','lectPackReqGrid_3','lectPackReqGrid_4','lectPackReqGrid_5','lectPackReqGrid_6', 'lectPackReqGrid_7']

while(True):
    now = time.time()
    driver.find_element_by_xpath('//*[@id="user.stu_nbr"]').send_keys(temp_std_num)
    time.sleep(time_small())
    driver.find_element_by_xpath('//*[@id="user.usr_id"]').send_keys(temp_id)
    time.sleep(time_small())
    driver.find_element_by_xpath('//*[@id="user.passwd"]').send_keys(temp_pw)
    time.sleep(time_small())

    driver.find_element_by_xpath('//*[@id="loginForm"]/table/tbody/tr[4]/td/button[1]').click()

    ## 여기까지 로그인 ##

    ##lectPackReqGrid_0, lectPackReqGrid_1,  lectPackReqGrid_2 ...
    for _ in range(1000):
        time.sleep(0.5)
        for skku_num in select_sukku_num:
            if skku_num == 1:
                if(check_empty(driver, grid_name[skku_num-1])):
                    driver.find_element_by_xpath('//*[@id="lectPackReqGrid_0"]/td[11]/a').click()
            elif skku_num == 2:
                if (check_empty(driver, grid_name[skku_num - 1])):
                    driver.find_element_by_xpath('//*[@id="lectPackReqGrid_1"]/td[11]/a').click()
            elif skku_num == 3:
                if (check_empty(driver, grid_name[skku_num - 1])):
                    driver.find_element_by_xpath('//*[@id="lectPackReqGrid_2"]/td[11]/a').click()
            elif skku_num == 4:
                if (check_empty(driver, grid_name[skku_num - 1])):
                    driver.find_element_by_xpath('//*[@id="lectPackReqGrid_3"]/td[11]/a').click()
            elif skku_num == 5:
                if (check_empty(driver, grid_name[skku_num - 1])):
                    driver.find_element_by_xpath('//*[@id="lectPackReqGrid_4"]/td[11]/a').click()
            elif skku_num == 6:
                if (check_empty(driver, grid_name[skku_num - 1])):
                    driver.find_element_by_xpath('//*[@id="lectPackReqGrid_5"]/td[11]/a').click()
            elif skku_num == 7:
                if (check_empty(driver, grid_name[skku_num - 1])):
                    driver.find_element_by_xpath('//*[@id="lectPackReqGrid_6"]/td[11]/a').click()
            elif skku_num == 8:
                if (check_empty(driver, grid_name[skku_num - 1])):
                    driver.find_element_by_xpath('//*[@id="lectPackReqGrid_7"]/td[11]/a').click()
        driver.refresh()

    driver.find_element_by_xpath('//*[@id="logout"]/button[1]').click()
    time.sleep(3)
    last = time.time()
    gap = float(last) - float(now)
    print("{}초 지난 후 다시 로그인했습니다.".format(gap))