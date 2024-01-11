# %%
from app.sonar import Sonar


# %%
sonar = Sonar()

# %%
pedidos = sonar.plugins.get('pedidos')


# %%
dteste = pedidos.load_all_pages(args={"startDate": "2023-11-20", "endDate": "2023-11-30"})

# %%

dados = dteste['data']

# %%
pedidos.appointment_info(args={"orderID": "SA-4812432", "infracoId": "VTAL"})

#%%
import xmlrpc.client
from dotenv import load_dotenv
from os import getenv

load_dotenv()
#%%
db = getenv("DB")
uid = getenv("UID")
password = getenv("PASSWORD")

print(db, uid, password)

#%%


models = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(getenv("URL_CRM")))



# %%
# Filtra pelo campo de "Novo pedido"
ids = models.execute_kw(db, uid, password, 'project.task', 'search', [[['stage_id', '=', "Novo Pedido"]]])


print(ids)

# %%
id = models.execute_kw(db, uid, password, 'project.task', 'create', [{'name': "Teste"}])


# %%

print(id)


# %%

changeId = models.execute_kw(db, uid, password, 'project.task', 'write', [[id], {'x_cpf': "123"}])




# %%
print(changeId)

#%%

models.execute_kw(db, uid, password, 'project.task', 'name_get',  [[id]])
# %%


