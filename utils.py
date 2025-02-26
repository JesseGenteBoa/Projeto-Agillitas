import pyautogui as ptg
from time import sleep
from email.message import EmailMessage
import pyscreeze
import smtplib


FAILSAFE = True

def enviar_email(rt, dono_da_rt, sem_xml, chave_inconforme, nf_ja_lancada, cond_pag, bloqueado, cnpj_inconclusivo, chave_sefaz, ncm_problematica):
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
 


def encontrar_imagem(imagem):
    cont = 0
    while True:
        try:
            encontrou = ptg.locateOnScreen(imagem, grayscale=True, confidence = 0.85)
            return encontrou
        except:
            sleep(0.8)
            cont += 1
            if cont == 2:
                break
            print("Imagem não encontrada")
            pass
            

def encontrar_centro_imagem(imagem):
    cont = 0
    while True:
        try:
            x, y = ptg.locateCenterOnScreen(imagem, grayscale=True, confidence=0.92)     
            return (x, y)
        except:
            sleep(0.8)
            cont += 1
            if cont == 2:
                break
            print("Imagem não encontrada")
            pass


def aguardar():
    _ = esperar_aparecer(r'Imagens\telaDeAguarde1.png')
    sleep(0.6)
    aguarde_final = encontrar_centro_imagem(r'Imagens\ultimoAguarde.png')
    while type(aguarde_final) == tuple:
        aguarde_final = encontrar_centro_imagem(r'Imagens\ultimoAguarde.png')
    sleep(2)


def aguardar1():
    aguarde = encontrar_imagem(r'Imagens\telaDeAguarde1.png')
    while type(aguarde) == pyscreeze.Box:
        aguarde = encontrar_imagem(r'Imagens\telaDeAguarde1.png')


def aguardar2():
    aguarde1 = encontrar_centro_imagem(r'Imagens\telaDeAguarde1.png')
    aguarde2 = encontrar_centro_imagem(r'Imagens\telaDeAguarde2.png')
    return aguarde1, aguarde2


def lancar_retroativo():
    lancamento_retroativo = encontrar_centro_imagem(r'Imagens\LancamentoRetroativo.png')
    if type(lancamento_retroativo) == tuple:
        sleep(0.5)
        ptg.press("enter")
        sleep(1)


def repetir_botao():
    repetir_acao = encontrar_centro_imagem(r'Imagens\botaoLancarNota.png')
    while type(repetir_acao) == tuple:
        ptg.press("enter")
        repetir_acao = encontrar_centro_imagem(r'Imagens\botaoLancarNota.png')


def tratar_processos_pendentes():
    ptg.press("enter")
    ptg.press(["tab"]*4)
    sleep(0.5)
    ptg.press("enter")
    sleep(2.5)
    repetir_botao()


def tratar_etapa_final():
    x, y = clicar_2x(r'Imagens\finalizarLancamento.png')
    sleep(0.7)
    while True:
        ptg.moveTo(150,100)
        quebrar_loop = encontrar_centro_imagem(r'Imagens\quebrarloop.png')
        if type(quebrar_loop) != tuple:
            break
        else:
            ptg.doubleClick(x, y)


def clicar_botao_sair():
    botao_sair = encontrar_centro_imagem(r'Imagens\finalizarESair.png')
    if type(botao_sair) == tuple:
        ptg.press(["tab"]*6)
        sleep(0.3)
        ptg.press("enter")
        sleep(1)
    

def esperar_aparecer(imagem):
    encontrar = encontrar_centro_imagem(imagem)
    while type(encontrar) != tuple:
        encontrar = encontrar_centro_imagem(imagem)
    return encontrar


def clicar_finalizar():
    ptg.press("enter")          
    sleep(1)  
    x, y = clicar_2x(r'Imagens\botaoFinalizar.png')
    sleep(1)
    return x, y


def clicar_2x(imagem):
    variavel = encontrar_centro_imagem(imagem)
    x, y = variavel
    ptg.doubleClick(x,y)
    return x, y


def clicar_microsiga(imagem=r'Imagens\microsiga.png'):
    try:
        x, y = encontrar_centro_imagem(imagem)
        ptg.click(x, y)
    except:
        x, y = encontrar_centro_imagem(r'Imagens\microsigaWin11.png')
        ptg.click(x, y)
    

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

