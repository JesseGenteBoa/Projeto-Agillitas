from pyautogui import hotkey, press, FAILSAFE
from pydirectinput import click as mouseClique, moveTo, doubleClick
from pyperclip import copy  
from time import sleep
from pathlib import Path
import utils
import pyscreeze
import acaoComum


FAILSAFE = True
doc = ''


def robozinho():
    sleep(0.5)
    pular_processo = []                     
    controle_de_repeticao = []
    dono_da_rt = []
    chave_inconforme = []
    sem_xml = []
    rt_contador = []
    nf_ja_lancada = []
    cond_pag = []
    bloqueado = []
    cnpj_inconclusivo = []
    chave_sefaz =[]
    ncm_problematica = []


    try:
        primeiro_clique = utils.encontrarImagemLocalizada(r'Imagens\filtrarPendentes.png')
        x, y = primeiro_clique
        mouseClique(x, y)
    except TypeError:
        primeiro_clique = utils.encontrarImagemLocalizada(r'Imagens\filtrarPendentesSelecionado.png')
        x, y = primeiro_clique
        mouseClique(x, y)

    controle_acao = utils.encontrarImagemLocalizada(r'Imagens\controleDeAcao.png')
    if type(controle_acao) != tuple:
        sleep(0.5)
        hotkey(["shift", "tab"]*4, interval=0.04)
        press("p", interval=0.1)
        mouseClique(x, y)
        hotkey("shift", "tab", interval=0.04)
        press("backspace")
        press(["tab"]*2, interval=0.04)
        press("enter", interval=1)

    acaoComum.procederPrimario()

    moveTo(150,100)
    esperar = utils.esperarAparecer(r'Imagens\statusPendente2.png')

    sleep(0.5)

    estado_do_caixa = acaoComum.filtrarPorStatus()
        
    def operarLancamento(pular_processo):
        estado_do_caixa = False
        global doc

        controlador = acaoComum.verificarStatus()

        if controlador == 1:
            estado_do_caixa = acaoComum.clicarEmLancar()
            cc_bloqueado = utils.encontrarImagem(r'Imagens\ccBloqueado.png')
            if type(cc_bloqueado) == pyscreeze.Box:
                press("enter", interval=0.5)
                acaoComum.rejeitarCaixa()
                return robozinho()
            
            repentina_etapa_final = utils.encontrarImagem(r'Imagens\etapaFinal.png')

            if type(repentina_etapa_final) == pyscreeze.Box:
                utils.tratarEtapaFinal()

            if estado_do_caixa == "NF já lançada":
                controle_de_repeticao.append(chave_de_acesso)
                pular_processo.append(chave_de_acesso)
                press("tab", interval=0.3)
                press("enter", interval=0.5)
                if not rt_contador:
                    autor_da_rt, rt = acaoComum.copiarRT()
                    dono_da_rt.append(autor_da_rt)
                    rt_contador.append(rt)
                nf_ja_lancada.append(rt_contador[0])
                acaoComum.pularProcesso()
                return operarLancamento(pular_processo)
            
            elif estado_do_caixa == True:
                x, y = utils.clicarEmFinalizar()
                finalizar = utils.encontrarImagemLocalizada(r'Imagens\finalizar.png')
                ainda_tem_processo_pendente = utils.encontrarImagemLocalizada(r'Imagens\aindaTemProcessoParaLancar.png')
                finalizar, ainda_tem_processo_pendente = acaoComum.insistirEmEncontrar(finalizar, ainda_tem_processo_pendente, x, y)

                if type(ainda_tem_processo_pendente) == tuple:
                    utils.tratarProcessosPendentes()
                    if rt_contador:
                        utils.enviarEmail(rt_contador, dono_da_rt, sem_xml, chave_inconforme, nf_ja_lancada, cond_pag, bloqueado, cnpj_inconclusivo, chave_sefaz, ncm_problematica)
                    return robozinho()
                
                if type(finalizar) == tuple:
                    press("enter")
                utils.aguardar()
                utils.clicarBotaoSair()
                if rt_contador:
                    utils.enviarEmail(rt_contador, dono_da_rt, sem_xml, chave_inconforme, nf_ja_lancada, cond_pag, bloqueado, cnpj_inconclusivo, chave_sefaz, ncm_problematica)
                return robozinho()
            
            else:
                estado_do_caixa = acaoComum.filtrarPorStatus()

                if type(estado_do_caixa) == tuple:
                    x, y = utils.clicarEmFinalizar()
                    finalizar = utils.encontrarImagemLocalizada(r'Imagens\finalizar.png')
                    ainda_tem_processo_pendente = utils.encontrarImagemLocalizada(r'Imagens\aindaTemProcessoParaLancar.png')
                    finalizar, ainda_tem_processo_pendente = acaoComum.insistirEmEncontrar(finalizar, ainda_tem_processo_pendente, x, y)

                    if type(ainda_tem_processo_pendente) == tuple:
                        utils.tratarProcessosPendentes()
                        if rt_contador:
                            utils.enviarEmail(rt_contador, dono_da_rt, sem_xml, chave_inconforme, nf_ja_lancada, cond_pag, bloqueado, cnpj_inconclusivo, chave_sefaz, ncm_problematica)
                        return robozinho()
                    
                    if type(finalizar) == tuple:
                        press("enter")
                    utils.aguardar()
                    utils.clicarBotaoSair()
                    if rt_contador:
                        utils.enviarEmail(rt_contador, dono_da_rt, sem_xml, chave_inconforme, nf_ja_lancada, cond_pag, bloqueado, cnpj_inconclusivo, chave_sefaz, ncm_problematica)
                    return robozinho()
                
                controle_de_repeticao.clear()
                return operarLancamento(pular_processo)
            

        elif controlador == 2:
            status_nf, falsa_duplicidade = acaoComum.solicitarXML()

            if type(status_nf) == tuple:
                try:
                    numero_nf = chave_de_acesso[25:34]
                except UnboundLocalError:
                    chave_de_acesso, processo_feito_errado = acaoComum.copiarChaveDeAcesso()
                    numero_nf = chave_de_acesso[25:34]
                acaoComum.rejeitarCaixa(mensagem = f"NF {numero_nf} foi cancelada pelo fornecedor.")
                print("NF cancelada")
                return robozinho()
            
            if type(falsa_duplicidade) == tuple:
                chave_de_acesso, processo_feito_errado = acaoComum.copiarChaveDeAcesso()
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
                                press("enter", interval=1)
                                utils.repetirBotao()
                                clique_status = utils.esperarAparecer(r'Imagens\statusNegrito.png')  
                                x, y = clique_status
                                mouseClique(x, y)
                                sleep(0.7)
                                press("down")
                                if rt_contador:
                                    utils.enviarEmail(rt_contador, dono_da_rt, sem_xml, chave_inconforme, nf_ja_lancada, cond_pag, bloqueado, cnpj_inconclusivo, chave_sefaz, ncm_problematica)
                                return robozinho()
                            
                            except:
                                press("right", interval=0.05)
                                press("enter")
                                acaoComum.pularProcesso()
                                print("Já vi esse, paizão")
                                controle_de_repeticao.append(chave_de_acesso)
                                return operarLancamento(pular_processo)
                            
                        except:
                            caminho = "C:\\Users\\User\\OneDrive - EQS Engenharia Ltda\\Área de Trabalho\\Mariquinha\\xmlFiscalio\\" + chave_de_acesso + ".xml"
                            path = Path(caminho)

                            if not path.exists():
                                press("right", interval=0.05)
                                press("enter")
                                pular_processo.append(chave_de_acesso)
                                controle_de_repeticao.append(chave_de_acesso)
                                if not rt_contador:
                                    autor_da_rt, rt = acaoComum.copiarRT(passos=2)
                                    dono_da_rt.append(autor_da_rt)
                                    rt_contador.append(rt)
                                acaoComum.tratarCasoXML()
                                sem_xml.append(rt_contador[0])
                                return operarLancamento(pular_processo)
                            
                        press("enter", interval=0.5)
                        press("tab")
                        #caminho_absoluto = str(Path('xmlFiscalio').resolve())
                        #caminho = fr'{caminho_absoluto}\{chave_de_acesso}.xml'
                        copy(caminho)
                        hotkey("ctrl", "v")
                        sleep(0.7)
                        hotkey(["shift", "tab"]*2, interval=0.4)
                        press("enter", interval=2)

                        erro_de_xml = utils.encontrarImagem(r'Imagens\erroNaImportacaoDoXML.png')
                        if type(erro_de_xml) == pyscreeze.Box:
                            press("enter")
                            pular_processo.append(chave_de_acesso)
                            controle_de_repeticao.append(chave_de_acesso)
                            if not rt_contador:
                                autor_da_rt, rt = acaoComum.copiarRT(passos=4)
                                dono_da_rt.append(autor_da_rt)
                                rt_contador.append(rt)
                            acaoComum.tratarCasoXML()
                            sem_xml.append(rt_contador[0])
                            return operarLancamento(pular_processo)
                        estado_do_caixa = acaoComum.filtrarPorStatus()
                        return operarLancamento(pular_processo)
                    
                    else:
                        clicar_novamente = utils.encontrarImagemLocalizada(r'Imagens\XMLPendente.png')
                        if type(clicar_novamente) == tuple:
                            doubleClick(x,y)
                        else:
                            break

            estado_do_caixa = acaoComum.filtrarPorStatus()
            return operarLancamento(pular_processo)
        

        elif controlador == 3 or controlador == 5:
            chave_de_acesso, processo_feito_errado = acaoComum.copiarChaveDeAcesso()

            if processo_feito_errado == True or controlador == 5:
                try:
                    verificador = controle_de_repeticao.index(chave_de_acesso)
                except:
                    controle_de_repeticao.append(chave_de_acesso)
                    print("Erro de Chave de Acesso")
                    if not rt_contador:
                        autor_da_rt, rt = acaoComum.copiarRT(passos=4)
                        dono_da_rt.append(autor_da_rt)
                        rt_contador.append(rt)
                    try:
                        verificador = pular_processo.index(chave_de_acesso)
                    except:
                        chave_inconforme.append(rt_contador[0])
                    pular_processo.append(chave_de_acesso)
                    acaoComum.pularProcesso()
                    return operarLancamento(pular_processo)
            
            try:
                verificador = pular_processo.index(chave_de_acesso)
                try:
                    verificador = controle_de_repeticao.index(chave_de_acesso)
                    press(["tab"]*7, interval=0.1)
                    sleep(1)
                    press("enter", interval=1)
                    utils.repetirBotao()
                    clique_status = utils.esperarAparecer(r'Imagens\status.png')  
                    x, y = clique_status
                    mouseClique(x, y)
                    sleep(0.7)
                    press("down")
                    if rt_contador:
                        utils.enviarEmail(rt_contador, dono_da_rt, sem_xml, chave_inconforme, nf_ja_lancada, cond_pag, bloqueado, cnpj_inconclusivo, chave_sefaz, ncm_problematica)
                    return robozinho()
                
                except:
                    acaoComum.pularProcesso()
                    print("Já vi esse, paizão")
                    controle_de_repeticao.append(chave_de_acesso)
                    return operarLancamento(pular_processo)
                
            except ValueError:
                caminho = "C:\\Users\\User\\OneDrive - EQS Engenharia Ltda\\Área de Trabalho\\Mariquinha\\xmlFiscalio\\" + chave_de_acesso + ".xml"
                path = Path(caminho)

                if not path.exists():
                    pular_processo.append(chave_de_acesso)
                    controle_de_repeticao.append(chave_de_acesso)
                    if not rt_contador:
                        autor_da_rt, rt = acaoComum.copiarRT(passos=4)
                        dono_da_rt.append(autor_da_rt)
                        rt_contador.append(rt)
                    acaoComum.tratarCasoXML()
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
                #caminho_absoluto = str(Path('xmlFiscalio').resolve())
                #caminho = fr'{caminho_absoluto}\{chave_de_acesso}.xml'
                copy(caminho)
                hotkey("ctrl", "v")
                sleep(0.7)
                hotkey(["shift", "tab"]*2, interval=0.4)
                press("enter", interval=2)

                erro_de_xml = utils.encontrarImagem(r'Imagens\erroNaImportacaoDoXML.png')
                if type(erro_de_xml) == pyscreeze.Box:
                    press("enter")
                    pular_processo.append(chave_de_acesso)
                    controle_de_repeticao.append(chave_de_acesso)
                    if not rt_contador:
                        autor_da_rt, rt = acaoComum.copiarRT(passos=4)
                        dono_da_rt.append(autor_da_rt)
                        rt_contador.append(rt)
                    acaoComum.tratarCasoXML()
                    sem_xml.append(rt_contador[0])
                    return operarLancamento(pular_processo)
                
                estado_do_caixa = acaoComum.filtrarPorStatus()
                return operarLancamento(pular_processo)
            
        else:
            chave_de_acesso, processo_feito_errado = acaoComum.copiarChaveDeAcesso()
            estado_do_caixa = chave_de_acesso

            if estado_do_caixa == True:
                x, y = utils.clicarEmFinalizar()
                finalizar = utils.encontrarImagemLocalizada(r'Imagens\finalizar.png')
                ainda_tem_processo_pendente = utils.encontrarImagemLocalizada(r'Imagens\aindaTemProcessoParaLancar.png')
                finalizar, ainda_tem_processo_pendente = acaoComum.insistirEmEncontrar(finalizar, ainda_tem_processo_pendente, x, y)

                if type(ainda_tem_processo_pendente) == tuple:
                    utils.tratarProcessosPendentes()
                    if rt_contador:
                        utils.enviarEmail(rt_contador, dono_da_rt, sem_xml, chave_inconforme, nf_ja_lancada, cond_pag, bloqueado, cnpj_inconclusivo, chave_sefaz, ncm_problematica)
                    return robozinho()
                
                if type(finalizar) == tuple:
                    press("enter")
                utils.aguardar()
                utils.clicarBotaoSair()
                if rt_contador:
                    utils.enviarEmail(rt_contador, dono_da_rt, sem_xml, chave_inconforme, nf_ja_lancada, cond_pag, bloqueado, cnpj_inconclusivo, chave_sefaz, ncm_problematica)
                return robozinho()
            
            try:
                verificador = pular_processo.index(chave_de_acesso)
                try:
                    verificador = controle_de_repeticao.index(chave_de_acesso)
                    press(["tab"]*7, interval=0.5)
                    sleep(2)
                    press("enter", interval=1)
                    utils.repetirBotao()
                    clique_status = utils.esperarAparecer(r'Imagens\statusNegrito.png')  
                    x, y = clique_status
                    mouseClique(x, y)
                    sleep(0.7)
                    press("down")
                    if rt_contador:
                        utils.enviarEmail(rt_contador, dono_da_rt, sem_xml, chave_inconforme, nf_ja_lancada, cond_pag, bloqueado, cnpj_inconclusivo, chave_sefaz, ncm_problematica)
                    return robozinho()
                
                except:
                    acaoComum.pularProcesso()
                    print("Já vi esse, paizão")
                    controle_de_repeticao.append(chave_de_acesso)
                    return operarLancamento(pular_processo)
                
            except:
                caminho = "C:\\Users\\User\\OneDrive - EQS Engenharia Ltda\\Área de Trabalho\\Mariquinha\\xmlFiscalio\\" + chave_de_acesso + ".xml"
                path = Path(caminho)
                
                if not path.exists():
                    pular_processo.append(chave_de_acesso)
                    controle_de_repeticao.append(chave_de_acesso)
                    if not rt_contador:
                        autor_da_rt, rt = acaoComum.copiarRT(passos=4)
                        dono_da_rt.append(autor_da_rt)
                        rt_contador.append(rt)
                    acaoComum.tratarCasoXML()
                    sem_xml.append(rt_contador[0])
                    return operarLancamento(pular_processo)
                
            estado_do_caixa = acaoComum.clicarEmLancar()
            if estado_do_caixa == "NF já lançada":
                controle_de_repeticao.append(chave_de_acesso)
                pular_processo.append(chave_de_acesso)
                press("tab", interval=0.3)
                press("enter", interval=0.5)
                if not rt_contador:
                    autor_da_rt, rt = acaoComum.copiarRT()
                    dono_da_rt.append(autor_da_rt)
                    rt_contador.append(rt)
                nf_ja_lancada.append(rt_contador[0])
                acaoComum.pularProcesso()
                return operarLancamento(pular_processo)
                
            elif estado_do_caixa == True:
                x, y = utils.clicarEmFinalizar()
                finalizar = utils.encontrarImagemLocalizada(r'Imagens\finalizar.png')
                ainda_tem_processo_pendente = utils.encontrarImagemLocalizada(r'Imagens\aindaTemProcessoParaLancar.png')
                finalizar, ainda_tem_processo_pendente = acaoComum.insistirEmEncontrar(finalizar, ainda_tem_processo_pendente, x, y)

                if type(ainda_tem_processo_pendente) == tuple:
                    utils.tratarProcessosPendentes()
                    if rt_contador:
                        utils.enviarEmail(rt_contador, dono_da_rt, sem_xml, chave_inconforme, nf_ja_lancada, cond_pag, bloqueado, cnpj_inconclusivo, chave_sefaz, ncm_problematica)
                    return robozinho()
                
                if type(finalizar) == tuple:
                    press("enter")
                utils.aguardar()
                utils.clicarBotaoSair()
                if rt_contador:
                    utils.enviarEmail(rt_contador, dono_da_rt, sem_xml, chave_inconforme, nf_ja_lancada, cond_pag, bloqueado, cnpj_inconclusivo, chave_sefaz, ncm_problematica)
                return robozinho()
            
            else:
                nome_fantasia_forn, itens, indices_e_impostos = acaoComum.extrairDadosXML(caminho)

                print(nome_fantasia_forn, itens, indices_e_impostos)


                tela_de_lancamento = utils.encontrarImagem(r'Imagens\documentoEntrada.png')
                while type(tela_de_lancamento) != pyscreeze.Box:

                    acaoComum.verificarCadastroForn(nome_fantasia_forn)

                    tela_de_lancamento = utils.encontrarImagem(r'Imagens\documentoEntrada.png')
                    utils.lancarRetroativo()

                    cc_bloqueado = utils.encontrarImagem(r'Imagens\ccBloqueado.png')
                    if type(cc_bloqueado) == pyscreeze.Box:
                        press("enter", interval=0.5)
                        acaoComum.rejeitarCaixa()
                        print("Erro de CC")
                        return robozinho()

                    tela_de_lancamento = utils.encontrarImagem(r'Imagens\documentoEntrada.png')
                    tela_bloqueio = utils.encontrarImagem(r'Imagens\algumBloqueio.png')
                    if type(tela_bloqueio) == pyscreeze.Box:
                        pular_processo.append(chave_de_acesso)
                        controle_de_repeticao.append(chave_de_acesso)
                        press("enter", interval=1)
                        utils.aguardar1()
                        prod_bloq = utils.encontrarImagemLocalizada(r'Imagens\produtoBloqueado.png')
                        erro_condicao_pag = utils.encontrarImagemLocalizada(r'Imagens\erroCondicaoDePagamento.png')
                        if type(prod_bloq) == tuple or type(erro_condicao_pag) == tuple:
                            press("enter", interval=0.5)
                            if not rt_contador:
                                autor_da_rt, rt = acaoComum.copiarRT()
                                dono_da_rt.append(autor_da_rt)
                                rt_contador.append(rt)
                        if type(erro_condicao_pag) == tuple:
                            cond_pag.append(rt_contador[0])
                            print("Erro de condição de pagamento, meu patrãozinho")
                        elif type(prod_bloq) == tuple:
                            bloqueado.append(rt_contador[0])
                            print("Problema de produto bloqueado, meu parceirinho")
                        acaoComum.pularProcesso()
                        return operarLancamento(pular_processo)

                    erro_cnpj = utils.encontrarImagemLocalizada(r'Imagens\erroEsquisito.png')
                    if type(erro_cnpj) == tuple:
                        press("enter", interval=1)
                        utils.aguardar1()

                    tela_de_lancamento = utils.encontrarImagem(r'Imagens\documentoEntrada.png')
                    erro_sefaz = utils.encontrarImagem(r'Imagens\naoEncontradaNoSefaz.png')
                    chave_divergente = utils.encontrarImagem(r'Imagens\chaveNaoConfereNF.png')
                    if type(erro_sefaz) == pyscreeze.Box or type(chave_divergente) == pyscreeze.Box:
                        pular_processo.append(chave_de_acesso)
                        controle_de_repeticao.append(chave_de_acesso)
                        press("enter", interval=0.5)
                        tela_bloqueio = utils.esperarAparecer(r'Imagens\algumBloqueio.png')
                        press("enter", interval=1)
                        utils.aguardar1()
                        erro_condicao_pag = utils.encontrarImagemLocalizada(r'Imagens\erroCondicaoDePagamento.png')
                        if type(erro_condicao_pag) == tuple:
                            press("enter", interval=0.5)
                        erro_generico = utils.encontrarImagemLocalizada(r'Imagens\erroGenerico.png')   
                        if type(erro_generico) == tuple:
                            press("enter", interval=0.5)
                        if not rt_contador:
                            autor_da_rt, rt = acaoComum.copiarRT()
                            dono_da_rt.append(autor_da_rt)
                            rt_contador.append(rt)
                        acaoComum.pularProcesso()
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
                        press("esc", interval=0.7)
                        if not rt_contador:
                            autor_da_rt, rt = acaoComum.copiarRT()
                            dono_da_rt.append(autor_da_rt)
                            rt_contador.append(rt)
                        acaoComum.pularProcesso()
                        ncm_problematica.append(rt_contador[0])
                        print("Problema na NCM, meu parceirinho")
                        return operarLancamento(pular_processo)
                    
                    tela_de_lancamento = utils.encontrarImagem(r'Imagens\documentoEntrada.png')
                    
                press(["tab"]*10)
                sleep(0.6)
                press(["right"]*8) 


                acaoComum.inserirValoresDaNFnoSistema(indices_e_impostos, itens)

                acaoComum.finalizarLancamento()

            
                estado_do_caixa = acaoComum.filtrarPorStatus()

                if type(estado_do_caixa) == tuple:
                    x, y = utils.clicarEmFinalizar()
                    finalizar = utils.encontrarImagemLocalizada(r'Imagens\finalizar.png')
                    ainda_tem_processo_pendente = utils.encontrarImagemLocalizada(r'Imagens\aindaTemProcessoParaLancar.png')
                    finalizar, ainda_tem_processo_pendente = acaoComum.insistirEmEncontrar(finalizar, ainda_tem_processo_pendente, x, y)

                    if type(ainda_tem_processo_pendente) == tuple:
                        utils.tratarProcessosPendentes()
                        if rt_contador:
                            utils.enviarEmail(rt_contador, dono_da_rt, sem_xml, chave_inconforme, nf_ja_lancada, cond_pag, bloqueado, cnpj_inconclusivo, chave_sefaz, ncm_problematica)
                        return robozinho()
                    
                    if type(finalizar) == tuple:
                        press("enter")
                    utils.aguardar()
                    utils.clicarBotaoSair()
                    if rt_contador:
                        utils.enviarEmail(rt_contador, dono_da_rt, sem_xml, chave_inconforme, nf_ja_lancada, cond_pag, bloqueado, cnpj_inconclusivo, chave_sefaz, ncm_problematica)
                    return robozinho()
    
                controle_de_repeticao.clear()
                return operarLancamento(pular_processo)

    operarLancamento(pular_processo)
    sleep(1)




