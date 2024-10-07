#!/usr/bin/env python

import argparse
from pyunifi.controller import Controller
from yattag import Doc
import os

parser = argparse.ArgumentParser()
parser.add_argument('-c', '--controller', default='unifi', help='the controller address (default "unifi")')
parser.add_argument('-u', '--username', default='admin', help='the controller username (default("admin")')
parser.add_argument('-p', '--password', default='', help='the controller password')
parser.add_argument('-b', '--port', default='8443', help='the controller port (default "8443")')
parser.add_argument('-v', '--version', default='v5', help='the controller base version (default "v5")')
parser.add_argument('-s', '--siteid', default='default', help='the site ID, UniFi >=3.x only (default "default")')
parser.add_argument('-V', '--no-ssl-verify', default='False', action='store_true', help='Don\'t verify ssl certificates')
parser.add_argument('-C', '--certificate', default='', help='verify with ssl certificate pem file')
args = parser.parse_args()

ssl_verify = (not args.no_ssl_verify)

if ssl_verify and len(args.certificate) > 0:
        ssl_verify = args.certificate

c = Controller(args.controller, args.username, args.password, args.port, args.version, args.siteid, ssl_verify=ssl_verify)

def format_code(string):
        length_string = len(string)
        first_length = round(length_string / 2)
        first_half = string[0:first_length].lower()
        second_half = string[first_length:].upper()
        return first_half + '-' + second_half

doc, tag, text = Doc().tagtext()

doc.asis('<!DOCTYPE html>')
with tag('html'):
    with tag('head'):
        with tag('style'):
            text('''
            @page {
                margin: 0.1in 0in 0in 0.04in;
            }
            body {
                font-family: Arial, sans-serif;
                margin: 0mm;
            }
            .voucher {
                border: 0.5mm dashed #000;
                padding: 1mm;
                font-size: 4.2mm;
                display: inline-block;
                text-align: center;
                font-weight: bold;
            }
            ''')
    with tag('body'):
        with tag('div', id='vouchers'):
            for _ in range(210): # set amount of vouchers here
                voucher = c.create_voucher(1, 1, 120, note="unifi-create-voucher")
                code = voucher[0].get('code')
                voucher_code = format_code(code)
                with tag('div', klass='voucher', style='width:{}ch;'.format(len(voucher_code) + 1)):
                    with tag('img', src='img.png', style='max-width:100%;'):
                        pass 
                    text(voucher_code)

with open('vouchers.html', 'w') as f:
    f.write(doc.getvalue())

os.system("chromium --headless --no-sandbox --disable-gpu --no-pdf-header-footer --print-to-pdf=vouchers.pdf vouchers.html")  

file_path = "vouchers.pdf"
os.system(f"lpr -P DCPT310 {file_path}")