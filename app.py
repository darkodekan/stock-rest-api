from flask import Flask, jsonify, request, render_template, make_response, Response
from flask_restful import Resource, Api
from flask_mysqldb import MySQL
from flask_sqlalchemy import SQLAlchemy
import random, configparser, logging
import time

#logging and logging configuration
LOG_FORMAT = "%(levelname)s %(asctime)s - %(message)s"
logging.basicConfig(filename = "LOGGING.log", level = logging.DEBUG, format = LOG_FORMAT)
logging.getLogger("urllib3").setLevel(logging.WARNING)
logger = logging.getLogger()

#read configuration file
config = configparser.ConfigParser()
config.read("SETTINGS.ini")
db_config = config["database"]
admin_config = config["admin"]
num_servers = len(config["general"]["server_ids"].split(","))


#initializing flask,api and database
app = Flask(__name__)
api = Api(app)
app.config['SQLALCHEMY_DATABASE_URI'] = "mysql://"+db_config["mysql_user"]+":"+db_config["mysql_password"]+"@"+db_config["mysql_host"]+"/"+db_config["mysql_database"]
db = SQLAlchemy(app)




class Product(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	product_id = db.Column(db.String(80), unique=True)
	server_id = db.Column(db.Integer)
	def __init__(self, product_id, server_id):
		self.product_id = product_id
		self.server_id = server_id
	def __repr__(self):
		return { "product_id" : self.product_id, "server_id" : self.server_id}
def is_product_exists(product_id):
	if db.session.query(Product.id).filter_by(product_id=product_id).scalar() != None:
		return True
	return False

class Introduction(Resource):
    def get(self):
        return {"app_name":"stock_rest_api"}

class AllProducts(Resource):
	def get(self):
		#return Product.query.all() 
		json_list = list()
		for product in Product.query.all():
			json_list.append(product.__repr__())
		return json_list
	def post(self):
		json_object = request.get_json()
		if not is_product_exists(product_id):
			db.session.add(Product(json_object["product_id"], json_object["server_id"]))
			return Response("OK", status=201, mimetype='application/json')
		return Response("Error 409", status=409, mimetype='application/json')

#MAKE JSON OBJECT TO PYTHON OBJECT CONVERTER

class OneProduct(Resource):
	def get(self,product_id):
		if is_product_exists(product_id):
			return Product.query.filter_by(product_id=product_id).first().__repr__()
		return Response("Error 404", status=404, mimetype='application/json')

	def delete(self, product_id):
		if is_product_exists(product_id):
			Product.query.filter_by(product_id=product_id).delete()
			db.session.commit()
		return Response("Error 404", status=404, mimetype='application/json')

	def put(self, product_id):
		if is_product_exists(product_id):
			product = Product.query.filter_by(product_id=product_id).first()
			product.product_id = request.get_json["product_id"]
			db.session.commit()
		return Response("Error 404", status=404, mimetype='application/json')

class ProductsServer(Resource):
	def get(self, server_id):
		json_list = list()
		products = Product.query.filter_by(server_id=server_id).all()
		for product in products:
			json_list.append(product.__repr__())
		return json_list
		
	
api.add_resource(Introduction, "/")
api.add_resource(AllProducts, "/product")
api.add_resource(OneProduct, "/product/product_id/<string:product_id>")
api.add_resource(ProductsServer, "/product/server_id/<int:server_id>")

if __name__ == "__main__":
    app.run(debug=True)
