from PIL import Image
import requests
from io import BytesIO



def search_result(i: int, url: str, tags: str, **kwargs) -> str:
        response = requests.get(url)
        img = Image.open(BytesIO(response.content))
        """ HTML scripts to display search results. """
        return f"""
            <div style="font-size:120%;">
                <b>Related Image{i}</b>
            </div>
            <div >
                <img src={url} width="500" >
            </div>
                
            
        """