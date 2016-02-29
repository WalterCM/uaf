from selenium import webdriver
from PIL import Image
from config import services, urls, xpaths

class Uaf:
    session = ''
    def __init__(self):
        print('Starting the Uaf')

    def start_session(self, service):
        print('Starting a session')
        self.browser = webdriver.Chrome()
        if service not in services:
            print("That service doesn't exist")
            return -1
        self.session = service
        url = urls[service + '_login']
        self.target(url)

    def end_session(self):
        print('Ending the session')
        self.browser.close()
        self.session = ''

    def target(self, url):
        if self.browser.current_url != url:
            print('The urls are different')
            self.browser.get(url)

    def get_captcha(self):
        if self.session == '':
            print('A session has not been started')
            return -1

        print('Getting the captcha of service' + self.session +'.')
        
        xpath = xpaths[self.session + '_img']
        
        self.browser.save_screenshot('screenshot.png')
        img = self.browser.find_element_by_xpath(xpath)
        loc = img.location

        image = Image.open('screenshot.png')

        left = int(loc['x'])
        top = int(loc['y'])
        right = left + 220
        bottom = top + 80

        box = (left, top, right, bottom)

        captcha = image.crop(box)

        return captcha

    def save_captcha(self, path):
        captcha = self.get_captcha()
        captcha.save(path)

    def login(self, user, password, captcha=''):
        if self.session == '':
            print('A session has not been started')
            return -1

        print('Logging in with user ' + user + ', and captcha ' 
            + captcha)
        user_xpath = xpaths[self.session + '_user']
        password_xpath = xpaths[self.session + '_password']
        captcha_xpath = xpaths[self.session + '_captcha']
        submit_xpath = xpaths[self.session + '_submit']

        user_input = self.browser.find_element_by_xpath(user_xpath)
        passowrd_input = self.browser.find_element_by_xpath(password_xpath)
        captcha_input = self.browser.find_element_by_xpath(captcha_xpath)

        user_input.clear()
        passowrd_input.clear()
        captcha_input.clear()

        user_input.send_keys(user)
        passowrd_input.send_keys(password)
        captcha_input.send_keys(captcha)
        self.browser.find_element_by_xpath(submit_xpath).click()

    def get_user_firstname(self):
        if not self.session == 'nimbus':
            print('You need to log in to nimbus')
            return -1

        print("Getting real user's firstname")
        url = urls['nimbus_profile']
        xpath = xpaths['user_firstname']

        self.target(url)
        firstname = self.browser.find_element_by_xpath(xpath).get_attribute('value')

        return firstname

    def get_user_lastname(self):
        if not self.session == 'nimbus':
            print('You need to log in to nimbus')
            return -1

        print("Getting real user's lastname")
        url = urls['nimbus_profile']
        xpath = xpaths['user_lastname']

        self.target(url)
        lastname = self.browser.find_element_by_xpath(xpath).get_attribute('value')

        return lastname

    def get_classes(self):
        if not self.session == 'nimbus':
            print('You need to log in to nimbus')
            return -1

        url = urls['nimbus_classes']

        self.target(url)

        print('Getting the whole classes of the session')

        class_ids = self.get_class_ids()
        course_ids = self.get_course_ids()
        course_names = self.get_course_names()
        class_turns = self.get_class_turns()
        class_sections = self.get_class_sections()
        course_terms = self.get_course_terms()
        class_modes = self.get_class_modes()

        classes = []
        for i in range(len(class_ids)):
            class_info = {}
            class_info["class_id"] = class_ids[i]
            class_info["course_id"] = course_ids[i]
            class_info["course_name"] = course_names[i]
            class_info["class_turn"] = class_turns[i]
            class_info["class_section"] = class_sections[i]
            class_info["course_term"] = course_terms[i]
            class_info["class_mode"] = class_modes[i]

            classes.append(class_info)
            
        print('Getting all the classes')
        return classes

    def get_class_ids(self):
        if not self.session == 'nimbus':
            print('You need to log in to nimbus')
            return -1

        url = urls['nimbus_classes']

        self.target(url)

        print('Getting the class ids of the session')

        class_ids = []
        elements = self.browser.find_elements_by_xpath(xpaths['class_ids'])

        for e in elements:
            class_ids.append(e.text)

        return class_ids

    def get_course_names(self):
        if not self.session == 'nimbus':
            print('You need to log in to nimbus')
            return -1

        url = urls['nimbus_classes']

        self.target(url)

        print('Getting the course names of the session')

        course_names = []
        elements = self.browser.find_elements_by_xpath(xpaths['course_names'])

        for e in elements:
            course_names.append(e.text)

        return course_names

    def get_course_ids(self):
        if not self.session == 'nimbus':
            print('You need to log in to nimbus')
            return -1

        url = urls['nimbus_classes']

        self.target(url)

        print('Getting the course ids of the session')

        course_ids = []
        elements = self.browser.find_elements_by_xpath(xpaths['course_ids'])

        for e in elements:
            course_ids.append(e.text[7:11])

        return course_ids

    def get_class_turns(self):
        if not self.session == 'nimbus':
            print('You need to log in to nimbus')
            return -1

        url = urls['nimbus_classes']

        self.target(url)

        print('Getting the class turns of the session')

        class_turns = []
        elements = self.browser.find_elements_by_xpath(xpaths['class_turns'])

        for e in elements:
            class_turns.append(e.text[20:21])

        return class_turns

    def get_course_terms(self):
        if not self.session == 'nimbus':
            print('You need to log in to nimbus')
            return -1

        url = urls['nimbus_classes']

        self.target(url)

        print('Getting the course terms of the session')

        course_terms = []
        elements = self.browser.find_elements_by_xpath(xpaths['course_terms'])

        for e in elements:
            course_terms.append(e.text[30:32])

        return course_terms

    def get_class_sections(self):
        if not self.session == 'nimbus':
            print('You need to log in to nimbus')
            return -1

        url = urls['nimbus_classes']

        self.target(url)

        print('Getting the class sections of the session')

        class_sections = []
        elements = self.browser.find_elements_by_xpath(xpaths['class_sections'])

        for e in elements:
            class_sections.append(e.text[43:45])

        return class_sections

    def get_class_modes(self):
        if not self.session == 'nimbus':
            print('You need to log in to nimbus')
            return -1

        url = urls['nimbus_classes']

        self.target(url)

        print('Getting the class modes of the session')

        class_modes = []
        elements = self.browser.find_elements_by_xpath(xpaths['class_modes'])

        for e in elements:
            class_modes.append(e.text[58:70])

        return class_modes
