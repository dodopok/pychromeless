import os
import json
import time

from firebase import firebase
from webdriver_wrapper import WebDriverWrapper
from selenium.webdriver.common.keys import Keys

def lambda_handler(*args, **kwargs):
  driver = WebDriverWrapper()._driver
  db = firebase.FirebaseApplication('https://dash-associados-default-rtdb.firebaseio.com/', None)

  data =  {
    "username": "dodopokcamilo@gmail.com"
  }

  db.post('/users', data)

  # driver.get("https://associados.amazon.com.br")
  # driver.get_url('http://example.com')
  # example_text = driver.get_inner_html('(//div//h1)[1]')

  # driver.close()

  driver.get("https://associados.amazon.com.br")

  try:
    cookies_file = open("cookies.txt")
    if os.fstat(cookies_file.fileno()).st_size == 0:
      raise IOError

    for cookie in cookies_file:
      driver.add_cookie(json.loads(cookie))
  except IOError:
    driver.find_element_by_xpath("//a[@href='/login']").click()

    username = driver.find_element_by_id("ap_email")
    username.clear()
    username.send_keys("dodopokcamilo@gmail.com")

    password = driver.find_element_by_id("ap_password")
    password.clear()
    password.send_keys("infOaz19!")

    driver.find_element_by_id("signInSubmit").click()

    while ('home' not in driver.current_url):
      if 'approval' in driver.current_url:
        print('Aprove o login no celular.')
        fastrack = WebDriverWait(driver, 300).until(ec.visibility_of_element_located((By.XPATH, "//div[@data-assoc-eid='ac-home-month-summary']")))
      elif 'signin' in driver.current_url:
        captcha_img = driver.find_element_by_xpath("//img[@alt='CAPTCHA']").get_attribute("src")
        print(captcha_img)

        captcha_input = driver.find_element_by_id("auth-captcha-guess")
        captcha = input("Digite o CAPTCHA e aperte ENTER\n")
        print(f'Usando o captcha "{captcha}"')
        captcha_input.send_keys(captcha)
        password = driver.find_element_by_id("ap_password")
        password.clear()
        password.send_keys("infOaz19")
        driver.find_element_by_id("signInSubmit").click()

    with open("cookies.txt", "w") as cookies_file:
      for cookie in driver.get_cookies():
        cookies_file.write(json.dumps(cookie) + '\n')

  finally:
    cookies_file.close()

    summaries = driver.find_elements_by_xpath("//div[@data-assoc-eid='ac-home-month-summary']//div[contains(@class, 'a-row')]//div[contains(@class, 'a-ws-span-last')]")
    total_sent = summaries[0].text
    total_gains = summaries[1].text
    total_ordered = summaries[2].text
    total_clicks = summaries[3].text

    driver.close()
    
    return f'Produtos pedidos: "{total_sent}" - Ganho: "{total_gains}" - Produtos pedidos: "{total_ordered}" - Cliques: "{total_clicks}"'
