from odoo import api, fields, models


class Jnscatering(models.Model):
    _name = 'catering.jnscatering'
    _description = 'Jenis Catering'

    name = fields.Char(string='Name')
    deskripsi = fields.Char(string='Deskripsi Jenis Catering')
    harga = fields.Integer(string='Harga')
    
    
