# -*- coding: utf-8 -*-
{
    'name': "MRP Control QTY Production by Employee",

    'summary': """
        Este modulo es para controlar las cantidades para cuando necesitas saber cuantos items manufacturaron tus empleados.""",

    'description': """
        Long description of module's purpose
    """,

    'author': "Wildy Estephan",
    'website': "http://www.wildyestephan.com",

    'category': 'Manufacturing',
    'version': '0.1',
    'price': 5.00,
    'currency': 'USD',
    'license': 'LGPL-3',

    # any module necessary for this one to work correctly
    'depends': ['mrp', 'hr'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/views.xml',
    ],
}
