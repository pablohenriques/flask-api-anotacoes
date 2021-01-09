from flask_restful import Resource
from models.site import SitelModel


class Sites(Resource):
    def get(self):
        return {'sites': [site.json() for site in SitelModel.query.all()]}


class Site(Resource):
    def get(self, url):
        site = SitelModel.find_site(url)

        if site:
            return site.json()
        return {'message': 'Site não Encontrado'}

    def post(self, url):
        if SitelModel.find_site(url):
            return {'message': 'Site já existe'}, 400

        site = SitelModel(url)
        try:
            site.save_site()
        except:
            return {'message': 'Erro Interno'}, 500

        return site.json()

    def delete(self, url):
        site = SitelModel.find_site(url)

        if site:
            site.delete_site()
            return {'message': 'Site Deletado'}
        return {'message': 'Site não Encontrado'}, 404
