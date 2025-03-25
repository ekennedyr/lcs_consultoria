from flask import Flask, render_template, session, redirect, url_for
from supabase import create_client
import os

app = Flask(__name__)
app.secret_key = os.environ.get('FLASK_SECRET', 'segredo-local')

supabase = create_client(
    os.getenv('SUPABASE_URL'),
    os.getenv('SUPABASE_KEY')
)

@app.route('/')
def index():
    user = session.get('user')
    if not user:
        return redirect(url_for('login'))
    
    documentos = supabase.table('documentos').select('*').eq(
        'prefeitura_id', user['prefeitura_id']
    ).execute().data
    
    return render_template('index.html', documentos=documentos)

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))