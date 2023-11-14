from banco import Connection
from pprint import pprint

teste = Connection()


pprint(teste.filter_by_quantity_lesser_than(3))

#TESTAR POST
# new_produto = {
#     'armazem': 1,
#     'categoria': 1,
#     'id': 2,
#     'nome': 'xampu',
#     'preco': 200,
#     'quantidade': 4,
# }

# teste.post_produto(new_produto)

