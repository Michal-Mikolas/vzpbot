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

