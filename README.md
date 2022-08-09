# SugangShinChung
# 수강신청.   
## python sugangshichung.py
## Ctrl+C로 종료
---
### dependency : 
python 3.10

pip install selenium 
크롬 드라이버 맞는 거 찾아서 설치!!(sugangshinchung.py와 같은 폴더에 있어야 합니다.

chromedriver.exe : 104 빌드
사용 시 브라우저 엔진에 따라 맞출 것.   
> https://sites.google.com/chromium.org/driver/downloads?authuser=0

이 프로젝트는 크롬 드라이버, 해상도 FHD에서 최적화 되었습니다.
---
다 설치 되면 cmd 창이나 터미널에서 다운로드 받은 디렉토리 들어가서 

python sugangshinchung.py 

입력.
안되면 파이썬 3.10이 설치되었는지, 셀레니움 패키지가 잘 설치되었는지 확인하시구
코드 상단에 본인 학번,아이디,비밀번호 입력해주시면 됩니다.
"사용자 입력부분.jpg 참조"

종료는 ctrl+c / mac은 command+c인가..? 여튼 

---

### background 동작

#### 주의: selelnium 크롬드라이버를 사용해본 분들 혹은 프로그래밍 좀 한다는 분들만. 
코드를 백그라운드에서 실행시키고 싶다면(크롬 드라이버 옵션)
__sugang.py__
파일의
options.add_experimental_option('prefs', prefs)
options.add_argument('headless')
두 줄의 주석을 해제하시면 됩니다.

백그라운드에서 실행 시 리소스가 줄어들어 더 빠릅니다.

---
셀레니움 참조   
> https://selenium-python.readthedocs.io/index.html
> https://greeksharifa.github.io/references/2020/10/30/python-selenium-usage/


혹시 엣지를 사용한다면
>https://developer.microsoft.com/en-us/microsoft-edge/tools/webdriver/

headlessmode 관련
https://beomi.github.io/2017/09/28/HowToMakeWebCrawler-Headless-Chrome/
