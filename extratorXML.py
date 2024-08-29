from utils import formatador, formatador2, formatador3

class ProcessadorXML:
    def __init__(self, doc):
        self.doc = doc
        self.valores_do_item = []
        self.indices_e_impostos = []
        self.itens = []


    def coletarNomeFantasia(self):
    
        try:
            nome_fantasia_forn = self.doc["nfeProc"]["NFe"]["infNFe"]["emit"]["xFant"]
        except KeyError:
            try:
                nome_fantasia_forn = self.doc["enviNFe"]["NFe"]["infNFe"]["emit"]["xFant"]
            except KeyError:
                try:
                    nome_fantasia_forn = self.doc["nfeProc"]["NFe"]["infNFe"]["emit"]["xNome"]
                except KeyError:
                    nome_fantasia_forn = self.doc["enviNFe"]["NFe"]["infNFe"]["emit"]["xNome"]


        nome_fantasia_forn = nome_fantasia_forn[:20]

        return nome_fantasia_forn


    def coletarDadosXML(self, coletor_xml, impostos_xml):
        valor_prod = coletor_xml["vProd"]
        valor_prod = formatador(valor_prod)
         
        quantidade_comprada = coletor_xml["qCom"]
        quantidade_comprada = formatador(quantidade_comprada, casas_decimais="{:.6f}")
        valor_unitario = coletor_xml["vUnCom"]
        valor_unitario = formatador(valor_unitario, casas_decimais="{:.6f}")

        self.valores_do_item.append(valor_prod)
        self.valores_do_item.append(quantidade_comprada)
        self.valores_do_item.append(valor_unitario)

        try:
            valor_desconto_xml = coletor_xml["vDesc"]
            valor_desconto_xml = formatador3(valor_desconto_xml)
        except KeyError:
            valor_desconto_xml = 0.00

        self.valores_do_item.append(valor_desconto_xml)

        try:
            valor_frete_xml = coletor_xml["vFrete"]
            valor_frete_xml = formatador3(valor_frete_xml)
        except KeyError:
            valor_frete_xml = 0.00

        self.valores_do_item.append(valor_frete_xml)

        try:
            valor_seguro_xml = coletor_xml["vSeg"]
            valor_seguro_xml = formatador3(valor_seguro_xml)
        except KeyError:
            valor_seguro_xml = 0.00

        self.valores_do_item.append(valor_seguro_xml)

        try:
            valor_desp_xml = coletor_xml["vOutro"]
            valor_desp_xml = formatador3(valor_desp_xml)
        except KeyError:
            valor_desp_xml = 0.00

        self.valores_do_item.append(valor_desp_xml)

        try:
            busca_icms_xml = impostos_xml["ICMS"]
            atributos_icms = busca_icms_xml.values()
            atributos_icms = list(atributos_icms)
            descompactar_lista = atributos_icms[0]
            valor_icms = descompactar_lista["vICMS"]
            valor_icms = formatador3(valor_icms)
        except KeyError:
            valor_icms = 0.00

        self.valores_do_item.append(valor_icms)

        if valor_icms != 0.00:
            aliquota_icms = descompactar_lista["pICMS"]
            aliquota_icms = formatador2(aliquota_icms)
            bc_icms = descompactar_lista["vBC"]
            bc_icms = formatador3(bc_icms)
            self.valores_do_item.append((bc_icms, aliquota_icms))

        try:
            busca_icms_xml = impostos_xml["ICMS"]
            atributos_icms = busca_icms_xml.values()
            atributos_icms = list(atributos_icms)
            descompactar_lista = atributos_icms[0]
            valor_icms_st = descompactar_lista["vICMSST"]
            valor_icms_st = formatador3(valor_icms_st)
        except KeyError:
            valor_icms_st = 0.00

        self.valores_do_item.append(valor_icms_st)

        if valor_icms_st != 0.00:
            aliquota_icms_st = descompactar_lista["pICMSST"]
            aliquota_icms_st = formatador2(aliquota_icms_st)
            bc_icms_st = descompactar_lista["vBCST"]
            bc_icms_st = formatador3(bc_icms_st)
            self.valores_do_item.append((bc_icms_st, aliquota_icms_st))

        try:
            busca_ipi_xml = impostos_xml["IPI"]["IPITrib"]
            valor_ipi = busca_ipi_xml["vIPI"]
            valor_ipi = formatador2(valor_ipi)
            valor_ipi = float(valor_ipi)
        except KeyError:
            valor_ipi = 0.00

        self.valores_do_item.append(valor_ipi)

        if valor_ipi != 0.00:
            aliquota_ipi = busca_ipi_xml["pIPI"]
            aliquota_ipi = formatador2(aliquota_ipi)
            bc_ipi = busca_ipi_xml["vBC"]
            bc_ipi = formatador3(bc_ipi)
            self.valores_do_item.append((bc_ipi, aliquota_ipi))

        return self.valores_do_item
    
    
    def trabalharDadosXML(self, valores_do_item):
        controlador = len(valores_do_item)
        cont = 0
        aux = 0
        try:
            while cont <= controlador:
                tem_icms = False
                tem_icms_st = False
                tem_ipi = False
                if valores_do_item[cont+7] != 0.00:
                    cont+=8
                    tem_icms = True
                else:
                    cont+=7
                if valores_do_item[cont+1] != 0.00:
                    cont+=3
                    tem_icms_st = True
                else:
                    cont+=2
                if valores_do_item[cont] != 0.00:
                    cont+=2
                    tem_ipi = True
                else:
                    cont+=1
                self.itens.append(self.valores_do_item[aux:cont])
                aux=cont
                if tem_icms == True and tem_icms_st == True and tem_ipi == True:
                    ctrl_imposto = 7
                elif tem_icms == True and tem_icms_st == True:
                    ctrl_imposto = 6
                elif tem_icms == True and tem_ipi == True:
                    ctrl_imposto = 5
                elif tem_icms_st == True and tem_ipi == True:
                    ctrl_imposto = 4
                elif tem_ipi == True:
                    ctrl_imposto = 3
                elif tem_icms_st == True:
                    ctrl_imposto = 2
                elif tem_icms == True:
                    ctrl_imposto = 1
                else:
                    ctrl_imposto = 0
                self.indices_e_impostos.append(ctrl_imposto)
        except IndexError:
            pass

        return self.itens, self.indices_e_impostos

