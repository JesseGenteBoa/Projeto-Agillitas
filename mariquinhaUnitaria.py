from pyautogui import hotkey, press, write, FAILSAFE, FailSafeException
from pydirectinput import click as mouseClique, moveTo, doubleClick
from pyperclip import paste, copy  
from time import sleep
from pathlib import Path
import utils
import pyscreeze
import xmltodict
import extratorXML
import tratamentoItem
import operadoresLancamento


FAILSAFE = True
doc = ''


def lancamentoIsolado(rt):
    pular_processo = []                     
    controle_de_repeticao = []
    dono_da_rt = []
    chave_inconforme = []
    sem_xml = []
    rt_contador = []
    xml_ilegivel = []
    cond_pag = []
    bloqueado = []
    cnpj_inconclusivo = []
    chave_sefaz =[]
    ncm_problematica = []

    utils.clicarMicrosiga()

    sleep(0.5)
    try:
        primeiro_clique = utils.encontrarImagemLocalizada(r'Imagens\filtrarPendentes.png')
        x, y = primeiro_clique
        mouseClique(x, y)
    except TypeError:
        primeiro_clique = utils.encontrarImagemLocalizada(r'Imagens\filtrarPendentesSelecionado.png')
        x, y = primeiro_clique
        mouseClique(x, y)
    sleep(0.5)
    hotkey(["shift", "tab"]*4, interval=0.04)
    press("t", interval=0.1)
    mouseClique(x, y)
    hotkey("shift", "tab", interval=0.04)
    write(rt, interval=0.05)
    press(["tab"]*2)
    sleep(0.7)
    press("enter", interval=0.3)
    sleep(1)

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

    sleep(1)
    quebra_de_seguranca = utils.encontrarImagem(r'Imagens\quebraDeSeguranca.png')
    if type(quebra_de_seguranca) == pyscreeze.Box:
        raise FailSafeException


    while True:
        try:
            clique_status = utils.encontrarImagemLocalizada(r'Imagens\statusNegrito.png')  
            x, y = clique_status
            break
        except TypeError:
            clique_status = utils.encontrarImagemLocalizada(r'Imagens\status.png')  
            x, y = clique_status
            break
        except:
            pass

    mouseClique(x, y)
    sleep(1)
    press("enter")
    sleep(1)

    moveTo(150,100)

    sleep(0.5)

    estado_do_caixa = utils.filtrarPorStatus()

    if type(estado_do_caixa) == tuple:
        cont = 0
        x, y = utils.clicarEmFinalizar()
        finalizar = utils.encontrarImagemLocalizada(r'Imagens\finalizar.png')
        ainda_tem_processo_pendente = utils.encontrarImagemLocalizada(r'Imagens\aindaTemProcessoParaLancar.png')
        if type(finalizar) != tuple and type(ainda_tem_processo_pendente) != tuple:
            while type(finalizar) != tuple and type(ainda_tem_processo_pendente) != tuple:
                finalizar = utils.encontrarImagemLocalizada(r'Imagens\finalizar.png')
                ainda_tem_processo_pendente = utils.encontrarImagemLocalizada(r'Imagens\aindaTemProcessoParaLancar.png')
                cont+=1
                if cont == 4:
                    moveTo(150,100)
                    doubleClick(x,y)
                    sleep(1)

        if type(ainda_tem_processo_pendente) == tuple:
            press("enter")
            utils.tabEEnter()
            sleep(2)
            repetir_acao = utils.encontrarImagemLocalizada(r'Imagens\botaoLancarNota.png')
            while type(repetir_acao) == tuple:
                press("enter")
                repetir_acao = utils.encontrarImagemLocalizada(r'Imagens\botaoLancarNota.png')
            if rt_contador:
                utils.enviarEmail(rt_contador, dono_da_rt, sem_xml, chave_inconforme, xml_ilegivel, cond_pag, bloqueado, cnpj_inconclusivo, chave_sefaz, ncm_problematica)
            raise FailSafeException
        
        if type(finalizar) == tuple:
            press("enter")
        utils.aguardar()
        utils.clicarBotaoSair()
        if rt_contador:
            utils.enviarEmail(rt_contador, dono_da_rt, sem_xml, chave_inconforme, xml_ilegivel, cond_pag, bloqueado, cnpj_inconclusivo, chave_sefaz, ncm_problematica)
        raise FailSafeException
        
    def operarLancamento(pular_processo):
        estado_do_caixa = False
        global doc

        controlador = utils.verificarStatus()

        if controlador == 1:
            estado_do_caixa = utils.clicarEmLancar()
            cc_bloqueado = utils.encontrarImagem(r'Imagens\ccBloqueado.png')
            if type(cc_bloqueado) == pyscreeze.Box:
                press("enter")
                sleep(0.5)
                utils.rejeitarCaixa()
                print("Erro de CC")
                raise FailSafeException
            
            repentina_etapa_final = utils.encontrarImagem(r'Imagens\etapaFinal.png')

            if type(repentina_etapa_final) == pyscreeze.Box:
                utils.tratarEtapaFinal()

            if estado_do_caixa == True:
                cont = 0
                x, y = utils.clicarEmFinalizar()
                finalizar = utils.encontrarImagemLocalizada(r'Imagens\finalizar.png')
                ainda_tem_processo_pendente = utils.encontrarImagemLocalizada(r'Imagens\aindaTemProcessoParaLancar.png')
                if type(finalizar) != tuple and type(ainda_tem_processo_pendente) != tuple:
                    while type(finalizar) != tuple and type(ainda_tem_processo_pendente) != tuple:
                        finalizar = utils.encontrarImagemLocalizada(r'Imagens\finalizar.png')
                        ainda_tem_processo_pendente = utils.encontrarImagemLocalizada(r'Imagens\aindaTemProcessoParaLancar.png')
                        cont+=1
                        if cont == 4:
                            moveTo(150,100)
                            doubleClick(x,y)
                            sleep(1)

                if type(ainda_tem_processo_pendente) == tuple:
                    press("enter")
                    utils.tabEEnter()
                    sleep(2)
                    repetir_acao = utils.encontrarImagemLocalizada(r'Imagens\botaoLancarNota.png')
                    while type(repetir_acao) == tuple:
                        press("enter")
                        repetir_acao = utils.encontrarImagemLocalizada(r'Imagens\botaoLancarNota.png')
                    if rt_contador:
                        utils.enviarEmail(rt_contador, dono_da_rt, sem_xml, chave_inconforme, xml_ilegivel, cond_pag, bloqueado, cnpj_inconclusivo, chave_sefaz, ncm_problematica)
                    raise FailSafeException
                
                if type(finalizar) == tuple:
                    press("enter")
                utils.aguardar()
                utils.clicarBotaoSair()
                if rt_contador:
                    utils.enviarEmail(rt_contador, dono_da_rt, sem_xml, chave_inconforme, xml_ilegivel, cond_pag, bloqueado, cnpj_inconclusivo, chave_sefaz, ncm_problematica)
                raise FailSafeException
            
            else:
                estado_do_caixa = utils.filtrarPorStatus()

                if type(estado_do_caixa) == tuple:
                    cont = 0
                    x, y = utils.clicarEmFinalizar()
                    finalizar = utils.encontrarImagemLocalizada(r'Imagens\finalizar.png')
                    ainda_tem_processo_pendente = utils.encontrarImagemLocalizada(r'Imagens\aindaTemProcessoParaLancar.png')
                    if type(finalizar) != tuple and type(ainda_tem_processo_pendente) != tuple:
                        while type(finalizar) != tuple and type(ainda_tem_processo_pendente) != tuple:
                            finalizar = utils.encontrarImagemLocalizada(r'Imagens\finalizar.png')
                            ainda_tem_processo_pendente = utils.encontrarImagemLocalizada(r'Imagens\aindaTemProcessoParaLancar.png')
                            cont+=1
                            if cont == 4:
                                moveTo(150,100)
                                doubleClick(x,y)
                                sleep(1)

                    if type(ainda_tem_processo_pendente) == tuple:
                        press("enter")
                        utils.tabEEnter()
                        sleep(2)
                        repetir_acao = utils.encontrarImagemLocalizada(r'Imagens\botaoLancarNota.png')
                        while type(repetir_acao) == tuple:
                            press("enter")
                            repetir_acao = utils.encontrarImagemLocalizada(r'Imagens\botaoLancarNota.png')
                        if rt_contador:
                            utils.enviarEmail(rt_contador, dono_da_rt, sem_xml, chave_inconforme, xml_ilegivel, cond_pag, bloqueado, cnpj_inconclusivo, chave_sefaz, ncm_problematica)
                        raise FailSafeException
                    
                    if type(finalizar) == tuple:
                        press("enter")
                    utils.aguardar()
                    utils.clicarBotaoSair()
                    if rt_contador:
                        utils.enviarEmail(rt_contador, dono_da_rt, sem_xml, chave_inconforme, xml_ilegivel, cond_pag, bloqueado, cnpj_inconclusivo, chave_sefaz, ncm_problematica)
                    raise FailSafeException
                
                controle_de_repeticao.clear()
                return operarLancamento(pular_processo)
            

        elif controlador == 2:
            status_nf, falsa_duplicidade = utils.solicitarXML()


            if type(status_nf) == tuple:
                try:
                    numero_nf = chave_de_acesso[25:34]
                except UnboundLocalError:
                    chave_de_acesso, processo_feito_errado = utils.copiarChaveDeAcesso()
                    numero_nf = chave_de_acesso[25:34]
                utils.rejeitarCaixa(mensagem = f"NF {numero_nf} foi cancelada pelo fornecedor.")
                print("NF cancelada")
                raise FailSafeException
            
            
            if type(falsa_duplicidade) == tuple:
                chave_de_acesso, processo_feito_errado = utils.copiarChaveDeAcesso()
                x, y = utils.clicarDuasVezes(r'Imagens\solicitarXML.png')

                while True:
                    aguardando = utils.encontrarImagemLocalizada(r'Imagens\telaDeAguarde1.png')
                    falsa_duplicidade = utils.encontrarImagemLocalizada(r'Imagens\falsaDuplicidade.png')
                    if type(aguardando) == tuple:
                        while type(aguardando) == tuple:
                            aguardando = utils.encontrarImagemLocalizada(r'Imagens\telaDeAguarde1.png')
                    elif type(falsa_duplicidade) == tuple:
                        try:
                            verificador = pular_processo.index(chave_de_acesso)
                            try:
                                verificador = controle_de_repeticao.index(chave_de_acesso)
                                press(["tab"]*7, interval=0.1)
                                sleep(1)
                                press("enter")
                                sleep(1)
                                repetir_acao = utils.encontrarImagemLocalizada(r'Imagens\botaoLancarNota.png')
                                while type(repetir_acao) == tuple:
                                    press("enter")
                                    repetir_acao = utils.encontrarImagemLocalizada(r'Imagens\botaoLancarNota.png')
                                clique_status = utils.esperarAparecer(r'Imagens\statusNegrito.png')  
                                x, y = clique_status
                                mouseClique(x, y)
                                sleep(0.7)
                                press("down")
                                if rt_contador:
                                    utils.enviarEmail(rt_contador, dono_da_rt, sem_xml, chave_inconforme, xml_ilegivel, cond_pag, bloqueado, cnpj_inconclusivo, chave_sefaz, ncm_problematica)
                                raise FailSafeException
                            
                            except ValueError:
                                estado_do_caixa = utils.filtrarPorStatus()
                                sleep(0.5)
                                press("down")
                                print("Já vi esse, paizão")
                                controle_de_repeticao.append(chave_de_acesso)
                                return operarLancamento(pular_processo)
                            
                        except:
                            caminho = "xmlFiscalio\\" + chave_de_acesso + ".xml"
                            path = Path(caminho)

                            if not path.exists():
                                pular_processo.append(chave_de_acesso)
                                controle_de_repeticao.append(chave_de_acesso)
                                if not rt_contador:
                                    autor_da_rt, rt = utils.copiarRT(passos=4)
                                    dono_da_rt.append(autor_da_rt)
                                    rt_contador.append(rt)
                                utils.tratarCasoXML()
                                sem_xml.append(rt_contador[0])
                                return operarLancamento(pular_processo)
                            
                        press("enter")
                        sleep(0.5)
                        press("tab")
                        caminho_absoluto = str(Path('xmlFiscalio').resolve())
                        caminho = fr'{caminho_absoluto}\{chave_de_acesso}.xml'
                        copy(caminho)
                        hotkey("ctrl", "v")
                        sleep(0.7)
                        hotkey(["shift", "tab"]*2, interval=0.4)
                        press("enter", interval=1)
                        sleep(1)

                        erro_de_xml = utils.encontrarImagem(r'Imagens\erroNaImportacaoDoXML.png')
                        if type(erro_de_xml) == pyscreeze.Box:
                            press("enter")
                            pular_processo.append(chave_de_acesso)
                            controle_de_repeticao.append(chave_de_acesso)
                            if not rt_contador:
                                autor_da_rt, rt = utils.copiarRT(passos=4)
                                dono_da_rt.append(autor_da_rt)
                                rt_contador.append(rt)
                            utils.tratarCasoXML()
                            xml_ilegivel.append(rt_contador[0])
                            return operarLancamento(pular_processo)
                        estado_do_caixa = utils.filtrarPorStatus()
                        return operarLancamento(pular_processo)
                    
                    else:
                        clicar_novamente = utils.encontrarImagemLocalizada(r'Imagens\XMLPendente.png')
                        if type(clicar_novamente) == tuple:
                            doubleClick(x,y)
                        else:
                            break

            estado_do_caixa = utils.filtrarPorStatus()
            return operarLancamento(pular_processo)
        
        
        elif controlador == 3:
            chave_de_acesso, processo_feito_errado = utils.copiarChaveDeAcesso()

            if processo_feito_errado == True:
                controle_de_repeticao.append(chave_de_acesso)
                print("Erro de Chave de Acesso")
                if not rt_contador:
                    autor_da_rt, rt = utils.copiarRT(passos=4)
                    dono_da_rt.append(autor_da_rt)
                    rt_contador.append(rt)
                try:
                    verificador = pular_processo.index(chave_de_acesso)
                except:
                    chave_inconforme.append(rt_contador[0])
                pular_processo.append(chave_de_acesso)
                estado_do_caixa = utils.filtrarPorStatus()
                sleep(0.5)
                press("down")
                return operarLancamento(pular_processo)
            
            try:
                verificador = pular_processo.index(chave_de_acesso)
                try:
                    verificador = controle_de_repeticao.index(chave_de_acesso)
                    press(["tab"]*7, interval=0.1)
                    sleep(1)
                    press("enter")
                    sleep(1)
                    repetir_acao = utils.encontrarImagemLocalizada(r'Imagens\botaoLancarNota.png')
                    while type(repetir_acao) == tuple:
                        press("enter")
                        repetir_acao = utils.encontrarImagemLocalizada(r'Imagens\botaoLancarNota.png')
                    if rt_contador:
                        utils.enviarEmail(rt_contador, dono_da_rt, sem_xml, chave_inconforme, xml_ilegivel, cond_pag, bloqueado, cnpj_inconclusivo, chave_sefaz, ncm_problematica)
                    raise FailSafeException
                
                except:
                    estado_do_caixa = utils.filtrarPorStatus()
                    sleep(0.5)
                    press("down")
                    print("Já vi esse, paizão")
                    controle_de_repeticao.append(chave_de_acesso)
                    return operarLancamento(pular_processo)
                
            except ValueError:
                caminho = "xmlFiscalio\\" + chave_de_acesso + ".xml"
                path = Path(caminho)

                if not path.exists():
                    pular_processo.append(chave_de_acesso)
                    controle_de_repeticao.append(chave_de_acesso)
                    if not rt_contador:
                        autor_da_rt, rt = utils.copiarRT(passos=4)
                        dono_da_rt.append(autor_da_rt)
                        rt_contador.append(rt)
                    utils.tratarCasoXML()
                    sem_xml.append(rt_contador[0])
                    return operarLancamento(pular_processo)
                
                x, y = utils.clicarDuasVezes(r'Imagens\solicitarXML.png')

                while True:
                    solicitar_xml = utils.encontrarImagem(r'Imagens\XMLAindaNaoSolicitado.png')
                    solicitar_xml2 = utils.encontrarImagem(r'Imagens\XMLAindaNaoSolicitado2.png')
                    if type(solicitar_xml) == pyscreeze.Box or type(solicitar_xml2) == pyscreeze.Box:
                        break

                press("enter", interval=1)
                press("tab")
                caminho_absoluto = str(Path('xmlFiscalio').resolve())
                caminho = fr'{caminho_absoluto}\{chave_de_acesso}.xml'
                copy(caminho)
                hotkey("ctrl", "v")
                sleep(0.7)
                hotkey(["shift", "tab"]*2, interval=0.4)
                press("enter", interval=1)
                sleep(1)

                erro_de_xml = utils.encontrarImagem(r'Imagens\erroNaImportacaoDoXML.png')
                if type(erro_de_xml) == pyscreeze.Box:
                    press("enter")
                    pular_processo.append(chave_de_acesso)
                    controle_de_repeticao.append(chave_de_acesso)
                    if not rt_contador:
                        autor_da_rt, rt = utils.copiarRT(passos=4)
                        dono_da_rt.append(autor_da_rt)
                        rt_contador.append(rt)
                    utils.tratarCasoXML()
                    xml_ilegivel.append(rt_contador[0])
                    return operarLancamento(pular_processo)
                
                estado_do_caixa = utils.filtrarPorStatus()
                return operarLancamento(pular_processo)
            

        else:
            chave_de_acesso, processo_feito_errado = utils.copiarChaveDeAcesso()
            estado_do_caixa = chave_de_acesso

            if estado_do_caixa == True:
                cont = 0
                x, y = utils.clicarEmFinalizar()
                finalizar = utils.encontrarImagemLocalizada(r'Imagens\finalizar.png')
                ainda_tem_processo_pendente = utils.encontrarImagemLocalizada(r'Imagens\aindaTemProcessoParaLancar.png')
                if type(finalizar) != tuple and type(ainda_tem_processo_pendente) != tuple:
                    while type(finalizar) != tuple and type(ainda_tem_processo_pendente) != tuple:
                        finalizar = utils.encontrarImagemLocalizada(r'Imagens\finalizar.png')
                        ainda_tem_processo_pendente = utils.encontrarImagemLocalizada(r'Imagens\aindaTemProcessoParaLancar.png')
                        cont+=1
                        if cont == 4:
                            moveTo(150,100)
                            doubleClick(x,y)
                            sleep(1)

                if type(ainda_tem_processo_pendente) == tuple:
                    press("enter")
                    utils.tabEEnter()
                    sleep(2)
                    repetir_acao = utils.encontrarImagemLocalizada(r'Imagens\botaoLancarNota.png')
                    while type(repetir_acao) == tuple:
                        press("enter")
                        repetir_acao = utils.encontrarImagemLocalizada(r'Imagens\botaoLancarNota.png')
                    if rt_contador:
                        utils.enviarEmail(rt_contador, dono_da_rt, sem_xml, chave_inconforme, xml_ilegivel, cond_pag, bloqueado, cnpj_inconclusivo, chave_sefaz, ncm_problematica)
                    raise FailSafeException
                
                if type(finalizar) == tuple:
                    press("enter")
                utils.aguardar()
                utils.clicarBotaoSair()
                if rt_contador:
                    utils.enviarEmail(rt_contador, dono_da_rt, sem_xml, chave_inconforme, xml_ilegivel, cond_pag, bloqueado, cnpj_inconclusivo, chave_sefaz, ncm_problematica)
                raise FailSafeException
            

            try:
                verificador = pular_processo.index(chave_de_acesso)
                try:
                    verificador = controle_de_repeticao.index(chave_de_acesso)
                    press(["tab"]*7, interval=0.5)
                    sleep(2)
                    press("enter")
                    sleep(1)
                    repetir_acao = utils.encontrarImagemLocalizada(r'Imagens\botaoLancarNota.png')
                    while type(repetir_acao) == tuple:
                        press("enter")
                        repetir_acao = utils.encontrarImagemLocalizada(r'Imagens\botaoLancarNota.png')
                    if rt_contador:
                        utils.enviarEmail(rt_contador, dono_da_rt, sem_xml, chave_inconforme, xml_ilegivel, cond_pag, bloqueado, cnpj_inconclusivo, chave_sefaz, ncm_problematica)
                    raise FailSafeException
                
                except:
                    estado_do_caixa = utils.filtrarPorStatus()
                    sleep(0.5)
                    press("down")
                    print("Já vi esse, paizão")
                    controle_de_repeticao.append(chave_de_acesso)
                    return operarLancamento(pular_processo)
                
            except:
                caminho = "xmlFiscalio\\" + chave_de_acesso + ".xml"
                path = Path(caminho)
                if not path.exists():
                    controle_de_repeticao.append(chave_de_acesso)
                    pular_processo.append(chave_de_acesso)
                    if not rt_contador:
                        autor_da_rt, rt = utils.copiarRT(passos=4)
                        dono_da_rt.append(autor_da_rt)
                        rt_contador.append(rt)
                    utils.tratarCasoXML()
                    sem_xml.append(rt_contador[0])
                    return operarLancamento(pular_processo)
                
                
                try:
                    with open(caminho) as fd:
                        doc = xmltodict.parse(fd.read())
                except UnicodeDecodeError:
                    with open(caminho, encoding='utf-8') as fd:
                        doc = xmltodict.parse(fd.read())
                except:
                    with open(caminho, encoding='utf-8') as fd:
                        doc = xmltodict.parse(fd.read(), attr_prefix="@", cdata_key="#text")
           

            estado_do_caixa = utils.clicarEmLancar()
            if estado_do_caixa == True:
                cont = 0
                x, y = utils.clicarEmFinalizar()
                finalizar = utils.encontrarImagemLocalizada(r'Imagens\finalizar.png')
                ainda_tem_processo_pendente = utils.encontrarImagemLocalizada(r'Imagens\aindaTemProcessoParaLancar.png')
                if type(finalizar) != tuple and type(ainda_tem_processo_pendente) != tuple:
                    while type(finalizar) != tuple and type(ainda_tem_processo_pendente) != tuple:
                        finalizar = utils.encontrarImagemLocalizada(r'Imagens\finalizar.png')
                        ainda_tem_processo_pendente = utils.encontrarImagemLocalizada(r'Imagens\aindaTemProcessoParaLancar.png')
                        cont+=1
                        if cont == 4:
                            moveTo(150,100)
                            doubleClick(x,y)
                            sleep(1)

                if type(ainda_tem_processo_pendente) == tuple:
                    press("enter")
                    utils.tabEEnter()
                    sleep(2)
                    repetir_acao = utils.encontrarImagemLocalizada(r'Imagens\botaoLancarNota.png')
                    while type(repetir_acao) == tuple:
                        press("enter")
                        repetir_acao = utils.encontrarImagemLocalizada(r'Imagens\botaoLancarNota.png')
                    if rt_contador:
                        utils.enviarEmail(rt_contador, dono_da_rt, sem_xml, chave_inconforme, xml_ilegivel, cond_pag, bloqueado, cnpj_inconclusivo, chave_sefaz, ncm_problematica)
                    raise FailSafeException
                
                if type(finalizar) == tuple:
                    press("enter")
                utils.aguardar()
                utils.clicarBotaoSair()
                if rt_contador:
                    utils.enviarEmail(rt_contador, dono_da_rt, sem_xml, chave_inconforme, xml_ilegivel, cond_pag, bloqueado, cnpj_inconclusivo, chave_sefaz, ncm_problematica)
                raise FailSafeException
            

            else:
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

                print(nome_fantasia_forn, itens, indices_e_impostos)


                tela_de_lancamento = utils.encontrarImagem(r'Imagens\documentoEntrada.png')
                while type(tela_de_lancamento) != pyscreeze.Box:
                    cadastro_fornecedor = utils.encontrarImagem(r'Imagens\telaCadastroDeFornecedor.png')
                    if type(cadastro_fornecedor) == pyscreeze.Box:
                        sem_nome_fantasia = utils.encontrarImagem(r'Imagens\semNomeFantasia.png')
                        if type(sem_nome_fantasia) == pyscreeze.Box:
                            press(["tab"]*2)
                            write(nome_fantasia_forn, interval=0.1)
                            press("tab")
                            sleep(1)
                        hotkey("alt", "a")
                        sleep(1)
                        press(["tab"]*5)
                        natureza = "2020087"
                        write(natureza, interval=0.1)
                        press("tab")
                        sleep(1)
                        hotkey("alt", "f")
                        sleep(1)
                        hotkey(["shift", "tab"]*3, interval=0.4)
                        sleep(0.5)
                        press("space")
                        sleep(0.5)
                        press(["up"]*2)
                        press("enter")
                        sleep(0.5)
                        hotkey("ctrl", "s")
                        sleep(0.5)

                    tela_de_lancamento = utils.encontrarImagem(r'Imagens\documentoEntrada.png')
                    utils.lancarRetroativo()

                    cc_bloqueado = utils.encontrarImagem(r'Imagens\ccBloqueado.png')
                    if type(cc_bloqueado) == pyscreeze.Box:
                        press("enter")
                        sleep(0.5)
                        utils.rejeitarCaixa()
                        print("Erro de CC")
                        raise FailSafeException

                    tela_de_lancamento = utils.encontrarImagem(r'Imagens\documentoEntrada.png')
                    tela_bloqueio = utils.encontrarImagem(r'Imagens\algumBloqueio.png')
                    if type(tela_bloqueio) == pyscreeze.Box:
                        pular_processo.append(chave_de_acesso)
                        controle_de_repeticao.append(chave_de_acesso)
                        press("enter")
                        sleep(1)
                        utils.aguardar1()
                        prod_bloq = utils.encontrarImagemLocalizada(r'Imagens\produtoBloqueado.png')
                        erro_condicao_pag = utils.esperarAparecer(r'Imagens\erroCondicaoDePagamento.png')
                        if type(prod_bloq) == tuple or type(erro_condicao_pag) == tuple:
                            press("enter")
                            sleep(0.5)
                            if not rt_contador:
                                autor_da_rt, rt = utils.copiarRT(passos=4)
                                dono_da_rt.append(autor_da_rt)
                                rt_contador.append(rt)
                        if type(erro_condicao_pag) == tuple:
                            cond_pag.append(rt_contador[0])
                            print("Erro de condição de pagamento, meu patrãozinho")
                        elif type(prod_bloq) == tuple:
                            bloqueado.append(rt_contador[0])
                            print("Problema de produto bloqueado, meu parceirinho")
                        estado_do_caixa = utils.filtrarPorStatus()
                        sleep(0.5)
                        press("down")
                        return operarLancamento(pular_processo)

                    erro_cnpj = utils.encontrarImagemLocalizada(r'Imagens\erroEsquisito.png')
                    if type(erro_cnpj) == tuple:
                        press("enter")
                        sleep(1)
                        utils.aguardar1()

                    tela_de_lancamento = utils.encontrarImagem(r'Imagens\documentoEntrada.png')
                    erro_sefaz = utils.encontrarImagem(r'Imagens\naoEncontradaNoSefaz.png')
                    chave_divergente = utils.encontrarImagem(r'Imagens\chaveNaoConfereNF.png')
                    if type(erro_sefaz) == pyscreeze.Box or type(chave_divergente) == pyscreeze.Box:
                        pular_processo.append(chave_de_acesso)
                        controle_de_repeticao.append(chave_de_acesso)
                        press("enter")
                        sleep(0.5)
                        tela_bloqueio = utils.esperarAparecer(r'Imagens\algumBloqueio.png')
                        press("enter")
                        sleep(1)
                        utils.aguardar1()
                        erro_condicao_pag = utils.encontrarImagemLocalizada(r'Imagens\erroCondicaoDePagamento.png')
                        if type(erro_condicao_pag) == tuple:
                            press("enter")
                            sleep(0.5)
                        erro_generico = utils.encontrarImagemLocalizada(r'Imagens\erroGenerico.png')   
                        if type(erro_generico) == tuple:
                            press("enter")
                            sleep(0.5) 
                        if not rt_contador:
                            autor_da_rt, rt = utils.copiarRT(passos=4)
                            dono_da_rt.append(autor_da_rt)
                            rt_contador.append(rt)
                        estado_do_caixa = utils.filtrarPorStatus()
                        sleep(0.5)
                        press("down")
                        if type(erro_cnpj) == tuple:
                            cnpj_inconclusivo.append(rt_contador[0])
                            print("Erro inconclusivo com o CNPJ")
                        elif type(erro_condicao_pag) == tuple:
                            cond_pag.append(rt_contador[0])
                            print("Erro de condição de pagamento, meu patrãozinho")
                        else:
                            chave_sefaz.append(rt_contador[0])
                            print("Problema com a chave de acesso, meu patrãozinho")
                        return operarLancamento(pular_processo)


                    tela_de_lancamento = utils.encontrarImagem(r'Imagens\documentoEntrada.png')
                    erro_ncm = utils.encontrarImagemLocalizada(r'Imagens\erroNCM.png')
                    if type(erro_ncm) == tuple:
                        pular_processo.append(chave_de_acesso)
                        controle_de_repeticao.append(chave_de_acesso)
                        press("esc")
                        sleep(0.7)
                        if not rt_contador:
                            autor_da_rt, rt = utils.copiarRT(passos=4)
                            dono_da_rt.append(autor_da_rt)
                            rt_contador.append(rt)
                        estado_do_caixa = utils.filtrarPorStatus()
                        sleep(0.5)
                        press("down")
                        ncm_problematica.append(rt_contador[0])
                        print("Problema na NCM, meu parceirinho")
                        return operarLancamento(pular_processo)
                    
                    tela_de_lancamento = utils.encontrarImagem(r'Imagens\documentoEntrada.png')
                    
                press(["tab"]*10)
                sleep(0.6)
                press(["right"]*8) 


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
                    sleep(1.5)

                hotkey("ctrl", "s")
                sleep(1)


                erro_cnpj = utils.encontrarImagemLocalizada(r'Imagens\erroCNPJ.png')
                if type(erro_cnpj) == tuple:
                    press("enter")
                    campo_sped = utils.encontrarImagemLocalizada(r'Imagens\campoSPED.png')
                    x, y = campo_sped
                    doubleClick(x,y)
                    sleep(0.4)
                    write("NF", interval=0.3)
                    press("tab")
                    hotkey("ctrl", "s")
                    sleep(1)

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


                estado_do_caixa = utils.filtrarPorStatus()

                if type(estado_do_caixa) == tuple:
                    cont = 0
                    x, y = utils.clicarEmFinalizar()
                    finalizar = utils.encontrarImagemLocalizada(r'Imagens\finalizar.png')
                    ainda_tem_processo_pendente = utils.encontrarImagemLocalizada(r'Imagens\aindaTemProcessoParaLancar.png')
                    if type(finalizar) != tuple and type(ainda_tem_processo_pendente) != tuple:
                        while type(finalizar) != tuple and type(ainda_tem_processo_pendente) != tuple:
                            finalizar = utils.encontrarImagemLocalizada(r'Imagens\finalizar.png')
                            ainda_tem_processo_pendente = utils.encontrarImagemLocalizada(r'Imagens\aindaTemProcessoParaLancar.png')
                            cont+=1
                            if cont == 4:
                                moveTo(150,100)
                                doubleClick(x,y)
                                sleep(1)

                    if type(ainda_tem_processo_pendente) == tuple:
                        press("enter")
                        utils.tabEEnter()
                        sleep(2)
                        repetir_acao = utils.encontrarImagemLocalizada(r'Imagens\botaoLancarNota.png')
                        while type(repetir_acao) == tuple:
                            press("enter")
                            repetir_acao = utils.encontrarImagemLocalizada(r'Imagens\botaoLancarNota.png')
                        if rt_contador:
                            utils.enviarEmail(rt_contador, dono_da_rt, sem_xml, chave_inconforme, xml_ilegivel, cond_pag, bloqueado, cnpj_inconclusivo, chave_sefaz, ncm_problematica)
                        raise FailSafeException
                    
                    if type(finalizar) == tuple:
                        press("enter")
                    utils.aguardar()
                    utils.clicarBotaoSair()
                    if rt_contador:
                        utils.enviarEmail(rt_contador, dono_da_rt, sem_xml, chave_inconforme, xml_ilegivel, cond_pag, bloqueado, cnpj_inconclusivo, chave_sefaz, ncm_problematica)
                    raise FailSafeException
                
                controle_de_repeticao.clear()
                return operarLancamento(pular_processo)

    operarLancamento(pular_processo)
    sleep(1)


