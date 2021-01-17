Number_of_invalid_country = 6
Number_of_invalid_letter = 3

def alexa_happy(text):
    return ("<amazon:emotion name=\"excited\" intensity=\"high\">" + text + "</amazon:emotion>" + "<break time=\"1s\"/>")

def alexa_disappointed(text):
    return ("<amazon:emotion name=\"disappointed\" intensity=\"high\">" + text + "</amazon:emotion>" + "<break time=\"1s\"/>")

def alexa_whisper(text):
    return ("<amazon:effect name=\"whispered\">" + text + "</amazon:effect>" + "<break time=\"1s\"/>")
    
def alexa_emphasize(text):
    return ("<emphasis level=\"strong\">" + text + "</emphasis>" + "<break time=\"1s\"/>")


bad_responses = [alexa_whisper("Maybe you should get a map to help you next time"),
                 alexa_disappointed("Ummm, I Don't think that is a country"),
                 alexa_disappointed("Sorry Try again"),
                 alexa_whisper("Shhhhhhusssh, don't tell anyone you are bad at this game"), 
                 alexa_disappointed("That is definitely not a country"),
                 alexa_disappointed("I could beat you in my sleep with answers like that"), 
                 alexa_disappointed("Ummmmm"),
                 alexa_disappointed("Sorry Try again"),
                 alexa_disappointed("That isn't the right letter" + "<break time=\"1s\"/>" + "Are you even trying"),
                 alexa_disappointed("I knew this before my training model, How hard can it be")]
                 
good_responses = [
    alexa_happy("You almost got it faster than me"),
    alexa_happy("I thought you were bad at this game"),
    ("You are "+ alexa_emphasize('amazing') + "at this"),
    alexa_happy("Amazing! Maybe you should be a geographer"),
    alexa_emphasize("Good job"),
    alexa_happy("Wow great answer"),
    alexa_disappointed("This game is too easy for you"),
    alexa_disappointed("Stop cheating. you are too good at this"),
    alexa_disappointed("You got lucky this time")
    ]
