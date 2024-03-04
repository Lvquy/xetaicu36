# -*- coding: utf-8 -*-
from odoo import fields, models, api
from datetime import date


class KhachHang(models.Model):
    _name = 'partner.xetaicu'
    _description = 'Khach hang Xe tai cu'

    name = fields.Char(string='Tên')
    add = fields.Text(string='Địa chỉ')
    phone = fields.Char(string='Số ĐT')
    img_avatar = fields.Image(string='Ảnh khách')
    img_can_cuoc_f = fields.Image(string='Ảnh căn cước trước')
    img_can_cuoc_b = fields.Image(string='Ảnh căn cước sau')
    img_giay_ket_hon = fields.Image(string='Giấy kết hôn')
    note = fields.Text(string='Ghi chú')
    log_muaban = fields.One2many('log.muaban','ref_partner', string='Lịch sử mua bán', readonly=True)

class Logmuaban(models.Model):
    _name = 'log.muaban'
    _description = 'Lịch sử mua bán'
    _rec_name = 'name'

    name = fields.Char(string='Loại giao dịch', readonly=True)
    ngay_giao_dich = fields.Date(string='Ngày giao dịch', readonly=True)
    chung_tu_mua = fields.Many2one('muaxe.xetaicu', string='Chứng từ mua', readonly=True)
    chung_tu_ban = fields.Many2one('banxe.xetaicu', string='Chứng từ bán', readonly=True)
    ref_partner = fields.Many2one('partner.xetaicu',string='Khách hàng', readonly=True)


class Xetai(models.Model):
    _name = 'xe.xetaicu'
    _description = 'Xe tai cu'

    dang_ban = fields.Boolean(string='Đăng bán trên web', default=False, readonly=True)
    name = fields.Char(string='Tên xe')
    mau_son = fields.Char(string='Màu sơn')
    nam_sx = fields.Integer(string='Năm sản xuất')
    kich_thuoc = fields.Char(string='Kích thước(D*R*C)')
    tai_trong = fields.Char(string='Tải trọng')
    ten_dong_co = fields.Char(string='Tên động cơ')
    dung_tich = fields.Integer(string='Dung tích')
    dang_kiem_toi = fields.Char(string='Đăng kiểm tới')
    xem_xe_tai = fields.Char(string='Xem xe tại')
    hang_xe = fields.Selection([
        ('0', 'Chọn hãng xe'),
        ('hn', 'HINO'),
        ('is', 'ISUZU'),
        ('hd', 'HYNDAI'),
        ('fu', 'FUSO'),
        ('da', 'DAEWOO'),
        ('th', 'THACO'),
        ('ja', 'JAC'),
        ('db', 'DONGBEN'),
        ('ka', 'KIA'),
        ('bg', 'BONGO'),
        ('su', 'SUZUKI'),
        ('tm', 'TMT CỬU LONG')], default='0',
        string='Hãng xe')
    img_xe = fields.Image(string='Hình xe')
    img_xe_1 = fields.Image(string='Hình xe 1')
    img_xe_2 = fields.Image(string='Hình xe 2')
    img_xe_3 = fields.Image(string='Hình xe 3')
    img_xe_4 = fields.Image(string='Hình xe 4')
    bien_ks = fields.Char(string='Biển số xe')
    dang_ky = fields.Image(string='Ảnh đăng ký')
    dang_kiem = fields.Image(string='Ảnh đăng kiểm')
    status = fields.Selection([('0', 'Mới tạo'), ('kho', 'Trong kho'), ('ban', 'Đã bán')], default='0',
                              string='Tình trạng xe')
    note = fields.Text(string='Ghi chú nội bộ')
    ngay_mua = fields.Date(string='Ngày mua', readonly=True)
    ngay_ban = fields.Date(string='Ngày bán', readonly=True)
    don_mua = fields.Many2one('muaxe.xetaicu', string='Đơn mua', readonly=True)
    gia_mua = fields.Integer(string='Giá mua', readonly=True)
    don_ban = fields.Many2one('banxe.xetaicu', string='Đơn bán', readonly=True)
    gia_ban = fields.Integer(string='Giá bán', readonly=True)
    loi = fields.Integer(string='Lời', readonly=True)
    gia_dang_ban = fields.Char(string='Giá đăng bán trên website')
    mua_tu = fields.Many2one('partner.xetaicu', string='Mua từ đâu', readonly=True)
    ban_cho = fields.Many2one('partner.xetaicu', string='Bán cho ai', readonly=True)
    chiphi_suachua = fields.Integer(string='Chi phí sửa chữa')

    def change_dang_ban(self):
        for rec in self:
            if rec.status == 'kho':
                rec.dang_ban = not rec.dang_ban
            else: rec.dang_ban = False
    def change_status_kho(self):
        for rec in self:
            rec.status = 'kho'
    def change_status_ban(self):
        for rec in self:
            rec.status = 'ban'

    def change_status_0(self):
        for rec in self:
            rec.status = '0'

    @api.onchange('gia_mua','gia_ban','chiphi_suachua')
    def compute_loi(self):
        for rec in self:
            rec.loi  = rec.gia_ban - rec.gia_mua - rec.chiphi_suachua

    def name_get(self):
        result = []
        for record in self:
            name = record.name
            if record.name:
                name = f"{name} - {record.bien_ks}"
            result.append((record.id, name))
        return result


class Muaxe(models.Model):
    _name = 'muaxe.xetaicu'
    _description = 'Mua  Xe tai cu'
    _rec_name = 'name'

    name = fields.Char(string='Tên đơn mua xe')
    ngay_mua = fields.Date(string='Ngày mua', required=True, default=date.today())
    nguoi_ban = fields.Many2one('partner.xetaicu', string='Người bán')
    giay_mua_ban_img = fields.Image(string='Giấy mua bán')
    giay_mua_ban_congchung_img = fields.Image(string='Giấy mua bán công chứng')
    xe = fields.Many2one('xe.xetaicu', string='Xe')
    status = fields.Selection([('0', 'Nháp'), ('1', 'Đã xác nhận')], string='Trạng thái')
    note = fields.Text(string='Ghi chú')
    gia = fields.Integer(string='Giá')

    def confirm_don(self):
        for rec in self:
            rec.status = '1'
            rec.nguoi_ban.log_muaban = [(0,0,{
                'name':'Khách bán xe - '+ str(rec.xe.bien_ks),
                'ngay_giao_dich':rec.ngay_mua,
                'chung_tu_mua':rec.id,
            })]
            if rec.xe:
                rec.xe.status = 'kho'
                rec.xe.ngay_mua = rec.ngay_mua
                rec.xe.don_mua = rec.id
                rec.xe.gia_mua = rec.gia
                rec.xe.loi = rec.xe.gia_ban - rec.xe.gia_mua - rec.chiphi_suachua
                rec.xe.mua_tu = rec.nguoi_ban

    def unconfirm_don(self):
        for rec in self:
            rec.status = '0'
            if rec.xe:
                rec.xe.compute_loi()
                rec.xe.status = '0'
                rec.xe.ngay_mua = False
                rec.xe.don_mua = False
                rec.xe.loi = rec.xe.gia_ban - rec.xe.gia_mua - rec.chiphi_suachua
                rec.xe.mua_tu = False


class Banxe(models.Model):
    _name = 'banxe.xetaicu'
    _description = 'Ban Xe tai cu'
    _rec_name = 'name'

    ngay_ban = fields.Date(string='Ngày bán')
    nguoi_mua = fields.Many2one('partner.xetaicu', string='Người mua')
    giay_mua_ban_img = fields.Image(string='Giấy mua bán')
    giay_mua_ban_congchung_img = fields.Image(string='Giấy mua bán công chứng')
    xe = fields.Many2one('xe.xetaicu', string='Xe')
    note = fields.Text(string='Ghi chú')
    status = fields.Selection([('0', 'Nháp'), ('1', 'Đã xác nhận')], string='Trạng thái')
    name = fields.Char(string='Tên đơn bán xe')
    gia = fields.Integer(string='Giá')

    def confirm_don(self):
        for rec in self:
            rec.status = '1'
            rec.nguoi_mua.log_muaban = [(0, 0, {
                'name': 'Khách mua xe - ' + str(rec.xe.bien_ks),
                'ngay_giao_dich': rec.ngay_ban,
                'chung_tu_ban': rec.id,
            })]
            if rec.xe:

                rec.xe.status = 'ban'
                rec.xe.ngay_ban = rec.ngay_ban
                rec.xe.don_ban = rec.id
                rec.xe.gia_ban = rec.gia
                rec.xe.loi = rec.xe.gia_ban - rec.xe.gia_mua - rec.chiphi_suachua
                rec.xe.ban_cho = rec.nguoi_mua
                rec.xe.dang_ban = False

    def unconfirm_don(self):
        for rec in self:
            rec.status = '0'
            if rec.xe:
                rec.xe.status = 'kho'
                rec.xe.ngay_ban = False
                rec.xe.don_ban = False
                rec.xe.gia_ban = 0
                rec.xe.loi = rec.xe.gia_ban - rec.xe.gia_mua - rec.chiphi_suachua
                rec.xe.ban_cho = False
