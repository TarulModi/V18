# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) Sitaram Solutions (<https://sitaramsolutions.in/>).
#
#    For Module Support : info@sitaramsolutions.in  or Skype : contact.hiren1188
#
##############################################################################

{
    'name': "Internal Payment Transfer (Account to Account, Account to Journal, Journal to Account)",
    'version': "17.0.0.0",
    'summary': "Internal Payment Transfer (Account to Account, Account to Journal, Journal to Account)",
    'category': 'Accounting',
    'description': """
    Internal Payment Transfer (Account to Account, Account to Journal, Journal to Account)"
    account to account internal payment transfer
    account to journal  internal payment transfer
    journal to account  internal payment transfer
    journal to journal  internal payment transfer
    working with by default odoo account payment transfer module
    internal payment transfer
    customer internal transfer 
    vendor internal transfer 
    supplier internal transfer
    حساب إلى حساب الدفع الداخلي
    счет на счет внутренний перевод платежа
    compte à compte transfert de paiement interne
    口座間の内部支払い振替
    transferencia de pago interno de cuenta a cuenta
    帐户到帐户内部付款转帐
    帳戶到帳戶內部付款轉帳
    계정 대 계정 내부 결제 이체
    et ideo ideo internum mercedem capiat
    حساب إلى دفتر يومية تحويل الدفع
    счет в журнал внутренний перевод платежей
    仕訳帳内部支払振替
    계정에서 분개 내부 지불 전송
    transferencia de pago interno de cuenta a diario
    帐户到日记帐内部付款转账
    帳戶到日記帳內部付款轉賬
    konto til journal intern betalingsoverførsel
    account naar journaal interne betalingsoverdracht
    account sa journal internal transfer transfer
    جرنل کے اندرونی ادائیگی کی منتقلی کے لئے اکاؤنٹ
    Konto zur Journal-internen Zahlungsüberweisung
    حساب به انتقال پرداخت داخلی مجله
    z konta na wewnętrzny przelew płatności do dziennika
    przelew na wewnętrzne konto płatności
    مجله به حساب انتقال پرداخت داخلی
    Journal zur internen Überweisung des Kontos
    اندرونی ادائیگی کی منتقلی کے لئے اکاؤنٹ کے لئے جرنل
    talaarawan sa account sa paglipat ng panloob na pagbabayad
    journal til konto intern overførsel
    napló a belső fizetési átutaláshoz
    دفتر اليومية لحساب تحويل الدفع الداخلي
    журнал на счет внутреннего перевода платежа
    inherit customer payment
    inherit voucher
    
    """,
    'author': "Sitaram",
    'website':"http://www.sitaramsolutions.in",
    'depends': ['base', 'account'],
    'data': [
        'views/inherited_account_payment.xml'
    ],
    'demo': [],
    "external_dependencies": {},
    "license": "OPL-1",
    'installable': True,
    'auto_install': False,
    'live_test_url':'https://youtu.be/DxLmJ6kRweU',
    'images': ['static/description/banner.png'],
    "price": 13,
    "currency": 'EUR',
    
}
