from flask import * 
from flask import jsonify
import sentiment_mod as s
import os
#import main_ocr_aadhar as ocr

app = Flask(__name__)  
  
@app.route('/sentiment',methods=['POST', 'GET']) 
def sentiment():
	if request.method == 'POST':
		data = request.get_json()
		print(data["text"])
		return jsonify(s.sentiment(data["text"]))


# @app.route('/aadhar_ocr',methods=['POST', 'GET']) 
# def aadhar_ocr():
# 	if request.method == 'POST':
# 		data = request.get_json()
# 		im_b64=data["payload"]
# 		return jsonify(ocr.main(data["text"],im_b64))

port = int(os.environ.get("PORT", 5000))
if __name__ == '__main__':  
   app.run(debug = True, host='0.0.0.0', port=port)  