from bs4 import BeautifulSoup
import nltk

html_doc = """
\n\n\n\n\n\n\n\n<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 3.2//EN">\n<html>\n<head>\n<title>The BodgeIt Store</title>\n<link href="style.css" rel="stylesheet" type="text/css" />\n<script type="text/javascript" src="./js/util.js"></script>\n</head>\n<body>\n\n<center>\n<table width="80%" class="border">\n<tr BGCOLOR=#C3D9FF>\n<td align="center" colspan="6">\n<H1>The BodgeIt Store</H1>\n<table width="100%" class=\\"noborder\\">\n<tr BGCOLOR=#C3D9FF>\n<td align="center" width="30%">&nbsp;</td>\n<td align="center" width="40%">We bodge it, so you dont have to!</td>\n<td align="center" width="30%" style="text-align: right" >\nGuest user\n\n</tr>\n</table>\n</td>\n</tr>\n<tr>\n<td align="center" width="16%" BGCOLOR=#EEEEEE><a href="home.jsp">Home</a></td>\n<td align="center" width="16%" BGCOLOR=#EEEEEE><a href="about.jsp">About Us</a></td>\n\n<td align="center" width="16%" BGCOLOR=#EEEEEE><a href="contact.jsp">Contact Us</a></td>\n<!-- td align="center" width="16%"><a href="admin.jsp">Admin</a></td-->\n\n<td align="center" width="16%" BGCOLOR=#EEEEEE>\n\n\t\t<a href="login.jsp">Login</a>\n\n</td>\n\n<td align="center" width="16%" BGCOLOR=#EEEEEE><a href="basket.jsp">Your Basket</a></td>\n\n<td align="center" width="16%" BGCOLOR=#EEEEEE><a href="search.jsp">Search</a></td>\n</tr>\n<tr>\n<td align="center" colspan="6">\n<table width="100%" class="border">\n<tr>\n<td align="left" valign="top" width="25%">\n<a href="product.jsp?typeid=6">Doodahs</a><br/>\n<a href="product.jsp?typeid=5">Gizmos</a><br/>\n<a href="product.jsp?typeid=3">Thingamajigs</a><br/>\n<a href="product.jsp?typeid=2">Thingies</a><br/>\n<a href="product.jsp?typeid=7">Whatchamacallits</a><br/>\n<a href="product.jsp?typeid=4">Whatsits</a><br/>\n<a href="product.jsp?typeid=1">Widgets</a><br/>\n\n<br/><br/><br/><br/><br/><br/><br/><br/><br/><br/><br/><br/><br/><br/><br/>\n</td>\n<td valign="top" width="70%">\n\n\n<h3>Our Best Deals!</h3>\n<center><table border="1" class="border" width="80%">\n<tr><th>Product</th><th>Type</th><th>Price</th></tr>\n<tr>\n<td><a href="product.jsp?prodid=26">Zip a dee doo dah</a></td><td>Doodahs</td><td align="right">¤3.99</td>\n</tr>\n<tr>\n<td><a href="product.jsp?prodid=13">TGJ EFF</a></td><td>Thingamajigs</td><td align="right">¤3.00</td>\n</tr>\n<tr>\n<td><a href="product.jsp?prodid=29">Tipofmytongue</a></td><td>Whatchamacallits</td><td align="right">¤3.74</td>\n</tr>\n<tr>\n<td><a href="product.jsp?prodid=27">Doo dah day</a></td><td>Doodahs</td><td align="right">¤6.50</td>\n</tr>\n<tr>\n<td><a href="product.jsp?prodid=16">TGJ JJJ</a></td><td>Thingamajigs</td><td align="right">¤0.80</td>\n</tr>\n<tr>\n<td><a href="product.jsp?prodid=31">Youknowwhat</a></td><td>Whatchamacallits</td><td align="right">¤4.32</td>\n</tr>\n<tr>\n<td><a href="product.jsp?prodid=23">GZ ZX3</a></td><td>Gizmos</td><td align="right">¤3.81</td>\n</tr>\n<tr>\n<td><a href="product.jsp?prodid=18">Whatsit weigh</a></td><td>Whatsits</td><td align="right">¤2.50</td>\n</tr>\n<tr>\n<td><a href="product.jsp?prodid=16">TGJ JJJ</a></td><td>Thingamajigs</td><td align="right">¤0.80</td>\n</tr>\n<tr>\n<td><a href="product.jsp?prodid=7">Thingie 4</a></td><td>Thingies</td><td align="right">¤3.50</td>\n</tr>\n</table></center><br/>\n\n\n</td>\n</tr>\n</table>\n</td>\n</tr>\n</table>\n</center>\n</body>\n</html>\n\n\n

"""


# 1. JSON lesen und tokenizen
# 2. RTT hinschreiben
# 3. resp.ResponseBody
# 3.a BeautifulSoup
# 3.b Buchstaben in kleinbuchstaben umwandeln
# 3.c URL-Normalisierung
###### Unbedingt NLTK-Library verwenden

html_doc = html_doc.replace('\n', ' ').replace('\r', ' ')
html_doc = html_doc.lower()



cleantext = BeautifulSoup(html_doc, "html.parser")
cleantext = cleantext.text


print(cleantext)