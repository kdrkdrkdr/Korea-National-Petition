from selenium.webdriver import PhantomJS, DesiredCapabilities
from selenium.common.exceptions import NoSuchElementException
from bs4 import BeautifulSoup
from time import sleep
from webbrowser import open_new
from sys import exit as terminate



printInfo = lambda msg : print(f'[국민청원-프로그램] {msg}')
def cleanStr(string, replList=['!', '?', '.']): 
    for i in replList: 
        string = string.replace(i, f'{i}\n'); 
    return string


headers = {
    'User-Agent' : 'Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko',
    'Referer' : 'https://www1.president.go.kr/',
}
serviceArgs = [
    '--webdriver-loglevel=ERROR'
]
for key, value in enumerate(headers):
    capabilityKey = f'phantomjs.page.customHeaders.{key}'
    DesiredCapabilities.PHANTOMJS[capabilityKey] = value


driver = PhantomJS(executable_path='phantomjs.exe', service_args=serviceArgs)


driver.get('https://www1.president.go.kr/petitions/Step1')
driver.find_element_by_class_name('facebook').click()



f = open('np_form.txt', 'r', encoding='utf-8')
npFormText = ''.join([i for i in ''.join(f.readlines()).split('\n') if i])

_facebookAccount = npFormText.split('#청원제목')
facebookAccount = _facebookAccount[0].replace(' ', '').split('facebook_email=')[1].split('facebook_password=')
facebookEmail = facebookAccount[0]
facebookPassword = facebookAccount[1]


printInfo('로그인중...')
driver.find_element_by_xpath('//*[@id="email"]').send_keys(facebookEmail)
driver.find_element_by_xpath('//*[@id="pass"]').send_keys(facebookPassword)
driver.find_element_by_xpath('//*[@id="loginbutton"]').click()

try:
    driver.find_element_by_xpath('//*[@id="loginbutton"]')
    printInfo('로그인에 실패했습니다. 이메일과 아이디를 확인해주십시오.')
    terminate()
except ( NoSuchElementException ):
    printInfo("로그인 완료!")

npCategoryName = [
    '정치개혁', '외교/통일/국방', '일자리', '미래', '성장동력', '농산어촌', '보건복지', '육아/교육', '안전/환경',
    '저출산/고령화대책', '행정', '반려동물', '교통/건축/국토', '경제민주화', '인권/성평등', '문화/예술/체육/언론', '기타'
]
np_Category = {}
for i in enumerate(npCategoryName): np_Category[i[1]] = f'//*[@id="pw_category"]/option[{i[0]+2}]'


_npTitle = _facebookAccount[1].split('#카테고리')
npTitle = _npTitle[0]

_npCategory = _npTitle[1].split('#청원내용')
try:
    npCategory = np_Category[_npCategory[0].replace(' ', '')]
except:
    printInfo(f"{_npCategory[0].replace(' ', '')} 은(는) 잘못된 카테고리 입니다.")
    terminate()

_npContent = _npCategory[1].split('#관련링크')
npContent = cleanStr(_npContent[0])


_npLinks = _npContent[1].split('#관련링크')[0].split('#관련태그')
npLinks = _npLinks[0].split('|')

npTags = _npLinks[1].split('|')

f.close()


try:
    driver.get('https://www1.president.go.kr/petitions/Step2')


    driver.find_element_by_xpath('//*[@id="pw_subject"]').send_keys(npTitle)
    printInfo("청원제목 입력완료")


    driver.find_element_by_xpath(npCategory).click()
    printInfo("카테고리 입력완료")


    driver.find_element_by_xpath('//*[@id="pw_contents"]').send_keys(npContent)
    printInfo("청원내용 입력완료")


    for l in range(len(npLinks)-1):
        driver.find_element_by_xpath('//*[@id="tw_link_add"]').click()

        for i in enumerate(driver.find_elements_by_name('wv_link[]')):
            i[1].send_keys(npLinks[i[0]])
    printInfo("관련링크 입력완료")


    tagCount = len(npTags)
    while True:
        if tagCount > 3:
            if tagCount == 3:
                npTags.pop(-1)
        else:
            break
    for t in enumerate(driver.find_elements_by_name('wv_tag[]')):
        if tagCount-1 >= t[0]:
            t[1].send_keys(npTags[t[0]])
    printInfo("검색태그 입력완료")


    driver.find_element_by_xpath('//*[@id="WriteBtn"]').click()
    printInfo("국민청원 작성완료")


    sleep(3)
    npURL =  BeautifulSoup(driver.page_source, 'html.parser').find('meta', {'property':'og:url'})['content']
    printInfo('청원링크 : ' + npURL)
    open_new(npURL)


    driver.find_element_by_xpath('//*[@id="cont_view"]/div[2]/div/div/div[2]/div[3]/ul/li[2]/a').click()
    printInfo("로그아웃 완료")

except:
    printInfo('프로그램에 오류가 발생했습니다. 다시 시도해주십시오.')

finally:
    driver.close()
    printInfo('프로그램을 종료하려면 아무키나 누르세요.')

input()