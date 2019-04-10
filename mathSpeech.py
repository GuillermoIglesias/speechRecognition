import speech_recognition as sr
from math import sqrt

def mathOperation(words):

	resp = { 'result': None, 'operation': None, 'success': True, 'error': None }
	op = { 'real': 0.0, 'test': 0.0 }

	try:
		if len(words) < 5:
			resp['success'] = False
			resp['error'] = 'No ha sido posible reconocer lo que dijiste.'
			return resp
			
		op['test'] = float(words[-1])

		if 'más' in words or '+' in words:
			op['real'] = float(words[0]) + float(words[-3])
			resp['operation'] = '{} + {} = {}'.format(words[0], words[-3], words[-1])

		elif 'menos' in words or '-' in words:
			op['real'] = float(words[0]) - float(words[-3])
			resp['operation'] = '{} - {} = {}'.format(words[0], words[-3], words[-1])

		elif 'por' in words or '*' in words:
			op['real'] = float(words[0]) * float(words[-3])
			resp['operation'] = '{} * {} = {}'.format(words[0], words[-3], words[-1])

		elif 'dividido' in words or '/' in words:
			op['real'] = float(words[0]) / float(words[-3])
			resp['operation'] = '{} / {} = {}'.format(words[0], words[-3], words[-1])

		elif 'elevado' in words or '^' in words:
			op['real'] = float(words[0]) ** float(words[-3])
			resp['operation'] = '{} ^ {} = {}'.format(words[0], words[-3], words[-1])

		elif 'raíz' in words:
			op['real'] = sqrt(float(words[3]))
			resp['operation'] = 'Raíz cuadrada de {} = {}'.format(words[-3], words[-1])
	
		if resp['operation'] is not None:
			if op['real'] == op['test']:
				resp['result'] = '¡Correcto!'
			else:
				resp['result'] = 'Incorrecto... (El resultado era: {})'.format(op['real'])
			return resp

	except:
		resp['success'] = False
		resp['error'] = 'No ha sido posible reconocer lo que dijiste.'
		return resp


def recognizeSpeech(rec, mic):
	with mic as source:
		rec.adjust_for_ambient_noise(source)
		audio = rec.listen(source)

	resp = { 'result': None, 'success': True, 'error': None}
	
	try:
		resp['result'] = rec.recognize_google(audio, language='es-CL')
	except sr.RequestError:
		resp['success'] = False
		resp['error'] = 'ERROR: La API no se encuentra disponible.'
	except sr.UnknownValueError:
		resp['error'] = 'No ha sido posible reconocer lo que dijiste.'

	return resp


if __name__ == '__main__':

	instructions = (
		'\nInstrucciones:\n'
		'Dime una operación matemática con su resultado y te diré si es correcto.\n'
		'Este programa funciona en idioma Español.\n'
		'Puedes operar siguiendo la siguiente estructura:\n'
		'\t- Suma: <número> más <número> igual <número>\n'
		'\t- Resta: <número> menos <número> igual <número> \n'
		'\t- Multiplicación: <número> por <número> igual <número>\n'
		'\t- División: <número> dividido <número> igual <número>\n'
		'\t- Exponenciación: <número> elevado <número> igual <número>\n'
		'\t- Raíz Cuadrada: Raíz cuadrada de <número> igual <número>'
	)

	start = '\nAhora puedes decir una operación:\n'

	rec = sr.Recognizer()
	mic = sr.Microphone()

	print(instructions)
	input('\nPresiona ENTER para comenzar...')

	running = True

	while(running):
		print(start)
		speech = recognizeSpeech(rec, mic)
		
		if speech['success']:
			if speech['result'] is not None:
				words = speech['result'].lower().replace(',', '.').split()
				print(words)
				math = mathOperation(words)
				if math['success']:
					print('Operación: ' + math['operation'])
					print('Resultado: ' + math['result'])
				else:
					print(math['error'])
			else:
				print(speech['error'])
		else:
			print(speech['error'])

		ans = 'y'
		ans = input('\n¿Deseas volver a intentar? [Y/n]: ').lower()
		if ans == 'n':
			running = False

		