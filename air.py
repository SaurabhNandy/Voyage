from flask import Flask, render_template, request
app = Flask(__name__)

@app.route('/aviair/home',methods = ['POST', 'GET'])
def home():
	airports=['Agartala (IXA)', 'Ahmedabad (AMD)','Prayagraj (IXD)', 'Amritsar (ATQ)', 'Bagdogra (IXB)','Bengaluru (BLR)', 'Bhopal (BHO)', 'Bhubaneswar (BBI)','Chandigarh (IXC)','Chennai (MAA)', 'Coimbatore (CJB)', 'Dehradun (DED)', 'Delhi (DEL)','Dibrugarh (DIB)', 'Dimapur (DMU)', 'Goa (GOI)','Gorakhpur (GOP)', 'Guwahati (GAU)','Hubli (HBX)', 'Hyderabad (HYD)', 'Imphal (IMF)', 'Indore (IDR)','Jabalpur (JLR)', 'Jaipur (JAI)', 'Jammu (IXJ)','Jorhat (JRH)', 'Kannur (CNN)', 'Kochi (COK)','Kolkata (CCU)', 'Kozhikode (CCJ)','Lucknow (LKO)', 'Madurai (IXM)','Mangalore (IXE)', 'Mumbai (BOM)', 'Nagpur (NAG)','Patna (PAT)', 'Port Blair (IXZ)','Pune (PNQ)', 'Raipur (RPR)', 'Rajahmundry (RJA)','Ranchi (IXR)', 'Srinagar (SXR)', 'Surat (STV)','Thiruvananthapuram (TRV)', 'Tiruchirappalli (TRZ)','Tirupati (TIR)',  'Udaipur (UDR)','Vadodara (BDQ)', 'Varanasi (VNS)','Vijayawada (VGA)', 'Visakhapatnam (VTZ)' ]
	if request.method=="POST":
		print(request.form)
		return render_template('home.html',airports=airports)
	else:
		return render_template('home.html',home='active',airports=airports)

if __name__ == '__main__':
   app.run(debug=True)