import os
import requests
from app.core.login import load_token_env



def load_success():
    print("PLUGIN: 'Pedidos' carregados com sucesso!")


def page_consult(args, tries=1):
    """Consulta página de Pedidos
    
    args
    str::startDate
    str::endDate
    int::page
    """

    startDate = args['startDate']
    endDate = args['endDate']
    page = args['page']

    if tries > 3:
        raise Exception("Tentativas excedidas")

    jconsulta = {"startDate": startDate,"endDate": endDate,"page": str(page)}
    token = "Bearer " + os.getenv("JWT_TOKEN")

    res = requests.post(
        'https://pmid.timbrasil.com.br/orders/v1/userInfo',
        headers={'Authorizationoam': token, "Clientid": "APPVAREJO"},
        json=jconsulta
    )

    if res.status_code == 401:
        print("Token expirado, carregando novo...")
        load_token_env()
        page_consult(args, tries+1)

    if res.status_code != 200:
        raise Exception(f"Erro ao consultar pedidos: {res.text}")

    res = res.json()
    return res


def load_all_pages(args):
    """Carrega todas as páginas
    
    args
    str::startDate
    str::endDate
    """
    page = 1
    data = []
    while True:
        args['page'] = page
        res = page_consult(args)
        if len(res['order']) == 0:
            break
        data.extend(res['order'])
        page += 1

    return {
        'count': len(data),
        'data': data
    }


def appointment_info(args, tries=1):
    """Consulta dados Appointment
    
    args
    str::orderID
    str::infracoId
    """
    orderID = args['orderID']
    infracoId = args['infracoId']

    if tries > 3:
        raise Exception("Tentativas excedidas")

    url = f"https://api.godigibee.io/pipeline/tim/v1/appointment/{orderID}"
    token = "Bearer " + os.getenv("JWT_TOKEN")

    res = requests.get(
        url,
        headers={'Authorization': token},
        params={'infracoId': infracoId}
    )

    if res.status_code == 401:
        load_token_env()
        appointment_info(args, tries+1)

    if res.status_code != 200:
        raise Exception("Erro ao consultar pedidos")

    res = res.json()

    if len(res) < 1:
        raise Exception("Nenhum dado encontrado")
    res = res[0]
    return res
