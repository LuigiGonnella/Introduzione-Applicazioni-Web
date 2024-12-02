import sqlite3

# Operazioni sugli Annunci


#GESTIONE VISUALIZZAZIONE ANNUNCI

def get_annunci_num_loc_cresc():
    conn = sqlite3.connect('db/Affitti.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    sql = 'SELECT ANNUNCI.id, ANNUNCI.titolo, ANNUNCI.indirizzo, ANNUNCI.tipo, ANNUNCI.prezzo, ANNUNCI.arredato, ANNUNCI.num_loc, ANNUNCI.desc, ANNUNCI.disponibile, ANNUNCI.immagine1, ANNUNCI.immagine2, ANNUNCI.immagine3, ANNUNCI.immagine4, ANNUNCI.immagine5, ANNUNCI.id_locatore, UTENTI.nickname FROM ANNUNCI, UTENTI WHERE ANNUNCI.id_locatore = UTENTI.id ORDER BY ANNUNCI.num_loc'
    cursor.execute(sql)
    annunci = cursor.fetchall()

    cursor.close()
    conn.close()

    return annunci

def get_annunci_prezzo_decresc():
    conn = sqlite3.connect('db/Affitti.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    sql = 'SELECT ANNUNCI.id, ANNUNCI.titolo, ANNUNCI.indirizzo, ANNUNCI.tipo, ANNUNCI.prezzo, ANNUNCI.arredato, ANNUNCI.num_loc, ANNUNCI.desc, ANNUNCI.disponibile, ANNUNCI.immagine1, ANNUNCI.immagine2, ANNUNCI.immagine3, ANNUNCI.immagine4, ANNUNCI.immagine5, ANNUNCI.id_locatore, UTENTI.nickname FROM ANNUNCI, UTENTI WHERE ANNUNCI.id_locatore = UTENTI.id ORDER BY ANNUNCI.prezzo DESC'
    cursor.execute(sql)
    annunci = cursor.fetchall()

    cursor.close()
    conn.close()

    return annunci

#PRENDO ANNUNCIO DATO UN ID

def get_annuncio(id):
    conn = sqlite3.connect('db/Affitti.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    sql = 'SELECT ANNUNCI.id, ANNUNCI.titolo, ANNUNCI.indirizzo, ANNUNCI.tipo, ANNUNCI.prezzo, ANNUNCI.arredato, ANNUNCI.num_loc, ANNUNCI.desc, ANNUNCI.disponibile, ANNUNCI.immagine1, ANNUNCI.immagine2, ANNUNCI.immagine3, ANNUNCI.immagine4, ANNUNCI.immagine5, ANNUNCI.id_locatore, UTENTI.nickname FROM ANNUNCI, UTENTI WHERE ANNUNCI.id_locatore = UTENTI.id AND ANNUNCI.id = ?'
    cursor.execute(sql, (id,))
    annuncio = cursor.fetchone()

    cursor.close()
    conn.close()

    return annuncio

#AGGIUNGO ANNUNCIO AL DB

def add_annuncio(annuncio):
    conn = sqlite3.connect('db/Affitti.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    success = False

    sql = 'INSERT INTO ANNUNCI(titolo, indirizzo, tipo, prezzo, arredato, num_loc, desc, disponibile, immagine1, immagine2, immagine3, immagine4, immagine5, id_locatore) VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)'
    cursor.execute(sql, (annuncio['titolo'], annuncio['indirizzo'], annuncio['tipo'], annuncio['prezzo'], annuncio['arredato'], annuncio['num_loc'], annuncio['desc'], annuncio['disponibile'], annuncio['immagine1'], annuncio['immagine2'], annuncio['immagine3'], annuncio['immagine4'], annuncio['immagine5'], annuncio['id_locatore']))
    
    try:
        conn.commit()
        success = True
    except Exception as e:
        print('ERROR', str(e))
        # se qualcosa da errore: rollback
        conn.rollback()

    cursor.close()
    conn.close()

    return success

def update_annuncio(annuncio, id_annuncio):
    conn = sqlite3.connect('db/Affitti.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    success = False

    sql='UPDATE ANNUNCI SET titolo=?, tipo=?, prezzo=?, arredato=?, num_loc=?, desc=?, disponibile=?, immagine1=?, immagine2=?, immagine3=?, immagine4=?, immagine5=? WHERE id=?'
    cursor.execute(sql, (annuncio['titolo'], annuncio['tipo'], annuncio['prezzo'], annuncio['arredato'], annuncio['num_loc'], annuncio['desc'], annuncio['disponibile'], annuncio['immagine1'], annuncio['immagine2'], annuncio['immagine3'], annuncio['immagine4'], annuncio['immagine5'], id_annuncio))
    
    try:
        conn.commit()
        success = True
    except Exception as e:
        print('ERROR', str(e))
        # se qualcosa da errore: rollback
        conn.rollback()

    cursor.close()
    conn.close()

    return success


#prendo tutte le prenotazioni di un'abitazione dato l'id_annuncio
def get_pren(id): 
    conn = sqlite3.connect('db/Affitti.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()



    sql = 'SELECT PREN.id_annuncio, PREN.id_cliente, PREN.stato, PREN.data, PREN.ora, PREN.tipo, PREN.motivo, UTENTI.nickname, ANNUNCI.titolo, ANNUNCI.indirizzo  FROM PREN, UTENTI, ANNUNCI WHERE PREN.id_annuncio = ? AND PREN.id_annuncio=ANNUNCI.id AND ANNUNCI.id_locatore=UTENTI.id'
    cursor.execute(sql, (id,))
    prenotazioni = cursor.fetchall()

    cursor.close()
    conn.close()

    return prenotazioni

#prendo tutte le prenotazioni di un cliente dato il suo id
def get_pren_by_id_cliente(id):
    conn = sqlite3.connect('db/Affitti.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    sql = 'SELECT PREN.id_annuncio, PREN.id_cliente, PREN.stato, PREN.data, PREN.ora, PREN.tipo, PREN.motivo, UTENTI.nickname, ANNUNCI.titolo, ANNUNCI.indirizzo  FROM PREN, UTENTI, ANNUNCI WHERE PREN.id_cliente = ? AND PREN.id_annuncio=ANNUNCI.id AND ANNUNCI.id_locatore=UTENTI.id'
    cursor.execute(sql, (id,))
    prenotazioni = cursor.fetchall()

    cursor.close()
    conn.close()

    return prenotazioni


#AGGIUNGO PRENOTAZIONE CON STATO PENDENTE
def add_pren(pren, data, id_annuncio, id_utente):
    conn = sqlite3.connect('db/Affitti.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    success = False
    stato= '?'

    sql = 'INSERT INTO PREN(id_annuncio, id_cliente,stato, data, ora, tipo, motivo) VALUES(?,?,?,?,?,?,?)'
    cursor.execute(sql, (id_annuncio, id_utente, stato, data, pren['ora'], pren['tipo'], False))
    try:
        conn.commit()
        success = True
    except Exception as e:
        print('ERROR', str(e))
        # in caso di errore: rollback
        conn.rollback()

    cursor.close()
    conn.close()

    return success

#CAMBIO STATO PRENOTAZIONE
def cambia_stato(id_annuncio, id_utente, stato):
    conn = sqlite3.connect('db/Affitti.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    success = False

    sql = 'UPDATE PREN SET stato= ? WHERE id_annuncio= ? AND id_cliente= ?'
    cursor.execute(sql, (stato, id_annuncio, id_utente))
    try:
        conn.commit()
        success = True
    except Exception as e:
        print('ERROR', str(e))
        # in caso di errore: rollback
        conn.rollback()

    cursor.close()
    conn.close()

    return success

#AGGIUNGO MOTIVO RIFIUTO ALLA PRENOTAZIONE
def aggiungi_motivo(id_annuncio, id_utente, motivo):
    conn = sqlite3.connect('db/Affitti.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    success = False

    sql = 'UPDATE PREN SET motivo= ? WHERE id_annuncio= ? AND id_cliente= ?'
    cursor.execute(sql, (motivo, id_annuncio, id_utente))
    try:
        conn.commit()
        success = True
    except Exception as e:
        print('ERROR', str(e))
        # in caso di errore: rollback
        conn.rollback()

    cursor.close()
    conn.close()

    return success



#prendo utente dato il nickname

def get_user_by_nickname(nickname):
    conn = sqlite3.connect('db/Affitti.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    sql = 'SELECT * FROM utenti WHERE nickname = ?'
    cursor.execute(sql, (nickname,))
    user = cursor.fetchone()

    cursor.close()
    conn.close()

    return user

#prendo utente dato l'id

def get_user_by_id(id):
    conn = sqlite3.connect('db/Affitti.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    sql = 'SELECT * FROM utenti WHERE id = ?'
    cursor.execute(sql, (id,))
    user = cursor.fetchone()

    cursor.close()
    conn.close()

    return user

#aggiungo utente

def add_user(user):
    conn = sqlite3.connect('db/Affitti.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    success = False

    #se è locatore, il campo "locatore" sarà true, altrimenti sarà false
    if user['locatore']=='locatore': 
        user['locatore']=True
    else:
        user['locatore']=False

    sql = 'INSERT INTO UTENTI(nickname,password,locatore) VALUES(?,?,?)'

    try:
        cursor.execute(
            sql, (user['nickname'], user['password'], user['locatore']))
        conn.commit()
        success = True
    except Exception as e:
        print('ERROR', str(e))
        # se qualcosa da errore: rollback
        conn.rollback()

    cursor.close()
    conn.close()

    return success

#prendo tutti gli utenti

def get_users():
    conn = sqlite3.connect('db/Affitti.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    sql = 'SELECT * FROM UTENTI'
    cursor.execute(sql)
    users = cursor.fetchall()

    cursor.close()
    conn.close()

    return users
