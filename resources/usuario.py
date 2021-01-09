from flask_restful import Resource, reqparse
from models.usuario import UserModel
from flask_jwt_extended import create_access_token, jwt_required, get_raw_jwt
from werkzeug.security import safe_str_cmp
from blacklist import BLACKLIST

atributos = reqparse.RequestParser()
atributos.add_argument('login', type=str, required=True, help="Campo não pode estar vazio")
atributos.add_argument('senha', type=str, required=True, help="Campo não pode estar vazio")


class User(Resource):
    #/usuarios/{user_id}
    def get(self, user_id):
        hotel = UserModel.find_user(user_id)

        if hotel:
            return hotel.json()
        return {'message': 'Usuário não encontrado'}, 400

    @jwt_required
    def delete(self, user_id):
        user = UserModel.find_user(user_id)

        if user:
            try:
                user.delete_user()
            except:
                return {'message': 'internal server error'}, 500
            return {'message': 'usuário deletado'}
        return {'message': 'usuário não encotrado'}, 404


class UserRegister(Resource):
    #/cadastro
    def post(self):
        dados = atributos.parse_args()

        if UserModel.find_by_login(dados['login']):
            return {"message": "O login já existe"}

        user = UserModel(**dados)
        user.save_user()
        return {"message": "Usuário criado com sucesso"}, 201


class UserLogin(Resource):

    @classmethod
    def post(cls):
        dados = atributos.parse_args()
        user = UserModel.find_by_login(dados['login'])

        if user and safe_str_cmp(user.senha, dados['senha']):
            token_de_acesso = create_access_token(identity=user.user_id)
            return {'access_token': token_de_acesso}, 200

        return {'message': 'Usuário ou senha incorreto (a)'}, 401


class UserLogout(Resource):

    @jwt_required
    def post(self):
        jwt_id = get_raw_jwt()['jti']
        BLACKLIST.add(jwt_id)
        return {'message': 'Logout realizado'}, 200



