from app     import get_app_with_config
app = get_app_with_config()

if __name__ == '__main__':
    app.run(host='0.0.0.0')