import os

from app import create_app

config_name = os.getenv('APP_SETTINGS')  # config_name = "development"
app = create_app(config_name)

@app.route('/', methods=['GET'])
def index():
    return "Hello world"

if __name__ == '__main__':
    app.run()
