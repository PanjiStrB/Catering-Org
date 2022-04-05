from odoo import api, fields, models


class Jnsmakanan(models.Model):
    _name = 'catering.jnsmakanan'
    _description = 'Jenis Makanan Yang Tersedia'

    name = fields.Char(string='Name')
    tipe = fields.Selection(string='Tipe Makanan', selection=[('sunda','Sunda'), ('jawatengah','Jawa Tengah'), ('aceh','Aceh'), ('minang','Minang'), ('bali','Bali'), ('betawi','Betawi'), ('itali','Itali'), ('perancis','Perancis'), ('inggris','Inggris'), ('jepang','Jepang'), ('cina','Cina'), ('korea','Korea')])
    deskripsi = fields.Char(string='Deskripsi Jenis Makanan')
    stok = fields.Integer(string='Stok Makanan')
    harga = fields.Integer(string='Harga Makanan')
    image = fields.Binary(
        string='image',
    )