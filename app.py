from flask import Flask, request, jsonify
from flask_cors import CORS
import csv, smtplib, ssl, os

app = Flask(__name__)
CORS(app)  # active CORS pour toutes les routes (autorise les requêtes cross-origin):contentReference[oaicite:6]{index=6}

# Route POST pour recevoir la soumission du formulaire
@app.route('/submit', methods=['POST'])
def submit():
    # Récupérer les données JSON envoyées
    data = request.get_json()
    name = data.get('nom') or data.get('name')
    email = data.get('email')
    message = data.get('message')
    # Vérifier que tous les champs sont présents
    if not (name and email and message):
        return jsonify({'status': 'error', 'message': 'Champs manquants'}), 400

    # Enregistrer dans le fichier CSV (en créant s'il n'existe pas, et en ajoutant une ligne)
    try:
        with open('data.csv', 'a', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow([name, email, message])
    except Exception as e:
        return jsonify({'status': 'error', 'message': 'Impossible d\'écrire le fichier CSV'}), 500

    # Préparer et envoyer l'email via SMTP Gmail
    try:
        sender_email = os.environ.get('EMAIL_USER')        # adresse Gmail utilisée pour envoyer
        sender_password = os.environ.get('EMAIL_PASS')     # mot de passe d'application Gmail:contentReference[oaicite:7]{index=7}
        receiver_email = os.environ.get('EMAIL_RECEIVER', sender_email)
        subject = "Nouvelle soumission SmartService"
        body = f"Nom: {name}\nEmail: {email}\nMessage: {message}"
        # Le message commence par 'Subject: ...' + deux sauts de ligne pour séparer objet et corps:contentReference[oaicite:8]{index=8}
        email_text = f"Subject: {subject}\n\n{body}"

        # Envoyer l'email en TLS
        context = ssl.create_default_context()
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls(context=context)
            server.login(sender_email, sender_password)
            server.sendmail(sender_email, receiver_email, email_text)
    except Exception as e:
        return jsonify({'status': 'error', 'message': 'Échec de l\'envoi du mail'}), 500

    # Tout s'est bien passé
    return jsonify({'status': 'success'}), 200

if __name__ == '__main__':
    app.run()
