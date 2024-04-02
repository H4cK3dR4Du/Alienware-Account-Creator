import time, re

from requests import Session

class Tempmail:
    def __init__(self, session: Session) -> None:
        self.session = session

    def _getEmail(self) -> tuple[str, str]:
        r = self.session.get('https://api.tempmail.lol/generate').json()
        if "address" in r:
            return r["address"], r["token"]
        else:
            Tempmail._getEmail()

    def _getLink(self, token) -> str:
        found_link = False
        while not found_link:
            time.sleep(9)
            r = self.session.get(f"https://api.tempmail.lol/v2/inbox?token={token}")
            json_data = r.json()
            all_links = re.findall(r'href="([^"]+)"', str(json_data))
            for link in all_links:
                if 'in.alienwarearena.com?' in link:
                    found_link = True
                    return link