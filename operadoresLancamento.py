from pyautogui import hotkey, press, write, FAILSAFE, FailSafeException
from pyperclip import paste
from time import sleep
import pyscreeze
import utils


def escreverValorUnit(valor_unit):
    press("right")
    valor_unit = utils.formatador(valor_unit, casas_decimais="{:.6f}")
    sleep(0.2)
    write(valor_unit)
    sleep(0.2)
    press(["right"]*3)


def verificarValorDoItem(lista, indiceX):
    cancelar_lancamento = False
    razoes = []
    sleep(0.7)
    press(["right"]*4)
    sleep(0.7)
    hotkey("ctrl", "c")
    sleep(0.7)
    valor_do_item_no_siga = paste()
    valor_do_item_no_siga = utils.formatador4(valor_do_item_no_siga)
    valor_do_item_na_NF = lista[indiceX][0]
    valor_do_item_na_NF = utils.formatador3(valor_do_item_na_NF)
    if valor_do_item_no_siga != valor_do_item_na_NF:
        write(lista[indiceX][0])
        sleep(0.8)
        encontrar = utils.encontrarImagem(r'Imagens\valitenErrado.png')
        if type(encontrar) == pyscreeze.Box:
            press("enter")
            sleep(0.5)
            encontrar = utils.encontrarImagem(r'Imagens\valitenErrado.png')
            if type(encontrar) == pyscreeze.Box:
                press("enter")
            press("esc")
            press(["left"]*5)
            sleep(0.2)
            hotkey("ctrl", "c", interval=0.5)
            quantidade_siga = paste()
            quantidade_siga = utils.formatador4(quantidade_siga)
            quantidade_NF = lista[indiceX][1]
            quantidade_NF = utils.formatador3(quantidade_NF)
            valor_unit_NF = lista[indiceX][2]
            valor_unit_NF = utils.formatador3(valor_unit_NF)
            if quantidade_siga == quantidade_NF:
                escreverValorUnit(valor_unit_NF)
            else:
                valor_unit_NF = utils.formatador(valor_unit_NF, casas_decimais="{:.6f}")
                cont = 0
                quantidade_total = []
                quantidade_total.append(quantidade_siga)
                press(["left"]*6)
                sleep(0.2)
                hotkey("ctrl", "c", interval=0.5)
                cod_item = paste()
                try:
                    while sum(quantidade_total) < quantidade_NF:
                        press("down")
                        sleep(0.5)
                        hotkey("ctrl", "c", interval=0.8)
                        item_dividido = paste()
                        cont+=1
                        if item_dividido == cod_item:
                            press(["right"]*6)
                            hotkey("ctrl", "c", interval=0.8)
                            qtd_dividida = paste()
                            qtd_dividida = utils.formatador4(qtd_dividida)
                            quantidade_total.append(qtd_dividida)
                            press("right")
                            write(valor_unit_NF, interval=0.05)
                            press(["left"]*8)      
                        else:
                            break
                except TypeError:
                    pass
                if len(quantidade_total) > 10:
                    press(["up"]*cont, interval=20)
                else:
                    press(["up"]*cont, interval=0.1)
                sleep(0.5)
                press(["right"]*7)
                sleep(0.5)
                write(valor_unit_NF, interval=0.05)
                try:
                    if sum(quantidade_total) != quantidade_NF:
                        cancelar_lancamento = True
                    else:
                        for qtd in quantidade_total:
                            razao = qtd / quantidade_NF
                            razoes.append(razao)
                        press(["right"]*3)
                except TypeError:
                    cancelar_lancamento = True
        else:
            press("left")
    return cancelar_lancamento, razoes


def definirTES(ctrl_imposto):
    if ctrl_imposto != 0:
        tes = "154"
    else:
        tes = "155"
    if tes == "154":
        press(["left"]*9)
        press("enter", interval=0.3)
        write(tes)
        press(["right"]*9)
        natureza = "2020087"
        write(natureza)
        press("enter", interval=0.3)
        press(["left"]*6)
    else:
        press(["left"]*4)


def inserirDesconto(desc_no_item):
    press(["right"]*3)
    sleep(0.5)
    press("enter")
    desc_no_item = utils.formatador2(desc_no_item)
    write(desc_no_item, interval=0.02)
    sleep(0.5)


def inserirFrete(frete_no_item):
    press(["right"]*105)
    sleep(0.6)
    press("enter")
    frete_no_item = utils.formatador2(frete_no_item)
    write(frete_no_item, interval=0.05)
    sleep(0.6)


def inserirSeguro(seg_no_item):
    sleep(0.3)
    press("enter")
    seg_no_item = utils.formatador2(seg_no_item)
    write(seg_no_item, interval=0.05)
    sleep(0.6)


def inserirDespesa(desp_no_item):
    sleep(0.3)
    press("enter")
    desp_no_item = utils.formatador2(desp_no_item)
    write(desp_no_item, interval=0.05)
    sleep(0.6)
    press(["left"]*112)


def inserirICMS(icms_no_item, bc_icms, aliq_icms):
    press(["right"]*7)
    sleep(0.5)
    press("enter")
    bc_icms = utils.formatador2(bc_icms)
    write(bc_icms)
    press(["right"]*8)
    sleep(0.5)
    press("enter")
    write(aliq_icms)
    sleep(0.5)
    press(["left"]*9)
    sleep(0.5)
    press("enter")
    icms_no_item = utils.formatador2(icms_no_item)
    write(icms_no_item)


def inserirICMSST(icmsST_no_item, base_icms_ST, aliq_icms_ST, passosST=9):
    press(["right"]*passosST)
    sleep(0.5)
    press("enter")
    write(aliq_icms_ST)
    press(["left"]*2)
    sleep(0.5)
    press("enter")
    base_icms_ST = utils.formatador2(base_icms_ST)
    write(base_icms_ST)
    sleep(0.5)
    press("right")
    sleep(0.5)
    press("enter")
    icmsST_no_item = utils.formatador2(icmsST_no_item)
    write(icmsST_no_item)
    press(["left"]*12)    


def inserirIPI(ipi_no_item, base_ipi, aliq_ipi, passosIPI=12):
    press(["right"]*passosIPI)
    sleep(0.5)
    press("enter")
    base_ipi = utils.formatador2(base_ipi)
    write(base_ipi)
    press(["right"]*5)
    sleep(0.5)
    press("enter")
    write(aliq_ipi)
    press(["left"]*6)
    sleep(0.5)
    press("enter")
    ipi_no_item = utils.formatador2(ipi_no_item)
    write(ipi_no_item)
    press(["left"]*14)


def zerarImposto(passos_ida=7, passos_volta=8):
    press(["right"]*passos_ida)
    press("enter")
    press("backspace")
    press("enter")
    press(["left"]*passos_volta)


def corrigirPassosHorizontal(cont, item):
    if len(item) > 1:
        press(["right"]*4)
        sleep(1)
        if cont == len(item):
            press(["left"]*4)