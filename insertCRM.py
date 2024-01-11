from pymongo import MongoClient
from datetime import datetime
import xmlrpc.client
from dotenv import load_dotenv
from os import getenv

load_dotenv()
mongo_url = 'mongodb://ali2:Teste%402020@192.168.196.76:27017/?authMechanism=DEFAULT'
mongo_client = MongoClient(mongo_url)
mongo_db = mongo_client.sonarTeste
collection = mongo_db.sonarData

def insertCrm():
    odoo_url = getenv("URL_CRM")    
    models = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(odoo_url), allow_none=True)
    db = getenv('DB')
    uid = getenv('UID')
    password = getenv('PASSWORD')

    for data in collection.find():
        protocolNumber = data.get('protocolNumber')

        task_ids = models.execute_kw(db, uid, password, 'project.task', 'search_read', [[['x_numero_protocolo', '=', protocolNumber]]], {'fields': ['x_lead']})
        if task_ids:  
            start_date_time_str = data.get('appointment')[0]['validFor']['startDateTime']
            start_date_time = datetime.strptime(start_date_time_str, '%Y-%m-%dT%H:%M:%S')
            formatted_start_date_time = start_date_time.strftime('%Y-%m-%d %H:%M:%S')

            for task_id in task_ids:
                id_task = task_id['id']
                id_lead = task_id['x_lead'][0]
                # start_date_time_str = data.get('appointment')[0]['validFor']['startDateTime']
                # start_date_time = datetime.strptime(start_date_time_str, '%Y-%m-%dT%H:%M:%S')
                # formatted_start_date_time = start_date_time.strftime('%Y-%m-%d %H:%M:%S')
                # print(data)
                #     protocolNumber = data.get('protocolNumber')

                update_data_task = {
                        'x_numero_protocolo': protocolNumber,
                        'x_status_pedido': data.get('status'),
                        'x_data_instalacao': formatted_start_date_time,
                        'x_instalacao': data.get('lifeCycleStatus')
                    }

                models.execute_kw(db, uid, password, 'project.task', 'write', [[id_task], update_data_task])
                models.execute_kw(db, uid, password, 'crm.lead', 'write', [[id_lead], update_data_task])

                print(f"Atualizado protocolo {protocolNumber} na tarefa com ID: {task_id}, {update_data_task}")

            #     lead_ids = models.execute_kw(db, uid, password, 'project.task', 'search', [[['x_numero_protocolo', '=', protocolNumber]]])

            #     if lead_ids:
            #         lead_id = lead_ids[0]  

            #         update_data_lead = {
            #             'x_numero_protocolo': data.get(protocolNumber),     
            #         }

                    
            #         models.execute_kw(db, uid, password, 'crm.lead', 'write', [[lead_id], update_data_lead])

            #         print(f"Atualizado protocolo {protocolNumber} na lead com ID: {lead_id}, {update_data_lead}")
            #     else:
            #         print(f"Lead com x_numero_protocolo {protocolNumber} não encontrada no Odoo.")
            # else:
            #     print(f"Tarefa com ID {task_id} não encontrada no Odoo.")

insertCrm()