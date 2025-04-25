from flask import Flask, request, jsonify
from flask_cors import CORS
import os
from werkzeug.utils import secure_filename
from ocr_service import process_image  # Cambiado a usar ocr_service en lugar de aws_ocr_service

app = Flask(__name__)
CORS(app)  # Habilitar CORS para todas las rutas

# Configuraciones
UPLOAD_FOLDER = 'uploads'  # Directorio local para desarrollo
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'tiff', 'pdf'}

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/upload-ocr', methods=['POST'])
def upload_ocr():
    # Verificar si la petición contiene un archivo
    if 'file' not in request.files:
        return jsonify({"error": "No se encontró ningún archivo"}), 400
    
    file = request.files['file']
    
    # Si el usuario no selecciona un archivo
    if file.filename == '':
        return jsonify({"error": "No se seleccionó ningún archivo"}), 400
    
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        try:
            # Procesar la imagen con OCR usando Tesseract
            result = process_image(filepath)  # Usando la función de ocr_service.py
            
            # Verificar si se extrajo texto
            if not result or not result.strip():
                return jsonify({
                    "error": "No se pudo extraer texto de la imagen",
                    "text": ""
                }), 422
            
            return jsonify({"text": result})
            
        except Exception as e:
            return jsonify({"error": f"Error al procesar la imagen: {str(e)}"}), 500
        finally:
            # Limpiar el archivo después de procesarlo
            if os.path.exists(filepath):
                os.remove(filepath)
    else:
        return jsonify({"error": "Tipo de archivo no permitido"}), 400

# Manejo de error para archivos muy grandes
@app.errorhandler(413)
def too_large(e):
    return jsonify({"error": "El archivo es demasiado grande"}), 413

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=True, host='0.0.0.0', port=port)