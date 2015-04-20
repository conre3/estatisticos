#! /usr/bin/python
# -*- coding: utf-8 -*-
"""
Created on Tue Jul 15 11:33:59 2014
@author: julio
"""

from pyvirtualdisplay import Display
from selenium import webdriver
import selenium.webdriver.support.ui as ui
import sys
import time
import os
import os.path

disp = True

if disp:
  display = Display(visible=0, size=(800, 600))
  aux = display.start()
chromedriver = "chromedriver"
os.environ["webdriver.chrome.driver"] = chromedriver
driver = webdriver.Chrome(chromedriver)
# driver = webdriver.Firefox()
wait = ui.WebDriverWait(driver, 20)

def pega_pessoa(nm, path):
  link = 'http://www.google.com/search?q=%s' % (nm)
  arq = path + str(nm).encode('UTF-8').replace(' ', '_') + '.html'
  if not os.path.isfile(arq):
    print arq
    driver.get(link)
    f = open(arq, 'w')
    f.write(driver.page_source.encode('UTF-8'))
    f.close()
