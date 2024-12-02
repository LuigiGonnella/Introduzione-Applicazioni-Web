# IMPORTO MODULI
from flask import Flask, render_template, request, redirect, flash, url_for
from datetime import *
import dao

from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename #elimina spazi e caratteri indesiderati dal nome del file
from models import User


# CREO APPLICAZIONE
app = Flask(__name__)
app.config['SECRET_KEY'] = '9OLWxND4o83j4K4iuopO'

login_manager = LoginManager()
login_manager.login_view = 'login'
login_manager.init_app(app)


# definisco homepage gestendo ordinamento annunci
@app.route('/', methods=['GET']) 
def home():
    flag=request.args.get('id')

    if flag:
        annunci=dao.get_annunci_num_loc_cresc()
    else:
        annunci=dao.get_annunci_prezzo_decresc()

    return render_template('home.html', annunci=annunci)


#prendo annuncio dall'id
@app.route('/annunci/<int:id>', methods=['GET']) 
def single(id):
    flag=True
    annuncio = dao.get_annuncio(id)
    pren= dao.get_pren(id)
    if current_user.is_authenticated:
        for p in pren:
            if p['id_cliente'] == current_user.id and p['id_annuncio'] == id and p['stato'] != 'R':
                flag=False #flag per capire se l'utente può prenotare l'abitazione


    return render_template('single.html', annuncio=annuncio, flag=flag)

#aggiungo annuncio
@app.route('/annunci/new', methods=['GET', 'POST'])
@login_required
def new_annuncio():
    if request.method == 'POST':
        if current_user.is_authenticated:

            annuncio = request.form.to_dict()

            #se l'annuncio è disponibile il campo "disponibile" sarà true, altrimenti sarà false
            if annuncio['disponibile']=='Sì': 
                annuncio['disponibile']=True
            else:
                annuncio['disponibile']=False

            if annuncio['titolo'] == '':
                app.logger.error('Il titolo non può essere vuoto!')
                flash(
                    'Annuncio non creato correttamente: il titolo non può essere vuoto!', 'danger')
                return redirect(url_for('home'))

            if annuncio['indirizzo'] == '':
                app.logger.error('Devi selezionare un indirizzo')
                flash(
                    'Annuncio non creato correttamente: devi aggiungere un indirizzo!', 'danger')
                return redirect(url_for('home'))
            
            if annuncio['prezzo'] == '':
                app.logger.error('Devi selezionare un prezzo')
                flash(
                    'Annuncio non creato correttamente: devi aggiungere un prezzo!', 'danger')
                return redirect(url_for('home'))
            
            immagine1 = request.files['immagine1']
            immagine2 = request.files['immagine2']
            immagine3 = request.files['immagine3']
            immagine4 = request.files['immagine4']
            immagine5 = request.files['immagine5']

            immagini=[immagine1, immagine2, immagine3, immagine4, immagine5]
            i=1

            for img in immagini:
                if img:
                    img.save('static/' + secure_filename(img.filename))
                    annuncio[f'immagine{i}'] = '/static/' + secure_filename(img.filename)
                else:
                    annuncio[f'immagine{i}'] = False #se non esiste l'immagine metto il campo a false
                i=i+1


            id_locatore = current_user.id
            annuncio['id_locatore'] = id_locatore

            success = dao.add_annuncio(annuncio)

            if success:
                flash('Annuncio creato correttamente', 'success')
            else:
                flash("Errore nella creazione dell'annuncio: riprova!", 'danger')

    return redirect(url_for('home'))

@app.route('/annunci/modifica/<int:id_annuncio>', methods=['GET', 'POST'])
@login_required
def modifica_annuncio(id_annuncio): 
    if request.method == 'POST':
        if current_user.is_authenticated:

            annuncio = request.form.to_dict()

            #se l'annuncio è disponibile il campo "disponibile" sarà true, altrimenti sarà false
            if annuncio['disponibile']=='Sì': 
                annuncio['disponibile']=True
            else:
                annuncio['disponibile']=False

            if annuncio['titolo'] == '':
                app.logger.error('Il titolo non può essere vuoto!')
                flash(
                    'Annuncio non creato correttamente: il titolo non può essere vuoto!', 'danger')
                return redirect(url_for('home'))
            
            if annuncio['prezzo'] == '':
                app.logger.error('Devi selezionare un prezzo')
                flash(
                    'Annuncio non creato correttamente: devi aggiungere un prezzo!', 'danger')
                return redirect(url_for('home'))
            
            immagine1 = request.files['immagine1']
            immagine2 = request.files['immagine2']
            immagine3 = request.files['immagine3']
            immagine4 = request.files['immagine4']
            immagine5 = request.files['immagine5']

            immagini=[immagine1, immagine2, immagine3, immagine4, immagine5]
            i=1

            for img in immagini:
                if img:
                    img.save('static/' + secure_filename(img.filename))
                    annuncio[f'immagine{i}'] = '/static/' + secure_filename(img.filename)
                else:
                    annuncio[f'immagine{i}'] = False #se non esiste l'immagine metto il campo a false
                i=i+1


            id_locatore = current_user.id
            annuncio['id_locatore'] = id_locatore

            success = dao.update_annuncio(annuncio, id_annuncio)

            if success:
                flash('Annuncio creato correttamente', 'success')
            else:
                flash("Errore nella creazione dell'annuncio: riprova!", 'danger')

    return redirect(url_for('single', id=id_annuncio))


#PRENDO DATA PRENOTAZIONE
@app.route('/prenotazioni/new/<int:id_annuncio>', methods=['POST'])
@login_required
def data_pren(id_annuncio):
    annuncio=dao.get_annuncio(id_annuncio)
    ora=[True,True,True,True] #vettore degli orari disponibili vet[0]=9-12, vet[1]=12-14 ecc, se l'istanza è a true, quella fascia è disponibile, se è a false, non è disponibile
    orari_tot=['9-12', '12-14', '14-17', '17-20']
    orari_disp=['0', '0', '0', '0']
    data = request.form.to_dict()

    if data['data'] == '':
        app.logger.error('La data non può essere vuota!')
        flash('Errore nella selezione della data!', 'danger')
        return redirect(url_for('single', id=id_annuncio))
    
    dataSel = datetime.strptime(data['data'], '%Y-%m-%d')
    Oggi = datetime.now() - timedelta(days=1)

    # dataMassima = 7 giorni dalla data di oggi
    dataMax = Oggi + timedelta(days=8)

    if dataSel < Oggi:
        flash('La data deve essere pari o successiva ad oggi!', 'danger')
        return redirect(url_for('single', id=id_annuncio))
    elif dataSel > dataMax:
        flash('La data deve essere entro 7 giorni da oggi!', 'danger')
        return redirect(url_for('single', id=id_annuncio))


    prens=dao.get_pren(id_annuncio)

    

    for p in prens:
        if p['data']==data['data'] and p['stato']!='R': #A=accettata, R=rifiutata, '?'=pendente, se non è rifiutata, lo slot non è disponibile
            if p['ora']=='9-12':
                ora[0]=False
            elif p['ora']=='12-14':
                ora[1]=False
            elif p['ora']=='14-17':
                ora[2]=False
            elif p['ora']=='17-20':
                ora[3]=False

    indice=-1 #indice per orari_tot e orari_disp
    for o in ora:
        indice=indice+1
        if o==True:
            orari_disp[indice]=orari_tot[indice]


    return render_template('singlebis.html', orari=orari_disp, data=data['data'], annuncio=annuncio)



#AGGIUNGO PRENOTAZIONE COMPLETA

@app.route('/prenotazioni/new/orari/<int:id_annuncio>/<data>', methods=['POST'])
@login_required
def nuova_pren(id_annuncio, data):

    campi=request.form.to_dict()
    id_utente=current_user.id

    success=dao.add_pren(campi, data, id_annuncio, id_utente)

    if success:
        flash('Richiesta prenotazione effettuata correttamente', 'success')
    else:
        flash('Errore nella creazione della richiesta: riprova!', 'danger')

    return redirect(url_for('single', id=id_annuncio))



# definisco le pagine personali


@app.route('/area_cliente')
@login_required
def area_cliente():

    id=current_user.id
    pren=dao.get_pren_by_id_cliente(id)

    return render_template('area_cliente.html', prenotazioni=pren)

@app.route('/area_locatore')
@login_required
def area_locatore():
    id=request.args.get('id')
    ann=dao.get_annunci_prezzo_decresc()

    annunci=[] #annunci del locatore
    prenotazioni=[] #ogni istanza è l'insieme delle prenotazioni per un annuncio

    for annuncio in ann:
        if annuncio['id_locatore']==current_user.id:
            annunci.append(annuncio)
            pren=dao.get_pren(annuncio['id'])
            prenotazioni.append(pren)

    return render_template('area_locatore.html', id=id, annunci=annunci, prenotazioni=prenotazioni)


@app.route('/area_locatore_accetta/<int:id_annuncio>/<int:id_utente>', methods=['GET', 'POST'])
@login_required
def locatore_accetta(id_annuncio, id_utente):
    stato='A'
    success=dao.cambia_stato(id_annuncio, id_utente, stato)

    if success:
        flash('Prenotazione accettata correttamente', 'success')
    else:
        flash('Prenotazione non accettata correttamente: riprova!', 'danger')

    return redirect(url_for('area_locatore')) #reindirizzo alle richieste

@app.route('/area_locatore_rifiuta/<int:id_annuncio>/<int:id_utente>', methods=['GET', 'POST'])
@login_required
def locatore_rifiuta(id_annuncio, id_utente):
    stato='R'
    motivo=request.form.get('motivo')

    success1=dao.cambia_stato(id_annuncio, id_utente, stato)
    success2=dao.aggiungi_motivo(id_annuncio, id_utente, motivo)


    if success1 and success2:
        flash('Prenotazione rifiutata correttamente', 'success')
    else:
        flash('Prenotazione non rifiutata correttamente: riprova!', 'danger')

    return redirect(url_for('area_locatore')) #reindirizzo alle richieste



@login_manager.user_loader
def load_user(user_id):

    utente = dao.get_user_by_id(user_id)

    if utente is not None:
        user = User(id=utente['id'], nickname=utente['nickname'], password=utente['password'],
                    locatore=utente['locatore'])
    else:
        user = None

    return user

@app.route('/accedi')
def login():
    return render_template('login.html')

#gestisco login

@app.route('/accedi', methods=['POST'])
def login_post():
    nickname = request.form.get('nickname')
    password = request.form.get('password')

    user = dao.get_user_by_nickname(nickname)

    #se non c'è l'utente o la password è sbagliata->errore
    if not user or not check_password_hash(user['password'], password):
        flash('Credenziali non valide, riprovare', 'danger')
        return redirect(url_for('login'))
    #altrimenti ->login
    else:
        new = User(id=user['id'], nickname=user['nickname'], password=user['password'],
                   locatore=user['locatore'])
        login_user(new, True)
        flash('Login con successo!', 'success')
        return redirect(url_for('home'))
    

@app.route('/iscriviti')
def signup():
    return render_template('signup.html')


#gestisco iscrizione
@app.route('/iscriviti', methods=['POST'])
def signup_post():
    nickname = request.form.get('nickname')
    password = request.form.get('password')
    locatore= request.form.get('locatore')

    user_in_db = dao.get_user_by_nickname(nickname)

    if user_in_db:
        flash('C\'è già un utente registrato con questo nickname', 'danger')
        return redirect(url_for('signup'))
    else:
        new_user = {
            "nickname": nickname,
            "password": generate_password_hash(password, method='pbkdf2:sha256'),
            "locatore": locatore
        }

        success = dao.add_user(new_user)

        if success:
            flash('Utente creato correttamente', 'success')
            return redirect(url_for('home'))
        else:
            flash('Errore nella creazione del utente: riprova!', 'danger')

    return redirect(url_for('signup'))

#gestisco logout

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))





if __name__ == "__main__":
    app.run(host='0.0.0.0', port=3000, debug=True)
