import os
from flask import Flask, render_template, request, send_from_directory, redirect, url_for
from flask_mail import Mail, Message
from dotenv import load_dotenv

# 1. Načtení proměnných z .env souboru
load_dotenv()

app = Flask(__name__)

# 2. Konfigurace aplikace a mail serveru z prostředí
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'default-dev-key')
app.config['MAIL_SERVER'] = os.getenv('MAIL_SERVER')
app.config['MAIL_PORT'] = int(os.getenv('MAIL_PORT', 587))
app.config['MAIL_USE_TLS'] = os.getenv('MAIL_USE_TLS') == 'True'
app.config['MAIL_USE_SSL'] = os.getenv('MAIL_USE_SSL') == 'True'
app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD')

# Nastavení výchozího odesílatele
app.config['MAIL_DEFAULT_SENDER'] = os.getenv('MAIL_DEFAULT_SENDER', os.getenv('MAIL_USERNAME'))

# Inicializace Mail rozšíření
mail = Mail(app)

# --- KONFIGURACE SEO METADAT ---
page_meta = {
    'home': {
        'title': 'ÚčtoVšem | Účetnictví, daně a krypto - Praha a Online',
        'description': 'Profesionální vedení účetnictví, zpracování mezd a daňová přiznání. Specializujeme se na firmy, OSVČ a zdanění kryptoměn. Působíme v Praze i online.'
    },
    'accounting': {
        'title': 'Vedení účetnictví Praha a Online | ÚčtoVšem',
        'description': 'Kompletní vedení účetnictví pro firmy i OSVČ. Zpracování dokladů, DPH, kontrolní hlášení a závěrky. Online přístup a lidský servis.'
    },
    'taxes': {
        'title': 'Daňové poradenství a přiznání Praha | ÚčtoVšem',
        'description': 'Zpracování daňových přiznání pro firmy i fyzické osoby. Specializujeme se na DPH, daň z příjmů a zdanění kryptoměn. Daňová optimalizace a poradenství.'
    },
    'payroll': {
        'title': 'Zpracování mezd a personalistika Praha | ÚčtoVšem',
        'description': 'Kompletní mzdová agenda a personalistika. Výpočet mezd, přihlášky zaměstnanců, komunikace s ČSSZ a zdravotními pojišťovnami.'
    },
    'privacy': {
        'title': 'Zásady ochrany osobních údajů | ÚčtoVšem',
        'description': 'Informace o zpracování a ochraně osobních údajů dle GDPR.'
    },
    'thank_you': {
        'title': 'Děkujeme za poptávku | ÚčtoVšem',
        'description': 'Vaše poptávka byla úspěšně odeslána.'
    }
}

# --- HLAVNÍ STRÁNKA ---
@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        # Zpracování formuláře
        jmeno = request.form.get('jmeno')
        email = request.form.get('email')
        telefon = request.form.get('telefon')
        zprava = request.form.get('zprava')
        
        # Sestavení obsahu e-mailu
        email_body = f"""
        Nová poptávka z webu ÚčtoVšem.cz
        
        Jméno: {jmeno}
        Email: {email}
        Telefon: {telefon}
        
        Zpráva:
        {zprava}
        """

        # Odeslání e-mailu
        try:
            recipient = os.getenv('MAIL_RECIPIENT')
            msg = Message(
                subject=f"Nová poptávka: {jmeno}",
                recipients=[recipient] 
            )
            msg.body = email_body
            msg.reply_to = email 
            
            mail.send(msg)
            print(f"--- EMAIL ODESLÁN NA {recipient} ---")
            
        except Exception as e:
            print(f"!!! CHYBA PŘI ODESÍLÁNÍ EMAILU !!!: {e}")
            # I při chybě přesměrujeme (log máme v konzoli), nebo můžeme zobrazit error stránku.
            # Pro uživatele je lepší "Success" zpráva, my chybu vyřešíme interně.
        
        # PŘESMĚROVÁNÍ NA DĚKOVACÍ STRÁNKU
        return redirect(url_for('thank_you_page'))

    return render_template('index.html', meta=page_meta['home'])

# --- DĚKOVACÍ STRÁNKA ---
@app.route('/dekujeme')
def thank_you_page():
    return render_template('thank-you.html', meta=page_meta['thank_you'])

# --- PODSTRÁNKY SLUŽEB ---
@app.route('/vedeni-ucetnictvi')
def accounting_page():
    return render_template('accounting.html', meta=page_meta['accounting'])

@app.route('/danove-poradenstvi')
def taxes_page():
    return render_template('taxes.html', meta=page_meta['taxes'])

@app.route('/mzdy-a-personalistika')
def payroll_page():
    return render_template('payroll.html', meta=page_meta['payroll'])

@app.route('/zasady-ochrany-osobnich-udaju')
def privacy():
    return render_template('privacy.html', meta=page_meta['privacy'])

# --- TECHNICKÉ SEO SOUBORY ---
@app.route('/sitemap.xml')
def sitemap():
    return send_from_directory(app.root_path, 'sitemap.xml')

@app.route('/robots.txt')
def robots():
    return send_from_directory(app.root_path, 'robots.txt')

# --- CHYBOVÁ STRÁNKA 404 ---
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 9020))
    app.run(debug=True, port=port, host='0.0.0.0')