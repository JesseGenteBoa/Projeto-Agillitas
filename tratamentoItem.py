
class TratadorItem:

    def __init__(self, item_fracionado, itens, i, ctrl_imposto):
        self.item_fracionado = item_fracionado
        self.itens = itens
        self.i = i
        self.ctrl_imposto = ctrl_imposto
        self.item = []
 
 
    def tratarItem(self):
        if self.ctrl_imposto == 0:
            valor_do_item, quant_do_item, vl_unit_item, desc_no_item, frete_no_item, seg_no_item, desp_no_item, icms_no_item, icmsST_no_item, ipi_no_item = self.itens[self.i]
            if self.item_fracionado != []:
                 for razao in self.item_fracionado:
                    desc = desc_no_item * razao
                    frete = frete_no_item * razao
                    seg = seg_no_item * razao
                    desp = desp_no_item * razao
                    self.item.append([desc, frete, seg, desp, icms_no_item, icmsST_no_item, ipi_no_item])
            else:
                self.item.append([desc_no_item, frete_no_item, seg_no_item, desp_no_item, icms_no_item, icmsST_no_item, ipi_no_item])
       
        elif self.ctrl_imposto == 1:
            valor_do_item, quant_do_item, vl_unit_item, desc_no_item, frete_no_item, seg_no_item, desp_no_item, icms_no_item, base_e_aliq_icms, icmsST_no_item, ipi_no_item = self.itens[self.i]
            base_icms, aliq_icms = base_e_aliq_icms
            if self.item_fracionado != []:
                for razao in self.item_fracionado:
                    desc = desc_no_item * razao
                    frete = frete_no_item * razao
                    seg = seg_no_item * razao
                    desp = desp_no_item * razao
                    icms = icms_no_item * razao
                    bc_icms = base_icms * razao
                    self.item.append([desc, frete, seg, desp, icms, bc_icms, aliq_icms, icmsST_no_item, ipi_no_item])
            else:
                self.item.append([desc_no_item, frete_no_item, seg_no_item, desp_no_item, icms_no_item, base_icms, aliq_icms, icmsST_no_item, ipi_no_item])
       
        elif self.ctrl_imposto == 2:
            valor_do_item, quant_do_item, vl_unit_item, desc_no_item, frete_no_item, seg_no_item, desp_no_item, icms_no_item, icmsST_no_item, base_e_aliq_ST, ipi_no_item = self.itens[self.i]
            base_icms_ST, aliq_icms_ST = base_e_aliq_ST
            if self.item_fracionado != []:
                for razao in self.item_fracionado:
                    desc = desc_no_item * razao
                    frete = frete_no_item * razao
                    seg = seg_no_item * razao
                    desp = desp_no_item * razao
                    icmsST = icmsST_no_item * razao
                    bc_icms_ST = base_icms_ST * razao
                    self.item.append([desc, frete, seg, desp, icms_no_item, icmsST, bc_icms_ST, aliq_icms_ST, ipi_no_item])
            else:
                self.item.append([desc_no_item, frete_no_item, seg_no_item, desp_no_item, icms_no_item, icmsST_no_item, base_icms_ST, aliq_icms_ST, ipi_no_item])
       
        elif self.ctrl_imposto == 3:
            valor_do_item, quant_do_item, vl_unit_item, desc_no_item, frete_no_item, seg_no_item, desp_no_item, icms_no_item, icmsST_no_item, ipi_no_item, base_e_aliq_ipi = self.itens[self.i]
            base_ipi, aliq_ipi = base_e_aliq_ipi
            if self.item_fracionado != []:
                for razao in self.item_fracionado:
                    desc = desc_no_item * razao
                    frete = frete_no_item * razao
                    seg = seg_no_item * razao
                    desp = desp_no_item * razao
                    ipi = ipi_no_item * razao
                    bc_ipi = base_ipi * razao
                    self.item.append([desc, frete, seg, desp, icms_no_item, icmsST_no_item, ipi, bc_ipi, aliq_ipi])
            else:
                self.item.append([desc_no_item, frete_no_item, seg_no_item, desp_no_item, icms_no_item, icmsST_no_item, ipi_no_item, base_ipi, aliq_ipi])
       
        elif self.ctrl_imposto == 4:
            valor_do_item, quant_do_item, vl_unit_item, desc_no_item, frete_no_item, seg_no_item, desp_no_item, icms_no_item, icmsST_no_item, base_e_aliq_ST, ipi_no_item, base_e_aliq_ipi = self.itens[self.i]
            base_icms_ST, aliq_icms_ST = base_e_aliq_ST
            base_ipi, aliq_ipi = base_e_aliq_ipi
            if self.item_fracionado != []:
                for razao in self.item_fracionado:
                    desc = desc_no_item * razao
                    frete = frete_no_item * razao
                    seg = seg_no_item * razao
                    desp = desp_no_item * razao
                    icmsST = icmsST_no_item * razao
                    bc_icms_ST = base_icms_ST * razao
                    ipi = ipi_no_item * razao
                    bc_ipi = base_ipi * razao
                    self.item.append([desc, frete, seg, desp, icms_no_item, icmsST, bc_icms_ST, aliq_icms_ST, ipi, bc_ipi, aliq_ipi])
            else:
                self.item.append([desc_no_item, frete_no_item, seg_no_item, desp_no_item, icms_no_item, icmsST_no_item, base_icms_ST, aliq_icms_ST, ipi_no_item, base_ipi, aliq_ipi])
           
        elif self.ctrl_imposto == 5:
            valor_do_item, quant_do_item, vl_unit_item, desc_no_item, frete_no_item, seg_no_item, desp_no_item, icms_no_item, base_e_aliq_icms, icmsST_no_item, ipi_no_item, base_e_aliq_ipi = self.itens[self.i]
            base_icms, aliq_icms = base_e_aliq_icms
            base_ipi, aliq_ipi = base_e_aliq_ipi
            if self.item_fracionado != []:
                for razao in self.item_fracionado:
                    desc = desc_no_item * razao
                    frete = frete_no_item * razao
                    seg = seg_no_item * razao
                    desp = desp_no_item * razao
                    icms = icms_no_item * razao
                    bc_icms = base_icms * razao
                    ipi = ipi_no_item * razao
                    bc_ipi = base_ipi * razao
                    self.item.append([desc, frete, seg, desp, icms, bc_icms, aliq_icms, icmsST_no_item, ipi, bc_ipi, aliq_ipi])
            else:
                self.item.append([desc_no_item, frete_no_item, seg_no_item, desp_no_item, icms_no_item, base_icms, aliq_icms, icmsST_no_item, ipi_no_item, base_ipi, aliq_ipi])
           
        elif self.ctrl_imposto == 6:
            valor_do_item, quant_do_item, vl_unit_item, desc_no_item, frete_no_item, seg_no_item, desp_no_item, icms_no_item, base_e_aliq_icms, icmsST_no_item, base_e_aliq_ST, ipi_no_item = self.itens[self.i]
            base_icms, aliq_icms = base_e_aliq_icms
            base_icms_ST, aliq_icms_ST = base_e_aliq_ST
            if self.item_fracionado != []:
                for razao in self.item_fracionado:
                    desc = desc_no_item * razao
                    frete = frete_no_item * razao
                    seg = seg_no_item * razao
                    desp = desp_no_item * razao
                    icms = icms_no_item * razao
                    bc_icms = base_icms * razao
                    icmsST = icmsST_no_item * razao
                    bc_icms_ST = base_icms_ST * razao
                    self.item.append([desc, frete, seg, desp, icms, bc_icms, aliq_icms, icmsST, bc_icms_ST, aliq_icms_ST, ipi_no_item])
            else:
                self.item.append([desc_no_item, frete_no_item, seg_no_item, desp_no_item, icms_no_item, base_icms, aliq_icms, icmsST_no_item, base_icms_ST, aliq_icms_ST, ipi_no_item])
           
        elif self.ctrl_imposto == 7:
            valor_do_item, quant_do_item, vl_unit_item, desc_no_item, frete_no_item, seg_no_item, desp_no_item, icms_no_item, base_e_aliq_icms, icmsST_no_item, base_e_aliq_ST, ipi_no_item, base_e_aliq_ipi = self.itens[self.i]
            base_icms, aliq_icms = base_e_aliq_icms
            base_icms_ST, aliq_icms_ST = base_e_aliq_ST
            base_ipi, aliq_ipi = base_e_aliq_ipi
            if self.item_fracionado != []:
                for razao in self.item_fracionado:
                    desc = desc_no_item * razao
                    frete = frete_no_item * razao
                    seg = seg_no_item * razao
                    desp = desp_no_item * razao
                    icms = icms_no_item * razao
                    bc_icms = base_icms * razao
                    icmsST = icmsST_no_item * razao
                    bc_icms_ST = base_icms_ST * razao
                    ipi = ipi_no_item * razao
                    bc_ipi = base_ipi * razao
                    self.item.append([desc, frete, seg, desp, icms, bc_icms, aliq_icms, icmsST, bc_icms_ST, aliq_icms_ST, ipi, bc_ipi, aliq_ipi])
            else:
                self.item.append([desc_no_item, frete_no_item, seg_no_item, desp_no_item, icms_no_item, base_icms, aliq_icms, icmsST_no_item, base_icms_ST, aliq_icms_ST, ipi_no_item, base_ipi, aliq_ipi])
           
        return self.item
 
