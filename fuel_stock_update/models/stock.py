# -*- coding: utf-8 -*-
from odoo import api, fields, models
from collections import defaultdict

INDUSTRY_TYPE = [
    ('Aerolíneas','Aerolíneas'),
    ('Agencias Marítimas','Agencias Marítimas'),
    ('Alimentos','Alimentos'),
    ('Clientes','Clientes'),
    ('Combustibles','Combustibles'),
    ('Entretenimiento','Entretenimiento'),
    ('Ferreteros','Ferreteros'),
    ('Financiera','Financiera'),
    ('Finanzas / Seguros','Finanzas / Seguros'),
    ('Laboratorio','Laboratorio'),
    ('Mantenimiento','Mantenimiento'),
    ('Materia Prima','Materia Prima'),
    ('Otros Servicios','Otros Servicios'),
    ('Pozo','Pozo'),
    ('Recursos Humanos','Recursos Humanos'),
    ('Transporte','Transporte'),
    ('Vehículo','Vehículo'),
    ('Vessel','Vessel'),
]

class AforoTanques(models.Model):
    _name = 'aforo.tanques'

    name = fields.Char('Código Tanque')
    barcaza_tanque = fields.Char('Barcaza / Tanque')
    equivalente_barriles = fields.Float('Equivalente Barriles')
    equivalente_galones_1 = fields.Float('Equivalente Galones')
    company_id = fields.Many2one(
        'res.company',
        string='Compañías',
    )
    medida_tanque = fields.Integer(
        string='Medida Tanque',
    )
# class StockLocation(models.Model):
#     _inherit = 'stock.location'

#     vessel = fields.Boolean(string='Vessel')
#     responsable = fields.Boolean(string='Responsable')
#     placa = fields.Boolean(string='Placa')
#     conductor = fields.Boolean(string='Conductor')
#     hora_inicio = fields.Boolean(string='Hora inicio')
#     fecha_estimada_de_llegada = fields.Boolean(string='Fecha estimada de llegada')



class Employee(models.Model):
    _inherit = 'hr.employee'

    responsable = fields.Boolean(
        string='Responsable', default=False
    )

class ResPartnerIndustry(models.Model):
    _inherit = 'res.partner.industry'

    industry_type = fields.Selection(INDUSTRY_TYPE, string="Type")

class ResPartner(models.Model):
    _inherit = 'res.partner'

    placa_remolque = fields.Char('Placa remolque')
    conductor = fields.Char('Conductor')

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    vessel =  fields.Many2one(
        'res.partner',
        string='Vessel'
    )

class StockPickingType(models.Model):
    _inherit = 'stock.picking.type'

    operation_type_internal = fields.Selection([
        ('it_prog_carg','IT: Cargue en proveedor'),
        ('it_carg_tank','IT: Carrotanque a tanque'),
        ('it_tank_tank','IT: Tank > Tank')], string="Operation Type Internal")

class stockpicking(models.Model):
    _inherit = "stock.picking"

    # location_vessel = fields.Boolean(related='location_id.vessel')
    # location_responsable = fields.Boolean(related='location_id.responsable')
    # location_placa = fields.Boolean(related='location_id.placa')
    # location_conductor = fields.Boolean(related='location_id.conductor')
    # location_hora_inicio = fields.Boolean(related='location_id.hora_inicio')
    # location_fecha_estimada_de_llegada = fields.Boolean(related='location_id.fecha_estimada_de_llegada')
    operation_type_internal = fields.Selection(related='picking_type_id.operation_type_internal')
    vendedor_del_producto = fields.Many2one(
        'res.partner',
        string='Vendedor del producto'
    )
    origen = fields.Many2one('res.partner',string='Origen')
    empresa_transportadora = fields.Many2one('res.partner',string='Empresa Transportadora')
    placa = fields.Many2one('res.partner',string='Placa')

    responsable =  fields.Many2one(
        'hr.employee',
        string='Responsable',
    )
    vessel = fields.Char(related='sale_id.vessel.name')
    placa_remolque = fields.Char(related='placa.placa_remolque')
    conductor_2 = fields.Char(related='placa.conductor')
    cdula_conductor = fields.Char(related='placa.vat')
    sellos_instalados = fields.Char('Sellos instalados')
    para_relacionar = fields.Char(related='product_id.name')
    tanque_de_origen =fields.Char()
    medida_inicial =fields.Many2one('aforo.tanques')
    equivalente_galones_medida_inicial =fields.Float(related='medida_inicial.equivalente_galones_1')
    medida_final_tanque = fields.Many2one(
        'aforo.tanques',
        string='Medida final tanque',
    )
    equivalente_galones_medida_final =fields.Float('medida_final_tanque.equivalente_galones_1')
    galones_brutos_1 =fields.Float(compute='compute_galones_brutos', store=True)
    galones_netos_2 =fields.Float(compute='compute_galones_brutos', store=True)
    barriles_brutos =fields.Float(compute='compute_galones_brutos', store=True)
    barriles_netos =fields.Float(compute='compute_galones_brutos', store=True)
    ton_metricas =fields.Float(compute='compute_galones_brutos', store=True)
    temp_f =fields.Integer()
    temp_f_1 =fields.Integer()
    grados_api_lab =fields.Float()
    factor_pv = fields.Float(compute='compute_factor_pv', store=True)
    factor =fields.Float(compute='compute_factor', store=True)
    hora_inicio = fields.Float()
    hora_final = fields.Float()
    fecha_estimada_de_llegada = fields.Date()
    peso_asfalto_kg = fields.Float()
    vol_asfalto_gal = fields.Float(compute='compute_volume_asfalto', store=True)
    barriles_asfalto = fields.Float(compute='compute_barriles_asfalto', store=True)
    tanque_de_destino = fields.Char()
    medida_inicial_tanque = fields.Many2one('aforo.tanques')
    related_field_bt8DU = fields.Float(related='medida_inicial_tanque.equivalente_galones_1')
    medida_final_tanque_1 = fields.Many2one('aforo.tanques')
    equivalente_galones_medida_final_1 = fields.Float(related='medida_final_tanque_1.equivalente_galones_1')
    galones_brutos_3 = fields.Float(compute='compute_galones_brutos_destino', store=True)
    galones_netos_3 = fields.Float(compute='compute_galones_brutos_destino', store=True)
    barriles_brutos_1 = fields.Float(compute='compute_galones_brutos_destino', store=True)
    barriles_netos_1 = fields.Float(compute='compute_galones_brutos_destino', store=True)
    ton_metricas_1 = fields.Float(compute='compute_galones_brutos_destino', store=True)
    grados_api_lab_1 = fields.Float(string="Grados API (lab)")
    factor_vp_1 = fields.Float(compute='compute_factor_vp_1', store=True)
    factor_pv_2 = fields.Float(compute='compute_factor_pv_2', store=True)

    peso_inicial = fields.Integer()
    peso_final = fields.Integer()
    peso_neto = fields.Integer(compute='diff_peso', store=True)
    galones_brutos = fields.Float(compute='calculate_galones_brutos', store=True)
    galones_netos = fields.Float(compute='calculate_galones_brutos', store=True)
    barriles = fields.Float(compute='calculate_galones_brutos', store=True)
    toneladas_netas_descargue = fields.Float(compute='calculate_galones_brutos', store=True)

    tomo_muestra = fields.Boolean()
    realiza_analisis_externo = fields.Boolean()
    nombre_laboratorio = fields.Many2one('res.partner')

    guia_no = fields.Char()
    grados_api = fields.Float()
    volmen_observado_gov = fields.Float()
    volumen_corregido_gsv = fields.Float()
    volumen_neto_sin_agua_nsv = fields.Float()
    bsw_2 = fields.Float()
    ctl_ctq = fields.Float()
    temperatura_tanque_f = fields.Float()
    porcentaje_s = fields.Float()

    aforo_agua = fields.Many2one('aforo.tanques')
    equivalente_barriles_1 = fields.Float(related='aforo_agua.equivalente_barriles')
    api_mne_tnk_descarga = fields.Float()
    temp_mne_tnk_descarga = fields.Float()
    api_correg_mne_tnk_decarga = fields.Float()
    azufre_mne_tnk_descarga = fields.Float()
    temp_del_tnk_descarga_mne = fields.Float()
    temp_ambiente_mne_descarga = fields.Float()
    sw_mne_tnk_descarga = fields.Float()
    flash_p_mne_tnk_descarga = fields.Float()
    viscosidad_mne_tnk_descarga = fields.Float()
    stock_water_bls = fields.Float()
    gov_tanque = fields.Float()
    ctl = fields.Float()
    ctsh = fields.Float(compute='compute_ctsh', store=True)
    gsv_tanque = fields.Float()
    factor_sw_tanque_1 = fields.Float()
    nsv_tanque = fields.Float()

    initial_qty = fields.Float(default=10)
    final_qty = fields.Float(default=9)

    @api.depends('temp_del_tnk_descarga_mne', 'temp_ambiente_mne_descarga')
    def compute_ctsh(self):
        for record in self:
            resultado = (1+0.0000124*(((record["temp_del_tnk_descarga_mne"]*7+record["temp_ambiente_mne_descarga"])/8)-82) + 0.0000062**2*(((record["temp_ambiente_mne_descarga"]*7+record ["temp_ambiente_mne_descarga"])/8)-82)**2)
            record ["ctsh"]=resultado



    @api.depends('galones_netos','factor','factor_pv', 'peso_neto')
    def calculate_galones_brutos(self):
        for record in self:
            record['galones_brutos'] = record.galones_netos / record.factor
            record['galones_netos'] = record.peso_neto / record.factor_pv
            record['barriles'] = record.galones_netos / 42
            record['toneladas_netas_descargue'] = record.galones_netos * record.factor_pv / 1000


    @api.depends('peso_inicial','peso_final')
    def diff_peso(self):
        for record in self:
            record['peso_neto'] = record.peso_inicial - record.peso_final

    @api.depends('grados_api_lab_1')
    def compute_factor_vp_1(self):
        for record in self:
            resultado = 1/((0.245985788480079+(0.00187273461953527*record["grados_api_lab_1"]))+((1.644783638504/100000000)*(record["grados_api_lab_1"]**2)))
            record ["factor_vp_1"]=resultado




    @api.depends('grados_api_lab')
    def compute_factor_pv(self):
        for record in self:
            resultado = 1/((0.245985788480079+(0.00187273461953527*record["grados_api_lab"]))+((1.644783638504/100000000)*(record["grados_api_lab"]**2)))
            record ["factor_pv"] = resultado

    @api.depends('grados_api_lab_1', 'factor_pv_2', 'temp_f_1')
    def compute_factor_pv_2(self):
        for record in self:
            resultado = 1.02028515096129+(0.000194498131055654*record["grados_api_lab_1"])
            resultado += -0.000335112618276416*record["temp_f_1"]
            resultado += 3.35554549752086*(0.0000001)*(record["grados_api_lab_1"]**2)
            resultado += -5.4984909894376*0.00000001*(record["temp_f_1"]**2)
            resultado += -3.20176029557111*(0.000001)*record["grados_api_lab_1"]*record["temp_f_1"]
            resultado += 1.10831738046135*(0.0000000001)*(record["grados_api_lab_1"]**3)
            resultado += 7.58210695329154*(0.00000000001)*(record["temp_f_1"]**3)
            resultado += -6.39779900461012*(0.0000000001)*(record["temp_f_1"])*(record["temp_f_1"]**2)
            resultado += -5.50364339588239*(0.000000001)*(record["grados_api_lab_1"]**2)*record["temp_f_1"]
            record ["factor_pv_2"]=resultado

    @api.depends('grados_api_lab', 'temp_f')
    def compute_factor(self):
        for record in self:
            resultado = 1.02028515096129+(0.000194498131055654*record["grados_api_lab"])
            resultado += -0.000335112618276416*record["temp_f"]
            resultado += 3.35554549752086*(0.0000001)*(record["grados_api_lab"]**2)
            resultado += -5.4984909894376*0.00000001*(record["temp_f"]**2)
            resultado += -3.20176029557111*(0.000001)*record["grados_api_lab"]*record["temp_f"]
            resultado += 1.10831738046135*(0.0000000001)*(record["grados_api_lab"]**3)
            resultado += 7.58210695329154*(0.00000000001)*(record["temp_f"]**3)
            resultado += -6.39779900461012*(0.0000000001)*(record["temp_f"])*(record["temp_f"]**2)
            resultado += -5.50364339588239*(0.000000001)*(record["grados_api_lab"]**2)*record["temp_f"]
            record ["factor"] = resultado


    @api.depends('equivalente_galones_medida_final_1', 'related_field_bt8DU','factor_pv_2','factor_vp_1')
    def compute_galones_brutos_destino(self):
        for record in self:
            record['galones_brutos_3'] = record.equivalente_galones_medida_final_1 - record.related_field_bt8DU
            record['galones_netos_3'] = record.galones_brutos_3 * record.factor_pv_2
            record['barriles_brutos_1'] = record.galones_brutos_3 / 42
            record['barriles_netos_1'] = record.galones_netos_3 / 42
            record['ton_metricas_1'] = record.galones_netos_3 * record.factor_vp_1 / 1000



    


    @api.depends('equivalente_galones_medida_inicial', 'equivalente_galones_medida_final','factor','factor_pv')
    def compute_galones_brutos(self):
        for record in self:
            record['galones_brutos_1'] = record.equivalente_galones_medida_final - record.equivalente_galones_medida_inicial
            record['galones_netos_2'] = record.galones_brutos_1 * record.factor
            record['barriles_brutos'] = record.galones_brutos_1 / 42
            record['barriles_netos'] = record.galones_netos_2 / 42
            record['ton_metricas'] = record.galones_netos_2 * record.factor_pv / 1000

    @api.depends('peso_asfalto_kg','factor_pv')
    def compute_volume_asfalto(self):
        for record in self:
            record['vol_asfalto_gal'] = record.peso_asfalto_kg / record.factor_pv
            record['barriles_asfalto'] = record.vol_asfalto_gal / 42

    def update_initial_final_qty(self):
        self.move_ids_without_package.update({
            'product_uom_qty': self.initial_qty,
            'quantity_done': self.final_qty,
            'variance': abs(self.initial_qty - self.final_qty),
            })
        return True




class StockMove(models.Model):
    _inherit = 'stock.move'

    variance = fields.Float('Var(Barriles)')
    metric_tonnes = fields.Float('Ton Métricas')
    gallons = fields.Float('Galones')
