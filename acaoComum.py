from pyautogui import hotkey, press, write, FAILSAFE, FailSafeException
from pydirectinput import click as mouseClique, moveTo, doubleClick
from time import sleep
from pyperclip import paste, copy
import utils
import operadoresLancamento
import tratamentoItem
import xmltodict
import pyscreeze
import extratorXML


FAILSAFE = True

def procederPrimario():
    aguarde = utils.encontrarImagemLocalizada(r'Imagens\telaDeAguarde2.png')
    while type(aguarde) == tuple:
        aguarde = utils.encontrarImagemLocalizada(r'Imagens\telaDeAguarde2.png')
    encontrar = utils.encontrarImagem(r'Imagens\statusPendente.png')
    cont = 0
    while type(encontrar) != pyscreeze.Box:
        encontrar = utils.encontrarImagem(r'Imagens\statusPendente.png')
        cont+=1
        if cont == 2:
            press("enter")
            break 

    sleep(1)
    quebra_de_seguranca = utils.encontrarImagem(r'Imagens\quebraDeSeguranca.png')
    if type(quebra_de_seguranca) == pyscreeze.Box:
        raise FailSafeException

    while True:
        try:
            clique_status = utils.encontrarImagemLocalizada(r'Imagens\statusPendente.png')  
            x, y = clique_status
            break
        except TypeError:
            clique_status = utils.encontrarImagemLocalizada(r'Imagens\status.png')  
            x, y = clique_status
            break
        except:
            pass

    for _ in range(5):
        doubleClick(x, y, interval=0.07)
    sleep(1)
    press("enter", interval=1)



def insistirEmEncontrar(finalizar, ainda_tem_processo_pendente, x, y):
    cont = 0
    if type(finalizar) != tuple and type(ainda_tem_processo_pendente) != tuple:
        while type(finalizar) != tuple and type(ainda_tem_processo_pendente) != tuple:
            finalizar = utils.encontrarImagemLocalizada(r'Imagens\finalizar.png')
            ainda_tem_processo_pendente = utils.encontrarImagemLocalizada(r'Imagens\aindaTemProcessoParaLancar.png')
            cont+=1
            if cont == 4:
                moveTo(150,100)
                doubleClick(x,y)
                sleep(1)
    return finalizar, ainda_tem_processo_pendente


def pularProcesso():
    _ = filtrarPorStatus()
    sleep(0.5)
    press("down", interval=0.7)


def solicitarXML():
    x, y = utils.clicarDuasVezes(r'Imagens\solicitarXML.png')
    nf_cancelada = ""
    falsa_duplicidade = ""
    sleep(0.5)
    while True:
        nf_cancelada = utils.encontrarImagemLocalizada(r'Imagens\nfCancelada.png')
        falsa_duplicidade = utils.encontrarImagemLocalizada(r'Imagens\falsaDuplicidade.png')
        xml_manual = utils.encontrarImagemLocalizada(r'Imagens\inserirXML.png')
        if type(nf_cancelada) == tuple or type(falsa_duplicidade) == tuple or type(xml_manual) == tuple:
            press("right", interval=0.05)
            press("enter")
            sleep(0.5)
            break
        aguardando = utils.encontrarImagemLocalizada(r'Imagens\telaDeAguarde1.png')
        if type(aguardando) == tuple:
            while type(aguardando) == tuple:
                aguardando = utils.encontrarImagemLocalizada(r'Imagens\telaDeAguarde1.png')
        else:
            clicar_novamente = utils.encontrarImagemLocalizada(r'Imagens\XMLPendente.png')
            if type(clicar_novamente) == tuple:
                doubleClick(x,y)
            else:
                break
    sleep(1)
    if type(falsa_duplicidade) == tuple:
        inserir_xml = falsa_duplicidade
    elif type(xml_manual) == tuple:
        inserir_xml = xml_manual
    else:
        inserir_xml = None
    return nf_cancelada, inserir_xml



def verificarStatus():
    sleep(0.3)
    status_xml2 = utils.encontrarImagemLocalizada(r'Imagens\XMLPendente.png')
    if type(status_xml2) == tuple:
        controlador = 2
    else:
        status_xml3 = utils.encontrarImagemLocalizada(r'Imagens\statusChaveDanfeNaoDisponivel.png')
        if type(status_xml3) == tuple:
            controlador = 3
        else:
            status_xml4 = utils.encontrarImagemLocalizada(r'Imagens\disponivelPLancamento.png')
            if type(status_xml4) == tuple:
                controlador = 4
            else:
                status_xml1 = utils.encontrarImagemLocalizada(r'Imagens\statusRecibo.png')
                if type(status_xml1) == tuple:
                    controlador = 1
                else:
                    status_xml5 = utils.encontrarImagemLocalizada(r'Imagens\XMLPendente2.png')
                    if type(status_xml5) == tuple:
                        controlador = 2
                    else:
                        status_xml6 = utils.encontrarImagemLocalizada(r'Imagens\semChaveInformada.png')
                        if type(status_xml6) == tuple:
                            controlador = 5
                        else:
                            raise Exception
    return controlador



def filtrarPorStatus(imagem=r'Imagens\status.png'):
    caixa_finalizado = ''
    try:
        x, y = utils.encontrarImagemLocalizada(imagem)
    except TypeError:
        x, y = utils.encontrarImagemLocalizada(r'Imagens\statusNegrito.png')
    doubleClick(x, y)
    sleep(1.5)
    doubleClick(x, y)
    sleep(1.5)
    caixa_finalizado = utils.encontrarImagemLocalizada(r'Imagens\aindaNaoETempo.png')
    if type(caixa_finalizado) == tuple:
        doubleClick(x, y)
        caixa_finalizado = utils.encontrarImagemLocalizada(r'Imagens\aindaNaoETempo.png')
        sleep(0.5)
    return caixa_finalizado
    


def clicarEmLancar():
    sleep(0.5)
    x, y = utils.clicarDuasVezes(r'Imagens\botaoLancarNota.png')
    doubleClick(x,y)
    sleep(0.3)

    utils.lancarRetroativo()
    aguarde1, aguarde2 = utils.aguardar2()
    if type(aguarde1) == tuple or type(aguarde2) == tuple:
        while True:
            aguarde3, aguarde4 = utils.aguardar2()
            if type(aguarde3) != tuple and type(aguarde4) != tuple:
                utils.lancarRetroativo()
                aguarde3, aguarde4 = utils.aguardar2()
                if type(aguarde3) != tuple and type(aguarde4) != tuple:
                    break
    else:
        utils.lancarRetroativo()
        aguarde1, aguarde2 = utils.aguardar2()
        if type(aguarde1) != tuple and type(aguarde2) != tuple:
            doubleClick(x,y)
    sleep(1)

    caixa_finalizado = utils.encontrarImagemLocalizada(r'Imagens\jaLancado.png')
    nf_ja_lancada = utils.encontrarImagemLocalizada(r'Imagens\NFjaLancada.png')
    if type(caixa_finalizado) == tuple:
        caixa_finalizado = True
    elif type(nf_ja_lancada) == tuple:
        caixa_finalizado = "NF já lançada"
    else:
        caixa_finalizado = False
    return caixa_finalizado



def copiarChaveDeAcesso():
    processo_feito_errado = False
    x, y = utils.clicarDuasVezes(r'Imagens\copiarChaveDeAcesso.png')
    sleep(1)
    encontrar_chave_de_acesso = utils.encontrarImagem(r'Imagens\abriuChaveDeAcesso.png')
    caixa_finalizado = utils.encontrarImagem(r'Imagens\jaLancado.png')
    while type(encontrar_chave_de_acesso) != pyscreeze.Box:
        if type(caixa_finalizado) == pyscreeze.Box:
            caixa_finalizado = True
            chave_de_acesso = caixa_finalizado
            return chave_de_acesso, processo_feito_errado
        if type(encontrar_chave_de_acesso) != pyscreeze.Box:
            encontrar_chave_de_acesso = utils.encontrarImagem(r'Imagens\abriuChaveDeAcesso.png')
            doubleClick(x, y)
            caixa_finalizado = utils.encontrarImagem(r'Imagens\jaLancado.png')
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



def rejeitarCaixa(mensagem="Centro de Custo Bloqueado.", tipo="Programado"):
    if tipo == "Independente":
        utils.clicarMicrosiga()
    abriu = utils.encontrarImagemLocalizada(r'Imagens\botaoRejeitarCaixa.png')
    while type(abriu) != tuple:
        utils.clicarMicrosiga()
        abriu = utils.encontrarImagemLocalizada(r'Imagens\botaoRejeitarCaixa.png')

    sleep(0.5)
    while True:
        x, y = utils.clicarDuasVezes(r'Imagens\status.png')
        sleep(1.5)
        aux = 0
        repetir_clique = utils.encontrarImagemLocalizada(r'Imagens\aindaNaoETempo.png')
        if type(repetir_clique) != tuple:
            while type(repetir_clique) != tuple and aux < 3:
                doubleClick(x, y)
                moveTo(150,100)
                aux+=1
                repetir_clique = utils.encontrarImagemLocalizada(r'Imagens\aindaNaoETempo.png')
        sleep(0.5)
        if aux != 3:
            x, y = utils.clicarDuasVezes(r'Imagens\botaoCancelar.png')
            tela_de_lancamento = utils.esperarAparecer(r'Imagens\documentoEntrada.png')
            hotkey("ctrl", "s", interval=0.5)
            aguarde1, aguarde2 = utils.aguardar2()
            if type(aguarde1) == tuple or type(aguarde2) == tuple:
                while True:
                    aguarde3, aguarde4 = utils.aguardar2()
                    if type(aguarde3) != tuple and type(aguarde4) != tuple:
                        break
        else:
            break
    x, y = abriu
    doubleClick(x,y)
    campo_mensagem = utils.encontrarImagemLocalizada(r'Imagens\campoObservacaoRejeicao.png')

    while type(campo_mensagem) != tuple:
        sleep(0.6)
        x, y = utils.clicarDuasVezes(r'Imagens\botaoRejeitarCaixa.png')
        sleep(0.7)
        campo_mensagem = utils.encontrarImagemLocalizada(r'Imagens\campoObservacaoRejeicao.png')

    moveTo(150,100)

    copy(mensagem)
    hotkey("ctrl", "v")
    press("tab")
    press("enter")
    aguarde = utils.encontrarImagem(r'Imagens\telaDeAguarde1.png')
    aux_cont = 0
    while type(aguarde) != pyscreeze.Box:
        aguarde = utils.encontrarImagem(r'Imagens\telaDeAguarde1.png')
        aux_cont+=1
        if aux_cont == 0:
            break
    sleep(2)


def copiarRT(passos=2):
    sleep(1)
    hotkey(["shift", "tab"]*passos)
    hotkey("ctrl", "c", interval=2)
    dono_da_rt = paste()
    hotkey(["shift", "tab"]*2)
    hotkey("ctrl", "c", interval=2)
    rt = paste()
    rt = rt.replace(" ", "")
    return dono_da_rt, rt



def extrairDadosXML(caminho):
    try:
        with open(caminho) as fd:
            doc = xmltodict.parse(fd.read())
    except UnicodeDecodeError:
        with open(caminho, encoding='utf-8') as fd:
            doc = xmltodict.parse(fd.read())
    except:
        with open(caminho, encoding='utf-8') as fd:
            doc = xmltodict.parse(fd.read(), attr_prefix="@", cdata_key="#text")

    processador = extratorXML.ProcessadorXML(doc)
    nome_fantasia_forn = processador.coletarNomeFantasia()

    const_item = 0
    while True:
        try:
            coletor_xml = doc["nfeProc"]["NFe"]["infNFe"]["det"]["prod"]
            impostos_xml = doc["nfeProc"]["NFe"]["infNFe"]["det"]["imposto"]
            valores_do_item = processador.coletarDadosXML(coletor_xml, impostos_xml)
            break
        except KeyError:
            try:
                coletor_xml = doc["enviNFe"]["NFe"]["infNFe"]["det"]["prod"]
                impostos_xml = doc["enviNFe"]["NFe"]["infNFe"]["det"]["imposto"]
                valores_do_item = processador.coletarDadosXML(coletor_xml, impostos_xml)
                break
            except KeyError:
                try:
                    coletor_xml = doc["NFe"]["infNFe"]["det"]["prod"]
                    impostos_xml = doc["NFe"]["infNFe"]["det"]["imposto"]
                    valores_do_item = processador.coletarDadosXML(coletor_xml, impostos_xml)
                    break
                except TypeError:
                    try:
                        coletor_xml = doc["NFe"]["infNFe"]["det"][const_item]["prod"]
                        impostos_xml = doc["NFe"]["infNFe"]["det"][const_item]["imposto"]
                        valores_do_item = processador.coletarDadosXML(coletor_xml, impostos_xml)
                        const_item += 1
                    except IndexError:
                        break
            except TypeError:
                try:
                    coletor_xml = doc["enviNFe"]["NFe"]["infNFe"]["det"][const_item]["prod"]
                    impostos_xml = doc["enviNFe"]["NFe"]["infNFe"]["det"][const_item]["imposto"]
                    valores_do_item = processador.coletarDadosXML(coletor_xml, impostos_xml)
                    const_item += 1
                except IndexError:
                    break
        except TypeError:
            try:
                coletor_xml = doc["nfeProc"]["NFe"]["infNFe"]["det"][const_item]["prod"]
                impostos_xml = doc["nfeProc"]["NFe"]["infNFe"]["det"][const_item]["imposto"]
                valores_do_item = processador.coletarDadosXML(coletor_xml, impostos_xml)
                const_item += 1
            except IndexError:
                break

    itens, indices_e_impostos = processador.trabalharDadosXML(valores_do_item)

    return nome_fantasia_forn, itens, indices_e_impostos



def verificarCadastroForn(nome_fantasia_forn):
    cadastro_fornecedor = utils.encontrarImagem(r'Imagens\telaCadastroDeFornecedor.png')
    if type(cadastro_fornecedor) == pyscreeze.Box:
        sem_nome_fantasia = utils.encontrarImagem(r'Imagens\semNomeFantasia.png')
        if type(sem_nome_fantasia) == pyscreeze.Box:
            press(["tab"]*2)
            write(nome_fantasia_forn, interval=0.1)
            press("tab", interval=1)
        hotkey("alt", "a", interval=1)
        press(["tab"]*5)
        natureza = "2020087"
        write(natureza, interval=0.1)
        press("tab", interval=1)
        hotkey("alt", "f", interval=1)
        hotkey(["shift", "tab"]*3, interval=0.4)
        sleep(0.5)
        press("space", interval=0.5)
        press(["up"]*2)
        press("enter", interval=0.5)
        hotkey("ctrl", "s", interval=0.5)



def inserirValoresDaNFnoSistema(indices_e_impostos, itens):
    for i, ctrl_imposto in enumerate(indices_e_impostos):

        verificador, item_fracionado = operadoresLancamento.verificarValorDoItem(itens, i)
        if verificador == True:
            print("Que quantidade paia, meu parceiro")
            exit()
        tratamento_item = tratamentoItem.TratadorItem(item_fracionado, itens, i, ctrl_imposto)
        item = tratamento_item.tratarItem()
        cont = 0

        if ctrl_imposto == 0:
            press(["left"]*4)
                                    #SEQUENCIA LOGICA DE LANÇAMENTO SEM IMPOSTO
        elif ctrl_imposto == 1:
            for lista in item:
                icms_no_item, bc_icms, aliq_icms, icmsST_no_item, ipi_no_item = lista
                operadoresLancamento.definirTES(ctrl_imposto)
                operadoresLancamento.inserirICMS(icms_no_item, bc_icms, aliq_icms)
                press(["left"]*9)
                press("down")
                cont+=1
                operadoresLancamento.corrigirPassosHorizontal(cont, item)
            press("up")
                                        #SEQUENCIA LOGICA DE LANÇAMENTO SÓ PARA ICMS
        elif ctrl_imposto == 2:
            for lista in item:
                icms_no_item, icmsST_no_item, base_icms_ST, aliq_icms_ST, ipi_no_item = lista
                operadoresLancamento.definirTES(ctrl_imposto)
                operadoresLancamento.zerarImposto()
                operadoresLancamento.inserirICMSST(icmsST_no_item, base_icms_ST, aliq_icms_ST, passosST=9)
                press("down")
                cont+=1
                operadoresLancamento.corrigirPassosHorizontal(cont, item)
            press("up")
                                        #SEQUENCIA LOGICA DE LANÇAMENTO SÓ PARA ICMSST
        elif ctrl_imposto == 3:
            for lista in item:
                icms_no_item, icmsST_no_item, ipi_no_item, base_ipi, aliq_ipi = lista
                operadoresLancamento.definirTES(ctrl_imposto)
                operadoresLancamento.inserirIPI(ipi_no_item, base_ipi, aliq_ipi)
                operadoresLancamento.zerarImposto()
                press("down")
                cont+=1
                operadoresLancamento.corrigirPassosHorizontal(cont, item)
            press("up")
                                        #SEQUENCIA LOGICA DE LANÇAMENTO SÓ PARA IPI
        elif ctrl_imposto == 4:
            for lista in item:
                icms_no_item, icmsST_no_item, base_icms_ST, aliq_icms_ST, ipi_no_item, base_ipi, aliq_ipi = lista
                operadoresLancamento.definirTES(ctrl_imposto)
                operadoresLancamento.zerarImposto()
                operadoresLancamento.inserirICMSST(icmsST_no_item, base_icms_ST, aliq_icms_ST, passosST=9)
                operadoresLancamento.inserirIPI(ipi_no_item, base_ipi, aliq_ipi, passosIPI=0)
                press("down")
                cont+=1
                operadoresLancamento.corrigirPassosHorizontal(cont, item)
            press("up")
                                        #SEQUENCIA LOGICA DE LANÇAMENTO SÓ PARA ICMSST E IPI
        elif ctrl_imposto == 5:
            for lista in item:
                icms_no_item, base_icms, aliq_icms, icmsST_no_item, ipi_no_item, base_ipi, aliq_ipi = lista
                operadoresLancamento.definirTES(ctrl_imposto)
                operadoresLancamento.inserirICMS(icms_no_item, base_icms, aliq_icms)
                operadoresLancamento.inserirIPI(ipi_no_item, base_ipi, aliq_ipi, passosIPI=3)
                press("down")
                cont+=1
                operadoresLancamento.corrigirPassosHorizontal(cont, item)
            press("up")
                                        #SEQUENCIA LOGICA DE LANÇAMENTO SÓ PARA ICMS E IPI
        elif ctrl_imposto == 6:
            for lista in item:
                icms_no_item, base_icms, aliq_icms, icmsST_no_item, base_icms_ST, aliq_icms_ST, ipi_no_item = lista
                operadoresLancamento.definirTES(ctrl_imposto)
                operadoresLancamento.inserirICMS(icms_no_item, base_icms, aliq_icms)
                operadoresLancamento.inserirICMSST(icmsST_no_item, base_icms_ST, aliq_icms_ST, passosST=0)
                press("down")
                cont+=1
                operadoresLancamento.corrigirPassosHorizontal(cont, item)
            press("up")
                                        #SEQUENCIA LOGICA DE LANÇAMENTO SÓ PARA ICMS E ICMSST
        elif ctrl_imposto == 7:
            for lista in item:
                icms_no_item, base_icms, aliq_icms, icmsST_no_item, base_icms_ST, aliq_icms_ST, ipi_no_item, base_ipi, aliq_ipi = lista
                operadoresLancamento.definirTES(ctrl_imposto)
                operadoresLancamento.inserirICMS(icms_no_item, base_icms, aliq_icms)
                operadoresLancamento.inserirICMSST(icmsST_no_item, base_icms_ST, aliq_icms_ST, passosST=0)
                operadoresLancamento.inserirIPI(ipi_no_item, base_ipi, aliq_ipi, passosIPI=12)
                press("down")
                cont+=1
                operadoresLancamento.corrigirPassosHorizontal(cont, item)
            press("up")
                                        #SEQUENCIA LOGICA DE LANÇAMENTO PARA TODOS OS IMPOSTOS

        if len(indices_e_impostos) > 1:
            press("down")
        if i+1 == len(indices_e_impostos):
            press("up")
        sleep(2)



def finalizarLancamento():
    hotkey("ctrl", "s", interval=1.5)

    erro_cnpj = utils.encontrarImagemLocalizada(r'Imagens\erroCNPJ.png')
    if type(erro_cnpj) == tuple:
        press("enter")
        campo_sped = utils.encontrarImagemLocalizada(r'Imagens\campoSPED.png')
        x, y = campo_sped
        sleep(1)
        doubleClick(x,y)
        sleep(1)
        write("NF", interval=0.3)
        press("tab")
        hotkey("ctrl", "s", interval=1)

    while True:
        sem_tela_final = utils.encontrarImagemLocalizada(r'Imagens\semTelaFinal.png')
        repentina_etapa_final = utils.encontrarImagemLocalizada(r'Imagens\etapaFinal.png')
        aguarde = utils.encontrarImagemLocalizada(r'Imagens\telaDeAguarde2.png')
        if type(aguarde) == tuple:
            sleep(0.5)
            continue
        if type(repentina_etapa_final) == tuple:
            utils.tratarEtapaFinal()
            break
        elif type(sem_tela_final) == tuple:
            break

    repentina_etapa_final = utils.encontrarImagemLocalizada(r'Imagens\etapaFinal.png')
    if type(repentina_etapa_final) == tuple:
        utils.tratarEtapaFinal()
        
