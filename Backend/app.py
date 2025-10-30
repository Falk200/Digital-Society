from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import csv
import os
from datetime import datetime
import uuid

app = Flask(__name__)
CORS(app)  # Erlaubt Cross-Origin Requests vom Frontend

# CSV-Dateiname
CSV_FILE = 'survey_responses.csv'

# CSV-Datei initialisieren, falls sie nicht existiert
def init_csv():
    if not os.path.exists(CSV_FILE):
        with open(CSV_FILE, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow([
                'timestamp',
                'session_id',
                'q1_kosten',
                'q1_qualitaet',
                'q1_zeit',
                'q2_innovation',
                'q2_stabilitaet',
                'q2_effizienz'
            ])

@app.route('/submit', methods=['POST'])
def submit_response():
    try:
        data = request.json
        
        # Session-ID generieren
        session_id = str(uuid.uuid4())
        
        # Timestamp
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        # Daten extrahieren
        q1 = data.get('question1', {})
        q2 = data.get('question2', {})
        
        # In CSV schreiben
        with open(CSV_FILE, 'a', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow([
                timestamp,
                session_id,
                q1.get('Kosten', 0),
                q1.get('Qualität', 0),
                q1.get('Zeit', 0),
                q2.get('Innovation', 0),
                q2.get('Stabilität', 0),
                q2.get('Effizienz', 0)
            ])
        
        return jsonify({
            'success': True,
            'session_id': session_id,
            'message': 'Antwort erfolgreich gespeichert'
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/export', methods=['GET'])
def export_data():
    """Endpunkt zum Herunterladen der CSV-Datei"""
    try:
        if not os.path.exists(CSV_FILE):
            return jsonify({
                'success': False,
                'error': 'Keine Daten vorhanden'
            }), 404
        
        # CSV-Datei direkt senden
        from flask import send_file
        return send_file(
            CSV_FILE,
            mimetype='text/csv',
            as_attachment=True,
            download_name=f'survey_responses_{datetime.now().strftime("%Y%m%d_%H%M%S")}.csv'
        )
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/health', methods=['GET'])
def health_check():
    """Health Check Endpunkt"""
    return jsonify({'status': 'ok'}), 200

if __name__ == '__main__':
    # CSV initialisieren
    init_csv()
    
    print("Server startet auf http://localhost:5000")
    print(f"Antworten werden in '{CSV_FILE}' gespeichert")
    print("\nVerfügbare Endpunkte:")
    print("  POST /submit   - Antworten einreichen")
    print("  GET  /export   - Alle Daten abrufen")
    print("  GET  /health   - Server Status")
    
    app.run(debug=True, port=5000)
