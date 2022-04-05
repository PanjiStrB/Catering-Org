from odoo import api, fields, models


class Jnsminuman(models.Model):
    _name = 'catering.jnsminuman'
    _description = 'Jenis Minuman'

    name = fields.Char(string='Name')
    deskripsi = fields.Char(string='Deskripsi Jenis Minuman')
    stok = fields.Integer(string='Stok Minuman')
    harga = fields.Integer(string='Harga Minuman')
    image = fields.Binary(
        string='image',
    )
    