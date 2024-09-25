from flask import Flask, request, render_template
import aspose.pdf as ap
import os

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

#check if the upload folder exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/')
def index():
    return '''
        <h1>Upload PDF to Print</h1>
        <form method="POST" enctype="multipart/form-data" action="/print">
            <input type="file" name="pdf_file" accept=".pdf">
            <input type="submit" value="Upload and Print">
        </form>
    '''

@app.route('/print', methods=['POST'])
def print_pdf():
    if 'pdf_file' not in request.files:
        return "No file part", 400

    file = request.files['pdf_file']
    
    if file.filename == '':
        return "No selected file", 400

    if file and file.filename.endswith('.pdf'):
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(file_path)

        #print the PDF using Aspose
        try:
            viewer = ap.facades.PdfViewer()
            viewer.bind_pdf(file_path)
            viewer.print_document()
            viewer.close()

            return "PDF printed successfully"
        except Exception as e:
            return f"Error printing PDF: {str(e)}", 500
    else:
        return "Invalid file type", 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
