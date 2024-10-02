from pyautogui import locateOnScreen, locateCenterOnScreen, hotkey, press, position, write, FAILSAFE, FailSafeException
from pydirectinput import click as mouseClique, moveTo, doubleClick                        
from pyperclip import paste, copy
from time import sleep
from email.message import EmailMessage
import pyscreeze
import smtplib


FAILSAFE = True

def enviarEmail(rt, dono_da_rt, sem_xml, chave_inconforme, xml_ilegivel, cond_pag, bloqueado, cnpj_inconclusivo, chave_sefaz, ncm_problematica):
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

    if len(xml_ilegivel) > 0:
        mensagem_xml = f"{len(xml_ilegivel)} processo(s) com um XML ilegível para mim."
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
    carta['To'] = "jesse.silva@eqsengenharia.com.br, caixa@eqsengenharia.com.br"

    try:
        with smtplib.SMTP_SSL('mail.eqseng.com.br', 465) as servidor:
            servidor.login("bot.contabil@eqseng.com.br", "EQSeng852@")
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


def filtrarPorStatus(imagem=r'Imagens\statusNegrito.png'):
    caixa_finalizado = ''
    try:
        x, y = encontrarImagemLocalizada(imagem)
    except TypeError:
        x, y = encontrarImagemLocalizada(r'Imagens\status.png')
    doubleClick(x, y)
    sleep(1)
    doubleClick(x, y)
    sleep(1)
    caixa_finalizado = encontrarImagemLocalizada(r'Imagens\aindaNaoETempo.png')
    if type(caixa_finalizado) == tuple:
        doubleClick(x, y)
        caixa_finalizado = encontrarImagemLocalizada(r'Imagens\aindaNaoETempo.png')
        sleep(0.5)
    return caixa_finalizado


def solicitarXML():
    x, y = clicarDuasVezes(r'Imagens\solicitarXML.png')
    nf_cancelada = ""
    falsa_duplicidade = ""
    sleep(0.5)
    while True:
        nf_cancelada = encontrarImagemLocalizada(r'Imagens\nfCancelada.png')
        falsa_duplicidade = encontrarImagemLocalizada(r'Imagens\falsaDuplicidade.png')
        if type(nf_cancelada) == tuple or type(falsa_duplicidade) == tuple:
            press("right", interval=0.05)
            press("enter")
            sleep(0.5)
            break
        aguardando = encontrarImagemLocalizada(r'Imagens\telaDeAguarde1.png')
        if type(aguardando) == tuple:
            while type(aguardando) == tuple:
                aguardando = encontrarImagemLocalizada(r'Imagens\telaDeAguarde1.png')
        else:
            clicar_novamente = encontrarImagemLocalizada(r'Imagens\XMLPendente.png')
            if type(clicar_novamente) == tuple:
                doubleClick(x,y)
            else:
                break
    sleep(1)
    return nf_cancelada, falsa_duplicidade
    

def verificarStatus():
    sleep(0.3)
    status_xml2 = encontrarImagemLocalizada(r'Imagens\XMLPendente.png')
    if type(status_xml2) == tuple:
        controlador = 2
    else:
        status_xml3 = encontrarImagemLocalizada(r'Imagens\statusChaveDanfeNaoDisponivel.png')
        if type(status_xml3) == tuple:
            controlador = 3
        else:
            status_xml4 = encontrarImagemLocalizada(r'Imagens\disponivelPLancamento.png')
            if type(status_xml4) == tuple:
                controlador = 4
            else:
                status_xml1 = encontrarImagemLocalizada(r'Imagens\statusRecibo.png')
                if type(status_xml1) == tuple:
                    controlador = 1
                else:
                    status_xml5 = encontrarImagemLocalizada(r'Imagens\XMLPendente2.png')
                    if type(status_xml5) == tuple:
                        controlador = 2
                    else:
                        raise FailSafeException
    return controlador


def clicarEmLancar():
    sleep(0.5)
    x, y = clicarDuasVezes(r'Imagens\botaoLancarNota.png')
    doubleClick(x,y)
    sleep(0.3)

    lancarRetroativo()
    aguarde1, aguarde2 = aguardar2()
    if type(aguarde1) == tuple or type(aguarde2) == tuple:
        while True:
            aguarde3, aguarde4 = aguardar2()
            if type(aguarde3) != tuple and type(aguarde4) != tuple:
                lancarRetroativo()
                aguarde3, aguarde4 = aguardar2()
                if type(aguarde3) != tuple and type(aguarde4) != tuple:
                    break
    else:
        lancarRetroativo()
        aguarde1, aguarde2 = aguardar2()
        if type(aguarde1) != tuple and type(aguarde2) != tuple:
            doubleClick(x,y)
    sleep(1)

    caixa_finalizado = encontrarImagem(r'Imagens\jaLancado.png')
    if type(caixa_finalizado) == pyscreeze.Box:
        caixa_finalizado = True
    else:
        caixa_finalizado = False
    return caixa_finalizado


def copiarChaveDeAcesso():
    processo_feito_errado = False
    x, y = clicarDuasVezes(r'Imagens\copiarChaveDeAcesso.png')
    sleep(1)

    encontrar_chave_de_acesso = encontrarImagem(r'Imagens\abriuChaveDeAcesso.png')
    caixa_finalizado = encontrarImagem(r'Imagens\jaLancado.png')
    while type(encontrar_chave_de_acesso) != pyscreeze.Box:
        if type(caixa_finalizado) == pyscreeze.Box:
            caixa_finalizado = True
            chave_de_acesso = caixa_finalizado
            return chave_de_acesso, processo_feito_errado
        if type(encontrar_chave_de_acesso) != pyscreeze.Box:
            encontrar_chave_de_acesso = encontrarImagem(r'Imagens\abriuChaveDeAcesso.png')
            doubleClick(x, y)
            caixa_finalizado = encontrarImagem(r'Imagens\jaLancado.png')
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


def rejeitarCaixa(mensagem="Centro de Custo Bloqueado."):
    campo_mensagem = encontrarImagemLocalizada(r'Imagens\campoObservacaoRejeicao.png')

    while type(campo_mensagem) != tuple:
        sleep(0.6)
        x, y = clicarDuasVezes(r'Imagens\botaoRejeitarCaixa.png')
        sleep(0.7)
        campo_mensagem = encontrarImagemLocalizada(r'Imagens\campoObservacaoRejeicao.png')
        bloqueio_da_rejeicao = encontrarImagemLocalizada(r'Imagens\naoPodeRejeitar.png')
        if type(bloqueio_da_rejeicao) == tuple:
            press("enter")
            sleep(0.6)
            x, y = clicarDuasVezes(r'Imagens\statusNegrito.png')
            sleep(0.8)
            repetir_clique = encontrarImagemLocalizada(r'Imagens\aindaNaoETempo.png')
            if type(repetir_clique) != tuple:
                while type(repetir_clique) != tuple:
                    doubleClick(x, y)
                    moveTo(150,100)
                    repetir_clique = encontrarImagemLocalizada(r'Imagens\aindaNaoETempo.png')
            sleep(0.5)
            x, y = clicarDuasVezes(r'Imagens\botaoCancelar.png')
            tela_de_lancamento = esperarAparecer(r'Imagens\documentoEntrada.png')
            hotkey("ctrl", "s")
            sleep(0.5)
            aguarde1, aguarde2 = aguardar2()
            if type(aguarde1) == tuple or type(aguarde2) == tuple:
                while True:
                    aguarde3, aguarde4 = aguardar2()
                    if type(aguarde3) != tuple and type(aguarde4) != tuple:
                        break
        moveTo(150,100)

    copy(mensagem)
    hotkey("ctrl", "v")
    press("tab")
    press("enter")
    aguarde = encontrarImagem(r'Imagens\telaDeAguarde1.png')
    aux_cont = 0
    while type(aguarde) != pyscreeze.Box:
        aguarde = encontrarImagem(r'Imagens\telaDeAguarde1.png')
        aux_cont+=1
        if aux_cont == 0:
            break


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


def tratarCasoXML():
    filtrarPorStatus()
    press("down")


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
    x, y = encontrarImagemLocalizada(imagem)
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

