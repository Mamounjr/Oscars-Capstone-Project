from flask import Flask, redirect, url_for, session, render_template, request
from authlib.integrations.flask_client import OAuth
import os

app = Flask(__name__)
app.secret_key = os.urandom(24)  # Use a secure random key in production
oauth = OAuth(app)

oauth.register(
  name='oidc',
  authority='https://cognito-idp.us-east-1.amazonaws.com/us-east-1_LmA1QKf4K',
  client_id='2ruo7oiuuiq1dnnlg0cq38n791',
  client_secret='<client secret>',
  server_metadata_url='https://cognito-idp.us-east-1.amazonaws.com/us-east-1_LmA1QKf4K/.well-known/openid-configuration',
  client_kwargs={'scope': 'email openid phone'}
)


@app.route('/')
def index():
    user = session.get('user')
    if user:
        return render_template('index.html', user=user)
    else:
        return f'''
        <b style="display: flex; justify-content: center; align-items: center; padding: 20px; background-color: #f1f1f1; border-radius: 8px; font-size: 1.2em;">
        Welcome! Please <a href="/login" style="text-decoration: none; color: white; background-color: #333; padding: 10px 20px; border-radius: 5px; font-size: 1.1em; display: inline-block; margin-left: 10px;">Login</a>
        </b>
        '''
    

@app.route('/login')
def login():
    # Alternate option to redirect to /authorize
    # redirect_uri = url_for('authorize', _external=True)
    # return oauth.oidc.authorize_redirect(redirect_uri)
    return oauth.oidc.authorize_redirect('https://52.2.181.92')


@app.route('/authorize')
def authorize():
    token = oauth.oidc.authorize_access_token()
    user = token['userinfo']
    session['user'] = user
    return redirect(url_for('index'))


@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
