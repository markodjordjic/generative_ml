from fastapi import APIRouter
from utilities.calling import Caller
router = APIRouter()

@router.post("/read_request")
async def read_request(query: str):

    prompt_template = f'''
        You are a color palette generating assistant that responds to text 
        prompts for color palettes. The palettes should have between 2 
        and 8 colors. Colors should be stored in a list of hexadecimal 
        color codes. Read the example below.

        Q: Convert the following description of a color palette into a 
        list of colors: The Mediterranean Sea
        A: ["#006699", "#66CCCC", "#F0E68C", "#008000", "#F08080"]

        By using the format above as an example, send me a palette of 
        colors for: {query}
        A:    
    '''

    caller = Caller(max_tokens=128, prompt=prompt_template)
    caller.make_call()
    response = caller.get_response()

    return {
        'query': query,
        'response': response
    }

@router.get("/get_response")
async def get_response():
    pass