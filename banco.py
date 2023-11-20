from bson.objectid import ObjectId
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
    
    def get_armazem_by_id(self, id) -> list:
        response = self.db['armazem'].find_one({'_id': ObjectId(id)})
        return response
    
    def post_armazem(self, armazem):
        result = self.db['armazem'].insert_one(armazem)

        if result.inserted_id:
            return f"O armazem foi inserido com o ID {result.inserted_id}"
        else:
            return "Falha ao adicionar o armazem"

    def get_categoria(self) -> list:
        response = self.db['categoria'].find()
        response_builder = [ data for data in response ]
        return response_builder
    
    def get_categoria_by_id(self, id) -> list:
        response = self.db['categoria'].find_one({'_id': ObjectId(id)})
        return response
    
    def post_categoria(self, categoria):
        result = self.db['categoria'].insert_one(categoria)

        if result.inserted_id:
            return f"A categoria foi inserida com o ID {result.inserted_id}"
        else:
            return "Falha ao adicionar a categoria"
        
    
    def get_produto(self) -> list:
        response = self.db['produto'].find()
        response_builder = [ data for data in response ]
        
        for data in response_builder:
            data['armazem'] = self.get_armazem_by_id(data['armazem'])['nome']
            data['categoria'] = self.get_categoria_by_id(data['categoria'])['nome']
        
        return response_builder
    
    def get_produto_by_id(self, id) -> list:
        response = self.db['produto'].find_one({'_id': ObjectId(id)})
        
        response['armazem'] = self.get_armazem_by_id(response['armazem'])['nome']
        response['categoria'] = self.get_categoria_by_id(response['categoria'])['nome']

        return response
    
    def update_produto(self, id, produto):
        result = self.db['produto'].update_one({'_id': ObjectId(id)}, {'$set': produto})
        if result.modified_count:
            return f"O produto foi atualizado com sucesso"
        else:
            return "Falha ao atualizar o produto"
    
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
    def delete_produto(self, id):
        product = self.get_produto_by_id(id)
        
        result = product and self.db['produto'].delete_one({'_id': ObjectId(id)}) 
        
        if result.deleted_count:
            return f"O produto foi deletado com sucesso"
        else:
            return "Falha ao deletar o produto"
    

    # METODOS DESTINADOS A TABLE PRODUTO
    def filter_by_quantity_greater_than(self, products: list, quantidade : int) -> list:

        filter_func = lambda data: True if data['quantidade'] >= quantidade else False

        filtered_list = filter(filter_func, products)

        return list(filtered_list)

    def filter_by_quantity_lesser_than(self, products: list, quantidade: int) -> list:

        recursive_filter = lambda data_list: list(filter(lambda data: isinstance(data.get("quantidade"), int) and data["quantidade"] <= quantidade, data_list)) + list(map(lambda data: recursive_filter(data["dado_aninhado"]), filter(lambda data: isinstance(data.get("dado_aninhado"), list), data_list)))

        filtered_list = recursive_filter(products)

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
    



    
    
    
        

        