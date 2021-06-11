import smtplib
from bs4 import BeautifulSoup
import requests
import eel
from email.message import EmailMessage
import matplotlib.pyplot as plt
import pandas as pd

message = ""
eel.init('web')


@eel.expose
def bar(type):
	df = pd.read_csv(r"flipkart.csv")
	data = df.sort_values([f"{type}"], axis=0, ascending=False)[:10]
	name = []
	for x in data['Name']:
		if (len(x)>15):
			x = x[:15]+'...'
		name.append(x)
	y = [x for x in data[f'{type}']]
	name.reverse()
	y.reverse()
	fig = plt.figure(figsize=(9.8,5))
	ax1 = fig.add_subplot(1,1,1)
	ax1.barh(name,y, color = 'orange')
	ax1.set_title(f'{type} comparison')
	ax1.set_xlabel(f'{type}')
	fig.subplots_adjust(left=0.25)
	plt.show()

@eel.expose
def selector(category, max_price):
	max_price = int(max_price)
	global URL
	URL=''
	global no_pages
	global category1
	category1 = category
	if category == 'camera':
		if max_price<=50000:
			URL += 'https://www.flipkart.com/search?sid=jek%2Cp31%2Ctrv&otracker=CLP_Filters&p%5B%5D=facets.price_range.from%3DMin&sort=price_desc&p%5B%5D=facets.price_range.to%3D50000&page='
			no_pages = 2
		elif max_price<=300000:
			URL += 'https://www.flipkart.com/search?sid=jek%2Cp31%2Ctrv&otracker=CLP_Filters&p%5B%5D=facets.price_range.from%3DMin&p%5B%5D=facets.price_range.to%3DMax&sort=price_desc&page='
			no_pages = 5 #6
	elif category == 'mobile':
		if max_price<=4000:
			URL += 'https://www.flipkart.com/search?sid=tyy%2C4io&otracker=CLP_Filters&p%5B%5D=facets.price_range.from%3DMin&sort=price_desc&p%5B%5D=facets.price_range.to%3D4000&page='
			no_pages = 281
		elif max_price<=7000:
			URL += 'https://www.flipkart.com/search?sid=tyy%2C4io&otracker=CLP_Filters&p%5B%5D=facets.price_range.from%3DMin&sort=price_desc&p%5B%5D=facets.price_range.to%3D7000&page='
			no_pages = 66
		elif max_price<=10000:
			URL += 'https://www.flipkart.com/search?sid=tyy%2C4io&otracker=CLP_Filters&p%5B%5D=facets.price_range.from%3DMin&sort=price_desc&p%5B%5D=facets.price_range.to%3D10000&page='
			no_pages = 36
		elif max_price<=20000:
			URL += 'https://www.flipkart.com/search?sid=tyy%2C4io&otracker=CLP_Filters&p%5B%5D=facets.price_range.from%3DMin&sort=price_desc&p%5B%5D=facets.price_range.to%3D20000&page='
			no_pages = 37
		elif max_price<=30000:
			URL += 'https://www.flipkart.com/search?sid=tyy%2C4io&otracker=CLP_Filters&p%5B%5D=facets.price_range.from%3DMin&sort=price_desc&p%5B%5D=facets.price_range.to%3D30000&page='
			no_pages = 10
		elif max_price<=50000:
			URL += 'https://www.flipkart.com/search?sid=tyy%2C4io&otracker=CLP_Filters&p%5B%5D=facets.price_range.from%3DMin&sort=price_desc&p%5B%5D=facets.price_range.to%3D50000&page='
			no_pages = 12
		elif max_price<=200000:
			URL += 'https://www.flipkart.com/search?sid=tyy%2C4io&otracker=CLP_Filters&p%5B%5D=facets.price_range.from%3DMin&p%5B%5D=facets.price_range.to%3DMax&sort=price_desc&page='
			no_pages = 10 #129
	else :
		if max_price<=30000:
			URL += 'https://www.flipkart.com/search?sid=6bo%2Cb5g&otracker=CLP_Filters&p%5B%5D=facets.price_range.from%3DMin&sort=price_desc&p%5B%5D=facets.price_range.to%3D30000&page='
			no_pages = 3
		elif max_price<=40000:
			URL += 'https://www.flipkart.com/search?sid=6bo%2Cb5g&otracker=CLP_Filters&p%5B%5D=facets.price_range.from%3DMin&sort=price_desc&p%5B%5D=facets.price_range.to%3D40000&page='
			no_pages = 5
		elif max_price<=50000:
			URL += 'https://www.flipkart.com/search?sid=6bo%2Cb5g&otracker=CLP_Filters&p%5B%5D=facets.price_range.from%3DMin&sort=price_desc&p%5B%5D=facets.price_range.to%3D50000&page='
			no_pages = 5
		elif max_price<=60000:
			URL += 'https://www.flipkart.com/search?sid=6bo%2Cb5g&otracker=CLP_Filters&p%5B%5D=facets.price_range.from%3DMin&sort=price_desc&p%5B%5D=facets.price_range.to%3D60000&page='
			no_pages = 5
		elif max_price<=75000:
			URL += 'https://www.flipkart.com/search?sid=6bo%2Cb5g&otracker=CLP_Filters&p%5B%5D=facets.price_range.from%3DMin&sort=price_desc&p%5B%5D=facets.price_range.to%3D75000&page='
			no_pages = 5
		elif max_price<=400000:
			URL += 'https://www.flipkart.com/search?sid=6bo%2Cb5g&otracker=CLP_Filters&p%5B%5D=facets.price_range.from%3DMin&p%5B%5D=facets.price_range.to%3DMax&sort=price_desc&page='
			no_pages = 10

@eel.expose
def sendemail(max_price,email):
	global counter
	counter = 0
	def get_data(pageNo):
		headers = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:66.0) Gecko/20100101 Firefox/66.0", "Accept-Encoding":"gzip, deflate", "Accept":"text/html,application/xhtml+xml,application/xml ;q=0.9,*/*;q=0.8", "DNT":"1", "Connection":"close", "Upgrade-Insecure-Requests":"1"}
		global URL
		global category1
		global counter
		URL += f'{pageNo}'
		r = requests.get(URL, headers=headers)#, proxies=proxies)
		content = r.content
		soup = BeautifulSoup(content, 'lxml')
		alls = []
		for d in soup.find_all('div', attrs={'class':'_3O0U0u'}):
			price = d.find('div', attrs={'class':'_1vC4OE _2rQ-NK'}).text
			price = int(price[1:].replace(",",""))
			if (price < int(max_price)) :
				counter += 1
				all1=[]
				name = d.find('div', attrs={'class':'_3wU53n'}).text
				rating = d.find('div', attrs={'class':'hGSR34'})
				users_rated = d.find('span', attrs={'class':'_38sUEc'})
				if name is not None:
					if (category1 == 'camera'):
						all1.append(name)
					elif (category1 == 'mobile'):
						all1.append(name)
					else:
						all1.append(name.split("(")[0][:-3])
				else:
					all1.append("unknown-product")
				if rating is not None:
					all1.append(rating.text)
				else:
					all1.append('')
				if users_rated is not None:
					all1.append(users_rated.find('span').find('span').text.split(" ")[0])
				else:
					all1.append('0')
				if price is not None:
					all1.append(price)
				else:
					all1.append('0')
				alls.append(all1)
				if category1 == 'laptop':
					if name is not None:
						all1.append(name.split("(")[1].split(")")[0])
					else:
						all1.append("N/A")
			if counter >= 14 :
				break
			else:
				continue
		return alls
	def send_mail(all_item):
		server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
		server.login('email', 'password')
		global category1
		global URL
		URL += '1'
		msg = EmailMessage()
		html = f"""\
			<!DOCTYPE html>
			<html>
			<head>
				<meta charset="utf-8">
				<meta name="viewport" content="width=device-width">
				<meta http-equiv="X-UA-Compatible">

				<link href="https://fonts.googleapis.com/css?family=Josefin+Sans:300,400,600,700|Lato:300,400,700" rel="stylesheet">
				<link href="'https://fonts.googleapis.com/css?family=Cabin:400,500,700|Montserrat:400,500,700'" rel="stylesheet">
			</head>

			<body width="100%" style="margin: 0; padding: 0 !important; background-color: #111111;">
				<center style="width: 100%;" width="100%">
					<div style="max-width: 600px; margin: 0 auto;">
					<table align="center" role="presentation" cellspacing="0" cellpadding="0" border="0" width="100%" style="margin: auto;">
						<tr style="text-align:center; background: #ffffff;">
							<td>
							<h1 style = "font-family: 'Cabin', sans-serif; color:black">Flipkart Scraper</h1>
		"""
		if all_item:
			html += f"""\
							<h3 style = "font-family: 'Cabin', sans-serif; color: #505050">{category1}s under Rs. {max_price}</h3>
							</td>
						</tr>
					</table>
					<table align="center" role="presentation" cellspacing="0" cellpadding="0" border="0" width="100%" style="margin: auto;">
			"""
			msg['Subject'] = "Price fell down ! Hurry !"
			body = f"{category1}\n\n"
			counter = 0
			for item in all_item:
				if item:
					if category1 == 'laptop':
						laptop_text = f" with spec: {item[1]},"
						laptop_html = f"<p>{item[4]}</p>"
					else:
						laptop_text = ""
						laptop_html = "\n "
					if item[1]:
						rating = f': {item[1]}/5'
					else:
						rating = ""
					if (counter % 2) ==  0:
						ppt = {'bg':'#f1c638', 'btn':'#ffffff'}
					else:
						ppt = {'bg':'#ffffff', 'btn':'#f1c638'}
					body += f'{item[0]}{laptop_text} is available at Rs. {item[3]}\n{item[2]} costumers rated {item[1]}/5\n\n'
					html += f"""\
        <tr style="background: {ppt['bg']}">
            <td width="70%">
                <div style="padding-left:10%">
                    <b><h3>{item[0]}</h3></b>
					{laptop_html}
                    <p>{item[2]} costumers rated {rating}</p>
                </div>
            </td >
            <td>
                <div style="text-align:center">
                    <h4 style="margin-top:0px">Rs. {item[3]}</h4>
					<a href="{URL}" style="margin-top:-10px;display:inline-block;font-weight:400;text-align:center;white-space:nowrap;vertical-align:middle;-webkit-user-select:none;-moz-user-select:none;-ms-user-select:none;user-select:none;border:1px solid transparent;padding:.375rem .75rem;font-size:1rem;line-height:1.5;color: #000000;border-radius:.25rem;background-color:{ppt['btn']};border-color:{ppt['btn']};text-decoration:none;">Shop Now</a>
                </div>
            </td>
        </tr>
					"""
				counter += 1
			body += f'check the flipkart link {URL}'
			html += """\
		</table>
			"""
		else:
			msg['Subject']= f"Sorry, no {category1} found"
			body = f"No {category1} is available under {max_price}"
			html += f"""\
				<h3 style = "font-family: 'Cabin', sans-serif; color: #505050">No {category1} is found under Rs. {max_price}</h3>
            	</td>
            </tr>
        </table>
			"""
		html += """\
	<table align="center" role="presentation" cellspacing="0" cellpadding="0" border="0" width="100%" style="margin: auto;">
        <tr style="background: #000000;color:#505050;">
			<td><center>
                <b><h3 style="margin-bottom:-15px">RIG</h3></b>
                <p style="margin-bottom:-15px">Flipkart Scraper</p>
                <p>developed by Amirul Haqe</p>
			</center></td>
        </tr>
	</table>
    </div>
    </center>
</body>
</html>
		"""
		msg.set_content(body)
		msg.add_alternative(html, subtype = 'html')
		server.sendmail('amiruldev1@gmail.com', email , msg.as_string())
		server.quit()
	results = []
	global no_pages
	for i in range(1, no_pages+1):
		if counter < 14 :
			results.append(get_data(i))
		else :
			break
	flatten = lambda l: [item for sublist in l for item in sublist]
	send_mail(flatten(results))

@eel.expose
def save(max_price):
	global counter2
	counter2 = 0
	def get_data(pageNo):
		headers = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:66.0) Gecko/20100101 Firefox/66.0", "Accept-Encoding":"gzip, deflate", "Accept":"text/html,application/xhtml+xml,application/xml ;q=0.9,*/*;q=0.8", "DNT":"1", "Connection":"close", "Upgrade-Insecure-Requests":"1"}
		global URL
		global category1
		global counter2
		URL += f'{pageNo}'
		r = requests.get(URL, headers=headers)#, proxies=proxies)
		content = r.content
		soup = BeautifulSoup(content, 'lxml')
		alls = []
		for d in soup.find_all('div', attrs={'class':'_3O0U0u'}):
			price = d.find('div', attrs={'class':'_1vC4OE _2rQ-NK'}).text
			price = int(price[1:].replace(",",""))
			if (price < int(max_price)):
				counter2 += 1
				all1=[]
				name = d.find('div', attrs={'class':'_3wU53n'}).text
				rating = d.find('div', attrs={'class':'hGSR34'})
				users_rated = d.find('span', attrs={'class':'_38sUEc'})
				if name is not None:
					if (category1 == 'camera'):
						all1.append(name)
					elif (category1 == 'mobile'):
						all1.append(name)
					else:
						all1.append(name.split("(")[0][:-3])
				else:
					all1.append("unknown-product")
				if rating is not None:
					all1.append(rating.text)
				else:
					all1.append('')
				if users_rated is not None:
					all1.append(users_rated.find('span').find('span').text.split(" ")[0])
				else:
					all1.append('0')
				if price is not None:
					all1.append(price)
				else:
					all1.append('0')
				alls.append(all1)
				if category1 == 'laptop':
					if name is not None:
						all1.append(name.split("(")[1].split(")")[0])
					else:
						all1.append("N/A")
			if counter2 >= 20 :
				break
			else:
				continue
		return alls
	results = []
	global no_pages
	global category1
	for i in range(1, no_pages+1):
		if counter2 < 20:
			results.append(get_data(i))
		else:
			break
	flatten = lambda l: [item for sublist in l for item in sublist]
	data = (flatten(results))
	if category1 =='laptop':
		df = pd.DataFrame(data, columns=['Name', 'Rating', 'Customers', 'Price', 'Spec'])
	else:
		df = pd.DataFrame(data, columns=['Name', 'Rating', 'Customers', 'Price'])
	df.to_csv(r'flipkart.csv', index=False, encoding='utf-8')

eel.start('index.html', port = 8002, size=(1000, 600))
