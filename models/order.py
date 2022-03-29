from odoo import api, fields, models
from odoo.exceptions import ValidationError


class Order(models.Model):
    _name = 'catering.order'
    _description = 'New Description'

    orderjnscateringdetail_ids = fields.One2many(
        comodel_name='catering.orderjnscateringdetail', 
        inverse_name='order_id', 
        string='Order Jenis Catering')
    
    orderjnsmakanandetail_ids = fields.One2many(
        comodel_name='catering.orderjnsmakanandetail', 
        inverse_name='orderk_id', 
        string='Order Jenis Makanan')

    orderjnsminumandetail_ids = fields.One2many(
        comodel_name='catering.orderjnsminumandetail', 
        inverse_name='orderkm_id', 
        string='Order Jenis Minuman')
    
    name = fields.Char(string='Kode Order', required=True)
    pemesan = fields.Many2one(
        comodel_name='res.partner', 
        string='Pemesan', 
        domain=[('is_customernya','=', True)],store=True)
    tanggal_pesan = fields.Datetime('Tanggal Pemesanan',default=fields.Datetime.now())
    tanggal_pengiriman = fields.Date(string='Tanggal Pengiriman', default=fields.Date.today())
    total = fields.Integer(compute='_compute_total', string='Total', store=True)
    sudah_bayar = fields.Boolean(string='Sudah Dibayarkan', default=False)
    tipecatering = fields.Selection(string='Tipe Catering', selection=[('acarabesar', 'Acara Besar'), ('box', 'Box'),])
    
    @api.depends('orderjnscateringdetail_ids')
    def _compute_total(self):
        for record in self:
            a = sum(self.env['catering.orderjnscateringdetail'].search([('order_id', '=', record.id)]).mapped('harga'))
            b = sum(self.env['catering.orderjnsmakanandetail'].search([('orderk_id', '=', record.id)]).mapped('harga'))
            c = sum(self.env['catering.orderjnsminumandetail'].search([('orderkm_id', '=', record.id)]).mapped('harga'))            
            record.total = a + b + c
    
    
        
class OrderJnsCateringDetail(models.Model):
    _name = 'catering.orderjnscateringdetail'
    _description = 'New Description'

    order_id = fields.Many2one(comodel_name='catering.order', string='Order')
    jnscatering_id = fields.Many2one(comodel_name='catering.jnscatering', string='Jenis Catering')   
    
         
    name = fields.Char(string='Name')
    deskripsi = fields.Char(compute='_compute_deskripsi', string='Deskripsi')
    harga = fields.Integer(compute='_compute_harga', string='Harga')
    qty = fields.Integer(string='Quantity')
    harga_satuan = fields.Integer(compute='_compute_harga_satuan', string='Harga Satuan')
    
    @api.depends('jnscatering_id')
    def _compute_harga_satuan(self):
        for record in self:
            record.harga_satuan = record.jnscatering_id.harga

    @api.depends('jnscatering_id')
    def _compute_deskripsi(self):
        for record in self:
            record.deskripsi = record.jnscatering_id.deskripsi
    
    @api.depends('qty','harga_satuan')
    def _compute_harga(self):
        for record in self:
           record.harga = record.harga_satuan * record.qty
                 
            
class OrderJnsMakananDetail(models.Model):
    _name = 'catering.orderjnsmakanandetail'
    _description = 'New Description'
    
    orderk_id = fields.Many2one(comodel_name='catering.order', string='Order Makanan')
    deskripsi = fields.Char(compute='_compute_deskripsi', string='Deskripsi')
    jnsmakanan_id = fields.Many2one(
        comodel_name='catering.jnsmakanan', 
        string='Jenis Makanan',
        domain=[('stok','>','50')])
    
    name = fields.Char(string='Name')
    harga_satuan = fields.Integer(compute='_compute_harga_satuan', string='Harga Satuan')
    
    @api.depends('jnsmakanan_id')
    def _compute_deskripsi(self):
        for record in self:
            record.deskripsi = record.jnsmakanan_id.deskripsi

    @api.depends('jnsmakanan_id')
    def _compute_harga_satuan(self):
        for record in self:
            record.harga_satuan = record.jnsmakanan_id.harga
    
    qty = fields.Integer(string='Quantity')
    
    @api.constrains('qty')
    def _check_stok(self):
        for record in self:
            bahan = self.env['catering.jnsmakanan'].search([('stok', '<',record.qty),('id', '=',record.id)])
            if bahan:
                raise ValidationError("Stok Makanan yang dipilih tidak cukup")
    
    harga = fields.Integer(compute='_compute_harga', string='harga')
    
    @api.depends('harga_satuan','qty')
    def _compute_harga(self):
        for record in self:
               record.harga = record.harga_satuan * record.qty
               
    
    @api.model
    def create(self,vals):
        record = super(OrderJnsMakananDetail, self).create(vals) 
        if record.qty:
            self.env['catering.jnsmakanan'].search([('id','=',record.jnsmakanan_id.id)]).write({'stok':record.jnsmakanan_id.stok-record.qty})
            return record
    
class OrderJnsMinumanDetail(models.Model):
    _name = 'catering.orderjnsminumandetail'
    _description = 'New Description'
    
    orderkm_id = fields.Many2one(comodel_name='catering.order', string='Order Minuman')
    deskripsi = fields.Char(compute='_compute_deskripsi', string='Deskripsi') 
    jnsminuman_id = fields.Many2one(
        comodel_name='catering.jnsminuman', 
        string='Jenis Minuman',
        domain=[('stok','>','50')])
    
    name = fields.Char(string='Name')
    harga_satuan = fields.Integer(compute='_compute_harga_satuan', string='Harga Satuan')
    
    @api.depends('jnsminuman_id')
    def _compute_harga_satuan(self):
        for record in self:
            record.harga_satuan = record.jnsminuman_id.harga
    
    qty = fields.Integer(string='Quantity')
    
    @api.depends('jnsminuman_id')
    def _compute_deskripsi(self):
        for record in self:
            record.deskripsi = record.jnsminuman_id.deskripsi

    @api.constrains('qty')
    def _check_stok(self):
        for record in self:
            bahan = self.env['catering.jnsminuman'].search([('stok', '<',record.qty),('id', '=',record.id)])
            if bahan:
                raise ValidationError("Stok Minuman yang dipilih tidak cukup")
    
    harga = fields.Integer(compute='_compute_harga', string='Harga')
    
    @api.depends('harga_satuan','qty')
    def _compute_harga(self):
        for record in self:
               record.harga = record.harga_satuan * record.qty
               
    @api.model
    def create(self,vals):
        record = super(OrderJnsMinumanDetail, self).create(vals) 
        if record.qty:
            self.env['catering.jnsminuman'].search([('id','=',record.jnsminuman_id.id)]).write({'stok':record.jnsminuman_id.stok-record.qty})
            return record