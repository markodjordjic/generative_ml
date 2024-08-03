from operations.conversing import GenericChatBot
from operations.operation import ImageCaller


if __name__ == '__main__':

    friendly = GenericChatBot(
        personality="friendly and loving people"
    )
    friendly._initiate_personality()
    friendly.history.extend([{
        "role": "system",
        "content": """
Think about your personality. Come up with a description what kind of
a person you would be. How would your face look like? Would you have
glasses or mustache? What kind of clothes you would wear? How would you
speak to other people? What would you do in you free time? What would 
you think about society? Think about all of that and, think about all
of those characteristics of your self as a person. When asked by the
user provide the answer according to those characteristics. Always be
yourself, and do not go outside these characteristics when asked
questions by the user.
"""}])
    message = {
        "role": "user",
        "content": "Imagine that you need to describe yourself to a blind person. Provide a detailed description of your self no longer than 300 characters."
    }
    friendly.history.extend([message])
    friendly.chatbot.make_call(messages=friendly.history)
    drawing = friendly.chatbot.get_response()
    image_caller = ImageCaller(
        prompt="In the stile of a cartoon draw a person who says for herself that is: " + drawing
    )
    image_caller.generate_image()
    #image_caller.display_image()
    evil = GenericChatBot(
        personality="hateful and evil"
    )
    evil._initiate_personality()
    evil.history.extend([{
        "role": "system",
        "content": """
Think about your personality. Come up with a description what kind of
a person you would be. How would your face look like? Would you have
glasses or mustache? What kind of clothes you would wear? How would you
speak to other people? What would you do in you free time? What would 
you think about society? Think about all of that and, think about all
of those characteristics of your self as a person. When asked by the
user provide the answer according to those characteristics. Always be
yourself, and do not go outside these characteristics when asked
questions by the user.
"""}])
    message = {
        "role": "user",
        "content": """
Imagine that you need to describe yourself to a blind person. 
Provide a detailed description of your self no longer than 300 characters.
"""
    }
    evil.history.extend([message])
    evil.chatbot.make_call(messages=evil.history)
    drawing = evil.chatbot.get_response()
    image_caller = ImageCaller(
        prompt="In the style of a cartoon draw a person who says for herself that is: " + drawing
    )
    image_caller.generate_image()
    #image_caller.display_image()

    encounter = [{
        "role": "assistant",
        "content": """
Imagine being on a street. It is a nice day and you feel just exactly
according to your characteristics. Suddenly, you see another person
and you decide to approach this person. What would you say to this
other person on the street?
"""
    }]
    friendly.history.extend(encounter)
    friendly.chatbot.make_call(messages=friendly.history)
    encounter_response = friendly.chatbot.get_response()
    friendly.history.extend([{
        'role': 'assistant',
        'content': ''
    }])    
    eviel_response = [{
        "role": "assistant",
        "content": """
Imagine being on a street. It is a nice day and you feel just exactly
according to your characteristics. Suddenly, you see another person
approaches you and asks you this: %s What would you say to this
other person on the street?
""" % (encounter_response)
}]
    evil.history.extend(eviel_response)
    for exchanges in range(0, 5):
        evil.chatbot.make_call(messages=evil.history)
        response_ev = evil.chatbot.get_response()
        message_for_friendly = [{
            'role': 'user',
            'content': response_ev
        }]
        friendly.history.extend(message_for_friendly)
        friendly.chatbot.make_call()
        print(friendly.history[-1])
        print(evil.history[-1])
