from pyautogui import locateOnScreen, locateCenterOnScreen, hotkey, press, position, write, FAILSAFE, FailSafeException
from pydirectinput import click as mouseClique, moveTo, doubleClick                        
from pyperclip import paste
from time import sleep
import pyscreeze


FAILSAFE = True

def encontrarImagem(imagem):
    cont = 0
    while True:
        try:
            encontrou = locateOnScreen(imagem, grayscale=True, confidence = 0.85)
            return encontrou
        except:
            sleep(0.8)
            cont += 1
            if cont == 2:
                break
            print("Imagem não encontrada")
            pass
            

def encontrarImagemLocalizada(imagem):
    cont = 0
    while True:
        try:
            x, y = locateCenterOnScreen(imagem, grayscale=True, confidence=0.92)     
            return (x, y)
        except:
            sleep(0.8)
            cont += 1
            if cont == 2:
                break
            print("Imagem não encontrada")
            pass


def clicarMicrosiga(imagem=r'Imagens\microsiga.png'):
    x, y = encontrarImagemLocalizada(imagem)
    mouseClique(x, y)


def filtrarPorStatus(imagem=r'Imagens\statusNegrito.png'):
    try:
        x, y = encontrarImagemLocalizada(imagem)
    except TypeError:
        x, y = encontrarImagemLocalizada(r'Imagens\status.png')
    doubleClick(x, y)
    sleep(1)
    doubleClick(x, y)
    sleep(1)
    repetir_clique = encontrarImagemLocalizada(r'Imagens\aindaNaoETempo.png')
    if type(repetir_clique) == tuple:
        doubleClick(x, y)


def solicitarXML():
    solicitar_xml = encontrarImagemLocalizada(r'Imagens\solicitarXML.png')
    x, y = solicitar_xml
    doubleClick(x,y)
    while True:
        aguardando = encontrarImagemLocalizada(r'Imagens\solicitandoXML.png')
        if type(aguardando) == tuple:
            while type(aguardando) == tuple:
                aguardando = encontrarImagemLocalizada(r'Imagens\solicitandoXML.png')
        else:
            clicar_novamente = encontrarImagemLocalizada(r'Imagens\XMLPendente.png')
            if type(clicar_novamente) == tuple:
                doubleClick(x,y)
            else:
                break
    sleep(1)
    

def formatador(variavel, casas_decimais="{:.2f}"):
    variavel = float(variavel)
    variavel = casas_decimais.format(variavel)
    variavel = variavel.replace(".", ",")
    return variavel

def formatador2(variavel):
    variavel = float(variavel)
    variavel = "{:.2f}".format(variavel)
    return variavel

def formatador3(variavel):
    variavel = variavel.replace(",", ".")
    variavel = float(variavel)
    return variavel

def formatador4(variavel):
    variavel = variavel.replace(".", "")
    variavel = formatador3(variavel)
    return variavel


def verificarStatus():
    sleep(0.5)
    status_xml1 = encontrarImagemLocalizada(r'Imagens\statusRecibo.png')
    status_xml2 = encontrarImagemLocalizada(r'Imagens\XMLPendente.png')
    status_xml3 = encontrarImagemLocalizada(r'Imagens\statusChaveDanfeNaoDisponivel.png')
    status_xml4 = encontrarImagemLocalizada(r'Imagens\disponivelPLancamento.png')
    if type(status_xml1) == tuple:
        controlador = 1
    elif type(status_xml2) == tuple:
        controlador = 2
    elif type(status_xml3) == tuple:
        controlador = 3
    elif type(status_xml4) == tuple:
        controlador = 4
    else:
        print("Abóbora Bliu Sunshine")
    return controlador


def clicarEmLancar():
    sleep(0.5)
    botao_lancar = encontrarImagemLocalizada(r'Imagens\botaoLancarNota.png')
    x, y = botao_lancar
    doubleClick(x,y)
    doubleClick(x,y)
    aguarde1 = encontrarImagem(r'Imagens\telaDeAguarde1.png')
    aguarde2 = encontrarImagem(r'Imagens\telaDeAguarde2.png')
    if type(aguarde1) == pyscreeze.Box or type(aguarde2) == pyscreeze.Box:
        while True:
            aguarde3 = encontrarImagemLocalizada(r'Imagens\telaDeAguarde1.png')
            aguarde4 = encontrarImagemLocalizada(r'Imagens\telaDeAguarde2.png')
            if type(aguarde3) != tuple and type(aguarde4) != tuple:
                break
    else:
        aguarde1 = encontrarImagem(r'Imagens\telaDeAguarde1.png')
        aguarde2 = encontrarImagem(r'Imagens\telaDeAguarde2.png')
        if type(aguarde1) != pyscreeze.Box and type(aguarde2) != pyscreeze.Box:
            doubleClick(x,y)
    sleep(0.5)
    caixa_finalizado = encontrarImagem(r'Imagens\jaLancado.png')
    if type(caixa_finalizado) == pyscreeze.Box:
        caixa_finalizado = True
    else:
        caixa_finalizado = False
    return caixa_finalizado


def tratarCCBloqueado():
    estado_do_caixa = False
    sleep(0.7)
    hotkey("shift", "tab", interval=0.05)
    press("down")
    outro_recibo = verificarStatus()
    if outro_recibo == 1:
        sleep(0.5)
        filtro_de_tipo = encontrarImagemLocalizada(r'Imagens\filtroTipo.png')
        x, y = filtro_de_tipo
        doubleClick(x,y)
        sleep(1)
        doubleClick(x,y)
        outro_recibo = verificarStatus()
        if outro_recibo == 1:
            estado_do_caixa = True
            return estado_do_caixa


def copiarChaveDeAcesso():
    processo_feito_errado = False
    botao_chave_de_acesso = encontrarImagemLocalizada(r'Imagens\copiarChaveDeAcesso.png')
    x, y = botao_chave_de_acesso
    doubleClick(x, y)
    sleep(1)
    encontrar_chave_de_acesso = encontrarImagem(r'Imagens\abriuChaveDeAcesso.png')
    caixa_finalizado = encontrarImagem(r'Imagens\jaLancado.png')
    if type(caixa_finalizado) == pyscreeze.Box:
        caixa_finalizado = True
        chave_de_acesso = caixa_finalizado
        return chave_de_acesso, processo_feito_errado
    while type(encontrar_chave_de_acesso) != pyscreeze.Box:
        encontrar_chave_de_acesso = encontrarImagem(r'Imagens\abriuChaveDeAcesso.png')
        doubleClick(x, y)
    sleep(0.5)
    hotkey("ctrl", "c")
    chave_de_acesso = paste()
    chave_de_acesso = chave_de_acesso.replace(" ", "")
    if len(chave_de_acesso) != 44:
        processo_feito_errado = True
    sleep(0.5)
    press("esc")
    sleep(2)
    return chave_de_acesso, processo_feito_errado


def copiarRT(passos=1):
    sleep(0.5)
    hotkey(["shift", "tab"]*passos)
    sleep(0.5)
    hotkey("ctrl", "c")
    dono_da_rt = paste()
    hotkey(["shift", "tab"]*2)
    sleep(0.5)
    hotkey("ctrl", "c")
    rt = paste()
    rt = rt.replace(" ", "")
    return dono_da_rt, rt


def aguardar():
    penultimo_aguarde = esperarAparecer(r'Imagens\telaDeAguarde1.png')
    sleep(0.6)
    aguarde_final = encontrarImagemLocalizada(r'Imagens\ultimoAguarde.png')
    while type(aguarde_final) == tuple:
        aguarde_final = encontrarImagemLocalizada(r'Imagens\ultimoAguarde.png')
    sleep(2)


def tratarEtapaFinal():
    press(["tab"]*3, interval=0.9)
    press("enter")
    sleep(1.5)
    repentina_etapa_final = encontrarImagemLocalizada(r'Imagens\etapaFinal.png')
    if type(repentina_etapa_final) == tuple:
        press("enter")
        sleep(1.5)


def clicarBotaoSair():
    botao_sair = encontrarImagem(r'Imagens\finalizarESair.png')
    if type(botao_sair) == pyscreeze.Box:
        print("Strogonoff")
        press(["tab"]*6)
        sleep(0.3)
        press("enter")
        sleep(1)


def tabEEnter():
    press(["tab"]*4)
    sleep(0.5)
    press("enter")
    sleep(1)


def esperarAparecer(imagem):
    encontrar = encontrarImagemLocalizada(imagem)
    while type(encontrar) != tuple:
        encontrar = encontrarImagemLocalizada(imagem)
    return encontrar


def clicarEmFinalizar():
    press("enter")          
    sleep(1)  
    x, y = clicarDuasVezes(r'Imagens\botaoFinalizar.png')
    sleep(1)
    return x, y


def tratarCasoXML():
    dono_da_rt, rt = copiarRT(passos=4)
    filtrarPorStatus()
    press("down")
    print("Não tenho essa XML, meu nobre", rt, dono_da_rt)
    #enviar Email


def passosParaRecomecar():
    hotkey("shift", "tab", interval=0.05)
    press("enter")
    sleep(1)
    press("down")


def clicarDuasVezes(imagem):
    variavel = encontrarImagemLocalizada(imagem)
    x, y = variavel
    doubleClick(x,y)
    return x, y