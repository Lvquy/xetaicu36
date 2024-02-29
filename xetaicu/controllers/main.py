# -*- coding: utf-8 -*-
from odoo import http
from odoo.http import request


class Book(http.Controller):

    @http.route(['/list_xe','/list_xe/page/<int:page>'], auth='public', website=True)
    def list_xe(self, page=0, search='', **kw):
        uid = request.session['uid']
        USER = request.env['res.users'].sudo()
        user = USER.search([('id', '=', uid)])

        breadcrumb = [{'name': 'Trang chủ', 'url': '/'},
                      {'name': 'Trang của tôi', 'url': '/list_xe'}]
        domain = [('dang_ban','=',True)]
        XETAI = request.env['xe.xetaicu'].sudo()
        total_xe = XETAI.search_count(domain)
        per_page = 12
        pager = request.website.pager(url='/list_xe', total=total_xe, page=page, step=per_page, scope=3,
                                      url_args=None)
        XE = XETAI.search(domain, limit=per_page, offset=pager['offset'])
        company = request.env['res.company'].sudo().search([],limit=1)
        values = {
            'XETAI': XE,
            'pager': pager,
            'breadcrumb': breadcrumb,
            'company':company
        }
        return request.render('xetaicu.list_xe', values)

    @http.route(['/list_xe/details/<model("xe.xetaicu"):xe>'], auth='public', website=True, csrf=False)
    def xetai(self, xe):
        company = request.env['res.company'].sudo().search([], limit=1)
        values = {
            'xe': xe,
            'company': company
        }
        return request.render('xetaicu.xe_details', values)
