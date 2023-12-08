from app.sonar import Sonar
import pytest
import os


sonar = Sonar()


def test_page():
    args_null = {
        "startDate": "2022-12-01",
        "endDate": "2022-12-31",
        "page": 1 
    }

    func = getattr(sonar.plugins['pedidos'], 'page_consult')
    assert func(args=args_null)['order'] == []


def test_load_all_pages():
    args_novembro = {
        "startDate": "2023-11-01",
        "endDate": "2023-11-30"
    }
    func = getattr(sonar.plugins['pedidos'], 'load_all_pages')
    assert func(args=args_novembro)['count'] == 244


def test_appointment_info():
    args_appointment = {
        "orderID": "SA-4912313",
        "infracoId": "VTAL"
    }
    func = getattr(sonar.plugins['pedidos'], 'appointment_info')
    assert func(args=args_appointment)['lifeCycleStatus'] == 'Concluído sem sucesso'


    