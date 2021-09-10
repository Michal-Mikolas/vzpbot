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

	def fetch_insurance(self, data):
		write(data['name'], S('#Search_FirstName'))
		write(data['surname'], S('#Search_LastName'))
		write(data['birthdate'].strftime('%d.%m.%Y'), S('#Search_BirthDate'))
		click(S('.active.start-date.active.end-date.available'))  # confirm birthdate

		click('Ověřit pojištění')

		wait_until(S('#result').exists)

		data['insurance_text'] = S('#result').web_element.text.replace(u'Výsledek ověření', '').strip()
		if u'platné pojištění' in data['insurance_text']:
			data['insurance_type'] = 1
		elif u'žádný pojištěnec' in data['insurance_text']:
			data['insurance_type'] = 0
		elif u'nebyl ke dni' in data['insurance_text']:
			data['insurance_type'] = 0
		elif u'více pojištěnců' in data['insurance_text']:
			data['insurance_type'] = 2
		else:
			data['insurance_type'] = 'ERROR'

		return data
