"""
Author : Abhinav Tyagi 

Date : 28-Aug-2022 
"""





import pandas as pd
from selenium import webdriver
import random
import os
from time import sleep

os.chdir(r'C:\Users\tyagi\Documents\Naukri Bot')



info = pd.read_excel(os.path.join(os.getcwd(), 'Credentials\Credentials.xlsx'))
Resume = pd.read_excel(os.path.join(os.getcwd(),'Credentials\ResumeHeadline.xlsx'))
Report = pd.read_excel(os.path.join(os.getcwd(), 'Jobs\Job_Report.xlsx'))

driver = webdriver.Edge(os.path.join(os.getcwd(),'driver\msedgedriver.exe'))
driver.get("https://www.naukri.com/")
driver.maximize_window()

driver.find_element_by_xpath('//*[@id="login_Layer"]').click()
sleep(2)
#UserName
driver.find_element_by_xpath('//*[@id="root"]/div[4]/div[2]/div/div/div[2]/div/form/div[2]/input').send_keys(info['Username'])
driver.find_element_by_xpath('//*[@id="root"]/div[4]/div[2]/div/div/div[2]/div/form/div[3]/input').send_keys(info['Password'])
#Login
driver.find_element_by_xpath('//*[@id="root"]/div[4]/div[2]/div/div/div[2]/div/form/div[6]/button').click()

sleep(2)
#Naukri Update Profile
driver.get('https://www.naukri.com/mnjuser/profile?id=&altresid')

#Chatbot
try: 
    driver.find_element_by_xpath('//*[@id="_4mwl2w02fNavbar"]/div').click()
except:
    print('no chat bot find')

#HeadLine
driver.find_element_by_xpath('//*[@id="lazyResumeHead"]/div/div/div/div[1]/span[2]').click()
driver.find_element_by_id('resumeHeadlineTxt').clear()
driver.find_element_by_id('resumeHeadlineTxt').send_keys(Resume['Headline'][random.randrange(0,len(Resume))])
sleep(2)
driver.find_element_by_xpath('/html/body/div[6]/div[4]/div[2]/form/div[3]/div/button').click()

#Back to naukrijobs homepage
try:
    sleep(2)
    driver.get('https://www.naukri.com/mnjuser/recommendedjobs')
except: 
    sleep(2)
    driver.get('https://www.naukri.com/mnjuser/recommendedjobs')

# jobs = driver.find_elements_by_tag_name('article')
jobs = driver.find_elements_by_class_name('jobTuple')


try: 
    driver.implicitly_wait(2)
    driver.find_element_by_xpath('//*[@id="root"]/div[2]/div[1]/div[1]/div[1]/div[3]/div[3]/div/button[1]').click()
except Exception as e:
    print(e)

report = pd.DataFrame(index=[0],columns=['LINK', 'JOB', 'COMPANY', 'REQ EXPERIENCE', 'SALARY', 'LOCATION',
       'JOB DESCRIPTION', 'POSTED DAYS', 'NO. APPLICANTS', 'APPLY', 'REFFERED LINK'])

print("No. of Jobs found on Homepage",len(jobs))
if(len(jobs)==0):
    driver.quit()

for i,j in enumerate(jobs):
    print(f"Job No. : {i}")
    try:
        j.click()
    except:
        driver.switch_to.window(driver.window_handles[0])
        try:
            j.click()
        except Exception as e:
            print(e)
            
        
    p = driver.current_window_handle
    parent = driver.window_handles[0]
    #obtain browser tab window
    chld = driver.window_handles[1]
    driver.switch_to.window(chld)
    try:
        link = driver.current_url
        report.loc[i,'LINK'] = link
        try:
            Job = driver.find_element_by_class_name('jd-header-title').text
        except:
            Job = ""
        report.loc[i,'JOB'] = Job
        try :
            Company = driver.find_element_by_class_name("jd-header-comp-name").text
        except:
            Company = ''
        report.loc[i,'COMPANY'] = Company
        try:
            Req_ex = driver.find_element_by_class_name('exp').text
        except:
            Req_ex = ''
        report.loc[i,'REQ EXPERIENCE'] = Req_ex
        try:
            Salary = driver.find_element_by_class_name('salary').text
        except:
            Salary=''
        report.loc[i,'SALARY'] = Salary
        
        try:
            Job_location = driver.find_element_by_class_name('location ').text
        except:
            Job_location = ''
        report.loc[i,'LOCATION'] = Job_location
        try:
            Job_Desc = driver.find_element_by_class_name('job-desc').text
            Job_Desc = ' '.join(Job_Desc.split('\n'))
        except:
            Job_Desc = ''
        report.loc[i,'JOB DESCRIPTION']= Job_Desc
        try:
            posted = driver.find_element_by_class_name('jd-stats').text
            a=posted.split(':')
            Posted = ' '.join(a[1].split(' ')[0:2])
            Applicants = a[-1].removeprefix(' ')
            
        except:
            Posted = ''
            Applicants=''
        
        report.loc[i,'POSTED DAYS'] = Posted
        report.loc[i,'NO. APPLICANTS'] = Applicants
        
    except Exception as e:
        print(e)
        driver.switch_to.window(driver.window_handles[0])
       
               
    #Lets Apply
    try:
        driver.find_element_by_class_name('apply-button').click()
        driver.implicitly_wait(2)
        print('Applied')
        report.loc[i,'APPLY'] = 'APPLIED'
        report.loc[i,'REFFERED LINK'] = ''
        driver.close()
        driver.switch_to.window(driver.window_handles[0])
        
        try:
            if driver.find_element_by_class_name('apply-message').text == 'You were redirected to the company website for completing your job application process.':
                refer_tab = driver.switch_to.window(driver.window_handles[2])
                report.loc[i,'APPLY'] = 'NOT APPLIED'
                report.loc[i,'REFFERED LINK'] = driver.current_url
                refer_tab.close()
                driver.close()
                driver.switch_to.window(driver.window_handles[0])
        except:
            print('No Ref.')
            report.loc[i,'APPLY'] = 'APPLIED'
            report.loc[i,'REFFERED LINK'] = ''
            if len(driver.window_handles)>2:
                driver.switch_to.window(driver.window_handles[1]).close()
                driver.switch_to.window(driver.window_handles[0])
            else:
                driver.switch_to.window(driver.window_handles[0])
            
    except:
        report.loc[i,'APPLY'] = 'NOT APPLIED'
        report.loc[i,'REFFERED LINK'] = ''
        try:
            report1 = report
        except Exception as e:
            print(e)
        Final = pd.concat([Report,report1],ignore_index=True)
        Final.drop_duplicates(subset = 'LINK',keep='first',ignore_index=True,inplace=True)
        Final.to_excel(os.path.join(os.getcwd(), 'Jobs\Job_Report.xlsx'),index=False)
        
        #
# job_list = Final.LINK.to_list()
# num = 40
# driver.switch_to.window(driver.window_handles[0])
# for i,link in enumerate(job_list[num:num+20]):
#     print(num+i)
#     if(i==20):
#         break
#     driver.get(link)
#     driver.execute_script("window.open('');")
#     driver.switch_to.window(driver.window_handles[i+1])
    



