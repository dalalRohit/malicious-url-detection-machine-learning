from flask import Flask,render_template,request,redirect,url_for
import Feature_extraction as urlfeature
import pickle
import pandas as pd

#----------------------------PICKLE--------------------
Pkl_Filename = "my_model.pkl"
with open(Pkl_Filename, 'rb') as file:
    rf_model = pickle.load(file)

app = Flask(__name__)

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


# -----------------------FLASK ROUTES------------------------

#GET /
@app.route('/')
def hello_world():
    return render_template('index.html')

#POST /submit
@app.route('/submit',methods = ['POST'])
def submit():
	if(request.method=='POST'):
		features=[]
		link=request.form['msg']
		if link != '':
			link=link.strip()
			features.append(urlfeature.feature_extract(link))

		df=pd.DataFrame(features)
		ans=rf_model.predict(df[train_cols])
		
		print(ans)
		
		# features.append(ans)
		# return redirect(url_for('/'))
		return {'features':features}

app.run(debug=True)