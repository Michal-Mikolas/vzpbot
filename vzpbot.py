from helium import *
import time

class VZPBot(object):

	def init(self):
		# start_firefox()
		start_chrome()
		go_to('https://auth.vzp.cz/signin')
		click(u'CERTIFIKÁT')
		wait_until(S('h2.heading.heading--medium.u-mb-1h').exists, timeout_secs=120)

		go_to('https://point.vzp.cz/online/online01')
		wait_until(lambda: self.shadow('#queryBy_radioinput_8'))
		click(self.shadow('#queryBy_radioinput_8'))

	def fetch_insurance(self, data):
		write(data['name'], self.shadow('[name=firstName]'))
		write(data['surname'], self.shadow('[name=lastName]'))
		write(data['birthdate'].strftime('%d.%m.%Y'), self.shadow('[name=birthDate]'))
		# click(self.shadow('.active.start-date.active.end-date.available'))  # confirm birthdate

		click(self.shadow('.btn.btn-primary.btn-lg'))

		wait_until(lambda: self.shadow('.form-container > div.well:nth-child(5)'))

		data['insurance_text'] = self.shadow('.form-container > div.well:nth-child(5)').text.replace(u'Výsledek ověření', '').strip()
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

	def shadow(self, query):
		shadowQuery = """return document.querySelector('#content-panel > div').shadowRoot.querySelector('{}');"""
		return get_driver().execute_script(shadowQuery.format(query))
data
