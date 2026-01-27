from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        # Zde zachytíme data z formuláře
        jmeno = request.form.get('jmeno') # Musíme přidat name="jmeno" do HTML
        email = request.form.get('email')
        sluzba = request.form.get('service')
        zprava = request.form.get('zprava')
        
        # Simulace odeslání (vypíše se do konzole serveru)
        print(f"--- NOVÁ POPTÁVKA ---")
        print(f"Jméno: {jmeno}")
        print(f"Email: {email}")
        print(f"Služba: {sluzba}")
        print(f"Zpráva: {zprava}")
        print(f"---------------------")
        
        # Zde by se normálně odesílal email
        return render_template('index.html', success=True)

    return render_template('index.html')

@app.route('/zasady-ochrany-osobnich-udaju')
def privacy():
    return render_template('privacy.html')

# Přidat tuto novou trasu (route)
@app.route('/sitemap.xml')
def sitemap():
    return send_from_directory('static', 'sitemap.xml')

@app.route('/robots.txt')
def robots():
    return send_from_directory('static', 'robots.txt')

if __name__ == '__main__':
    app.run(debug=True, port=9020, host='0.0.0.0')