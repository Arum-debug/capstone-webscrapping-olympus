from flask import Flask, render_template
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
from io import BytesIO
import base64
from bs4 import BeautifulSoup 
import requests

#don't change this
matplotlib.use('Agg')
app = Flask(__name__) #do not change this

#insert the scrapping here
url_get = requests.get('https://www.exchange-rates.org/history/IDR/USD/T')
soup = BeautifulSoup(url_get.content,"html.parser")

#find your right key here
table = soup.find('div', attrs={'class':'table-responsive'})
row = table.find_all('tr', attrs={'td':''})

row_length = len(row)

temp = [] #initiating a list 

for i in range(1, row_length):
#insert the scrapping process here
    
    data = table.find_all('tr', attrs={'td':''})[i].text
       
    temp.append((data)) 

temp = temp[::-1]

#change into dataframe
df = pd.DataFrame(temp, columns = ['data'])
 
#insert data wrangling here
df[['a','b','c','d','e','f']]= df.data.str.split(expand=True)
df1 = df.drop(['data','b','c','d','e'], axis = 1)
df1['exchange_rates'] = df1['a'].str[-12:]
df2 = df1.drop(['a'], axis=1)
df2['date'] = df2['f'].astype('datetime64')
df3 = df2.drop(['f'], axis = 1)
df3['exchange_rates_clean'] = df3['exchange_rates'].str.replace(',', '')
df4 = df3.drop(['exchange_rates'], axis=1)
df4['exchange_rates_clean'] = df4['exchange_rates_clean'].astype('float64').round()
df4 = df4.set_index(['date'])
df4['exchange_rates'] = df4['exchange_rates_clean']
df4 = df4.drop(['exchange_rates_clean'], axis=1)
#end of data wranggling 

@app.route("/")
def index(): 
	
	card_data = f'{df4["exchange_rates"].mean().round(2)}' #be careful with the " and ' 

	# generate plot
	ax = df4.plot(figsize = (20,9)) 
	
	# Rendering plot
	# Do not change this
	figfile = BytesIO()
	plt.savefig(figfile, format='png', transparent=True)
	figfile.seek(0)
	figdata_png = base64.b64encode(figfile.getvalue())
	plot_result = str(figdata_png)[2:-1]

	# render to html
	return render_template('index.html',
		card_data = card_data, 
		plot_result=plot_result
		)


if __name__ == "__main__": 
    app.run(debug=True)