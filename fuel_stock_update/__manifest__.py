# -*- coding: utf-8 -*-
{
    'name': 'Fuel Stock Update',
    'version': '14.0',
    'author': 'Preciseways IT Solutions',
    "category": "Warehouse",
    "depends": ['sale_stock'],
    'summary': 'Sale multi warehouse | Different Warehouse on sale orderline | Sale Order multiple warehouse | Deliver product from multiple warehouses set warehouse on sale order line ',
    'description': """Sale Order Picking Warehouse Multiple Warehouse on sale order line ship from multiple warehouse outgoing shipment
    """,
    'data': [
    'security/ir.model.access.csv',
    'views/aforo_tanques_view.xml',
    'views/stock_view.xml'
    ],
    "images":[],
    'application': True,
    'installable': True,
}
