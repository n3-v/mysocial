from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.service import Service
import time

def visit_url(user):

    path = "/usr/local/bin/chromedriver"
    service = Service(executable_path=path)
    options = Options()
    options.add_argument('headless')
    options.add_argument('no-sandbox')
    options.add_argument('disable-dev-shm-usage')
    options.add_argument('disable-infobars')
    options.add_argument('disable-background-networking')
    options.add_argument('disable-default-apps')
    options.add_argument('disable-extensions')
    options.add_argument('disable-gpu')
    options.add_argument('disable-sync')
    options.add_argument('disable-translate')
    options.add_argument('hide-scrollbars')
    options.add_argument('metrics-recording-only')
    options.add_argument('mute-audio')
    options.add_argument('no-first-run')
    options.add_argument('dns-prefetch-disable')
    options.add_argument('safebrowsing-disable-auto-update')
    options.add_argument('media-cache-size=1')
    options.add_argument('disk-cache-size=1')

    browser = webdriver.Chrome(service=service, options=options)

    browser.get('http://localhost/')

    browser.add_cookie({
        'name': 'session',
        'value': 'eyJ1c2VybmFtZSI6ImFkbWluIn0.ZvTNMA.ONzkjz_Ml13QWZQ_kUG1QSvtNvc'
    })


    try:
        browser.get("http://localhost/profile/" + user)
        time.sleep(2)
        WebDriverWait(browser, 5).until(lambda r: r.execute_script('return document.readyState') == 'complete')
    except:
        pass
    finally:
        browser.quit()
