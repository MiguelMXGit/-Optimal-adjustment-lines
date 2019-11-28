from configparser import ConfigParser

class Config:
    # Habilitar ambiente de desarrollo
    DEBUG = True
    HOST='0.0.0.0'
    # CORS
    CORS_HEADERS = 'Content-Type'
    # JWT 
    JWT_SECRET_KEY = 'Super_Secret_JWT_KEY'
    JWT_ACCESS_TOKEN_EXPIRES = False


 
 
def config_db(filename='database.ini', section='postgresql'):
    # crear parser
    parser = ConfigParser()
    # leer archivo de parametros
    parser.read(filename)
 
    # obtener seccion  postgresql
    db = {}
    if parser.has_section(section):
        params = parser.items(section)
        for param in params:
            db[param[0]] = param[1]
    else:
        raise Exception('Section {0} not found in the {1} file'.format(section, filename))
 
    return db