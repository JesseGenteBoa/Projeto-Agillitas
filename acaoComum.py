import pyautogui as ptg
from time import sleep
from tkinter import messagebox
from pyperclip import paste, copy
import utils
import operadoresLancamento
import tratamentoItem
import xmltodict
import pyscreeze
import extratorXML


FAILSAFE = True

def proceder_primario():
    aguarde = utils.encontrar_centro_imagem(r'Imagens\telaDeAguarde2.png')
    while type(aguarde) == tuple:
        aguarde = utils.encontrar_centro_imagem(r'Imagens\telaDeAguarde2.png')
    encontrar = utils.encontrar_imagem(r'Imagens\statusPendente.png')
    cont = 0
    while type(encontrar) != pyscreeze.Box:
        encontrar = utils.encontrar_imagem(r'Imagens\statusPendente.png')
        cont+=1
        if cont == 2:
            ptg.press("enter")
            break 

    sleep(1)
    quebra_de_seguranca = utils.encontrar_imagem(r'Imagens\quebraDeSeguranca.png')
    if type(quebra_de_seguranca) == pyscreeze.Box:
        messagebox.showerror("Erro!", "Interrompido por falta de processos.")
        raise Exception("Interrompido por falta de processos.")

    while True:
        try:
            clique_status = utils.encontrar_centro_imagem(r'Imagens\statusPendente.png')  
            x, y = clique_status
            break
        except TypeError:
            clique_status = utils.encontrar_centro_imagem(r'Imagens\status.png')  
            x, y = clique_status
            break
        except:
            pass

    for _ in range(5):
        ptg.doubleClick(x, y, interval=0.07)
    sleep(1)
    ptg.press("enter", interval=1)



def insistir_ate_encontrar(finalizar, ainda_tem_processo_pendente, x, y):
    cont = 0
    if type(finalizar) != tuple and type(ainda_tem_processo_pendente) != tuple:
        while type(finalizar) != tuple and type(ainda_tem_processo_pendente) != tuple:
            finalizar = utils.encontrar_centro_imagem(r'Imagens\finalizar.png')
            ainda_tem_processo_pendente = utils.encontrar_centro_imagem(r'Imagens\aindaTemProcessoParaLancar.png')
            cont+=1
            if cont == 4:
                ptg.moveTo(150,100)
                ptg.doubleClick(x,y)
                sleep(1)
    return finalizar, ainda_tem_processo_pendente


def pular_processo():
    _ = filtrar_status()
    sleep(0.5)
    ptg.press("down", interval=0.7)


def solicitar_XML():
    x, y = utils.clicar_2x(r'Imagens\solicitarXML.png')
    nf_cancelada = ""
    falsa_duplicidade = ""
    sleep(0.5)
    while True:
        nf_cancelada = utils.encontrar_centro_imagem(r'Imagens\nfCancelada.png')
        falsa_duplicidade = utils.encontrar_centro_imagem(r'Imagens\falsaDuplicidade.png')
        xml_manual = utils.encontrar_centro_imagem(r'Imagens\inserirXML.png')
        if type(nf_cancelada) == tuple or type(falsa_duplicidade) == tuple or type(xml_manual) == tuple:
            ptg.press("right", interval=0.05)
            ptg.press("enter")
            sleep(0.5)
            break
        aguardando = utils.encontrar_centro_imagem(r'Imagens\telaDeAguarde1.png')
        if type(aguardando) == tuple:
            while type(aguardando) == tuple:
                aguardando = utils.encontrar_centro_imagem(r'Imagens\telaDeAguarde1.png')
        else:
            clicar_novamente = utils.encontrar_centro_imagem(r'Imagens\XMLPendente.png')
            if type(clicar_novamente) == tuple:
                ptg.doubleClick(x,y)
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



def verificar_status():
    sleep(0.3)
    status_xml2 = utils.encontrar_centro_imagem(r'Imagens\XMLPendente.png')
    if type(status_xml2) == tuple:
        controlador = 2
    else:
        status_xml3 = utils.encontrar_centro_imagem(r'Imagens\statusChaveDanfeNaoDisponivel.png')
        if type(status_xml3) == tuple:
            controlador = 3
        else:
            status_xml4 = utils.encontrar_centro_imagem(r'Imagens\disponivelPLancamento.png')
            if type(status_xml4) == tuple:
                controlador = 4
            else:
                status_xml1 = utils.encontrar_centro_imagem(r'Imagens\statusRecibo.png')
                if type(status_xml1) == tuple:
                    controlador = 1
                else:
                    status_xml5 = utils.encontrar_centro_imagem(r'Imagens\XMLPendente2.png')
                    if type(status_xml5) == tuple:
                        controlador = 2
                    else:
                        status_xml6 = utils.encontrar_centro_imagem(r'Imagens\semChaveInformada.png')
                        if type(status_xml6) == tuple:
                            controlador = 5
                        else:
                            messagebox.showerror("Erro!", "Status não mapeado.")
                            raise Exception("Status não mapeado.")
    return controlador



def filtrar_status(imagem=r'Imagens\status.png'):
    caixa_finalizado = ''
    try:
        x, y = utils.encontrar_centro_imagem(imagem)
    except TypeError:
        x, y = utils.encontrar_centro_imagem(r'Imagens\statusNegrito.png')
    ptg.doubleClick(x, y)
    sleep(1.5)
    ptg.doubleClick(x, y)
    sleep(1.5)
    caixa_finalizado = utils.encontrar_centro_imagem(r'Imagens\aindaNaoETempo.png')
    if type(caixa_finalizado) == tuple:
        ptg.doubleClick(x, y)
        caixa_finalizado = utils.encontrar_centro_imagem(r'Imagens\aindaNaoETempo.png')
        sleep(0.5)
    return caixa_finalizado
    


def clicar_Lancar():
    sleep(0.5)
    x, y = utils.clicar_2x(r'Imagens\botaoLancarNota.png')
    ptg.doubleClick(x,y)
    sleep(0.3)

    utils.lancar_retroativo()
    aguarde1, aguarde2 = utils.aguardar2()
    if type(aguarde1) == tuple or type(aguarde2) == tuple:
        while True:
            aguarde3, aguarde4 = utils.aguardar2()
            if type(aguarde3) != tuple and type(aguarde4) != tuple:
                utils.lancar_retroativo()
                aguarde3, aguarde4 = utils.aguardar2()
                if type(aguarde3) != tuple and type(aguarde4) != tuple:
                    break
    else:
        utils.lancar_retroativo()
        aguarde1, aguarde2 = utils.aguardar2()
        if type(aguarde1) != tuple and type(aguarde2) != tuple:
            ptg.doubleClick(x,y)
    sleep(1)

    caixa_finalizado = utils.encontrar_centro_imagem(r'Imagens\jaLancado.png')
    nf_ja_lancada = utils.encontrar_centro_imagem(r'Imagens\NFjaLancada.png')
    if type(caixa_finalizado) == tuple:
        caixa_finalizado = True
    elif type(nf_ja_lancada) == tuple:
        caixa_finalizado = "NF já lançada"
    else:
        caixa_finalizado = False
    return caixa_finalizado



def copiar_chave_acesso():
    processo_feito_errado = False
    x, y = utils.clicar_2x(r'Imagens\copiarChaveDeAcesso.png')
    sleep(1)
    encontrar_chave_de_acesso = utils.encontrar_imagem(r'Imagens\abriuChaveDeAcesso.png')
    caixa_finalizado = utils.encontrar_imagem(r'Imagens\jaLancado.png')
    while type(encontrar_chave_de_acesso) != pyscreeze.Box:
        if type(caixa_finalizado) == pyscreeze.Box:
            caixa_finalizado = True
            chave_de_acesso = caixa_finalizado
            return chave_de_acesso, processo_feito_errado
        if type(encontrar_chave_de_acesso) != pyscreeze.Box:
            encontrar_chave_de_acesso = utils.encontrar_imagem(r'Imagens\abriuChaveDeAcesso.png')
            ptg.doubleClick(x, y)
            caixa_finalizado = utils.encontrar_imagem(r'Imagens\jaLancado.png')
    sleep(0.5)
    ptg.hotkey("ctrl", "c")
    chave_de_acesso = paste()
    chave_de_acesso = chave_de_acesso.replace(" ", "")
    if len(chave_de_acesso) != 44:
        processo_feito_errado = True
    sleep(0.5)
    ptg.press("esc")
    sleep(2)
    return chave_de_acesso, processo_feito_errado



def rejeitar_caixa(mensagem="Centro de Custo Bloqueado.", tipo="Programado"):
    if tipo == "Independente":
        utils.clicar_microsiga()
    abriu = utils.encontrar_centro_imagem(r'Imagens\botaoRejeitarCaixa.png')
    while type(abriu) != tuple:
        utils.clicar_microsiga()
        abriu = utils.encontrar_centro_imagem(r'Imagens\botaoRejeitarCaixa.png')

    sleep(0.5)
    while True:
        x, y = utils.clicar_2x(r'Imagens\status.png')
        sleep(1.5)
        aux = 0
        repetir_clique = utils.encontrar_centro_imagem(r'Imagens\aindaNaoETempo.png')
        if type(repetir_clique) != tuple:
            while type(repetir_clique) != tuple and aux < 3:
                ptg.doubleClick(x, y)
                ptg.moveTo(150,100)
                aux+=1
                repetir_clique = utils.encontrar_centro_imagem(r'Imagens\aindaNaoETempo.png')
        sleep(0.5)
        if aux != 3:
            x, y = utils.clicar_2x(r'Imagens\botaoCancelar.png')
            tela_de_lancamento = utils.esperar_aparecer(r'Imagens\documentoEntrada.png')
            ptg.hotkey("ctrl", "s", interval=0.5)
            aguarde1, aguarde2 = utils.aguardar2()
            if type(aguarde1) == tuple or type(aguarde2) == tuple:
                while True:
                    aguarde3, aguarde4 = utils.aguardar2()
                    if type(aguarde3) != tuple and type(aguarde4) != tuple:
                        break
        else:
            break
    x, y = abriu
    ptg.doubleClick(x,y)
    campo_mensagem = utils.encontrar_centro_imagem(r'Imagens\campoObservacaoRejeicao.png')

    while type(campo_mensagem) != tuple:
        sleep(0.6)
        x, y = utils.clicar_2x(r'Imagens\botaoRejeitarCaixa.png')
        sleep(0.7)
        campo_mensagem = utils.encontrar_centro_imagem(r'Imagens\campoObservacaoRejeicao.png')

    ptg.moveTo(150,100)

    copy(mensagem)
    ptg.hotkey("ctrl", "v")
    ptg.press("tab")
    ptg.press("enter")
    aguarde = utils.encontrar_imagem(r'Imagens\telaDeAguarde1.png')
    aux_cont = 0
    while type(aguarde) != pyscreeze.Box:
        aguarde = utils.encontrar_imagem(r'Imagens\telaDeAguarde1.png')
        aux_cont+=1
        if aux_cont == 0:
            break
    sleep(2)


def copiar_RT(passos=2):
    sleep(1)
    ptg.hotkey(["shift", "tab"]*passos)
    ptg.hotkey("ctrl", "c", interval=2)
    dono_da_rt = paste()
    ptg.hotkey(["shift", "tab"]*2)
    ptg.hotkey("ctrl", "c", interval=2)
    rt = paste()
    rt = rt.replace(" ", "")
    return dono_da_rt, rt



def extrair_dados_XML(caminho):
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
    nome_fantasia_forn = processador.coletar_nome_fantasia()

    const_item = 0
    while True:
        try:
            coletor_xml = doc["nfeProc"]["NFe"]["infNFe"]["det"]["prod"]
            impostos_xml = doc["nfeProc"]["NFe"]["infNFe"]["det"]["imposto"]
            valores_do_item = processador.coletar_dados_XML(coletor_xml, impostos_xml)
            break
        except KeyError:
            try:
                coletor_xml = doc["enviNFe"]["NFe"]["infNFe"]["det"]["prod"]
                impostos_xml = doc["enviNFe"]["NFe"]["infNFe"]["det"]["imposto"]
                valores_do_item = processador.coletar_dados_XML(coletor_xml, impostos_xml)
                break
            except KeyError:
                try:
                    coletor_xml = doc["NFe"]["infNFe"]["det"]["prod"]
                    impostos_xml = doc["NFe"]["infNFe"]["det"]["imposto"]
                    valores_do_item = processador.coletar_dados_XML(coletor_xml, impostos_xml)
                    break
                except TypeError:
                    try:
                        coletor_xml = doc["NFe"]["infNFe"]["det"][const_item]["prod"]
                        impostos_xml = doc["NFe"]["infNFe"]["det"][const_item]["imposto"]
                        valores_do_item = processador.coletar_dados_XML(coletor_xml, impostos_xml)
                        const_item += 1
                    except IndexError:
                        break
            except TypeError:
                try:
                    coletor_xml = doc["enviNFe"]["NFe"]["infNFe"]["det"][const_item]["prod"]
                    impostos_xml = doc["enviNFe"]["NFe"]["infNFe"]["det"][const_item]["imposto"]
                    valores_do_item = processador.coletar_dados_XML(coletor_xml, impostos_xml)
                    const_item += 1
                except IndexError:
                    break
        except TypeError:
            try:
                coletor_xml = doc["nfeProc"]["NFe"]["infNFe"]["det"][const_item]["prod"]
                impostos_xml = doc["nfeProc"]["NFe"]["infNFe"]["det"][const_item]["imposto"]
                valores_do_item = processador.coletar_dados_XML(coletor_xml, impostos_xml)
                const_item += 1
            except IndexError:
                break

    itens, indices_e_impostos = processador.trabalhar_dados_XML(valores_do_item)

    return nome_fantasia_forn, itens, indices_e_impostos



def verificar_cadastro_forn(nome_fantasia_forn):
    cadastro_fornecedor = utils.encontrar_imagem(r'Imagens\telaCadastroDeFornecedor.png')
    if type(cadastro_fornecedor) == pyscreeze.Box:
        sem_nome_fantasia = utils.encontrar_imagem(r'Imagens\semNomeFantasia.png')
        if type(sem_nome_fantasia) == pyscreeze.Box:
            ptg.press(["tab"]*2)
            ptg.write(nome_fantasia_forn, interval=0.1)
            ptg.press("tab", interval=1)
        ptg.hotkey("alt", "a", interval=1)
        ptg.press(["tab"]*5)
        natureza = "2020087"
        ptg.write(natureza, interval=0.1)
        ptg.press("tab", interval=1)
        ptg.hotkey("alt", "f", interval=1)
        ptg.hotkey(["shift", "tab"]*3, interval=0.4)
        sleep(0.5)
        ptg.press("space", interval=0.5)
        ptg.press(["up"]*2)
        ptg.press("enter", interval=0.5)
        ptg.hotkey("ctrl", "s", interval=0.5)



def inserir_valores_da_NF_no_siga(indices_e_impostos, itens):
    for i, ctrl_imposto in enumerate(indices_e_impostos):

        verificador, item_fracionado = operadoresLancamento.verificar_valor_do_item(itens, i)
        if verificador == True:
            messagebox.showerror("Erro!", "Contate a +TI imediatamente.")
            raise Exception("Contate a +TI imediatamente.")
        tratamento_item = tratamentoItem.TratadorItem(item_fracionado, itens, i, ctrl_imposto)
        item = tratamento_item.tratar_item()
        cont = 0

        if ctrl_imposto == 0:
            ptg.press(["left"]*4)
                                    #SEQUENCIA LOGICA DE LANÇAMENTO SEM IMPOSTO
        elif ctrl_imposto == 1:
            for lista in item:
                icms_no_item, bc_icms, aliq_icms, icmsST_no_item, ipi_no_item = lista
                operadoresLancamento.definir_TES(ctrl_imposto)
                operadoresLancamento.inserir_ICMS(icms_no_item, bc_icms, aliq_icms)
                ptg.press(["left"]*9)
                ptg.press("down")
                cont+=1
                operadoresLancamento.corrigir_passos_horizontal(cont, item)
            ptg.press("up")
                                        #SEQUENCIA LOGICA DE LANÇAMENTO SÓ PARA ICMS
        elif ctrl_imposto == 2:
            for lista in item:
                icms_no_item, icmsST_no_item, base_icms_ST, aliq_icms_ST, ipi_no_item = lista
                operadoresLancamento.definir_TES(ctrl_imposto)
                operadoresLancamento.zerar_imposto()
                operadoresLancamento.inserir_ICMSST(icmsST_no_item, base_icms_ST, aliq_icms_ST, passosST=9)
                ptg.press("down")
                cont+=1
                operadoresLancamento.corrigir_passos_horizontal(cont, item)
            ptg.press("up")
                                        #SEQUENCIA LOGICA DE LANÇAMENTO SÓ PARA ICMSST
        elif ctrl_imposto == 3:
            for lista in item:
                icms_no_item, icmsST_no_item, ipi_no_item, base_ipi, aliq_ipi = lista
                operadoresLancamento.definir_TES(ctrl_imposto)
                operadoresLancamento.inserir_IPI(ipi_no_item, base_ipi, aliq_ipi)
                operadoresLancamento.zerar_imposto()
                ptg.press("down")
                cont+=1
                operadoresLancamento.corrigir_passos_horizontal(cont, item)
            ptg.press("up")
                                        #SEQUENCIA LOGICA DE LANÇAMENTO SÓ PARA IPI
        elif ctrl_imposto == 4:
            for lista in item:
                icms_no_item, icmsST_no_item, base_icms_ST, aliq_icms_ST, ipi_no_item, base_ipi, aliq_ipi = lista
                operadoresLancamento.definir_TES(ctrl_imposto)
                operadoresLancamento.zerar_imposto()
                operadoresLancamento.inserir_ICMSST(icmsST_no_item, base_icms_ST, aliq_icms_ST, passosST=9)
                operadoresLancamento.inserir_IPI(ipi_no_item, base_ipi, aliq_ipi, passosIPI=0)
                ptg.press("down")
                cont+=1
                operadoresLancamento.corrigir_passos_horizontal(cont, item)
            ptg.press("up")
                                        #SEQUENCIA LOGICA DE LANÇAMENTO SÓ PARA ICMSST E IPI
        elif ctrl_imposto == 5:
            for lista in item:
                icms_no_item, base_icms, aliq_icms, icmsST_no_item, ipi_no_item, base_ipi, aliq_ipi = lista
                operadoresLancamento.definir_TES(ctrl_imposto)
                operadoresLancamento.inserir_ICMS(icms_no_item, base_icms, aliq_icms)
                operadoresLancamento.inserir_IPI(ipi_no_item, base_ipi, aliq_ipi, passosIPI=3)
                ptg.press("down")
                cont+=1
                operadoresLancamento.corrigir_passos_horizontal(cont, item)
            ptg.press("up")
                                        #SEQUENCIA LOGICA DE LANÇAMENTO SÓ PARA ICMS E IPI
        elif ctrl_imposto == 6:
            for lista in item:
                icms_no_item, base_icms, aliq_icms, icmsST_no_item, base_icms_ST, aliq_icms_ST, ipi_no_item = lista
                operadoresLancamento.definir_TES(ctrl_imposto)
                operadoresLancamento.inserir_ICMS(icms_no_item, base_icms, aliq_icms)
                operadoresLancamento.inserir_ICMSST(icmsST_no_item, base_icms_ST, aliq_icms_ST, passosST=0)
                ptg.press("down")
                cont+=1
                operadoresLancamento.corrigir_passos_horizontal(cont, item)
            ptg.press("up")
                                        #SEQUENCIA LOGICA DE LANÇAMENTO SÓ PARA ICMS E ICMSST
        elif ctrl_imposto == 7:
            for lista in item:
                icms_no_item, base_icms, aliq_icms, icmsST_no_item, base_icms_ST, aliq_icms_ST, ipi_no_item, base_ipi, aliq_ipi = lista
                operadoresLancamento.definir_TES(ctrl_imposto)
                operadoresLancamento.inserir_ICMS(icms_no_item, base_icms, aliq_icms)
                operadoresLancamento.inserir_ICMSST(icmsST_no_item, base_icms_ST, aliq_icms_ST, passosST=0)
                operadoresLancamento.inserir_IPI(ipi_no_item, base_ipi, aliq_ipi, passosIPI=12)
                ptg.press("down")
                cont+=1
                operadoresLancamento.corrigir_passos_horizontal(cont, item)
            ptg.press("up")
                                        #SEQUENCIA LOGICA DE LANÇAMENTO PARA TODOS OS IMPOSTOS

        if len(indices_e_impostos) > 1:
            ptg.press("down")
        if i+1 == len(indices_e_impostos):
            ptg.press("up")
        sleep(2)



def finalizar_lancamento():
    ptg.hotkey("ctrl", "s", interval=1.5)

    erro_cnpj = utils.encontrar_centro_imagem(r'Imagens\erroCNPJ.png')
    if type(erro_cnpj) == tuple:
        ptg.press("enter")
        campo_sped = utils.encontrar_centro_imagem(r'Imagens\campoSPED.png')
        x, y = campo_sped
        sleep(1)
        ptg.doubleClick(x,y)
        sleep(1)
        ptg.write("NF", interval=0.3)
        ptg.press("tab")
        ptg.hotkey("ctrl", "s", interval=1)

    while True:
        sem_tela_final = utils.encontrar_centro_imagem(r'Imagens\semTelaFinal.png')
        repentina_etapa_final = utils.encontrar_centro_imagem(r'Imagens\etapaFinal.png')
        aguarde = utils.encontrar_centro_imagem(r'Imagens\telaDeAguarde2.png')
        if type(aguarde) == tuple:
            sleep(0.5)
            continue
        if type(repentina_etapa_final) == tuple:
            utils.tratar_etapa_final()
            break
        elif type(sem_tela_final) == tuple:
            break

    repentina_etapa_final = utils.encontrar_centro_imagem(r'Imagens\etapaFinal.png')
    if type(repentina_etapa_final) == tuple:
        utils.tratar_etapa_final()
        
