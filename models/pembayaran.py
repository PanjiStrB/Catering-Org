from odoo import api, fields, models


class Pembayaran(models.Model):
    _name = 'catering.pembayaran'
    _description = 'Pembayaran Barang Sewa'

    name = fields.Char(compute='_compute_nama_penyewa', string='Nama Pemesan')
    order_id = fields.Many2one(comodel_name='catering.order', string='No. Order')
    
    @api.depends('order_id')
    def _compute_nama_penyewa(self):
        for record in self:
            record.name = self.env['catering.order'].search([('id', '=', record.order_id.id)]).mapped('pemesan').name
    
    tgl_pembayaran = fields.Date(string='', default=fields.Date.today())
    
    tagihan = fields.Integer(compute='_compute_tagihan', string='Tagihan')
    
    @api.depends('order_id')
    def _compute_tagihan(self):
        for record in self:
            record.tagihan = record.order_id.total            
   
        
    @api.model
    def create(self,vals):
        record = super(Pembayaran, self).create(vals) 
        if record.tgl_pembayaran:
            self.env['catering.order'].search([('id','=',record.order_id.id)]).write({'sudah_bayar':True}) 
            self.env['catering.akunting'].create({'kredit' : record.tagihan, 'name':record.name})          
            return record

    def unlink(self):
        for wiku in self:
            self.env['catering.order'].search([('id','=',wiku.order_id.id)]).write({'sudah_bayar':False})
        record = super(Pembayaran, self).unlink()
   
        
            