import os, re, sys, time, json, random, string, ctypes, threading

from time import sleep

try:
    from pystyle import System, Colorate, Colors, Write
    from colorama import Fore, Style, init
    from requests import Session
    from bs4 import BeautifulSoup
    from datetime import datetime
except ModuleNotFoundError:
    os.system("pip install pystyle")
    os.system("pip install colorama")
    os.system("pip install requests")
    os.system("pip install bs4")
    os.system("pip install datetime")

from modules.tempmail import Tempmail
from modules.console import Output
from modules.utils import Utils

class Console:
    def title():
        while Stats.working:
            current_time = time.time()
            elapsed_time = current_time - Stats.start
            if elapsed_time != 0:
                try:
                    success_rate = round((Stats.created / (Stats.failed + Stats.created)) * 100, 2)
                except ZeroDivisionError:
                    success_rate = 0

                elapsed_days = int(elapsed_time // 86400)
                elapsed_hours = int((elapsed_time % 86400) // 3600)
                elapsed_minutes = int((elapsed_time % 3600) // 60)
                elapsed_seconds = int(elapsed_time % 60)
                ctypes.windll.kernel32.SetConsoleTitleW(f'𝓐𝓵𝓲𝓮𝓷𝔀𝓪𝓻𝓮 𝓐𝓬𝓬𝓸𝓾𝓷𝓽 𝓖𝓮𝓷𝓮𝓻𝓪𝓽𝓸𝓻 | 𝓖𝓮𝓷𝓮𝓻𝓪𝓽𝓮𝓭: {Stats.created} - 𝓕𝓪𝓲𝓵𝓮𝓭: {Stats.failed} @ 𝓢𝓾𝓬𝓬𝓮𝓼𝓼 𝓡𝓪𝓽𝓮: {success_rate}% - 𝓔𝓵𝓪𝓹𝓼𝓮𝓭: {elapsed_days}𝓭 {elapsed_hours}𝓱 {elapsed_minutes}𝓶 {elapsed_seconds}𝓼 | 𝓭𝓲𝓼𝓬𝓸𝓻𝓭.𝓰𝓰/𝓻𝓪𝓭𝓾𝓬𝓸𝓻𝓭')
            sleep(0.1)

class Stats:
    created = 0
    failed = 0
    errors = 0
    start = time.time()
    working = True

class Headers:
    csrf_headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'es',
        'Referer': 'https://eu.alienwarearena.com/login?return=%2Fucf%2FGiveaway',
        'Sec-Ch-Ua': '"Chromium";v="122", "Not(A:Brand";v="24", "Microsoft Edge";v="122"',
        'Sec-Ch-Ua-Mobile': '?0',
        'Sec-Ch-Ua-Platform': '"Windows"',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Fetch-User': '?1',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36 Edg/122.0.0.0'
    }

    register_headers = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "es",
        "Cache-Control": "max-age=0",
        "Connection": "keep-alive",
        "Host": "in.alienwarearena.com",
        "Origin": "https://in.alienwarearena.com",
        "Referer": "https://in.alienwarearena.com/account/register",
        "Sec-Ch-Ua": '"Chromium";v="122", "Not(A:Brand";v="24", "Microsoft Edge";v="122"',
        "Sec-Ch-Ua-Mobile": "?0",
        "Sec-Ch-Ua-Platform": '"Windows"',
        "Sec-Fetch-Dest": "document",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-Site": "same-origin",
        "Sec-Fetch-User": "?1",
        "Upgrade-Insecure-Requests": "1",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36 Edg/122.0.0.0"
    }

    email_headers = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "es",
        "Connection": "keep-alive",
        "Host": "mandrillapp.com",
        "sec-ch-ua": '"Chromium";v="122", "Not(A:Brand";v="24", "Microsoft Edge";v="122"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"Windows"',
        "Sec-Fetch-Dest": "document",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-Site": "none",
        "Sec-Fetch-User": "?1",
        "Upgrade-Insecure-Requests": "1"
    }

    promo_headers = {
        "Accept": "*/*",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "es",
        "Authorization": "",
        "Connection": "keep-alive",
        "Host": "giveawayapi.alienwarearena.com",
        "Origin": "https://in.alienwarearena.com",
        "Referer": "https://in.alienwarearena.com/",
        "sec-ch-ua": '"Chromium";v="122", "Not(A:Brand";v="24", "Microsoft Edge";v="122"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"Windows"',
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-site",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36 Edg/122.0.0.0"
    }

class Gen:
    def __init__(self) -> None:
        self.session = self._getSession()
        self.tempmail = Tempmail(self.session)
    
    def _getSession(self) -> str:
        session = Session()

        with open('proxies.txt', 'r') as f:
            proxies_list = f.readlines()

        proxy = random.choice(proxies_list).strip()

        session.proxies = {
            'https': f'http://{proxy}',
            'https': f'http://{proxy}'
        }

        return session
    
    def _makeAccount(self) -> str:
        try:
            email, token = self.tempmail._getEmail()
            print(f"{Output.gray} {Utils._time()} {Output.reset}({Output.blue}*{Output.reset}) {Output.gray}Got Email: {Output.light_cyan}{email} {Output.gray}({Output.cyan}{token}{Output.gray})")

            found = False
            while not found:
                time.sleep(1)
                cs = self.session.get('https://in.alienwarearena.com/account/register', headers=Headers.csrf_headers, allow_redirects=True)
                csrf = re.search(r'id="user_registration__token" name="user_registration\[_token\]" value="([^"]+)"', cs.text).group(1)
                if csrf != None:
                    found = True

            print(f"{Output.gray} {Utils._time()} {Output.reset}({Output.light_blue}?{Output.reset}) {Output.gray}Got Csrf: {Output.light_cyan}{csrf[:69]}********")

            data = {
                "user_registration[email][first]": email,
                "user_registration[email][second]": email,
                "user_registration[birthdate][month]": random.randint(1, 12),
                "user_registration[birthdate][day]": random.randint(1, 28),
                "user_registration[birthdate][year]": random.randint(1980, 2000),
                "user_registration[termsAccepted]": 1,
                "user_registration[_token]": csrf,
                "user_registration[steamId]": "",
                "user_registration[battlenetOauthProfileId]": "",
                "user_registration[timezone]": "Europe/Madrid",
                "user_registration[sourceInfo]": None,
                "user_registration[referralCode]": "",
                "user_registration[recaptcha3]": "" # Ez Bypass 😂💀
            }

            r = self.session.post("https://in.alienwarearena.com/account/register", headers=Headers.register_headers, data=data)
            if r.url != 'https://in.alienwarearena.com/account/check-email':
                print(f"{Output.gray} {Utils._time()} {Output.reset}({Output.red}-{Output.reset}) {Output.gray}Error Registering: {Output.light_cyan}{email}")
                Stats.failed += 1
                self._makeAccount()
            
            print(f"{Output.gray} {Utils._time()} {Output.reset}({Output.light_magenta}^{Output.reset}) {Output.gray}Sent Verification Link: {Output.light_cyan}{email}")
            verify_link = self.tempmail._getLink(token)
            print(f"{Output.gray} {Utils._time()} {Output.reset}({Output.light_cyan}@{Output.reset}) {Output.gray}Verify Link: {Output.light_cyan}{verify_link[:85]}********")
            r = self.session.get(verify_link, allow_redirects=True)

            found = False
            while not found:
                time.sleep(1)
                reg = self.session.get(r.url)
                regToken = re.search(r'name="platformd_user_confirm_registration\[_token\]" value="([^"]+)"', reg.text).group(1)
                if regToken != None:
                    found = True

            data = {
                "platformd_user_confirm_registration[confirm]": "",
                "platformd_user_confirm_registration[_token]": regToken
            }

            r = self.session.post(r.url, headers=Headers.register_headers, data=data, allow_redirects=True)
            print(f"{Output.gray} {Utils._time()} {Output.reset}({Output.light_green}#{Output.reset}) {Output.gray}Confirmed Token: {Output.light_cyan}{verify_link[69:129]}********")
            
            found = False
            while not found:
                time.sleep(1)
                inc = self.session.get("https://www.alienwarearena.com/incomplete")
                incToken = re.search(r'name="platformd_incomplete_account\[_token\]" value="([^"]+)"', inc.text).group(1)
                if incToken != None:
                    found = True

            data = {
                "platformd_incomplete_account[username]": f'H4cK3dR4Du{random.randint(9999, 9999999)}',
                "platformd_incomplete_account[password][first]": "H4cK3dR4Du@",
                "platformd_incomplete_account[password][second]": "H4cK3dR4Du@",
                "platformd_incomplete_account[_token]": incToken
            }

            r = self.session.post("https://in.alienwarearena.com/incomplete", headers=Headers.register_headers, data=data, allow_redirects=True)

            found = False
            while not found:
                time.sleep(1)
                inc = self.session.get("https://www.alienwarearena.com/incomplete")
                incToken = re.search(r'name="platformd_incomplete_account\[_token\]" value="([^"]+)"', inc.text).group(1)
                if incToken != None:
                    found = True

            data = {
                "platformd_incomplete_account[firstname]": "Jorge",
                "platformd_incomplete_account[lastname]": "Mendoza",
                "platformd_incomplete_account[country]": "LT",
                "platformd_incomplete_account[state]": "2250",
                "platformd_incomplete_account[preferredGenre]": random.choice(["indie", "action", "adventure"]),
                "platformd_incomplete_account[_token]": incToken
            }

            r = self.session.post("https://in.alienwarearena.com/incomplete", headers=Headers.register_headers, data=data, allow_redirects=True)
            if r.status_code != 200:
                print(f"{Output.gray} {Utils._time()} {Output.reset}({Output.red}-{Output.reset}) {Output.gray}Failed Registering Account: {Output.light_cyan}{email}")
                Stats.failed += 1
                self._makeAccount()
            
            print(f"{Output.gray} {Utils._time()} {Output.reset}({Output.green}+{Output.reset}) {Output.gray}Account Created: {Output.light_cyan}{email}:H4cK3dR4Du@")
            Stats.created += 1
            with open("Results/accounts.txt", "a+", encoding="utf-8") as f:
                f.write(f"{email}:H4cK3dR4Du@\n") 
        except:
            pass

        """
        r = self.session.get("https://in.alienwarearena.com/ucf/show/2170237/boards/contest-and-giveaways-global/one-month-of-discord-nitro-exclusive-key-giveaway", headers=Headers.register_headers)
        user_id_match = re.search(r'var user_id\s*=\s*(\d+);', r.text)
        user_uuid_match = re.search(r'var user_uuid\s*=\s*"(.*?)";', r.text)
        user_country_match = re.search(r'var user_country\s*=\s*"(.*?)";', r.text)
        login_id_match = re.search(r'var login_id\s*=\s*(\d+);', r.text)
        authorization_token_match = re.search(r'"token"\s*:\s*"([^"]+)"', r.text)
        user_id = int(user_id_match.group(1))
        user_uuid = user_uuid_match.group(1)
        user_country = user_country_match.group(1)
        login_id = int(login_id_match.group(1))
        token_value = authorization_token_match.group(1)

        Headers.promo_headers['Authorization'] = token_value

        got_promo = False
        while not got_promo:
            params = {
                "giveaway_uuid": "df863897-304c-4985-830c-56414830ade7",
                "api_key": "a75eb2f0-3f7a-4742-96c7-202977acb4cf",
                "user_uuid": user_uuid,
                "recaptcha_token": "03AFcWeA74rXJ6jT5eL0H38rZ4KbJKV2e-nyClcCdBTT0LKGbguZh05SFVBO0IRvCjlptl3jj8NTOhTVwmRcS_MMw49xxU9tGmRh_tXpuK8y0sfsRpKdLpCX53iLPPC3OL7cyaVJphpn3_VV6Mq8kVqZDvKKPmZw2mwVsQOd_hghFQ1ulo7sWl5cdXkk3lT-3WjgG7MDi-tMm-j_EnropNqOMwpbb38F_DX_5sOCbYEZciSSRM174auHhBa8i7VBq9EwDoAecGDZMYNWCGA_QGiCY87Q4fRO2-JcGDOUTnjS4PiHFbN7yHDzq2RQ6kqjIclUVS11k05-hx-Wly2yJVvQ-wHZ8dWnzNy8YIVBJ75ulepY0elAQNwrW7Hf22Gb-T3_-4PiHhwdLsTnA5qKej1xdtyND_AgPiMhH_14Rm5SR6dFRgOEGYC2DMpwwUZ4-MCIuhmTx6Ieyrym61fVMOpTkacpWFT_0AkBuaWx-vV4onq6Q0EDIq8bysh_gniJIJdVE8cBkHynsROHjiKcvNydIEm-9MCSWwAsotK78vL3NF2Wq6OCmzGmz-BPos3PgrwepbcU1AMmPZACCbZ2M4aqcIlTwSTPQdu-QnZt5wi75PC-FdBOF9CDsfgfiXLDttdEC9cZ3MIehLRTmwueca5edpQcCYHYWWZaM09WH_iIXgDl7B_rK_VF99X5mFNxrTezTxeMZZ82UsxbzkmzG00mjVEah-a8LUF5Vt3ol1SA7H6CbrKKK31rt7YBNEgVKEghHNB-axSNzJmWjvx5t7OSrRvFL7X9eZCRo34hjf17n7Ax5uD6T004hxvNbDiOIMUMQVqc5Iiiv-cBmyK220mMU7UFzm0Ux798_OE90q0I3EbUEu2bMRzUJB9qZqQuPRFxqKp4FvXRxyMJ5RpDuXvxJSPTZx6QRGwVaNvp7ULaPloaKEcsIWcZaGJm4wffBplNdmYmDK12d1jL8jIPN-4BbmKo9tp6U5qBapxmHWIFXjhZVI70tj2-wqd3FMN2htPnlMdP0eLnxRS1Vy3r22fKrJ1P9Ei2I6V7i8GSCb9-qXAH6vPx_TLdbm6n6-r_LvmLq8IOydxquC0doNarmGJDaN-56NY3mQff_yWNikCzEJSkZWuFrGZVZTUp8LmBjVES8fUhgMS-ovrdbwkXqq1PwWRmro8vMX1vQbBKL7QxSTgvUKuPfTuvdDhITjV1cAmOO5JS1dDD00JLUtUFtrb0s31KMFRqMr5P3MzvbleK-2dGMZNHcYyDQnAYoTMXIKb7bLtUzKEZ0DmGXwB-hwsBnTDgiM6ZMTi_XmG2UGMJrzLIcuKNRCD-umijUfQNwjM2jAfBz8hbqQWd0uBsswJRxs7mI45BBrKDMJyIvWH25GlnVscfQv3A-JObc0ADEfUx3SVetmj9lNOarPyTzeWsh0kxdimr-kHmaD-ODw5myCvRhy5IoevQXRDZD49F5wHGXJEQMoAuiv8JXdLgd4AkHqLmvNfsiM88rMtNuTcMTF8ZAGeTjVj8St1wSYHZ0ZcOUZXvwQkDH7IbnjxWNjy3U-H21T9BbXnE1blqjbtBPvEXVC0Rkur5J9CUyM9eIzmoMZJqIg0R1-SAMZ8NPgr7bqx7iYyhAjfs4bx-_KxTVv9J3Smlmg-pFZ2ml-s7ycBCQG8zRC33jWVI__xlxjqBlwfIxjsOS8SWc4J_w_3nyhWNPByw-eKnc",
                "extra_info": json.dumps({
                    "siteId": 5,
                    "siteGroupId": 1,
                    "loginId": login_id,
                    "countryCode": user_country,
                    "userId": user_id
                })
            }
            
            time.sleep(3)

            r = self.session.get("https://giveawayapi.alienwarearena.com/production/key/get", headers=Headers.promo_headers, params=params)
            if r.status_code != 200:
                print(r.text)
            else:
                print(r.status_code)
                
        """
        # Im too lazy to get promos since Alienware always is at 0 stock 😂
        # You can continue ur code here

if __name__ == "__main__":
    threads = json.load(open("config.json"))['threads']
    System.Clear()

    try:
        threading.Thread(target=Console.title).start()
        while True:
            while threading.active_count()-1 < threads:
                alienware = Gen()
                threading.Thread(target=alienware._makeAccount).start()
            sleep(1)
    except:
        pass