from seleniumwire import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
from time import sleep
import json
import gzip
import os
from dotenv import load_dotenv
from securid.stoken import StokenFile


load_dotenv()


def token_now():
    stoken = StokenFile(data=os.getenv('RSA_TOKEN'))
    gen = stoken.get_token(password=os.getenv('RSA_USER'))

    return gen.now(int(os.getenv('RSA_PIN')))


def get_driver():
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    driver = webdriver.Chrome(options=options)

    return driver


def get_auth_token(requests_list, links):
    token = False
    for req in requests_list:
        if req.url == links['tokens']:
            if 'authorization_code' in req.body.decode():
                token = json.loads(gzip.decompress(req.response.body).decode())['access_token']

    return token


def login(driver, links, timeout_padrao=15, tries=1):
    """Efetua Login e retorna token de autorização para API"""


    print("Iniciando login")
    if tries == 3:
        raise Exception('Tentativas excedidas')
    
    driver.requests.clear()

    driver.get(links['login'])
    try:
        sleep(5)
        WebDriverWait(driver, timeout_padrao).until(EC.frame_to_be_available_and_switch_to_it((By.ID,"iframe")))

        login_field = WebDriverWait(driver, timeout_padrao).until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'input[ng-model="formData.cpf"]')))
        password_field = WebDriverWait(driver, timeout_padrao).until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'input[ng-model="formData.senha"]')))
        button = WebDriverWait(driver, timeout_padrao).until(EC.visibility_of_element_located((By.ID, 'btn-login')))

        login_field.clear()
        password_field.clear()

        login_field.send_keys(os.getenv('RSA_USER'))
        password_field.send_keys(token_now())
        button.click()
        sleep(5)

        print('Login efetuado com sucesso')
        res = get_auth_token(driver.requests, links)
        
        if res is False:
            raise Exception('Token não encontrada')
        
        print("Token Encontrada!")
        return res
    
    except Exception as e:
        print('Erro ao tentar logar', e)
        sleep(5)
        return login(driver, links, timeout_padrao, tries=tries+1)


def auth_token():
    links = {
        'login': 'https://apptimvendas.timbrasil.com.br/#/login',
        'tokens': 'https://authb2b2c.tim.com.br/ms_oauth/oauth2/endpoints/oauthservice/tokens/'
    }
    driver = get_driver()
    token = login(driver, links)
    driver.quit()
    return token


def load_token_env():
    load_dotenv()
    os.environ['JWT_TOKEN'] = auth_token()
    return os.getenv('JWT_TOKEN')

