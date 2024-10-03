# server/app.py
#!/usr/bin/env python3

from flask import Flask, make_response, jsonify
from flask_migrate import Migrate

from models import db, Earthquake

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///models.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)
db.init_app(app)


@app.route('/')
def index():
    body = {'message': 'Flask SQLAlchemy Lab 1'}
    return make_response(body, 200)

# Add views here
# get eartheqiuke by id
@app.route("/earthquakes/<int:id>", methods=["GET"])
def get_earthquake_by_id(id):

# query the database to get the earthquake by id
    earthquake = Earthquake.query.filter_by(id=id).first()

    if earthquake:
        # If the earthquake is found, return its details as JSON
        return jsonify({
            "id":earthquake.id,
            "location":earthquake.location,
            "magnitude":earthquake.magnitude,
            "year":earthquake.year
        }),200
    
    else: 
        # if no earthquake is found
        return jsonify({
            "message": f"Earthquake {id} not found."
        }), 404
    
# @app.route("/earthquakes/magnitude/<float:magnitude>", methods=["GET"])
# def get_earthquake_magnitude(magnitude):
#     # Query the database for earthquakes with a magnitude >= the specified value
#     earthquake = Earthquake.query.filter(Earthquake.magnitude>=magnitude).all()

#     # response data
#     earthquake_list= [
#         {
#             "id":earthquake.id,
#             "location": earthquake.location,
#             "magnitude": earthquake.magnitude,
#             "year": earthquake.year
#         }
#         for earthquake in Earthquake
#     ]

#     # Create the JSON response
#     response = {
#         "count": len(earthquake_list),
#         "earthquakes": earthquake_list
#     }
#     # Return the response with status 200
#     return jsonify(response), 200

# Route to get all earthquakes with a magnitude greater than or equal to the specified value
@app.route('/earthquakes/magnitude/<float:magnitude>', methods=['GET'])
def get_earthquakes_by_magnitude(magnitude):
    # Query the database for earthquakes with a magnitude >= the specified value
    earthquakes = Earthquake.query.filter(Earthquake.magnitude >= magnitude).all()
    
    # Prepare the response data
    earthquakes_list = [
        {
            "id": earthquake.id,
            "location": earthquake.location,
            "magnitude": earthquake.magnitude,
            "year": earthquake.year
        }
        for earthquake in earthquakes
    ]
    
    # Create the JSON response
    response = {
        "count": len(earthquakes_list),
        "quakes": earthquakes_list
    }

    # Return the response with status 200
    return jsonify(response), 200


if __name__ == '__main__':
    app.run(port=5555, debug=True)
