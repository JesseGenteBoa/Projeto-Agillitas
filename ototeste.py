from selenium import webdriver                         
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from time import sleep
from pyautogui import hotkey, press, write, FAILSAFE, FailSafeException



link = "https://www.fsist.com.br/"
options = webdriver.ChromeOptions()
options.add_argument(r'user-data-dir=C:\Users\User\AppData\Local\Google\Chrome\User Data\Perfil Selenium')
servico = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=servico, options=options)
driver.get(link)


chave_de_acesso = "11240602421421027230552720000151561747853050"


input_chave_de_acesso = driver.find_element(By.XPATH, '/html/body/div[3]/div[1]/div/div[1]/div[1]/table[1]/tbody/tr[2]/td/input')
sleep(0.3)
input_chave_de_acesso.send_keys(chave_de_acesso)
botao = driver.find_element(By.XPATH, "/html/body/div[3]/div[1]/div/div[1]/div[1]/table[2]/tbody/tr/td[3]/a").click()
sleep(1)
#hotkey(["shift", "tab"]*12, interval=0.08)
#press("space")
sleep(30)
#press(["tab"]*4, interval=0.01)
#press("enter")


cont = 0
etapa_final = utils.encontrarImagem(r'Imagens\etapaFinal.png')
while type(etapa_final) != pyscreeze.Box:
    sleep(0.2)
    etapa_final = utils.encontrarImagem(r'Imagens\etapaFinal.png')
press(["tab"]*3, interval=0.9)
press("enter")
sleep(1.5)
utils.checarFailsafe()
ultimo_enter = utils.encontrarImagem(r'Imagens\finalizarLancamento.png')
if type(ultimo_enter) != pyscreeze.Box:
    while type(ultimo_enter) != pyscreeze.Box:
        sleep(0.2)
        ultimo_enter = utils.encontrarImagem(r'Imagens\finalizarLancamento.png')
        cont +=1
        if cont == 6:
            press("enter")
            cont = 0