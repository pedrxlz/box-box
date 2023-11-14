from pymongo import MongoClient
from werkzeug.security import check_password_hash, generate_password_hash


class Connection():
    def __init__(self) -> None:
        cluster = MongoClient("mongodb+srv://felipegaby:12345@cluster0.tet07xv.mongodb.net/")
        self.db = cluster['productsDB']

    def get_armazem(self) -> list:
        response = self.db['armazem'].find()
        response_builder = [ data for data in response ]
        return response_builder

    def get_categoria(self) -> list:
        response = self.db['categoria'].find()
        response_builder = [ data for data in response ]
        return response_builder
    
    def get_produto(self) -> list:
        response = self.db['produto'].find()
        response_builder = [ data for data in response ]
        return response_builder
    
    def get_usuario(self) -> list:
        response = self.db['usuario'].find()
        response_builder = [ data for data in response ]
        return response_builder
    
    def post_produto(self, produto):
        result = self.db['produto'].insert_one(produto)

        if result.inserted_id:
            return f"O produto foi inserido com o ID {result.inserted_id}"
        else:
            return "Falha ao adicionar o produto"
    

    # METODOS DESTINADOS A TABLE PRODUTO
    def filter_by_quantity_greater_than(self, quantidade : int) -> list:
        all_data = self.get_produto()

        filter_func = lambda data: True if data['quantidade'] >= quantidade else "False"

        filtered_list = filter(filter_func, all_data)

        return list(filtered_list)

    def filter_by_quantity_lesser_than(self, quantidade: int) -> list:
        all_data = self.get_produto()

        recursive_filter = lambda data_list: list(filter(lambda data: isinstance(data.get("quantidade"), int) and data["quantidade"] <= quantidade, data_list)) + list(map(lambda data: recursive_filter(data["dado_aninhado"]), filter(lambda data: isinstance(data.get("dado_aninhado"), list), data_list)))

        filtered_list = recursive_filter(all_data)

        return filtered_list
    
  
    # METODOS DESTINADOS A TABLE USUARIO
    
    def register(self, nome : str, login : str, senha : str) -> bool:
        existing_user = self.db['usuario'].find_one({'login' : login})

        if existing_user is None:
            hashed_password = generate_password_hash(senha)
            result = self.db['usuario'].insert_one({'nome' : nome, 'login': login, 'senha' : hashed_password })
            if result.inserted_id:
                return True
            else:
                return False
        return False
        
    def login( self, username : str, password : str) -> bool:
       existing_user = self.db['usuario'].find_one({'login' : username})
       
       if existing_user:
           if check_password_hash(existing_user['senha'], password):
               return True
           else :
               return False
    



    
    
    
        

        