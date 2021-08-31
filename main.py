import os
import shutil
import pathlib
from datetime import datetime

from flask import Flask, render_template, request, send_file, request, jsonify
from mask_image import image_mask_resize

app = Flask(__name__)
APP_ROOT = APP_ROOT = os.path.dirname(os.path.abspath(__file__))


@app.route("/", methods=["GET", "POST"])
def index():
    upload_path = os.path.join(APP_ROOT, 'static/images_for_mask/')
    download_path = os.path.join(APP_ROOT, 'static/masked_images/')

    if not os.path.isdir(upload_path):
        os.mkdir(upload_path)

    if request.method == 'POST':
        
        category = request.form["category"].strip()
        usage = request.form["usage"].strip()
        
        dateTimeObj = datetime.now()
        timestampStr = dateTimeObj.strftime("%d-%b-%Y-%H-%M-%S-%f")
        
        new_folder_name = f"{category}-{usage}-{timestampStr}/"
        
        final_upload_path = os.path.join(upload_path, new_folder_name)
        
        os.mkdir(final_upload_path)
        
        for file in request.files.getlist("images"):
            sku = file.filename[:6]
            file_extension = pathlib.PurePosixPath(file.filename).suffix
            file.save(final_upload_path + f"{sku}-{category}-{usage}-{file.filename}")
            
        image_mask_resize(new_folder_name)

        shutil.make_archive(new_folder_name, "zip", os.path.join(download_path, new_folder_name))

        return send_file(f"{new_folder_name.rstrip(new_folder_name[-1])}.zip", as_attachment=True)

    return render_template("index.html")


if __name__ == '__main__':
    app.run(host='0.0.0.0')
    app.debug(True)
