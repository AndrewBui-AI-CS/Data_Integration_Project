from backend.api import search

if __name__ == '__main__':
    search = search.create_app()
    search.run(host='127.0.0.1', port=5000, debug=False)
else:
    gunicorn_app = search.create_app()
