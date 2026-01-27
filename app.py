import os
import markdown
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

# --- FUNKCE PRO BLOG ---
def get_posts():
    posts = []
    posts_dir = os.path.join(app.root_path, 'posts')
    
    # Pokud složka neexistuje, vrátíme prázdný seznam
    if not os.path.exists(posts_dir):
        return []

    for filename in os.listdir(posts_dir):
        print(f"Načítám soubor: {filename}")
        if filename.endswith('.md'):
            filepath = os.path.join(posts_dir, filename)
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
                
                # Vytvoříme Markdown objekt s podporou metadat
                md = markdown.Markdown(extensions=['meta'])
                md.convert(content)
                
                # Získáme metadata (titulek, datum...)
                if hasattr(md, 'Meta'):
                    meta = md.Meta
                    # Slug (URL adresa) bude název souboru bez .md
                    meta['slug'] = [filename[:-3]]
                    # Metadata jsou v listech, vezmeme první položku
                    post = {
                        'title': meta.get('title', ['Bez názvu'])[0],
                        'date': meta.get('date', [''])[0],
                        'description': meta.get('description', [''])[0],
                        'image': meta.get('image', [''])[0],
                        'slug': filename[:-3]
                    }
                    posts.append(post)
    
    # Seřadíme podle data (nejnovější nahoře)
    posts.sort(key=lambda x: x['date'], reverse=True)
    return posts

def get_single_post(slug):
    posts_dir = os.path.join(app.root_path, 'posts')
    filepath = os.path.join(posts_dir, f"{slug}.md")
    
    if not os.path.exists(filepath):
        return None
        
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
        md = markdown.Markdown(extensions=['meta'])
        html_content = md.convert(content)
        meta = md.Meta
        
        post = {
            'title': meta.get('title', ['Bez názvu'])[0],
            'date': meta.get('date', [''])[0],
            'image': meta.get('image', [''])[0],
            'content': html_content
        }
        return post

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
    },
    'blog': {
        'title': 'Blog a Novinky | ÚčtoVšem',
        'description': 'Aktuální informace ze světa účetnictví, daní a mezd. Rady a tipy pro podnikatele.'
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

# --- NOVÉ ROUTY PRO BLOG ---
@app.route('/blog')
def blog_list():
    posts = get_posts()
    return render_template('blog.html', posts=posts, meta=page_meta['blog'])

@app.route('/blog/<slug>')
def blog_detail(slug):
    post = get_single_post(slug)
    if post is None:
        return render_template('404.html'), 404
        
    # Dynamická metadata pro konkrétní článek
    meta = {
        'title': f"{post['title']} | Blog ÚčtoVšem",
        'description': post['title'] # Nebo description z MD, pokud bychom ho načítali i v detailu
    }
    return render_template('post.html', post=post, meta=meta)

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