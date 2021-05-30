import requests
import html2text
import csv

append = str(input("Append to Dataset? (y/n): "))
endyear = str(input("End Year: "))
pageamount = int(input("Page Amount: "))
path = str(input("Manual (m) or Automatic (a): "))
cinp = ""
companies = ""
camount = 0

if path == 'm':
	print("Companies (press 'q' to exit): ")

	while cinp != "Q|":
		cinp = "{}|".format(str(input("- ")))
		cinp = cinp.upper()
		companies += cinp
		camount += 1

	companies = companies[:-2]

elif path == 'a':
	with open('D:\\Users\\Koral Kulacoglu\\python\\stocklist.csv', 'r') as file:  
		reader = csv.reader(file)
		for row in reader:
			companies += row[0]

	for row in companies:
		if row == "|":
			camount += 1

for cnum in range(camount):
	company = companies[:companies.index("|")]
	companies = companies[companies.index("|")+1:]

	stop = 0
	full = 0
	while full < pageamount and stop == 0: #lenght of page amount and year limit
		newslist = "http://markets.financialcontent.com/stocks/quote/news?Symbol={}&CurrentPage={}&Limit=300".format(company,full)
		info = requests.get(newslist)
		raw = str(info.text)
		tx = html2text.HTML2Text()
		newspage = tx.handle(raw)
		newsite = "More](http://markets.financialcontent.com/stocks/news/read/"
		ip = ""

		#gathers news links
		l = 0
		while l != len(newspage):
			if newspage[l:l+59] == newsite:
				while newspage[l] != "\n" and l < len(newspage):
					ip += newspage[l]
					l += 1
			else:
				l += 1

		if newsite not in ip:
			stop = 1

		for row in range(len(ip)):
			if ip[row:row+5] == "More]":
				ip = ip[:row] + ip[row+5:]

		total = 0
		for row in ip:
			if row == "(":
				total += 1

		#goes through news links
		cycle = 0
		while "(" in ip and stop == 0:
			cycle += 1
			ip = ip[1:]

			if "(" in ip:
				article = ip[:ip.index("(")]
				ip = ip[ip.index("("):]
			else:
				article = ip

			info = requests.get(article)
			raw = str(info.text)
			tx = html2text.HTML2Text()
			tx.ignore_links = True
			news = tx.handle(raw)
			date = ""

			#gets rid of non-words
			l = 0
			while l != len(news) - 45:
				if " " not in news[l:l+45]:
					while news[l] != " " and l != len(news) - 45:
						news = news[:l] + news[l+1:]

				else:
					l += 1

			#filters random text
			for row in range(len(news)):
				if news[row:row+9] == "Related  " or news[row:row+12] == "Read More >>":
					news = news[:row]

			#finds date published
			for row in range(len(raw)):
				if raw[row:row+13] == "datePublished":
					while raw[row] != "<" and row < len(raw):
						date += raw[row]
						row += 1
			date = date[15:]
			
			#filters random text
			for row in range(len(news)):
				if news[row:row+2] == "AM" or news[row:row+2] == "PM":
					news = news[row+8:]

			#filters random text
			if "& News supplied by" in news:
				news = news[:news.index("& News supplied by")]

			l = 0
			while l != len(news):
				if news[l] == "|" or news[l-1:l+1] == "  " or news[l-1:l+1] == "\n\n":
					news = news[:l] + news[l+1:]
				else:
					l += 1

			if len(news) > 5000:
				news = news[:5000]

			#transforms dates
			if date[:7] == "January":
				s = "January"
				month = "Jan"
				monthn = "1"

			if date[:8] == "February":
				s = "February"
				month = "Feb"
				monthn = "2"

			if date[:5] == "March":
				s = "March"
				month = "Mar"
				monthn = "3"

			if date[:5] == "April":
				s = "April"
				month = "Apr"
				monthn = "4"

			if date[:3] == "May":
				s = "May"
				month = "May"
				monthn = "5"

			if date[:4] == "June":
				s = "June"
				month = "Jun"
				monthn = "6"

			if date[:4] == "July":
				s = "July"
				month = "Jul"
				monthn = "7"

			if date[:6] == "August":
				s = "August"
				month = "Aug"
				monthn = "8"

			if date[:9] == "September":
				s = "September"
				month = "Sep"
				monthn = "9"

			if date[:7] == "October":
				s = "October"
				month = "Oct"
				monthn = "10"

			if date[:8] == "November":
				s = "November"
				month = "Nov"
				monthn = "11"

			if date[:8] == "December":
				s = "December"
				month = "Dec"
				monthn = "12"

			day = date[len(s)+1:len(s)+3]
			year = date[len(s)+5:len(s)+9]

			date = "{} {}, {}".format(month,day,year)

			stocklink = "http://markets.financialcontent.com/stocks/quote/historical?Range=12&Symbol={}&Month={}&Year={}".format(company, monthn, year)

			info = requests.get(stocklink)
			raw = str(info.text)
			tx = html2text.HTML2Text()
			tx.ignore_links = True
			stock = tx.handle(raw)
			stock = stock[stock.index("Date | Open | High | Low | Close | Volume | Change (%)"):]
			change = ""

			if year not in stock:
				stop = 2
			
			if year == endyear:
				stop = 3

			#finds stock change based on date
			l = 0
			while stock[l:l+12] != date and l < len(stock):
				l += 1

			if l < len(stock):
				while stock[l] != "(":
					l += 1
				while stock[l] != ")":
					change += stock[l]
					l += 1

			if change == "":
				change = "(+0.00%"

			change = change[1:]

			pagec = format(cycle/total*100, ".2f")
			completion = format(((full+(float(pagec)*0.01))/pageamount+cnum)/camount*100, ".6f")
	
			if news[:13] != "# Bad Request" and year != endyear:
				print("\n"*100)
				print("{}%".format(completion))
				print("")
				print("Page {} of {}: {}%".format(full+1, pageamount, pagec))
				print("")
				print("Company {} of {}: ".format(cnum+1, camount) + company)
				print("")
				print("Date: " + date)
				print("")  
				print("Stock: " + change)
				print("")
				print("News: " + news[:news.find("\n")])
		
				if append == "y":
					with open('D:\\Users\\Koral Kulacoglu\\python\\news.csv','a') as file:
						file.write("\n{}|".format(company))
						file.write("{}|".format(date))
						file.write("{}|".format(change))
						file.write("{}||".format(news.encode('cp850','replace').decode('cp850')))

		full += 1

	print("\n"*100)
	print("{} COMPLETE".format(company))
	print("")

	if stop == 1 or full == pageamount:
		print("News Article Limit Reached")

	elif stop == 2:
		print("Historical Price Limit Reached")

	elif stop == 3:
		print("End Year Reached")

print("\n"*100)
print("FUNCTION COMPLETE")

# ©Koral Kulacoglu