from src import create_app
from config import DevConfig,ProdConfig,TestConfig

app=create_app(DevConfig)

if __name__ == '__main__':
    app.run()
