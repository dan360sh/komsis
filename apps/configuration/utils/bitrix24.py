import json

import requests
from apps.configuration.models import Settings


class Bitrix24:
    URL_PATTERN = "https://{domain}/rest/116/{key}/{command}"

    def __init__(self):
        super(BankPayment, self).__init__()

        settings = Settings.objects.filter(
            language=request.LANGUAGE_CODE).first()
        if settings and settings.bitrix24_domain and settings.bitrix24_key:
            self.url_pattern = URL_PATTERN.format(domain=settings.bitrix24_domain,
                                                  key=settings.bitrix24_key,
                                                  command="{}")
        else:
            raise Exception

    def call_webhook(self, command, data):
        """
        Отправляет POST запрос к REST bitrix24
        https://www.bitrix24.com/apps/webhooks.php
        """
        url = self.url_pattern.format(command)
        query = 1
        try:
            r = requests.post(url, json=params, params=query)
        except requests.exceptions.RequestException:
            r = None
        result = utils.resolve_response(r)
        return result
