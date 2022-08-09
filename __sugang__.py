# webdriver option params
from selenium.webdriver import ChromeOptions 

options = ChromeOptions()
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

class LOGIN_ERROR(Exception):
    def __str__(self):
        return "LOGIN ERROR"
    pass

class SUBMIT_ERROR(Exception):
    def __str__(self):
        return "SUBMIT ERROR"
    pass

class TEST_ERROR(Exception):
    def __str__(self):
        return "TEST ERROR"
    pass