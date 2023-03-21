# -*- coding: utf-8 -*-

import datetime
from lxml import etree
from dateutil.relativedelta import relativedelta
import re
import logging
from pytz import timezone

import requests

from odoo import api, fields, models
from odoo.addons.web.controllers.main import xml2json_from_elementtree
from odoo.exceptions import UserError
from odoo.tools.translate import _
from odoo.tools import DEFAULT_SERVER_DATE_FORMAT

import json


class ResCompany(models.Model):
    _inherit = 'res.company'

    currency_provider = fields.Selection(selection_add=[('col', 'Bank Of Colombia')])


    def _parse_col_data(self, available_currencies):
        url = 'https://www.superfinanciera.gov.co/SuperfinancieraWebServiceTRM/TCRMServicesWebService/TCRMServicesWebService?wsdl'
        template = """<Envelope xmlns=\"http://schemas.xmlsoap.org/soap/envelope/\">
            <Body>
                <queryTCRM xmlns=\"http://action.trm.services.generic.action.superfinanciera.nexura.sc.com.co/\">
                <tcrmQueryAssociatedDate xmlns=\"'${data}'"></tcrmQueryAssociatedDate>
                </queryTCRM>
            </Body>
        </Envelope>"""

        params = fields.Date.today().strftime(DEFAULT_SERVER_DATE_FORMAT)
        soap_env = template.format(data=params)
        soap_xml = requests.post(url, data=soap_env, timeout=20)
        if soap_xml.status_code == 500:
            raise UserError(_("Server error"))
        xmlstr = etree.fromstring(soap_xml.text)
        data = xml2json_from_elementtree(xmlstr)
        available_currency_names = available_currencies.mapped('name')
        rslt = {}
        if data.get('children'):
            rates_node = data['children'][0]['children'][0]['children'][0]['children'][4]['children'][0]
            rate = float(rates_node)
            if 'COP' in available_currency_names:
                rslt['COP'] = (rate, fields.Date.today())

            if 'USD' in available_currency_names:
                rslt['USD'] = (1.0, fields.Date.today())
        return rslt