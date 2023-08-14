from requests import Session
from requests.auth import HTTPBasicAuth
from zeep import Settings, Client
from zeep.transports import Transport

from config import USER, PASSWORD, WSDL


def get_soap_client():
    wsdl = WSDL
    user = USER
    password = PASSWORD

    settings = Settings(
        strict=True  # строгая обработка запроса
        # raw_response=True  # ответ без обработки lxml-модулем
        # force_https=False
        # xml_huge_tree=True  # ограничение глубины xml-дерева
        # forbid_dtd=True
        # forbid_entities=False
        # xsd_ignore_sequence_order=True
    )

    session = Session()
    session.auth = HTTPBasicAuth(user, password)

    client = Client(
        wsdl=wsdl,
        settings=settings,
        transport=Transport(session=session)
    )

    return client.service
