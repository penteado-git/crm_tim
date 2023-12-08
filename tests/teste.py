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