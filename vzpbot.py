from helium import *
import time

class VZPBot(object):

	def init(self):
		start_firefox()
		go_to('https://auth.vzp.cz/signin')
		click(u'Přihlásit se certifikátem')
		wait_until(S('h2.heading.heading--medium.u-mb-1h').exists)

		go_to('https://point.vzp.cz/online/online01')
		click(u'Ověřit pojištěnce dle jména a data narození')

	def search(self, data):
		write(data['name'], S('#Search_FirstName'))
		write(data['surname'], S('#Search_LastName'))
		write(data['birthdate'].strftime('%d.%m.%Y'), S('#Search_BirthDate'))

		click('Ověřit pojištění')
		click(S('button.btn.btn-primary.btn-lg'))

		time.sleep(0.1)
		wait_until(S('#result').exists)

		if S('#result > div > div:nth-child(3) > div.col-md-5 > p > span.text-strong').exists():
			return True
		else:
			return False
