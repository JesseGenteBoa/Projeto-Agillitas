from pyautogui import locateOnScreen, locateCenterOnScreen, hotkey, press, FAILSAFE
from pydirectinput import click as mouseClique, moveTo, doubleClick                        
from time import sleep
from email.message import EmailMessage
import pyscreeze
import smtplib


FAILSAFE = True

def enviarEmail(rt, dono_da_rt, sem_xml, chave_inconforme, nf_ja_lancada, cond_pag, bloqueado, cnpj_inconclusivo, chave_sefaz, ncm_problematica):
    mensagens = []
    
    if len(chave_sefaz) > 0:
        mensagem_chave = f"{len(chave_sefaz)} processo(s) onde o sistema aponta que a chave de acesso não foi encontrada no SEFAZ."
    else:
        mensagem_chave = ""
    mensagens.append(mensagem_chave)

    if len(ncm_problematica) > 0:
        mensagem_ncm = f"{len(ncm_problematica)} processo(s) onde o sistema aponta que a NCM está incorreta."
    else:
        mensagem_ncm = ""
    mensagens.append(mensagem_ncm)

    if len(sem_xml) > 0:
        mensagem_xml_aus = f"{len(sem_xml)} processo(s) que não tenho o XML no meu repositório."
    else:
        mensagem_xml_aus = ""
    mensagens.append(mensagem_xml_aus)

    if len(cond_pag) > 0:
        mensagem_cond_pag = f"{len(cond_pag)} processo(s) com erro na condição de pagamento."
    else:
        mensagem_cond_pag = ""
    mensagens.append(mensagem_cond_pag)

    if len(cnpj_inconclusivo) > 0:
        mensagem_cnpj = f"{len(cnpj_inconclusivo)} processo(s) onde o sistema aponta um erro no CNPJ."
    else:
        mensagem_cnpj = ""
    mensagens.append(mensagem_cnpj)

    if len(chave_inconforme) > 0:
        mensagem_ch_inc = f"{len(chave_inconforme)} processo(s) com uma chave de acesso impossível."
    else:
        mensagem_ch_inc = ""
    mensagens.append(mensagem_ch_inc)

    if len(nf_ja_lancada) > 0:
        mensagem_xml = f"{len(nf_ja_lancada)} processo(s) já lançados segundo a rotina IntAgillitas"
    else:
        mensagem_xml = ""
    mensagens.append(mensagem_xml)

    if len(bloqueado) > 0:
        mensagem_bloq = f"{len(bloqueado)} processo(s) com um item bloqueado."
    else:
        mensagem_bloq = ""
    mensagens.append(mensagem_bloq)

    mensagem = [str(elemento) for elemento in mensagens if elemento != ""]
    string = "\n".join(mensagem)


    corpo = f"""
Olá, colaborador!


Não consegui finalizar a {rt[0]} - {dono_da_rt[0]}                 

Causa:
{string}


Pode me ajudar?

Atenciosamente,
Mariquinha,
    """
    
    carta = EmailMessage()
    carta.set_content(corpo)
    carta['Subject'] = "RT para verificar"
    carta['From'] = "bot.contabil@eqseng.com.br"
    carta['To'] = ["caixa@eqsengenharia.com.br", "jesse.silva@eqsengenharia.com.br"]

    try:
        with smtplib.SMTP_SSL('grid331.mailgrid.com.br', 465) as servidor:
            servidor.login("eqsengenharia@eqsengenharia.com.br", "YXPLlbnL2N")
            servidor.send_message(carta)
    except Exception as e:
        pass
 


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


def aguardar():
    penultimo_aguarde = esperarAparecer(r'Imagens\telaDeAguarde1.png')
    sleep(0.6)
    aguarde_final = encontrarImagemLocalizada(r'Imagens\ultimoAguarde.png')
    while type(aguarde_final) == tuple:
        aguarde_final = encontrarImagemLocalizada(r'Imagens\ultimoAguarde.png')
    sleep(2)


def aguardar1():
    aguarde = encontrarImagem(r'Imagens\telaDeAguarde1.png')
    while type(aguarde) == pyscreeze.Box:
        aguarde = encontrarImagem(r'Imagens\telaDeAguarde1.png')


def aguardar2():
    aguarde1 = encontrarImagemLocalizada(r'Imagens\telaDeAguarde1.png')
    aguarde2 = encontrarImagemLocalizada(r'Imagens\telaDeAguarde2.png')
    return aguarde1, aguarde2


def lancarRetroativo():
    lancamento_retroativo = encontrarImagemLocalizada(r'Imagens\LancamentoRetroativo.png')
    if type(lancamento_retroativo) == tuple:
        sleep(0.5)
        press("enter")
        sleep(1)


def repetirBotao():
    repetir_acao = encontrarImagemLocalizada(r'Imagens\botaoLancarNota.png')
    while type(repetir_acao) == tuple:
        press("enter")
        repetir_acao = encontrarImagemLocalizada(r'Imagens\botaoLancarNota.png')


def tratarProcessosPendentes():
    press("enter")
    tabEEnter()
    sleep(2)
    repetirBotao()


def tratarEtapaFinal():
    x, y = clicarDuasVezes(r'Imagens\finalizarLancamento.png')
    sleep(0.7)
    while True:
        moveTo(150,100)
        quebrar_loop = encontrarImagemLocalizada(r'Imagens\quebrarloop.png')
        if type(quebrar_loop) != tuple:
            break
        else:
            doubleClick(x, y)


def clicarBotaoSair():
    botao_sair = encontrarImagemLocalizada(r'Imagens\finalizarESair.png')
    if type(botao_sair) == tuple:
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


def clicarMicrosiga(imagem=r'Imagens\microsiga.png'):
    try:
        x, y = encontrarImagemLocalizada(imagem)
        mouseClique(x, y)
    except:
        x, y = encontrarImagemLocalizada(r'Imagens\microsigaWin11.png')
        mouseClique(x, y)
    

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

