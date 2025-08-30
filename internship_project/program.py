import pyttsx3

def text_to_speech(text):
    # Initialize the pyttsx3 engine
    engine = pyttsx3.init()

    # Set properties (optional)
    #rate = engine.getProperty('rate')  # Speed of speech
    #engine.setProperty('rate', rate - 30)  # Adjust the speed

    """volume = engine.getProperty('volume')  # Volume level (0.0 to 1.0)
    engine.setProperty('volume', 0.5)  # Max volume"""

    # Speak the provided text
    engine.say(f"hello {text}")

    # Wait until the speech is finished
    #engine.runAndWait()

if __name__ == "__main__":
    # Example: Take text input and convert to speech
    text =["nikhitha","samhitha","vanitha"]
    for t in text:
        
        text_to_speech(t)
