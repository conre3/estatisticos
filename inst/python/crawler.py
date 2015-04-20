#! /usr/bin/python
# -*- coding: utf-8 -*-
"""
Created on Tue Jul 15 11:33:59 2014
@author: julio
"""

from pyvirtualdisplay import Display
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import selenium.webdriver.support.ui as ui
import sys
import time
import os
import os.path
import re
import unicodedata

disp = False
usuario = 'julioazt'
senha = '9517539'

if disp:
  display = Display(visible=0, size=(800, 600))
  aux = display.start()
chromedriver = "chromedriver"
os.environ["webdriver.chrome.driver"] = chromedriver
driver = webdriver.Chrome(chromedriver)
wait = ui.WebDriverWait(driver, 20)
url_login = 'https://www.tjsp.jus.br/cac/sge/login1.aspx'
driver.get(url_login)
wait.until(lambda driver: len(driver.find_elements_by_id("_CTL")) > 0)
time.sleep(1)
driver.find_element_by_id('_USR_LOGIN').send_keys(usuario)
driver.find_element_by_id('_CTL').click()
wait.until(lambda driver: len(driver.find_element_by_id("span__USR_NOME").get_attribute('innerHTML')) > 0)
driver.find_element_by_id('_CTL').send_keys(senha + Keys.ENTER)
time.sleep(5)

def espera():
  wait.until(lambda driver: ('display: none' in driver.find_element_by_id('gx_ajax_notification').get_attribute('style')))

def remove_accents(input_str):
    nkfd_form = unicodedata.normalize('NFKD', input_str)
    return u"".join([c for c in nkfd_form if not unicodedata.combining(c)])

def download_aulas_list():
  driver.find_element_by_xpath('//div[@id="Jscookmenu1"]//table//tbody//tr[1]//td[2]').click()
  driver.find_element_by_xpath('//table[@id="cmSubMenuID15Table"]//tbody//tr[1]//td[2]').click()
  driver.find_element_by_xpath('//table[@id="cmSubMenuID16Table"]//tbody//tr[1]//td[2]').click()
  time.sleep(2)

  xpath_tcurso = '//select[@id="_TCU_ID"]//option'
  xpath_cursos = '//select[@id="_CUR_ID"]//option'
  xpath_modulos = '//select[@id="_MOD_ID"]//option'
  xpath_aulas = '//select[@id="_CAL_ID"]//option'

  tirar = u'[$^",]|\n|\u2013|\u201c|\u201d'
  f = file('lista_aulas.csv', 'w')
  tipos_curso = driver.find_elements_by_xpath(xpath_tcurso)
  if len(tipos_curso) < 1 or tipos_curso[0].get_attribute('innerHTML') == '':
    tipos_curso = tipos_curso[1:]
  for tipo_curso in tipos_curso:
    id_tipo_curso = tipo_curso.get_attribute('value')
    nm_tipo_curso = tipo_curso.get_attribute('innerHTML')
    nm_tipo_curso = re.sub(tirar, '', nm_tipo_curso)
    tipo_curso.click()
    time.sleep(1)
    espera()
    cursos = driver.find_elements_by_xpath(xpath_cursos)
    if len(cursos) < 1 or cursos[0].get_attribute('innerHTML') == '':
      cursos = cursos[1:]
    for curso in cursos:
      id_curso = curso.get_attribute('value')
      nm_curso = curso.get_attribute('innerHTML')
      nm_curso = re.sub(tirar, '', nm_curso)
      curso.click()
      time.sleep(1)
      espera()
      modulos = driver.find_elements_by_xpath(xpath_modulos)
      if len(modulos) < 1 or modulos[0].get_attribute('innerHTML') == '':
        modulos = modulos[1:]
      for modulo in modulos:
        id_modulo = modulo.get_attribute('value')
        nm_modulo = modulo.get_attribute('innerHTML')
        nm_modulo = re.sub(tirar, '', nm_modulo)
        modulo.click()
        time.sleep(1)
        espera()
        time.sleep(1)
        aulas = driver.find_elements_by_xpath(xpath_aulas)
        if len(aulas) < 1 or aulas[0].get_attribute('innerHTML') == '':
          aulas = aulas[1:]
        for aula in aulas:
          try:
            id_aula = aula.get_attribute('value')
            nm_aula = aula.get_attribute('innerHTML')
            nm_aula = re.sub(tirar, '', nm_aula)
          except:
            id_aula = 'falhou'
            nm_aula = ''
          imprimir = '"%s","%s","%s","%s","%s","%s","%s","%s"\n' % (id_tipo_curso, nm_tipo_curso, id_curso, nm_curso, id_modulo, nm_modulo, id_aula, nm_aula)
          imprimir = remove_accents(imprimir)
          print imprimir
          f.write(imprimir)
  f.close()
  time.sleep(5)
  print '\n\nOK!!!'

#
# # __________________________________________________________________________________________________
#
# def baixa_freq_professores_from_list(path, usuario, senha):
#   display = Display(visible=0, size=(800, 600))
#   aux = display.start()
#   # LOGIN
#   # ________________________________________________________________________________________________
#   chromedriver = "chromedriver"
#   os.environ["webdriver.chrome.driver"] = chromedriver
#   driver = webdriver.Chrome(chromedriver)
#   wait = ui.WebDriverWait(driver, 20)
#   url_login = 'https://www.tjsp.jus.br/cac/sge/login1.aspx'
#   driver.get(url_login)
#   wait.until(lambda driver: len(driver.find_elements_by_id("_CTL")) > 0)
#   time.sleep(1)
#   driver.find_element_by_id('_USR_LOGIN').send_keys(usuario)
#   driver.find_element_by_id('_CTL').click()
#   wait.until(lambda driver: len(driver.find_element_by_id("span__USR_NOME").get_attribute('innerHTML')) > 0)
#   driver.find_element_by_id('_CTL').send_keys(senha + Keys.ENTER)
#   time.sleep(5)
#   driver.find_element_by_xpath('//div[@id="Jscookmenu1"]//table//tbody//tr[1]//td[2]').click()
#   driver.find_element_by_xpath('//table[@id="cmSubMenuID15Table"]//tbody//tr[1]//td[2]').click()
#   driver.find_element_by_xpath('//table[@id="cmSubMenuID16Table"]//tbody//tr[2]//td[2]').click()
#   time.sleep(2)
#   #_________________________________________________________________________________________________
#   # faltantes
#   f = file('faltantes.txt', 'r')
#   lista_faltantes = [a.replace('.html', '') for a in f.read().split(',')]
#   f.close()
#   for a in lista_faltantes[0:100]:
#     time.sleep(1)
#     try:
#       spl = a.split('_')
#       id_tipo_curso = spl[0]
#       id_curso = spl[1]
#       id_modulo = spl[2]
#       id_aula = spl[3]
#       time.sleep(1)
#       #wait.until(lambda driver: ('display: none' in driver.find_element_by_id('gx_ajax_notification').get_attribute('style')))
#       driver.find_element_by_xpath('//select[@id="_TCU_ID"]//option[@value="%s"]' % (id_tipo_curso)).click()
#       time.sleep(1)
#       #wait.until(lambda driver: ('display: none' in driver.find_element_by_id('gx_ajax_notification').get_attribute('style')))
#       driver.find_element_by_xpath('//select[@id="_CUR_ID"]//option[@value="%s"]' % (id_curso)).click()
#       time.sleep(1)
#       wait.until(lambda driver: ('display: none' in driver.find_element_by_id('gx_ajax_notification').get_attribute('style')))
#       driver.find_element_by_xpath('//select[@id="_MOD_ID"]//option[@value="%s"]' % (id_modulo)).click()
#       time.sleep(1)
#       wait.until(lambda driver: ('display: none' in driver.find_element_by_id('gx_ajax_notification').get_attribute('style')))
#       driver.find_element_by_xpath('//select[@id="_CAL_ID"]//option[@value="%s"]' % (id_aula)).click()
#       time.sleep(1)
#       wait.until(lambda driver: ('display: none' in driver.find_element_by_id('gx_ajax_notification').get_attribute('style')))
#       html = driver.page_source.encode('utf-8')
#       y = path + '/' + a + '.html'
#       print(y)
#       f = open(y, 'w')
#       f.write(html)
#       f.close()
#     except:
#       print '%s BUGOU !!!' % (a)
#   driver.close()
#   display.close()
#
#
# # __________________________________________________________________________________________________
# # __________________________________________________________________________________________________
# # __________________________________________________________________________________________________
#
#
# def baixa_freq_alunos(path, usuario, senha):
#
#   display = Display(visible=0, size=(800, 600))
#   aux = display.start()
#   chromedriver = "chromedriver"
#   os.environ["webdriver.chrome.driver"] = chromedriver
#   driver = webdriver.Chrome(chromedriver)
#
#   wait = ui.WebDriverWait(driver, 20)
#   url_login = 'https://www.tjsp.jus.br/cac/sge/login1.aspx'
#   driver.get(url_login)
#   wait.until(lambda driver: len(driver.find_elements_by_id("_CTL")) > 0)
#   time.sleep(1)
#   driver.find_element_by_id('_USR_LOGIN').send_keys(usuario)
#   driver.find_element_by_id('_CTL').click()
#   wait.until(lambda driver: len(driver.find_element_by_id("span__USR_NOME").get_attribute('innerHTML')) > 0)
#   driver.find_element_by_id('_CTL').send_keys(senha + Keys.ENTER)
#   time.sleep(5)
#
#   driver.find_element_by_xpath('//div[@id="Jscookmenu1"]//table//tbody//tr[1]//td[2]').click()
#   driver.find_element_by_xpath('//table[@id="cmSubMenuID15Table"]//tbody//tr[1]//td[2]').click()
#   driver.find_element_by_xpath('//table[@id="cmSubMenuID16Table"]//tbody//tr[1]//td[2]').click()
#   time.sleep(2)
#
#   # faltantes
#   f = file('faltantes.txt', 'r')
#   lista_faltantes = [a for a in f.read().split(',')]
#   f.close()
#
#   # frequencias dos alunos!!!
#   tipos_curso = driver.find_elements_by_xpath('//select[@id="_TCU_ID"]//option')
#   for tipo_curso in tipos_curso:
#     id_tipo_curso = tipo_curso.get_attribute('value')
#     tipo_curso.click()
#     time.sleep(1)
#     wait.until(lambda driver: ('display: none' in driver.find_element_by_id('gx_ajax_notification').get_attribute('style')))
#     cursos = driver.find_elements_by_xpath('//select[@id="_CUR_ID"]//option')
#     if len(cursos) < 1 or cursos[0].get_attribute('innerHTML') == '':
#       cursos = cursos[1:]
#     for curso in cursos:
#       id_curso = curso.get_attribute('value')
#       curso.click()
#       time.sleep(1)
#       wait.until(lambda driver: ('display: none' in driver.find_element_by_id('gx_ajax_notification').get_attribute('style')))
#       modulos = driver.find_elements_by_xpath('//select[@id="_MOD_ID"]//option')
#       if len(modulos) < 1 or modulos[0].get_attribute('innerHTML') == '':
#         modulos = modulos[1:]
#       for modulo in modulos:
#         id_modulo = modulo.get_attribute('value')
#         print id_modulo
#         modulo.click()
#         time.sleep(1)
#         wait.until(lambda driver: ('display: none' in driver.find_element_by_id('gx_ajax_notification').get_attribute('style')))
#         time.sleep(1)
#         aulas = driver.find_elements_by_xpath('//select[@id="_CAL_ID"]//option')
#         if len(aulas) < 1 or aulas[0].get_attribute('innerHTML') == '':
#           aulas = aulas[1:]
#         time.sleep(2)
#         aulas = driver.find_elements_by_xpath('//select[@id="_CAL_ID"]//option')
#         r = range(len(aulas))
#         for i in r:
#           if i < len(aulas):
#             aula = aulas[i]
#             try:
#               wait.until(lambda driver: ('display: none' in driver.find_element_by_id('gx_ajax_notification').get_attribute('style')))
#               id_aula = aula.get_attribute('value')
#               a = '%s_%s_%s_%s.html' % (id_tipo_curso, id_curso, id_modulo, id_aula)
#               arq = '%s/%s_%s_%s_%s.html' % (path, id_tipo_curso, id_curso, id_modulo, id_aula)
#               if a in lista_faltantes:
#                 aula.click()
#                 time.sleep(1)
#                 wait.until(lambda driver: ('display: none' in driver.find_element_by_id('gx_ajax_notification').get_attribute('style')))
#                 driver.find_element_by_xpath('//input[@name="BTNPESQUISAR"]').click()
#                 time.sleep(1)
#                 wait.until(lambda driver: ('display: none' in driver.find_element_by_id('gx_ajax_notification').get_attribute('style')))
#                 html = driver.page_source.encode('utf-8')
#                 print arq
#                 f = open(arq, 'w')
#                 f.write(html)
#                 f.close()
#                 time.sleep(1)
#                 wait.until(lambda driver: ('display: none' in driver.find_element_by_id('gx_ajax_notification').get_attribute('style')))
#             except:
#               id_aula = 'FALHOU'
#               arq = '%s/%s_%s_%s_%s.txt' % (path, id_tipo_curso, id_curso, id_modulo, id_aula)
#               print arq, 'BUGOU !!!'
#               f = open(arq, 'w')
#               f.write('falhou...')
#               f.close()
#             aulas = driver.find_elements_by_xpath('//select[@id="_CAL_ID"]//option')
#
#   time.sleep(5)
#   print 'OK'
#   driver.close()
#
# # __________________________________________________________________________________________________
# # __________________________________________________________________________________________________
# # __________________________________________________________________________________________________
#
#
# def lista_cursos(usuario, senha):
#   #display = Display(visible=0, size=(800, 600))
#   #aux = display.start()
#   chromedriver = "chromedriver"
#   os.environ["webdriver.chrome.driver"] = chromedriver
#   driver = webdriver.Chrome(chromedriver)
#   wait = ui.WebDriverWait(driver, 20)
#   url_login = 'https://www.tjsp.jus.br/cac/sge/login1.aspx'
#   driver.get(url_login)
#   wait.until(lambda driver: len(driver.find_elements_by_id("_CTL")) > 0)
#   time.sleep(1)
#   driver.find_element_by_id('_USR_LOGIN').send_keys(usuario)
#   driver.find_element_by_id('_CTL').click()
#   wait.until(lambda driver: len(driver.find_element_by_id("span__USR_NOME").get_attribute('innerHTML')) > 0)
#   driver.find_element_by_id('_CTL').send_keys(senha + Keys.ENTER)
#   time.sleep(5)
#   driver.find_element_by_xpath('//div[@id="Jscookmenu1"]//table//tbody//tr[1]//td[2]').click()
#   driver.find_element_by_xpath('//table[@id="cmSubMenuID15Table"]//tbody//tr[1]//td[2]').click()
#   driver.find_element_by_xpath('//table[@id="cmSubMenuID16Table"]//tbody//tr[1]//td[2]').click()
#   time.sleep(2)
#   tirar = u'[$^",]|\n|\u2013|\u201c|\u201d'
#   f = file('itens.csv', 'w')
#   tipos_curso = driver.find_elements_by_xpath('//select[@id="_TCU_ID"]//option')
#   if len(tipos_curso) < 1 or tipos_curso[0].get_attribute('innerHTML') == '':
#     tipos_curso = tipos_curso[1:]
#   for tipo_curso in tipos_curso:
#     id_tipo_curso = tipo_curso.get_attribute('value')
#     nm_tipo_curso = tipo_curso.get_attribute('innerHTML')
#     nm_tipo_curso = re.sub(tirar, '', nm_tipo_curso)
#     tipo_curso.click()
#     time.sleep(1)
#     wait.until(lambda driver: ('display: none' in driver.find_element_by_id('gx_ajax_notification').get_attribute('style')))
#     cursos = driver.find_elements_by_xpath('//select[@id="_CUR_ID"]//option')
#     if len(cursos) < 1 or cursos[0].get_attribute('innerHTML') == '':
#       cursos = cursos[1:]
#     for curso in cursos:
#       id_curso = curso.get_attribute('value')
#       nm_curso = curso.get_attribute('innerHTML')
#       nm_curso = re.sub(tirar, '', nm_curso)
#       curso.click()
#       time.sleep(1)
#       wait.until(lambda driver: ('display: none' in driver.find_element_by_id('gx_ajax_notification').get_attribute('style')))
#       modulos = driver.find_elements_by_xpath('//select[@id="_MOD_ID"]//option')
#       if len(modulos) < 1 or modulos[0].get_attribute('innerHTML') == '':
#         modulos = modulos[1:]
#       for modulo in modulos:
#         id_modulo = modulo.get_attribute('value')
#         nm_modulo = modulo.get_attribute('innerHTML')
#         nm_modulo = re.sub(tirar, '', nm_modulo)
#         modulo.click()
#         time.sleep(1)
#         wait.until(lambda driver: ('display: none' in driver.find_element_by_id('gx_ajax_notification').get_attribute('style')))
#         time.sleep(1)
#         aulas = driver.find_elements_by_xpath('//select[@id="_CAL_ID"]//option')
#         if len(aulas) < 1 or aulas[0].get_attribute('innerHTML') == '':
#           aulas = aulas[1:]
#         for aula in aulas:
#           try:
#             id_aula = aula.get_attribute('value')
#             nm_aula = aula.get_attribute('innerHTML')
#             nm_aula = re.sub(tirar, '', nm_aula)
#           except:
#             id_aula = 'falhou'
#             nm_aula = ''
#           imprimir = '"%s","%s","%s","%s","%s","%s","%s","%s"\n' % (id_tipo_curso, nm_tipo_curso, id_curso, nm_curso, id_modulo, nm_modulo, id_aula, nm_aula)
#           imprimir = remove_accents(imprimir)
#           print imprimir
#           f.write(imprimir)
#   f.close()
#   time.sleep(5)
#   print 'OK'
#   driver.close()
#
# # __________________________________________________________________________________________________
# # __________________________________________________________________________________________________
# # __________________________________________________________________________________________________
#
# def baixa_lista_aulas(path, usuario, senha):
#   driver.find_element_by_xpath('//div[@id="Jscookmenu1"]//table//tbody//tr[1]//td[2]').click()
#   driver.find_element_by_xpath('//table[@id="cmSubMenuID15Table"]//tbody//tr[1]//td[2]').click()
#   driver.find_element_by_xpath('//table[@id="cmSubMenuID16Table"]//tbody//tr[1]//td[2]').click()
#   time.sleep(2)
#   # faltantes
#   f = file('faltantes.txt', 'r')
#   lista_faltantes = [a.replace('.html', '') for a in f.read().split(',')]
#   f.close()
#   for a in lista_faltantes:
#     time.sleep(1)
#     try:
#       spl = a.split('_')
#       id_tipo_curso = spl[0]
#       id_curso = spl[1]
#       id_modulo = spl[2]
#       id_aula = spl[3]
#       time.sleep(1)
#       #wait.until(lambda driver: ('display: none' in driver.find_element_by_id('gx_ajax_notification').get_attribute('style')))
#       driver.find_element_by_xpath('//select[@id="_TCU_ID"]//option[@value="%s"]' % (id_tipo_curso)).click()
#       time.sleep(1)
#       #wait.until(lambda driver: ('display: none' in driver.find_element_by_id('gx_ajax_notification').get_attribute('style')))
#       driver.find_element_by_xpath('//select[@id="_CUR_ID"]//option[@value="%s"]' % (id_curso)).click()
#       time.sleep(1)
#       wait.until(lambda driver: ('display: none' in driver.find_element_by_id('gx_ajax_notification').get_attribute('style')))
#       driver.find_element_by_xpath('//select[@id="_MOD_ID"]//option[@value="%s"]' % (id_modulo)).click()
#       time.sleep(1)
#       wait.until(lambda driver: ('display: none' in driver.find_element_by_id('gx_ajax_notification').get_attribute('style')))
#       driver.find_element_by_xpath('//select[@id="_CAL_ID"]//option[@value="%s"]' % (id_aula)).click()
#       time.sleep(1)
#       wait.until(lambda driver: ('display: none' in driver.find_element_by_id('gx_ajax_notification').get_attribute('style')))
#       driver.find_element_by_xpath('//input[@name="BTNPESQUISAR"]').click()
#       time.sleep(1)
#       wait.until(lambda driver: ('display: none' in driver.find_element_by_id('gx_ajax_notification').get_attribute('style')))
#       html = driver.page_source.encode('utf-8')
#       y = path + '/' + a + '.html'
#       print(y)
#       f = open(y, 'w')
#       f.write(html)
#       f.close()
#     except:
#       print 'BUGOU !!!'

# __________________________________________________________________________________________________
# __________________________________________________________________________________________________
# __________________________________________________________________________________________________


# if __name__=='__main__':
#     if len(sys.argv) < 4:
#         sys.exit('Usage: python baixa_nfp.py path cpf senha')
#     if sys.argv[4] == 'lista':
#       lista_cursos(sys.argv[2], sys.argv[3])
#     else:
#       baixa_freq_professores_from_list(sys.argv[1], sys.argv[2], sys.argv[3])
