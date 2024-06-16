from transbank.webpay.webpay_plus.transaction import Transaction, WebpayOptions
from transbank.common.integration_type import IntegrationType

# Configuración de Webpay Plus para pruebas
commerce_code = '597055555532'
api_key = '579B532A7440BB0C9079DED94D31EA1615BACEB56610332264630D42D0A36B1C'  # API Key proporcionada por Transbank para pruebas

options = WebpayOptions(
    commerce_code=commerce_code,
    api_key=api_key,
    integration_type=IntegrationType.TEST
)

transaction = Transaction(options)



# tx = Transaction(WebpayOptions(IntegrationCommerceCodes.WEBPAY_PLUS, IntegrationApiKeys.WEBPAY, IntegrationType.TEST))

## Versión 2.x del SDK
# El SDK apunta por defecto al ambiente de pruebas, no es necesario configurar lo siguiente
# transbank.webpay.webpay_plus.webpay_plus_default_commerce_code = 597055555532
# transbank.webpay.webpay_plus.default_api_key = "579B532A7440BB0C9079DED94D31EA1615BACEB56610332264630D42D0A36B1C"
# transbank.webpay.webpay_plus.default_integration_type = IntegrationType.TEST
######

# from transbank.webpay.webpay_plus.transaction import Transaction

# tx = Transaction(WebpayOptions("commercecode", "apikey", IntegrationType.LIVE))
# # Oneclick
# from transbank.webpay.oneclick.mall_inscription import MallInscription
# from transbank.webpay.oneclick.mall_transaction import MallTransaction

# ins = MallInscription(WebpayOptions("commercecode", "apikey", IntegrationType.LIVE))
# tx = MallTransaction(WebpayOptions("commercecode", "apikey", IntegrationType.LIVE))
# # Transaccion Completa
# from transbank.webpay.transaccion_completa.transaction import Transaction

# tx = Transaction(WebpayOptions("commercecode", "apikey", IntegrationType.LIVE))
# # Transaccion Completa Mall
# from transbank.webpay.transaccion_completa.mall_transaction import MallTransaction

# tx = MallTransaction(WebpayOptions("commercecode", "apikey", IntegrationType.LIVE))

# ## Versión 2.x del SDK

# # Webpay Plus
# # WebpayPlus.configure_for_production('commerce_code', 'apikey')

# # Oneclick
# from transbank import oneclick as BaseOneClick
# from transbank.common.integration_type import IntegrationType

# BaseOneClick.commerce_code = "commercecode"
# BaseOneClick.api_key = "apikey"
# BaseOneClick.integration_type = IntegrationType.LIVE

# Transaccion Completa
# from transbank import transaccion_completa as BaseTransaccionCompleta
# from transbank.common.integration_type import IntegrationType

# BaseTransaccionCompleta.commerce_code = "commercecode"
# BaseTransaccionCompleta.api_key = "apikey"
# BaseTransaccionCompleta.integration_type = IntegrationType.LIVE