from app import app

if __name__ == '__main__':
    context = (r'tools/pem/cert.pem', r'tools/pem/key.pem') # For https service, ssl_context is needed.
    app.run(host='0.0.0.0', port=5000, debug=True, ssl_context=context)