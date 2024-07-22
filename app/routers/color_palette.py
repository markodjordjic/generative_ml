from fastapi import APIRouter
from utilities.calls import ChatCaller

router = APIRouter()

@router.post("/read_request")
async def read_request(query: str):

    system_content = """
        You are a color palette generating assistant that responds to text 
        prompts for color palettes. The palettes should have between 2 
        and 8 colors. Colors should be stored in a list of hexadecimal 
        color codes.
    """
    user_content = """
        Convert the following description of a color palette into a 
        list of colors: The Mediterranean Sea
    """

    messages = [
        {
            'role': 'system',
            'content': system_content.translate({'\t': None, '\n': None})
        },
        {
            'role': 'user',
            'content': user_content
        },
        {
            'role': 'assistant',
            'content': '["#006699", "#66CCCC", "#F0E68C", "#008000", "#F08080"]'
        },
        {
            'role': 'user',
            'content': f"By using the format above as an example, send me a palette of colors for: {query}"
        }
    ]

    caller = ChatCaller(max_tokens=128, messages=messages)
    caller.make_call()
    response = caller.get_response()

    return {
        'query': query,
        'response': response
    }

@router.get("/get_response")
async def get_response():
    pass