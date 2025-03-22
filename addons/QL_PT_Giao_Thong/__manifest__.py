# -*- coding: utf-8 -*-
{
    'name': "Quản Lý Phương Tiện",

    'summary': """
        Quản lý phương tiện giao thông, đăng kiểm và bảo dưỡng""",

    'description': """
        Long description of module's purpose
    """,

    'author': "My Company",
    'website': "http://www.yourcompany.com",
    'images': ['static/description/logo.png'],
    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/15.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',
    
    # any module necessary for this one to work correctly
    'depends': ['base'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/phuong_tien.xml',
        'views/tai_xe.xml',
        'views/chuyen_di.xml',
        'views/bao_tri_xe.xml',
        'views/nhien_lieu.xml',
        'views/vi_tri.xml',
        'views/don_dang_ky.xml',
        'views/lich_su_xe.xml',
        'views/khach_thue.xml',
        'views/don_thue_xe.xml',
        'views/loai_xe.xml',
        'views/thong_ke.xml',
        'views/menu.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
    'assets': {
    'web.assets_backend': [
        'QL_PT_Giao_Thong/static/src/js/vehicle_chart.js',
        'https://cdnjs.cloudflare.com/ajax/libs/Chart.js/4.4.0/chart.umd.min.js',  # Load Chart.js từ CDN
    ],
},


}
