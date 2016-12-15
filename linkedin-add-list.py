# python linkedin-add-list.py -i ../../data/list.txt

import sys
import json
import time
import getopt
import subprocess
from selenium import webdriver
from SeleniumHelper import SeleniumHelper

class LinkedinController(SeleniumHelper):

	TIMEOUT = 20
	LOGIN_USER_VALUE = ''
	LOGIN_PASS_VALUE = ''
	INITIAL_URL_NORMAL = 'https://www.linkedin.com/'
	LOGIN_USER_PATH_NORMAL = '#login-email'
	LOGIN_PASS_PATH_NORMAL = '#login-password'
	SEARCH_BAR_PATH_NORMAL = '#main-search-box'
	LAYOUT_PROFILE = '.profile-overview'
	USER_ADD_BUTTON_NORMAL = 'a[data-action-name="add-to-network"]'
	LAYOUT_FRIEND = '.iwrite'
	USER_ADD_FRIEND_OPTION = 'input[value="IF"]'
	USER_ADD_BUTTON_INVITE = '#send-invite-button'
	USER_ADD_ALERT = 'div.alert.success'
	WAIT = 99999
	driver = None
	data = {}
	baseUrl = ''

	def start(self, fileName):
		print 'Logging in'
		exit = []
		self.login()
		contactList = []
		with open(fileName) as f:
			contactList = f.readlines()
		num = 0
		for contact in contactList:
			print contact
			self.loadPage(contact)
			try:
				self.waitShowElement(self.LAYOUT_PROFILE)
				addButton = self.getElement(self.USER_ADD_BUTTON_NORMAL)
				if addButton:
					self.click(addButton)
					self.waitShowElement(self.LAYOUT_FRIEND)
					friendOption = self.getElement(self.USER_ADD_FRIEND_OPTION)
					if friendOption:
						self.click(friendOption)
						inviteButton = self.getElement(self.USER_ADD_BUTTON_INVITE)
						self.click(inviteButton)
						self.waitShowElement(self.USER_ADD_ALERT)
						num = num + 1
						print num
			except:
				pass
		self.close()
		return exit

	def login(self):
		self.loadPage(self.INITIAL_URL_NORMAL)
		self.waitAndWrite(self.LOGIN_USER_PATH_NORMAL, self.LOGIN_USER_VALUE)
		self.submitForm(self.selectAndWrite(self.LOGIN_PASS_PATH_NORMAL, self.LOGIN_PASS_VALUE))
		element = self.waitShowElement(self.SEARCH_BAR_PATH_NORMAL)

	def close(self):
		self.driver.quit()

	def __init__(self): 
		self.driver = webdriver.Firefox()
		self.driver.set_page_load_timeout(self.TIMEOUT)

def main(argv):
	fileName = 'list.txt'
	opts, args = getopt.getopt(argv, "i:")
	if opts:
		for o, a in opts:
			if o == "-i":
				fileName = a
	linkedin = LinkedinController()
	linkedin.start(fileName=fileName)

if __name__ == "__main__":
    main(sys.argv[1:])