from app.controller.main import app

if __name__ == '__main__':
    app.run(host="192.168.1.7", port=8000, debug=True)