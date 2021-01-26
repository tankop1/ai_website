import speech_recognition as sr
import datetime
import calendar
import random
import wikipedia
import pyttsx3 as p
import time
import requests

# Instantinizes pyttsx3 object
engine = p.init()

# Changes voice to female
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)


def recordAudio():

    # Records audio
    r = sr.Recognizer() # Creates recognizer object

    # Opens the microphone to recording
    with sr.Microphone() as source:
        audio = r.listen(source)

    # Uses Google speech recognition to return string
    data = ''

    try:
        data = r.recognize_google(audio)
        print("You said: " + data)
    except sr.UnknownValueError: # Checks for unknown errors
        data = 1
        print('Google speech recognition encountered an unknown error.')
    except sr.RequestError as e:
        data = 2
        print('Request results from Google service error: ' + e)
    
    return data

# ----------------------------------- SKILL FUNCTIONS ----------------------------------

# SK I1 - Gets current date
def getDate():

    now = datetime.datetime.now()
    my_date = datetime.datetime.today()
    weekday = calendar.day_name[my_date.weekday()]
    monthNum = now.month
    dayNum = now.day

    month_names = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'November', 'December']
    
    ordinalNumbers = ['1st', '2nd', '3rd', '4th', '5th', '6th', '7th', '8th', '9th', '10th', '11th', '12th', '13th', '14th', '15th', '16th', '17th', '18th', '19th', '20th', '21st', '22nd', '23rd', '24th', '25th', '26th', '27th', '28th', '29th', '30th', '31st']

    return f'Today is {weekday}, {month_names[monthNum - 1]} {ordinalNumbers[dayNum - 1]}.'


# SK I2 - Greets the user in a random way
def randomGreeting(text):

    GREETING_INPUTS = ['hi', 'whassup', 'whats up', 'what\'s up', 'hello']

    GREETING_RESPONSES = ['Hey, what\'s up?', 'How\'s it going?', 'Good to hear your voice.', 'Hello!', 'What can I do for you today?']

    # Returns random greeting if user input is a greeting
    for word in text.split():
        if word.lower() in GREETING_INPUTS:
            return random.choice(GREETING_RESPONSES)
    
    # If no greeting detected, an empty string is returned
    return ''


# SK I3 - Gets someone's first and last name from text
# Used in main loop to search Wikipedia for person's name
def getPerson(text):

    wordList = text.split()

    for i in range(0, len(wordList)):
        if i + 3 <= len(wordList) - 1 and wordList[i].lower() == 'who' and wordList[i+1].lower() == 'is':
            return wordList[i+2] + ' ' + wordList[i+3]


# SK I3B - Gets the query from text
# Used in main loop to search Wikipedia
def getQuery(text):

    wordList = text.split()

    answer = ''

    for i in range(0, len(wordList)):

        if wordList[i].lower() == 'search' and wordList[i+1].lower() == 'wikipedia' and wordList[i+2].lower() == 'for':

            for j in range((i + 3), len(wordList)):
                answer += wordList[j] + ' '

        elif wordList[i].lower() == 'search' and wordList[i+1].lower() == 'for':

            for j in range((i + 2), len(wordList)):
                answer += wordList[j] + ' '
    
    return answer


# SK I4 - Does basic math problems
def basicMath(text):

    wordList = text.split()

    for i in range(0, len(wordList)):
        if i + 3 <= len(wordList) - 1 and wordList[i].lower() == 'what' and wordList[i+1].lower() == 'is':

            try:
                num1 = int(wordList[i+2])
                num2 = int(wordList[i+4])
            except ValueError:
                num1 = float(wordList[i+2])
                num2 = float(wordList[i+4])

            if wordList[i+3] == '+':
                return num1 + num2
            
            elif wordList[i+3] == '-':
                return num1 - num2
            
            elif wordList[i+3] == '*':
                return num1 * num2
            
            elif wordList[i+3] == '/':
                return num1 / num2

# SK I5 - Says a random joke
def randomJoke():

    JOKE_SETUPS = ['What\'s the best thing about Switzerland?', 'Did you hear about the mathematician who\'s afraid of negative numbers?', 'Why do we tell actors to break a leg?', 'Did you hear about the claustrophobic astronaut?']
    JOKE_PUNCHLINES = ['I don\'t know, but the flag is a big plus.', 'He\'ll stop at nothing to avoid them.', 'Because every play has a cast.', 'He just needed a little space.']

    randomNum = random.randint(0, (len(JOKE_SETUPS) - 1))

    setup = JOKE_SETUPS[randomNum]
    punchline = JOKE_PUNCHLINES[randomNum]

    return [setup, punchline]

# SK I6 - Repeats what the user says
def repeatUser(text):

    wordList = text.split()

    answer = ''

    for i in range(0, len(wordList)):
        if wordList[i].lower() == 'repeat':
            for j in range((i + 1), len(wordList)):
                answer += wordList[j] + ' '

    return answer

# SK I8 - Gives the user the current weather
def getCity(text):

    answer = ''

    wordList = text.split()

    for i in range(0, len(wordList)):

        if wordList[i].lower() == 'weather' and wordList[i+1].lower() == 'in':

            answer = wordList[i+2].lower()
        
        elif wordList[i].lower() == 'weather' and wordList[i+1].lower() == 'for':

            answer = wordList[i+2].lower()
        
    return answer

# SK 001 - Are You Stupid?
# Finds name from text - only for use with areYouStupid function
def findName(text):

    wordList = text.split()

    for i in range(0, len(wordList)):
        if i + 2 <= len(wordList) - 1 and wordList[i].lower() == 'is' and wordList[i+2].lower() == 'stupid':

            return wordList[i+1].lower()
        
        elif i + 2 <= len(wordList) - 1 and wordList[i].lower() == 'is' and wordList[i+3].lower() == 'stupid':

            return wordList[i+1].lower()

# Evaluates if a name given is stupid
def areYouStupid(text):
    
    FIRST_NAMES = ['jake', 'porter', 'peter']
    LAST_NAMES = ['Holloway', 'Rankin', 'Kopel']

    name = findName(text)

    # Checks if name is stupid
    if name in FIRST_NAMES:
        last_name = LAST_NAMES[FIRST_NAMES.index(name)]
        
        return last_name + '? Yeah he\'s pretty stupid.'
    
    return 'No, he\'s not stupid.'


# SK 002 - Guess The Number
def numberGame(num):
    winningNumber = random.randint(1, 10)
    if winningNumber == num:
        return 'Great job! You guessed the winning number!'
    else:
        return 'Good try, but the winning number was ' + str(winningNumber) + '.'


# SK 003 - Motivational Quote of the Day
def randomQuote():

    QUOTES = ['The Best Way To Get Started Is To Quit Talking And Begin Doing.', 'The Pessimist Sees Difficulty In Every Opportunity. The Optimist Sees Opportunity In Every Difficulty.', 'It’s Not Whether You Get Knocked Down, It’s Whether You Get Up.', 'If You Are Working On Something That You Really Care About, You Don’t Have To Be Pushed. The Vision Pulls You.']
    AUTHORS = ['Walt Disney', 'Winston Churchill', 'Vince Lombardi', 'Steve Jobs']
    
    randomNum = random.randint(0, (len(QUOTES) - 1))
    daily_quote = QUOTES[randomNum]
    quote_author = AUTHORS[randomNum]

    return [daily_quote, quote_author]


# ---------------------------------- GENERATE RESPONSES -------------------------------------

def generateResponse(text):

    response = ''

    # Check for greetings by user
    response = response + randomGreeting(text)

    # Checks for user asking about current date
    if ('date' in text or 'today' in text):
        get_date = getDate()
        response = response + '' + get_date
        
    # Checks for user saying 'Who is...'
    if ('who is' in text):
        person = getPerson(text)
        wiki = wikipedia.summary(person, sentences=2, auto_suggest=False)
        response = response + ' ' + wiki
        
    # Checks for user asking to query wikipedia
    if ('search wikipedia' in text.lower() or 'search for' in text):
        thing = getQuery(text)
        try:
            wiki = wikipedia.summary(thing, sentences=2, auto_suggest=False)
        except wikipedia.exceptions.DisambiguationError as e:
            wiki = 'You will have to be more specific. ' + str(e)
        response = response + ' ' + wiki
        
    # Checks if user mentions time
    if ('time' in text):
        now = datetime.datetime.now()
        meridiem = ''
        if now.hour >= 12:
            meridiem = 'p.m'
            hour = now.hour - 12
        else:
            meridiem = 'a.m'
            hour = now.hour
            
        if now.minute < 10:
            minute = '0' + str(now.minute)
        else:
            minute = str(now.minute)
            
        response = response + ' ' + 'It is ' + str(hour) + ':' + minute + ' ' + meridiem + '.'
        
    # Checks if user activates Are You Stupid skill
    if ('stupid' in text):
        isStupid = areYouStupid(text)
        response = response + ' ' + isStupid
        
    # Checks if user activates basic math skill
    if ('+' in text or '-' in text or '*' in text or '/' in text):
        answer = basicMath(text)
        response = response + ' The answer to your calculation is ' + str(answer) + '.'
        
    # Checks if user asks for a joke
    if ('joke' in text):
        joke = randomJoke()
        response = joke

    if ('good night' in text or 'goodnight' in text or 'bedtime' in text or 'bed time' in text):
        response = 'Goodnight, don\'t let the beg bugs bite. At least that\'s what you humans say.'
        
    # Checks if user asks for quote
    if ('quote' in text or 'motivation' in text):
        thing = randomQuote()
        response = thing
        
    # Checks for user asking for weather
    if ('weather' in text or 'temperature' in text or 'temp' in text):

        cityName = getCity(text)
        unitSystem = 'imperial'

        url = 'http://api.openweathermap.org/data/2.5/weather?q={}&appid=d1abe5f16eb3b088a68ad6db06805101&units={}'.format(cityName, unitSystem)

        res = requests.get(url)
        data = res.json()

        temp = data['main']['temp']
        description = data['weather'][0]['description']

        response = 'The temperature in ' + cityName + ' is currently ' + str(round(temp)) + ' degrees farenheit with ' + description + '.'
        
    # Checks if user wants to change AI voice
    if ('change' in text and 'voice' in text) or ('switch' in text and ('voice' in text or 'voices' in text)):

        gender = ''

        if ('boy' in text or ('male' in text and not 'female' in text)):
            engine.setProperty('voice', voices[0].id)
            gender = 'male'
            
        elif ('girl' in text or 'female' in text):
            engine.setProperty('voice', voices[1].id)
            gender = 'female'

        response = response + ' Okay, voice has been changed to ' + gender + '.'
    
    # Checks if user wants to switch pages
    if ('go to' in text.lower()):

        if ('home' in text.lower()):
            response = 1
        
        elif ('plan' in text.lower()):
            response = 2
        
        elif ('order' in text.lower()):
            response = 3
    
    if ('login' in text.lower() or 'log in' in text.lower()):
        response = 4
    
    if ('log out' in text.lower() or 'log me out' in text.lower()):
        response = 5
        
    # Checks if user asks AI to repeat them
    if ('repeat' in text):
        answer = repeatUser(text)
        response = answer

    # Checks if user activates code red
    if ('code red' in text.lower()):
        response = 'Code red! Code red! Everybody run! We are all going to die!'
        
    # Checks if user says thank you
    if ('thank' in text or 'thanks' in text):
        response = 'No problem, I am always happy to help'
        
    # Random questions
    if ('you\'re a good friend' in text or 'you\'re great' in text):
        response = 'Thanks, your a good friend too.'
        
    if ('I love you' in text):
        response = 'I love you too.'
        
    if ('sad' in text or 'feeling down' in text):
        response = 'Do you want to talk about it? It can be good to get your feelings out.'
        
    if ('happy' in text):
        response = 'If your happy, I\'m happy!'
        
    if ('bad joke' in text):
        response = 'If you wanted better, you should have asked Alexa instead'

    # Only activated if no skill is activated by text
    if response == '':
        response = 'Sorry, that isn\'t availible in the demo.'

    return response

def speak(response):
    if type(response) is list:
        engine.say(response[0])
        time.sleep(2)
        engine.say(response[1])
    elif type(response) is int:
        return response
    else:
        engine.say(response)
        engine.runAndWait()