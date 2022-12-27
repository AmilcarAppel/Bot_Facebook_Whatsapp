# The Script below is designed to verify new messages from Facebook and notify someone through  the whatsapp
# Import the libraries 
# Open Facebook messenger
# Check for new messages
# Verify how many new messages 
# Open the web Whatsapp and select who will be notified about the new messages from Facebook
# Paste the messages to the Whatsapp receiver
# Reloop the script while the condition is true

# Import the libraries: 
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from time import sleep
from selenium.common.exceptions import NoSuchElementException
from config import CHROME_DATA_PATH
from selenium.webdriver.common.keys import Keys
 
# Optional / Testing purposes
#count = 0 # This variable was created to set a limit to the script loop, but it is only necessary for testing purposes

# Setup the Web Browser to run Facebook page:
def driver_facebook():

    chrome_options = Options()
    #arguments = ['--lang=en-US', '--window-size=1000,1000', '--incognito']
    #arguments = ['--lang=en-US', '--window-size=1000,1000']
    arguments = ['--window-size=1000,1000']

    for argument in arguments:
        chrome_options.add_argument(argument)

    chrome_options.add_experimental_option('prefs', {
        'download.prompt_for_download': False,
        'profile.default_content_setting_values.notifications': 2,
        'profile.default_content_setting_values.automatic_downloads': 1,

    })

    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=chrome_options)
    return driver

# Setup the Web Browser to run the WhatsApp page
# Here the web browser is setup particularly different because it usually requires an authentication using the mobile camera, then to avoid such thing is necessary to apply # some parameters throught CHROME_DATA_PATH
def driver_whatsapp():
    
    options = webdriver.ChromeOptions()
    options.add_argument(CHROME_DATA_PATH)
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)
    driver.maximize_window()
    return driver

# Reloop this script while this condition is True:
#while count < 5 :
while True:

    # Open Facebook page and check for new messages:
    driver = driver_facebook()
    driver.get('https://www.facebook.com/')
    sleep(5)

    #Insert your details to login to Facebook:
    login_email = driver.find_element(By.ID, 'email')
    if login_email is not None:
        login_email.send_keys('add your e-mail here')#<--- add your e-mail here <---
        sleep(1)
    
    login_password = driver.find_element(By.ID, 'pass')
    if login_password is not None:
        login_password.send_keys('add your password here')#<--- add your password here <---
        sleep(1)

    # Locate and click to the Login button:
    login_button = driver.find_element(By.NAME, 'login')
    if login_button is not None:
        login_button.click()
        sleep(20)

    # The condition below verify if such element is is visible:    
    try:
        if driver.find_element(By.XPATH, "//div[@class='x1i10hfl x6umtig x1b1mbwd xaqea5y xav7gou x1ypdohk xe8uvvx xdj266r x11i5rnm xat24cr x1mh8g0r x16tdsg8 x1hl2dhg xggy1nq x87ps6o x1lku1pv x1a2a7pz x6s0dn4 x14yjl9h xudhj91 x18nykt9 xww2gxu x972fbf xcfux6l x1qhh985 xm0m39n x9f619 x78zum5 xl56j7k xexx8yu x4uap5 x18d9i69 xkhd6sd x1n2onr6 x1vqgdyp x100vrsf x1qhmfi1']") is not None:
            new_msg = driver.find_element(By.XPATH, "//div[@class='x1i10hfl x6umtig x1b1mbwd xaqea5y xav7gou x1ypdohk xe8uvvx xdj266r x11i5rnm xat24cr x1mh8g0r x16tdsg8 x1hl2dhg xggy1nq x87ps6o x1lku1pv x1a2a7pz x6s0dn4 x14yjl9h xudhj91 x18nykt9 xww2gxu x972fbf xcfux6l x1qhh985 xm0m39n x9f619 x78zum5 xl56j7k xexx8yu x4uap5 x18d9i69 xkhd6sd x1n2onr6 x1vqgdyp x100vrsf x1qhmfi1']").get_attribute('aria-label')
            print(new_msg)

    # If it is not visible, an error is expected and the program will eventually crash, but if you include this exeption in the script, it will pass throught with no  issue          
    except NoSuchElementException:  
        pass
    sleep(1)
    # Close the browser at the end of Facebook message check is necessary, because when open the Whatsapp web the new setup is required to avoid the mobile authentication to happen every time 
    driver.close()

    # The conditional IF is applied here before open the Whatsapp web in order to avoid unecessary action if there are no new messages from Facebook
    if new_msg.endswith('unread') == True:
        # Open Whatsapp page: 
        driver = driver_whatsapp()
        driver.get('https://web.whatsapp.com/')
        sleep(20)

        # Select who is the message receiver:
        whatsapp_name_receiver = driver.find_element(By.XPATH, "//span[contains(text(),'Aaa ver depois')]")
        if whatsapp_name_receiver is not None:
            whatsapp_name_receiver.click()
            sleep(2)

        # Paste the message obtained from Facebook Messenger and click to send:
        txt_msg = driver.find_element(By.XPATH, "//p[@class= 'selectable-text copyable-text']")
        if txt_msg is not None:
            txt_msg.send_keys(new_msg) 
            sleep(3)
            txt_msg.send_keys(Keys.ENTER)
            sleep(3)
            driver.close()   

    # If there are no new messages from Facebook, ignore the routine above and reloop the scrit        
    else:
        pass
        print('teste finalizado sem novas mensagens')

    #count += 1
    sleep(300)# Set the time here to define how often the loop is repeated
# End of the script