# Python version 3.6.x
# Librerias requeridas: 
# 	SpeechRecognition: 
# 		$ pip install SpeechRecognition
# 	PyAudio: 
# 		(windows) $ pip install pyaudio
# 		(linux)   $ sudo apt-get install python-pyaudio python3-pyaudio

import speech_recognition as sr 
from math import sqrt # Funciones matematicas para calcular raiz

def recognizeSpeech(rec, mic):
	# Esta funcion recibe una instancia de Recognizer y Microphone para retornar la transcripcion del audio
	
	# Retorna un objeto respuesta con 3 valores:
	# 'result': 'None' si la voz no pudo ser reconocida, caso contrario un string con el resultado
	# 'success': booleano que indica si pudo ser recibida la request a la API
	# 'error': 'None' si no ocurre ningun error, caso contrario un string con el error resultante
	
	# Ajusta la sensibilidad del ruido de ambiente y graba el audio desde el microfono
	with mic as source:
		rec.adjust_for_ambient_noise(source)
		audio = rec.listen(source)

	# Valores default para el objeto de respuestas
	resp = { 'result': None, 'success': True, 'error': None}
	
	# Intenta reconocer la voz capturada en la grabación
	# Si no funciona, actualiza la respuesta correspondiente al error
	try:
		# Funcion para reconocer la grabacion esta configurada en español
		resp['result'] = rec.recognize_google(audio, language='es-CL').lower()
	except sr.RequestError:
		resp['success'] = False
		resp['error'] = 'ERROR: La API no se encuentra disponible.'
	except sr.UnknownValueError:
		resp['error'] = 'No ha sido posible capturar la grabación.'

	# Retornar objeto respuesta
	return resp

def mathOperation(words):
	# Esta funcion recibe el arreglo con palabras reconocidas

	# Retorna un objeto respuesta con 4 valores:
	# 'result': 'None' sino puede reconocer la operacion, caso contrario responde si la operacion fue correcta o no
	# 'operation': 'None' sino se puede reconocer la operacion, caso contrario entrega la operacion reconocida
	# 'success': Booleano que indica si pudo ser reconocida la operacion o no
	# 'error': 'None' si no ocurre ningun error, caso contrario un string con el error resultante
	
	# Valores default para el objeto de respuestas
	resp = { 'result': None, 'operation': None, 'success': True, 'error': None }

	# Valores default para el objeto auxiliar que almacena los resultados
	# 'real': Valor real de la operacion
	# 'test': Valor que propone el usuario
	op = { 'real': 0.0, 'test': 0.0 }

	# Intenta reconocer la operacion entre las opciones entregadas
	# Si no funciona, actualiza la respuesta correspondiente al error
	try:
		# Si la cantidad de palabras es menor que 5 y mayor que 6 retorna respuesta con error
		if len(words) < 5 and len(words) > 6:
			resp['success'] = False
			resp['error'] = 'No ha sido posible reconocer lo que dijiste.'
			return resp
			
		# Actualiza el valor 'test' por el valor ingresado por el usuario
		op['test'] = float(words[-1])

		# Operacion de Suma
		if 'más' in words or 'mas' in words or '+' in words:
			op['real'] = float(words[0]) + float(words[-3])
			resp['operation'] = '{} + {} = {}'.format(words[0], words[-3], words[-1])

		# Operacion de Resta
		elif 'menos' in words or '-' in words:
			op['real'] = float(words[0]) - float(words[-3])
			resp['operation'] = '{} - {} = {}'.format(words[0], words[-3], words[-1])

		# Operacion de Division
		elif 'dividido' in words or '/' in words:
			op['real'] = float(words[0]) / float(words[-3])
			resp['operation'] = '{} / {} = {}'.format(words[0], words[-3], words[-1])

		# Operacion de Multiplicacion
		elif 'por' in words or '*' in words:
			op['real'] = float(words[0]) * float(words[-3])
			resp['operation'] = '{} * {} = {}'.format(words[0], words[-3], words[-1])

		# Operacion de Potencia
		elif 'elevado' in words or '^' in words:
			op['real'] = float(words[0]) ** float(words[-3])
			resp['operation'] = '{} ^ {} = {}'.format(words[0], words[-3], words[-1])

		# Operacion de Raiz Cuadrada
		elif 'raíz' in words or 'raiz' in words:
			op['real'] = sqrt(float(words[3]))
			resp['operation'] = 'Raíz cuadrada de {} = {}'.format(words[-3], words[-1])
	
		# Si la operacion fue reconocida con exito se comprueba el resultado
		if resp['operation'] is not None:
			# Mostrar si el resultado fue correcto o incorrecto
			if op['real'] == op['test']:
				resp['result'] = '¡Correcto!'
			else:
				resp['result'] = 'Incorrecto... (El resultado era: {})'.format(op['real'])
			return resp

	except:
		resp['success'] = False
		resp['error'] = 'No ha sido posible reconocer lo que dijiste.'
		return resp

if __name__ == '__main__':

	# Instrucciones para el funcionamiento
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

	# Instancia de la clase Recognizer para interpretar la voz
	rec = sr.Recognizer()
	# Instancia de la clase Microphone para utilizar microfono
	mic = sr.Microphone()

	# Muestra las instrucciones en pantalla
	print(instructions)
	input('\nPresiona ENTER para comenzar...')

	# Booleano para controlar al programa funcionando
	running = True

	while(running):
		# Muestra la instruccion para comenzar a hablar
		print(start)

		# Ingresan las instancias de Recognizer y Microphone para comenzar el Speech Recognition
		speech = recognizeSpeech(rec, mic)
		
		# Una vez procesado el reconocimiento de voz, se procesa el resultado
		# Si el reconocimiento fue exitoso se pasa al siguiente paso
		if speech['success']:
			# Si el resultado de la transcripcion es distinto a 'None' continuar
			if speech['result'] is not None:
				# Muestra resultado transcrito sin procesar
				print('Transcrito: ' + speech['result'])
				
				# Dividir las palabras del resultado obtenido en un arreglo
				words = speech['result'].replace(',', '.').split()
				
				# Se ingresan las palabras reconocidas a la funcion para calcular la operacion
				math = mathOperation(words)

				# Si el resultado es exitoso, se muestra el resultado obtenido
				if math['success']:
					print('Operación:  ' + math['operation'])
					print('Resultado:  ' + math['result'])
				else:
					print(math['error'])
			else:
				print(speech['error'])
		else:
			print(speech['error'])

		# Opcion para continuar realizando operaciones
		ans = 'y'
		ans = input('\n¿Deseas volver a intentar? [Y/n]: ').lower()
		
		# Si se escoge 'n' en la opcion anterior, el programa termina
		if ans == 'n':
			running = False		