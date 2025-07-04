from flask import Flask, request, send_file, render_template_string, flash, redirect
from werkzeug.utils import secure_filename
from PIL import Image
from io import BytesIO
import os

app = Flask(__name__)
app.secret_key = "your_secret_key"

# Allowed image types
ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "webp", "bmp", "tiff", "gif"}

# HTML Template as string
HTML_TEMPLATE = """
<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <title>Convert Image to JPG</title>
  <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="stylesheet">
</head>
<body class="bg-light py-5">
  <div class="container">
    <h1 class="mb-4 text-center">Convert Any Image to JPG</h1>
    {% with messages = get_flashed_messages() %}
      {% if messages %}
        <div class="alert alert-warning">{{ messages[0] }}</div>
      {% endif %}
    {% endwith %}
    <form method="POST" enctype="multipart/form-data" class="card p-4 shadow-sm">
      <div class="mb-3">
        <input class="form-control" type="file" name="image" required>
      </div>
      <button class="btn btn-primary">Convert & Download JPG</button>
    </form>
  </div>
</body>
</html>
"""

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route("/", methods=["GET", "POST"])
def upload_file():
    if request.method == "POST":
        file = request.files.get("image")
        if not file or file.filename == '':
            flash("No file selected.")
            return redirect(request.url)
        if not allowed_file(file.filename):
            flash("Unsupported file type.")
            return redirect(request.url)

        # Secure and open the image
        filename = secure_filename(file.filename)
        image = Image.open(file).convert("RGB")

        # Convert and prepare in-memory file
        img_io = BytesIO()
        image.save(img_io, format='JPEG', quality=95)
        img_io.seek(0)

        download_name = os.path.splitext(filename)[0] + ".jpg"
        return send_file(
            img_io,
            mimetype='image/jpeg',
            as_attachment=True,
            download_name=download_name
        )

    return render_template_string(HTML_TEMPLATE)

if __name__ == "__main__":
    app.run(debug=True)
