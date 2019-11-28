from flask import request, jsonify
from app import app
from flask_jwt_extended import jwt_required, create_access_token, get_jwt_identity
import psycopg2
from config import config_db



@app.route('/login', methods=['POST'])
def login():
    username = request.json['username']
    password = request.json['password']

    if not username:
        return jsonify({"msg": "Missing username parameter"}), 400
    if not password:
        return jsonify({"msg": "Missing password parameter"}), 400
    
    params = config_db()
    print(params)
    conn = psycopg2.connect(**params)
    # conectar a la base de datos
    try:
       
        cursor = conn.cursor()

        # buscar usuario
        cursor.execute("SELECT id FROM users WHERE username='{}' AND password='{}' ".format(username,password))
        user = cursor.fetchone()
    except (Exception, psycopg2.Error) as error :
        print ("Error while connecting to PostgreSQL", error)
    finally:
        #cerrar conexion a la base de datos
            if(conn):
                cursor.close()
                conn.close()
                print("PostgreSQL connection is closed")

    ## ------
    print(user)
    if user is None:
        return jsonify({'success': False, 'message': 'Bad username or password'}), 401

    access_token = create_access_token(identity=username)
    return jsonify({'success': True, 'token': access_token}), 200


@app.route('/verify-token', methods=['POST'])
@jwt_required
def verify_token():
    return jsonify({'success': True}), 200


@app.route('/protected', methods=['GET'])
@jwt_required
def protected():
    current_user = get_jwt_identity()
    return jsonify(logged_in_as=current_user), 200