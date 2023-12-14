from src import create_app, socketio
from config import DevConfig, ProdConfig, TestConfig

app=create_app(DevConfig)

if __name__ == '__main__':
    socketio.run(app, debug=True)
