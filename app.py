from flask import Flask, render_template, request
from app_function import AppFunc
import shutil
import os
app = Flask(__name__, static_folder="./templates/img")

# @app.route("/", methods=["GET", "POST"])
# def home():
#     return render_template("index.html")

# zip_list = [url_list, format_list, title_list, channel_list, thumbnail_list]
zip_list = [[]*i for i in range(5)]
af = AppFunc()

@app.route("/", methods=["GET", "POST"])
def convert():
    if request.method == "GET":
        return render_template("convert_block.html", zip_list=zip_list)
        
    else:
        alert = False
        alert2 = False
        alert3 = False

        if ("url" in request.form) and ("format" in request.form):
            url = request.form["url"]
            format = request.form["format"]

            try:
                result = af.connecton(url)
                if format == "Select Format":
                    raise Exception
            except Exception as e:
                alert = True
            
            else:
                appends = [url, format, result[0], result[1], result[2]]
                for l, a in zip(zip_list, appends):
                    l.append(a)
        
        elif True in ["delete" in r for r in request.form]:
            delete_num = int([r for r in request.form if "delete" in r][0].replace("delete",""))
            for l in zip_list:
                l.pop(delete_num)
        
        elif "download" in request.form:
            try:
                if len(zip_list[0]) > 0:
                    af.youtube_dl(zip_list[0])
                    af.convert_dl(zip_list[2], zip_list[1])
                else:
                    raise Exception
            except Exception as e:
                alert2 = "[Error] : Could not convert files \n detail : " + str(e)

            else:
                shutil.make_archive('youtube_dl', format='zip', root_dir=af.savedir)
                shutil.move(str(os.getcwd())+"/youtube_dl.zip", str(os.environ['HOME'])+"/Downloads/")
                alert3 = "Download Success! check your download directory"

                for l in zip_list:
                    l.clear()
        
        return render_template("convert_block.html", alert=alert, alert2=alert2, alert3=alert3, zip_list=zip_list)


@app.route("/terms")
def terms():
    return render_template("terms_block.html")

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5596, debug=True)

