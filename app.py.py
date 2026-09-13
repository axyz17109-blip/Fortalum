import os
from flask import Flask
from firebase_admin import credentials, initialize_app, firestore

# Si vas a usar un archivo JSON de credenciales (recomendado para producción fuera de Google Cloud):
# cred = credentials.Certificate("serviceAccountKey.json")
# initialize_app(cred)

# O si prefieres que use las credenciales por defecto (si configuras la variable de entorno en Render):
initialize_app()
db = firestore.client()

app = Flask(__name__)

@app.route("/")
def fortalum_api():
    """Ruta principal que escribe y lee Firestore"""
    
    # Escribir un documento de prueba en Firestore
    doc_ref = db.collection("Fortalum_acceso").document("cloud_run_test")
    doc_ref.set({
        "modulo": "API Python en la Nube (Render)",
        "estado": "Activo",
        "mensaje": "¡Hola desde mi servidor gratuito en línea!",
        "timestamp": firestore.SERVER_TIMESTAMP
    })

    # Leer los documentos actuales
    docs = db.collection("Fortalum_acceso").stream()
    resultados = []
    for doc in docs:
        resultados.append(f"ID: {doc.id} | Datos: {doc.to_dict()}")

    texto_respuesta = "¡Ejecución exitosa en la nube!\n\n" + "\n".join(resultados)
    return texto_respuesta, 200, {'Content-Type': 'text/plain; charset=utf-8'}

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)