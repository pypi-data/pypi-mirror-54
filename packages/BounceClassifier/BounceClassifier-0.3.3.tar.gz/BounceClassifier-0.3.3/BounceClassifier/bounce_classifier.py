import re
import logging

logging.basicConfig(filename='error.log', level=logging.ERROR) 

class Bounce_classifier(object):
	'''Classify bounce messages using regex'''
	def __init__(self, email_text):
		
		self.email_text = email_text.lower()

	def recipient_email(self):
		try:
			rcpt = re.search('final-recipient: (rfc822;|)(.*?)\n', self.email_text).group(2)
		except Exception as e:
			rcpt = 'Not found'
			return rcpt
		return rcpt

	def diagonostic_code(self):
		try:
			dia_code = re.search('diagnostic-code: (.*?)\n', self.email_text).group(1)
		except Exception as e:
			dia_code = None
			classification = 'unclassified'
			return dia_code, classification

		if re.search('njabl', dia_code):
			classification = 'blacklist'
		elif re.search('message.*(size\sexceed|too\slarge)', dia_code):
			classification = 'msgsize'
		elif re.search('temporar.*(problem|reject)|insufficient.*resource|out\sof\ssequence|mail.*loop.*\
			.*detected|(service|transport)\sunavailable', dia_code):
			classification = 'temperr'
		elif re.search('(invalid|disabled|deactivated|malformed|norelay|inactiv(e|ity)|\
						no.*(account|such|mailbox|address)|\
						(address(ee?)|user).*(not\slisted|failed|doesn|unknown)|\
						not.*(exist|found|.*valid|our\scustomer)|\
						unknown(.*?)\s(user|alias|recipient)|\
						alias.*valid|\
						address\slookup.*fail|\
						format.*address|\
						unrouteable\saddress|\
						(recipient|address).*\s(rejected|no\slonger)|\
						none\s.*servers.*respond|\
						no\s(route\sto\shost|valid|recipient)|\
						hop\scount\sexceeded|\
						RP:RDN.*xrnet|\
						too\smany\shops|\
						list\sof\sallowed\srcpthosts|\
						user.*(reject|suspend)|\
						doesn.*\shandle\smail\sfor|\
						(user|recipient).*(not|only|unknown)|\
						unknow\suser\
						(access|relay).*\sdenied|\
						MX\spoints\sto|\
						refused\sdue\sto\srecipient|\
						(account|mailbox|address|recipient).*\
						(reserved|suspended|unavailable|not)|\
						loops\sback\sto\smyself)', dia_code):
			classification = 'deadrcpt'
		elif re.search('(\s550\s5\.7\.1|\
						too\s(many|fast|much)|slow\sdown|throttl(e|ing)|\
						to\sabuse|excessive|bl(a|o)cklist|\
						(junk|intrusion)|\
						listed\sat|\
						client.*not\sauthenticated|\
						administrative.*prohibit|\
						connection\srefused|\
						connection.*(timed\sout|limit)|\
						refused.*(mxrate|to\stalk)|\
						can.*connect\sto\s.*psmtp|\
						reject.*(content|policy)|\
						not\saccept.*mail|\
						message.*re(fused|ject)|\
						transaction\sfailed.*psmtp|\
						sorbs|rbl|spam|spamcop|block|blocked|den(y|ied)|\
						unsolicited|\
						not\sauthorized\sfrom\sthis\sip|\
						reject\smail\sfrom|try\sagain\slater)|\
						|too\s(much|many)', dia_code):
			classification = 'blocked'
		elif re.search('(overquota|over\squota|quota\sexceed|\
						exceeded.*storage|\
						(size|storage|mailbox).*(full|exceed)|\
						full\s.*mailbox)', dia_code):
			classification = 'fullbox'
		elif re.search('message.*delayed', dia_code):
			classification = 'delayed'
		else:
			classification = 'unclassified'

		return dia_code, classification

	def no_diagonostic_code(self):

		# BEGIN: message autoreply 

		if re.search(r'X-Autoreply:\s*yes', self.email_text):
			classification = "autoreply"
			key_word = 'X-Autoreply:\s*yes'
		elif re.search(r'Subject:.*(out\s+of.*office|auto.*re(ply|spon))', self.email_text):
			classification = "autoreply"
			key_word = 'out of office'
		elif re.search(r'\s\(aol;\saway\)', self.email_text):
			classification = "autoreply"
			key_word = 'away'
		elif re.search(r'dear|thank\s+you', self.email_text):
			classification = "autoreply"
			key_word = 'Dear|thank you'
		# elif re.search('auto-submitted:\s*auto-replied', self.email_text):
		# 	classification = "autoreply"
		# 	key_word = 'auto-submitted auto-reply'
		# BEGIN: message delayed notification
		elif re.search(r'(Action:\s*delayed|Will-Retry-Until)', self.email_text):
		  classification = "delayed"
		  key_word = 'delayed'
		elif re.search(r'Subject:.*delayed\smail', self.email_text):
		  classification = "delayed"
		  key_word = 'delayed'
		elif re.search(r'Subject:.*delivery.*status.*delay', self.email_text):
		  classification = "delayed"
		  key_word = 'delayed'
		elif re.search(r'delivery\sto.*has\sbeen\sdelayed', self.email_text):
		  classification = "delayed"
		  key_word = 'delayed'
		# BEGIN: dead recipient address
		elif re.search(r'this\suser\sdoesn\'t\shave\sa\s.*\saccount', self.email_text):
		  classification = "invalid"
		  key_word = 'doesnt have'
		elif re.search(r'user.*doesn.*mail.*your.*address|no\s*user', self.email_text):
		  classification = "invalid"
		  key_word = 'user doesn'
		elif re.search(r'in\smy\scontrol.*locals', self.email_text):
		  classification = "invalid"
		  key_word = ''
		elif re.search('invalid.*(mailbox|recipient)', self.email_text):
		  classification = "invalid"
		  key_word = 'invalid'
		elif re.search(r'user\sunknown|unknown\suser|unknown.*recipient', self.email_text):
		  classification = "invalid"
		  key_word = 'unknown'
		elif re.search('(not found|couldn\'t be found)', self.email_text):
		  classification = "invalid"
		  key_word = 'not found'
		elif re.search(r'(account.*disabled|mailbox.*disabled|no\s*mailbox)', self.email_text):
		  classification = 'invalid'
		  key_word = 'account,disabled|no mailbox'
		elif re.search('(address rejected|recipient rejected)', self.email_text):
		  classification = 'invalid'
		  key_word = 'address rejected or recipient rejected'
		# elif re.search('message.*not\sbe\sdelivered', self.email_text):
		#   classification = "deadrcpt"
		#   key_word = 'not delivered'
		elif re.search(r'address\swas\snot\sfound', self.email_text):
		  classification = "invalid"
		  key_word = 'found'
		elif re.search('protected.*bluebottle', self.email_text):
		  classification = "invalid"
		  key_word = 'protected'
		elif re.search(r'hop\scount\sexceeded', self.email_text):
		  classification = "invalid"
		  key_word = 'hop exceed'
		elif re.search(r'delivery\sto.*(failed|aborted\safter)', self.email_text):
		  classification = "invalid"
		  key_word = 'failed'
		elif re.search('mailbox unavailable', self.email_text):
		  classification = 'invalid'
		  key_word = 'mailbox unavailable'
		elif re.search('recipient.*unknown', self.email_text):
		  classification = 'invalid'
		  key_word = 'recipient unknown'
		elif re.search('not exist', self.email_text):
		  classification = 'invalid'
		  key_word = 'not exist'
		elif re.search('address.*(invalid|incorrect)', self.email_text):
		  classification = 'invalid'
		  key_word = 'address invalid|incorrect'

		# BEGIN: full mailbox
		elif re.search(r'(size|(in|mail)box).*(full|exceed|many\smessages|much\sdata)', self.email_text):
		  classification = "fullbox"
		  key_word = 'size'
		elif re.search(r'quota.*exceed\w*|over\s*quota', self.email_text):
		  classification = "fullbox"
		  key_word = 'exceed'

		# BEGIN: rbl'policy block
		elif re.search(r'(5\.7\.1.*reject|\sspam\s)', self.email_text):
		  classification = "blocked"
		  key_word = 'reject|spam'
		elif re.search('banned', self.email_text):
		  classification = "blocked"
		  key_word = 'banned'
		elif re.search('protected.*reflexion', self.email_text):
		  classification = "blocked"
		  key_word = 'protected'
		elif re.search(r'said:\s.*(spam|rbl|blocked|blacklist|abuse)', self.email_text):
		  classification = "blocked"
		  key_word = 'blacklist blocked spam'
		elif re.search('reputation', self.email_text):
		  classification = "blocked"
		  key_word = 'reputation'
		elif re.search('not (accept|permit|available)', self.email_text):
		  classification = 'blocked'
		  key_word = 'not (permitted|accept|available)'
		# BEGIN: temporary error
		elif re.search(r'open\smailbox\sfor\s.*\stemporary\serror', self.email_text):
		  classification = "tmperr"
		  key_word = 'temp error'
		elif re.search(r'subject.*mail\ssystem\serror', self.email_text):
		  classification = "tmperr"
		  key_word = 'system error'
		elif re.search('message filtered', self.email_text):
		  classification = 'blocked'
		  key_word = 'message filtered'
		elif re.search('administrative.*prohibition', self.email_text):
		  classification = 'blocked'
		  key_word = 'administrative prohibition'
		elif re.search('550.*IP.*rejected', self.email_text):
		  classification = 'blocked'
		  key_word = 'IP rejected'
		elif re.search('un-solicited|unsolicited', self.email_text):
		  classification = 'blocked'
		  key_word = 'unsolicited'
		elif re.search(r'security\s*policies', self.email_text):
		  classification = 'blocked'
		  key_word = 'security policies'
		elif re.search('complain', self.email_text):
		  classification = 'blocked'
		  key_word = 'complain'
		elif re.search('blocked', self.email_text):
		  classification = 'blocked'
		  key_word = 'blocked'
		elif re.search(r'lost\s*connection', self.email_text):
		  classification = 'blocked'
		  key_word = 'lost connection'
		elif re.search('connection.*timed out', self.email_text):
		  classification = 'invalid mx'
		  key_word = 'connection timed out'
		elif re.search('(qq write error|disk full)', self.email_text):
		  classification = 'mx error'
		  key_word = 'qq write error or disk full'
		elif re.search('prior approval', self.email_text):
		  classification = 'blocked'
		  key_word = 'prior approval'
		elif re.search('try again later', self.email_text):
		  classification = 'blocked'
		  key_word = 'try again later'
		elif re.search('not.*permitted sender', self.email_text):
		  classification = 'blocked'
		  key_word = 'not permitted sender'
		elif re.search('name service error', self.email_text):
		  classification = 'invalid mx'
		  key_word = 'name service error'
		elif re.search('too many hops', self.email_text):
		  classification = 'invalid'
		  key_word = 'too many hops'


		# BEGIN: unclassified catchall
		else:
		  classification = "unclassified"
		  key_word = '' 
		return classification, key_word
