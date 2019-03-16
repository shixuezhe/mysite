class BaseConfig(object):
    SECRET_KEY='shixuezhe'
    INDEX_PER_PAGE=9
    COMPANY_PER_PAGE=8
    ADMIN_PER_PAGE=15
    ONLINE_PER_PAGE=5
    SQLALCHEMY_TRACK_MODIFICATIONS=False

class DevelopmentConfig(BaseConfig):
    DEBUG=1
    SQLALCHEMY_DATABASE_URI='mysql+mysqldb://root@localhost:3306/liyang?charset=utf8'

class ProductionConfig(BaseConfig):
    pass

class TestingConfig(BaseConfig):
    pass

configs={
        'development':DevelopmentConfig,
        'production':ProductionConfig,
        'testing':TestingConfig
        }
