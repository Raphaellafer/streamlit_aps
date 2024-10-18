from flask import Flask, request
from flask_pymongo import PyMongo
import os
from bson.objectid import ObjectId
from datetime import datetime, timedelta

# Carrega as variáveis de ambiente do arquivo .cred (se disponível)

app = Flask(__name__)
app.config["MONGO_URI"] = os.getenv("MONGO_URI", "mongodb+srv://admin:admin@progeficaz.z7ujs.mongodb.net/aps_3")
mongo = PyMongo(app)


# Este é um exemplo simples sem grandes tratamentos de dados
@app.route('/usuarios', methods=['GET'])
def get_all_users():
    filtro = {}
    projecao = {"_id": 1, "nome": 1, "cpf": 1}
    dados_usuarios = mongo.db.usuarios.find(filtro, projecao)

    resp = {
        "usuarios": [{"id": str(user["_id"]), "nome": user.get("nome"), "cpf": user.get("cpf")} for user in dados_usuarios]
    }

    return resp, 200


@app.route('/usuarios/<string:_id>', methods=['GET'])
def get_user(_id):
    
    user = mongo.db.usuarios.find_one({"_id": ObjectId(_id)})

    
    if user is None:
        return {"erro": "Usuario não encontrado"}, 404
        
    
    user['_id'] = str(user['_id'])
        
    return user, 200


# Este é um exemplo simples sem grandes tratamentos de dados
@app.route('/usuarios', methods=['POST'])
def post_user():
    
    data = request.json
    

    if "cpf" not in data:
        return {"erro": "cpf é obrigatório"}, 400
    if "nome" not in data:
        return {"erro": "nome é obrigatório"}, 400
    if "data_de_nascimento" not in data:
        return {"erro": "data de nascimento é obrigatório"}, 400
    
    result = mongo.db.usuarios.insert_one(data)

    return {"id": str(result.inserted_id)}, 201


@app.route('/usuarios/<string:_id>', methods=['PUT'])
def put_user(_id):

    data = request.json

    result = mongo.db.usuarios.update_one({"_id": ObjectId(_id)}, {"$set": data})
    
    if result.modified_count == 0:
        return {"erro": "usuario não encontrado ou nenhuma alteração realizada"}, 404

    return {"message": "usuario atualizado com sucesso"}, 200


@app.route('/usuarios/<string:_id>', methods=['DELETE'])
def delete_user(_id):
    
        # Tenta deletar o documento no MongoDB
    result = mongo.db.usuarios.delete_one({"_id": ObjectId(_id)})

        # Verifica se um documento foi deletado
    if result.deleted_count == 0:
        return {"erro": "usuarios não encontrado"}, 404

    return {"message": "usuarios deletado com sucesso"}, 200

@app.route('/bikes', methods=['GET'])
def get_all_bikes():
    filtro = {}
    projecao = {"_id": 1, "marca": 1, "modelo": 1, "cidade": 1, "status": 1}  # Inclua os campos desejados
    dados_bikes = mongo.db.bikes.find(filtro, projecao)

    # Mapeando os dados para incluir o _id como string
    resp = {
        "bikes": [{"id": str(bike["_id"]), "marca": bike.get("marca"), "modelo": bike.get("modelo"),
                   "cidade": bike.get("cidade"), "status": bike.get("status")} for bike in dados_bikes]
    }

    if not resp["bikes"]:
        return {"message": "Nenhuma bike encontrada"}, 404

    return resp, 200


@app.route('/bikes/<string:_id>', methods=['GET'])
def get_bike(_id):
    
    bike = mongo.db.bikes.find_one({"_id": ObjectId(_id)})

    if bike is None:
        return {"erro": "bike não encontrado"}, 404
        
    
    bike['_id'] = str(bike['_id'])
        
    return bike, 200


@app.route('/bikes', methods=['POST'])
def post_bike():
    
    data = request.json

    if "marca" not in data or "modelo" not in data or "cidade" not in data:
        return {"erro": "Todas informacoes sao obrigatórias"}, 400
    
    data['status'] = "disponivel"
    
    result = mongo.db.bikes.insert_one(data)

    return {"id": str(result.inserted_id)}, 201

@app.route('/bikes/<string:_id>', methods=['PUT'])
def put_bike(_id):

    data = request.json

    result = mongo.db.bikes.update_one({"_id": ObjectId(_id)}, {"$set": data})
    
    if result.modified_count == 0:
        return {"erro": "bike não encontrado ou nenhuma alteração realizada"}, 404

    return {"message": "bike atualizado com sucesso"}, 200

@app.route('/bikes/<string:_id>', methods=['DELETE'])
def delete_bike(_id):
    result = mongo.db.bikes.delete_one({"_id": ObjectId(_id)})

        # Verifica se um documento foi deletado
    if result.deleted_count == 0:
        return {"erro": "bikes não encontrado"}, 404

    return {"message": "bikes deletado com sucesso"}, 200

@app.route('/emprestimos', methods=['GET'])
def get_all_emprestimos():

    filtro = {}
    projecao = {
        "_id": 1,  
        "usuario_id": 1,  
        "bike_id": 1,  
        "data_aluguel": 1  
    }

    dados_emprestimos = mongo.db.emprestimos.find(filtro, projecao)

    emprestimos = []

    for emprestimo in dados_emprestimos:
        emprestimo['_id'] = str(emprestimo['_id'])  
        emprestimos.append(emprestimo)


    resp = {
        "emprestimos": emprestimos
    }

    return resp, 200



@app.route('/emprestimos/usuarios/<string:id_usuario>/bikes/<string:id_bike>', methods=['POST'])
def post_emprestimos(id_usuario, id_bike):

    usuario = mongo.db.usuarios.find_one({"_id": ObjectId(id_usuario)})
    if not usuario:
        return {"erro": "Usuário não encontrado"}, 404


    bike = mongo.db.bikes.find_one({"_id": ObjectId(id_bike)})
    if not bike:
        return {"erro": "Bicicleta não encontrada"}, 404


    if bike.get("status") != "disponivel":
        return {"erro": "Bicicleta já está alugada"}, 400

    data_aluguel = datetime.now()
    data_devolucao = data_aluguel + timedelta(days=10)

    emprestimo_data = {
        "usuario_id": id_usuario,
        "bike_id": id_bike,
        "data_aluguel": data_aluguel.strftime('%Y-%m-%d %H:%M:%S'), 
        "data_devolucao": data_devolucao.strftime('%Y-%m-%d %H:%M:%S')  
    }

    # Inserir o empréstimo no banco de dados
    result = mongo.db.emprestimos.insert_one(emprestimo_data)

    # Atualizar o status da bicicleta para "em uso"
    mongo.db.bikes.update_one({"_id": ObjectId(id_bike)}, {"$set": {"status": "em uso"}})

    return {"id": str(result.inserted_id)}, 201


@app.route('/emprestimos/<string:_id>', methods=['DELETE'])
def delete_emprestimo(_id):

    emprestimo = mongo.db.emprestimos.find_one({"_id": ObjectId(_id)})
    if not emprestimo:
        return {"erro": "Empréstimo não encontrado"}, 404

    id_bike = emprestimo.get("bike_id")

    result = mongo.db.emprestimos.delete_one({"_id": ObjectId(_id)})

    if result.deleted_count == 0:
        return {"erro": "Empréstimo não encontrado"}, 404

    mongo.db.bikes.update_one({"_id": ObjectId(id_bike)}, {"$set": {"status": "disponivel"}})

    return {"message": "Empréstimo deletado e bicicleta liberada com sucesso"}, 200

if __name__ == '__main__':
    app.run(debug=True)