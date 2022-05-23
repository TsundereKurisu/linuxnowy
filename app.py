from flask import Flask, session, request, send_file, redirect, url_for
import os

app = Flask(__name__)
app.secret_key='secret_key'
login = 'login'
haslo = 'password'
@app.route("/")
def HomePage():

    uploads = os.listdir('./uploads')
    files = ""
    for upload in uploads:
        files += "<div>" + upload + "<div/>"
    output =  '''
        <form action="/login" method="get">
            <input type="submit" value="Login"/>
        </form>
        </form>
         <div>Files:<div/>  ''' + files + '''
         <div>
        <form action="/download">
        <input type=text name=file>
        <input type=submit value=Download>
        </form>
        </div>
        '''
    if 'username' in session:
        output+='''
        <div>
        <form action="/upload">
            <input type='submit' value='upload'/>
        </form>
        </div>
        <div>
        <form action="/logout" method="get">
            <input type="submit" value="Logout" name="Submit" id="goto_logout" />
        </form>
        </div>
        '''
    return output



@app.route("/download")
def download():
    filename = request.args.get('file')
    if filename in os.listdir('uploads'):
        return send_file(os.path.join('uploads/', filename), as_attachment=True)
    else:
        return "<div>Error 404 - not found</div>"



@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if 'username' in session:
        if request.method == 'POST':
            file = request.files['file']
            if file:
                file.save(os.path.join('uploads/', file.filename))
                return "Done" + '''
                <form action="/" method="get">
                    <input type="submit" value="Go to HomePage"/>
                </form>
                '''
        else:
            return '''
        <h1>Upload</h1>
        <form method=post enctype=multipart/form-data>
        <input type=file name=file>
        <input type=submit value=Upload>
        </form>
        <div>
        <form action="/" method="get">
                    <input type="submit" value="Go to HomePage"/>
                </form>
        </div>
        
        '''


@app.route('/login', methods=['GET', 'POST'])
def login():
    if 'username' in session:
        return 'You have succesfully logged in' + '''
        <form action="/" method="get">
            <input type="submit" value="Go to HomePage"/>
        </form>
        '''
    if request.method == 'POST':
        password = request.form['password']
        if haslo == password:
                session['username'] = request.form['username']
                return redirect(url_for('login'))
        else:
                return 'Wrong password' + ''' 
                <form action="/login" method="get">
                    <input type="submit" value="Login" name="Submit" />
                </form>
                <form action="/" method="get">
                    <input type="submit" value="Go to HomePage"/>
                </form>
                '''
    return '''
        <form action="" method="post">
            <p><input type=text name=username>
            <p><input type=password name=password>
            <p><input type=submit value=Login>
        </form>
        '''


@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))


if __name__ == '__main__':
    app.run(debug=True, port=22, host='0.0.0.0')