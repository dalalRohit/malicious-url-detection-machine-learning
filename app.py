from flask import Flask,render_template,request,redirect,url_for
import Feature_extraction as urlfeature
import pickle
import pandas as pd
import re
import numpy as np

app = Flask(__name__)


#----------------------------PICKLE--------------------
Pkl_Filename = "my_model.pkl"
with open(Pkl_Filename, 'rb') as file:
    rf_model = pickle.load(file)


# ----------------------------HELPER FUNCTIONS-----------------
train_cols=['token_count',
 'rank_host',
 'rank_country',
 'ASNno',
 'sec_sen_word_cnt',
 'avg_token_length',
 'No_of_dots',
 'Length_of_url',
 'avg_path_token',
 'IPaddress_presence',
 'Length_of_host',
 'safebrowsing',
 'avg_domain_token_length',
 'path_token_count',
 'largest_domain',
 'domain_token_count',
 'largest_path',
 'largest_token']

def get_nonstring_cols(data_cols):
	cols_to_keep=[]
	train_cols=[]
	for col in data_cols:
		if col!='URL' and col!='host' and col!='path':
			cols_to_keep.append(col)
			if col!='malicious' and col!='result':
				train_cols.append(col)
	return [cols_to_keep,train_cols]

def get_link_from_text(sms):
	url = re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+] |[!*\(\), ]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', sms) 
	return url 

# -----------------------FLASK ROUTES------------------------

#GET /
@app.route('/')
def main():
	if(request.args):
		ans=request.args.get('ans')
		error=request.args.get('error')
		return render_template('index.html',ans=ans,error=error)
	else:
		return render_template('index.html')

#POST /submit
@app.route('/submit',methods = ['POST'])
def submit():
	if(request.method=='POST'):
		features=[]
		sms=request.form['msg']
		url=''
		for w in sms.split(' '):
			if(w.startswith('https:') or w.startswith('http:') or w.startswith('www') ):
				url=w

		if url != '':
			url=str(url)
			features.append(urlfeature.feature_extract(url))

			df=pd.DataFrame(features)
			ans=rf_model.predict(df[train_cols])
			print('URL is: ',url)
			print('\n ANS  is: ',ans)

			return {'features':features}
		else:
			error='Please enter a valid URL'
			return redirect(url_for('main'))


app.run(debug=True)