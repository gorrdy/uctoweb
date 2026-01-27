import os
from flask import Flask, render_template, request, send_from_directory

app = Flask(__name__)

# --- KONFIGURACE SEO METADAT ---
# Zde můžete centrálně měnit titulky a popisky pro jednotlivé stránky
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
    }
}

# --- HLAVNÍ STRÁNKA ---
@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        # Zpracování formuláře
        jmeno = request.form.get('jmeno')
        email = request.form.get('email')
        sluzba = request.form.get('service')
        zprava = request.form.get('zprava')
        
        # Simulace odeslání (log do konzole)
        print(f"--- NOVÁ POPTÁVKA ---")
        print(f"Jméno: {jmeno}")
        print(f"Email: {email}")
        print(f"Služba: {sluzba}")
        print(f"Zpráva: {zprava}")
        print(f"---------------------")
        
        # Vrátíme stránku s potvrzením úspěchu
        return render_template('index.html', success=True, meta=page_meta['home'])

    return render_template('index.html', meta=page_meta['home'])

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
    # Hledá soubor v kořenovém adresáři aplikace (vedle app.py)
    return send_from_directory(app.root_path, 'sitemap.xml')

@app.route('/robots.txt')
def robots():
    # Hledá soubor v kořenovém adresáři aplikace (vedle app.py)
    return send_from_directory(app.root_path, 'robots.txt')

# --- CHYBOVÁ STRÁNKA 404 ---
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

if __name__ == '__main__':
    app.run(debug=True, port=9020, host='0.0.0.0')