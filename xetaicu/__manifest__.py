# -*- coding: utf-8 -*-
{
    'name': 'XeTaiCu',
    'version': '1',
    'category': 'Tools',
    'summary': '#',
    'author': 'Lv Quy',
    'company': 'itricks',
    'website': 'https://xetaicu36.com',
    'depends': ['base_setup', 'website'],
    'data': [
        # security
        'security/ir.model.access.csv',
        # views
        # 'views/custom_footer.xml',
        'views/partner_xetaicu.xml',
        'views/purchase.xml',
        'views/sale.xml',
        'views/xe_xetaicu.xml',

    ],

    'assets': {
        'web.assets_backend': ['xetaicu/static/src/css/style.css'],
    },
    'installable': True,
    'application': True,
    'auto_install': False,
    'license': 'AGPL-3',
}
