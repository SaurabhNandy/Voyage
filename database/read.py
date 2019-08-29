import pandas as pd

data=pd.read_excel('FlightSchedule_6May_New.xlsx',skiprows=4)

#print(data.columns)
#print(data.head)

a=['Agartala (IXA)', 'Ahmedabad (AMD)','Prayagraj (IXD)', 'Amritsar (ATQ)', 'Bagdogra (IXB)','Bengaluru (BLR)', 'Bhopal (BHO)', 'Bhubaneswar (BBI)','Chandigarh (IXC)','Chennai (MAA)', 'Coimbatore (CJB)', 'Dehradun (DED)', 'Delhi (DEL)','Dibrugarh (DIB)', 'Dimapur (DMU)', 'Goa (GOI)','Gorakhpur (GOP)', 'Guwahati (GAU)','Hubli (HBX)', 'Hyderabad (HYD)', 'Imphal (IMF)', 'Indore (IDR)','Jabalpur (JLR)', 'Jaipur (JAI)', 'Jammu (IXJ)','Jorhat (JRH)', 'Kannur (CNN)', 'Kochi (COK)','Kolkata (CCU)', 'Kozhikode (CCJ)','Lucknow (LKO)', 'Madurai (IXM)','Mangalore (IXE)', 'Mumbai (BOM)', 'Nagpur (NAG)','Patna (PAT)', 'Port Blair (IXZ)','Pune (PNQ)', 'Raipur (RPR)', 'Rajahmundry (RJA)','Ranchi (IXR)', 'Srinagar (SXR)', 'Surat (STV)','Thiruvananthapuram (TRV)', 'Tiruchirappalli (TRZ)','Tirupati (TIR)',  'Udaipur (UDR)','Vadodara (BDQ)', 'Varanasi (VNS)','Vijayawada (VGA)', 'Visakhapatnam (VTZ)' ]
d=data[data.Origin.isin(a) & data.Destination.isin(a)]

#codes=['IXA', 'AMD', 'IXD', 'ATQ', 'IXB', 'BLR', 'BHO', 'BBI', 'IXC', 'MAA', 'CJB', 'DED', 'DEL', 'DIB', 'DMU', 'GOI', 'GOP', 'GAU', 'HBX', 'HYD', 'IMF', 'IDR', 'JLR', 'JAI', 'IXJ', 'JRH', 'CNN', 'COK', 'CCU', 'CCJ', 'LKO', 'IXM', 'IXE', 'BOM', 'NAG', 'PAT', 'IXZ', 'PNQ', 'RPR', 'RJA', 'IXR', 'SXR', 'STV', 'TRV', 'TRZ', 'TIR', 'UDR', 'BDQ', 'VNS', 'VGA', 'VTZ']
#name=['Maharaja Bir Bikram Airport','Sardar Vallabhbhai Patel International Airport','Prayagraj Airport','Sri Guru Ram Dass Jee International Airport','Bagdogra International Airport','Kempegowda International Airport','Raja Bhoja Airport','Biju Patnaik International Airport','Chandigarh Airport','Chennai International Airport','Coimbatore International Airport','Jolly Grant Airport','Indira Gandhi International Airport','Dibrugarh Airport','Dimapur Airport','Dabolim Airport','Gorakhpur Airport','Lokpriya Gopinath Bordoloi International Airport','Hubli Airport','Rajiv Gandhi Hyderabad International Airport','Imphal Airport','Devi Ahilya Bai Holkar Airport','Jabalpur Airport','Jaipur International Airport','Jammu Airport','Jorhat Airport','Kannur International Airport','Cochin International Airport','Netaji Subhash Chandra Bose International Airport','Kozhikode International Airport','Chaudhary Charan Singh International Airport','Madurai Airport','Mangalore International Airport','Chhatrapati Shivaji Maharaj International Airport','Dr. Babasaheb Ambedkar International Airport','Jay Prakash Narayan Airport','Veer Savarkar International Airport','Pune Airport','Swami Vivekananda Airport','Rajahmundry Airport','Birsa Munda Airport','Sheikh ul-Alam International Airport','Surat International Airport','Trivandrum International Airport','Tiruchirappalli International Airport','Tirupati International Airport','Maharana Pratap Airport','Vadodara Airport','Lal Bahadur Shastri Airport','Vijayawada International Airport','Visakhapatnam Airport']
#location=['Agartala', 'Ahmedabad', 'Prayagraj', 'Amritsar', 'Bagdogra', 'Bengaluru', 'Bhopal', 'Bhubaneswar', 'Chandigarh', 'Chennai', 'Coimbatore', 'Dehradun', 'Delhi', 'Dibrugarh', 'Dimapur', 'Goa', 'Gorakhpur', 'Guwahati', 'Hubli', 'Hyderabad', 'Imphal', 'Indore', 'Jabalpur', 'Jaipur', 'Jammu', 'Jorhat', 'Kannur', 'Kochi', 'Kolkata', 'Kozhikode', 'Lucknow', 'Madurai', 'Mangalore', 'Mumbai', 'Nagpur', 'Patna', 'Port', 'Pune', 'Raipur', 'Rajahmundry', 'Ranchi', 'Srinagar', 'Surat', 'Thiruvananthapuram', 'Tiruchirappalli', 'Tirupati', 'Udaipur', 'Vadodara', 'Varanasi', 'Vijayawada', 'Visakhapatnam']

'''
query='INSERT INTO Airports VALUES '
for i in range(len(codes)):
	query+="('"+codes[i]+"','"+name[i]+"','"+location[i]+"','India'), "
print(query)
'''

query='INSERT INTO Flights VALUES '

k=1
days=['MON','TUE','WED','THU','FRI','SAT','SUN']
for j,i in d.iterrows():
        x=i['Days Of Operation']
        if x=='Daily':
                x='/'.join(days)
        elif 'Every ' in x:
                x=x.replace('Every ','')
        elif 'Except ' in x:
                x=x.replace('Except ','').split('/')
                x='/'.join([c for c in days if c not in x])
        query+="("+str(k)+",'"+i['6E FlightNumber'].split('/')[0]+"','"+i['Origin'].split('(')[1][:3]+"','"+i['Destination'].split('(')[1][:3]+"','6E','"+i['Arrival(LT)']+"','"+i['Departure(LT)']+"','"+i['Flight Type']+"','"+x+"'),\n ";
        k+=1
print(query)




	
