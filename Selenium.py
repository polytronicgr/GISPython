from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import time

'''
pageLink = "http://nomads.ncep.noaa.gov/cgi-bin/filter_seaice.pl?dir=%2Fsice.20181106"

driver = webdriver.Chrome( executable_path="/Users/FelipeGutierrez/Downloads/chromedriver" )
driver.get( pageLink )

time.sleep( 5 )

elements = driver.find_elements( By.XPATH, "/html/body/form/p[10]/input[1]" )
elements[0].click()

'''

pageLink = "http://nomads.ncep.noaa.gov/"

searchFor = raw_input( "Enter the specific data set you want to download: " )

driver = webdriver.Chrome( executable_path="/Users/FelipeGutierrez/Downloads/chromedriver" )
driver.get( pageLink )

elements = None
clicks = None

rowCount = len( driver.find_elements( By.XPATH, "/html/body/table[2]/tbody/tr/td[2]/center/table[3]/tbody/tr" ) )

for i in driver.find_elements( By.XPATH, "/html/body/table[2]/tbody/tr/td[2]/center/table[3]" ):
    for j in range( rowCount ):
        
        elements = i.find_elements_by_tag_name( "tr" )[j]
        
        if elements.text.find( searchFor ) == -1:
            
            print( "No: " + searchFor  )

        else:

            print( "Eureka: " + searchFor )
            clicks = elements.find_elements_by_link_text( "grib filter" )
            break

clicks[0].click()
listClicks = driver.find_elements_by_tag_name( 'a' )

#handles = None

for i in range( 0, len( listClicks ) ):

    driver.execute_script( "window.open('" + listClicks[i].get_attribute( "href" ) + "');" )
    
for handle in driver.window_handles:
    
    driver.switch_to.window( handle )
    links = driver.find_elements( By.XPATH, "/html/body/form/p[10]/input[1]" )
    
    if len( links ) > 0:
        
        #print( links )
        
        links[0].click()
