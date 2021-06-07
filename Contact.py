from flask import Flask, jsonify, request
from flask_restful import Api,Resource, reqparse,abort, fields, marshal_with
from flask_sqlalchemy import SQLAlchemy
from flask_httpauth import HTTPBasicAuth
import json


USER_DATA = {
    "hitesh": "hitesh_xyz"
}



app = Flask(__name__)
api = Api(app)
auth = HTTPBasicAuth()
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.bd'
db = SQLAlchemy(app)

class ContactModel(db.Model):
    id = db.Column(db.Integer, primary_key = True,autoincrement=True)
    email = db.Column(db.String(100), unique = True,nullable = False)
    name = db.Column(db.String(100), nullable = False)
    phone = db.Column(db.Integer, nullable = False)

    def __repr__(self):
        return f"Contact(email = {email}, name = {name}, phone = {phone})"

#db.create_all()


contact_create = reqparse.RequestParser()
contact_create.add_argument("email", type=str, help="Required Field", required = True)
contact_create.add_argument("name", type=str, help="Required Field", required = True)
contact_create.add_argument("phone", type=int, help="Required Field", required = True)


contact_update = reqparse.RequestParser()
contact_update.add_argument("email", type=str, help="email of person is required")
contact_update.add_argument("name", type=str, help="Required Field")
contact_update.add_argument("phone", type=int, help="Required Field")


resource_field = {
    'id' : fields.Integer,
    'email' : fields.String,
    'name' : fields.String,
    'phone' : fields.Integer
}


@auth.verify_password
def verify(username, password):
    if not (username and password):
        abort(404, message = "Authentication required")
    if USER_DATA.get(username) == password:
        return True
    abort(404, message = "Invalid Credentials")


class Contact(Resource):

    @auth.login_required
    @marshal_with(resource_field)
    def get(self):
        email = request.args.get('email',None)
        name = request.args.get('name',None)

        if email and name:
            result = ContactModel.query.filter_by(email = email,name = name).first()
            if not result:
                abort(409, message = "No such contact")
            return result
        elif email:
            result = ContactModel.query.filter_by(email = email).first()
            if not result:
                abort(409, message = "No such contact")
            return result
        elif name:
            results = ContactModel.query.filter_by(name = name).all()
            if len(results) == 0:
                abort(409, message = "No such contact")
            return results
        else:
            results = ContactModel.query.all()
            if len(results) == 0:
                abort(409, message = "No such contact")
            return results


    @auth.login_required
    @marshal_with(resource_field)
    def put(self):
        args = contact_create.parse_args()
    
        result = ContactModel.query.filter_by(email = args['email']).first()
        if result:
            abort(409, message = "Email already taken")
        contact = ContactModel(email = args['email'],name = args['name'],phone = args['phone'])
        db.session.add(contact)
        db.session.commit()
        return contact, 201


    @auth.login_required
    @marshal_with(resource_field)
    def patch(self,email):
        args = contact_update.parse_args()
        print(args)
        result = ContactModel.query.filter_by(email = email).first()
        if not result:
            abort("404",message = "No such contact")
        
        if args['email']:
            result2 = ContactModel.query.filter_by(email = args['email']).first()
            if result2:
                abort("409",message = "Email already taken")
            result.email = args['email']
        if args['name']:
            result.name = args['name']
        if args['phone']:
            result.phone = args['name']
        
        db.session.commit()

        return result

    @auth.login_required
    def delete(self,email):
        result = ContactModel.query.filter_by(email = email).first()
        if not result:
            abort(409, message = "No such contact")
        db.session.delete(result)
        db.session.commit()

        return {"message" : "Contact Deleted"}





api.add_resource(Contact,  "/contact/", "/contact/<string:email>")


if __name__ == "__main__":
    app.run(debug=True)