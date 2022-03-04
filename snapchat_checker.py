import asyncio
import aiohttp
import os, sys
import colorama

class Snapchat_Username_Checker:
    def __init__(self):
        self.available = 0
        self.taken = 0
        self.deleted = 0
        self.checked = 0
        self.request_errors = 0
        self.rate_limits = 0
        self.xsrf_token = "TvN9CadcuzoqIzEYieQae0"
        self.manager = Data_Manager()

    async def check_username(self, username, session: aiohttp.ClientSession):
        payload = {
            "requested_username": username,
            "xsrf_token": self.xsrf_token
        }

        cookies = {
            "xsrf_token": self.xsrf_token
        }

        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36",
            "Content-Type": "application/x-www-form-urlencoded; charset=utf-8"
        }

        async with session.post('https://accounts.snapchat.com/accounts/get_username_suggestions', headers=headers, data=payload, cookies=cookies) as checking_response:
            try:
                if checking_response.status == 200:
                    self.checked += 1
                    response_body = await checking_response.json()
                    if response_body["reference"]["status_code"] == "OK":
                        self.available += 1
                        self.manager.write_usernames(username, "available")
                    elif response_body["reference"]["status_code"] == "DELETED":
                        self.deleted += 1
                        self.manager.write_usernames(username, "deleted")
                    else:
                        self.taken += 1
                        self.manager.write_usernames(username, "taken")
                    self.manager.clean_username_list(username)
                elif checking_response.status == 429:
                    self.rate_limits += 1
                else:
                    self.request_errors += 1

                print(f' \x1b[1;39m[\x1b[1;36m*\x1b[1;39m] Checked: ({self.checked}/{len(self.manager.usernames)}) | Available: ({self.available}) | Taken: ({self.taken}) | Deleted: ({self.deleted}) | Errors: ({self.request_errors}) | Rate Limits: ({self.rate_limits})', end='\r', flush=True)
            except:
                pass

    async def run_check(self):
        async with aiohttp.ClientSession() as session:
            for username in self.manager.usernames:
                await self.check_username(username, session)
                await asyncio.sleep(1.75)

    async def startup(self):
        print(' \x1b[1;39m[\x1b[1;36m*\x1b[1;39m] \x1b[1;33mSnapchat\x1b[1;39m Username Checker v1.0')
        self.manager.get_usernames()
        self.manager.filter_usernames()
        if len(self.manager.usernames) > 0:
            print(f'\n \x1b[1;39m[\x1b[1;36m+\x1b[1;39m] Usernames Gathered: ({len(self.manager.usernames)})\n')
            await self.run_check()
        else:
            print("\n \x1b[1;39m[\x1b[1;31m-\x1b[1;39m] No Usernames to Check\n")
            os._exit(0)


class Data_Manager:
    def __init__(self):
        self.usernames = []
    
    def get_usernames(self):
        with open('username_lists/usernames.txt', 'r') as username_file:
            [self.usernames.append(username.strip()) for username in username_file]
    
    def filter_usernames(self):
        self.usernames = [username for username in self.usernames if not (username.count(' ') > 0 or username.count(',') > 0 or username.count('.') > 0 or username.count('/') > 0 or username.count('\\') > 0 or username.count(':') > 0 or username.count(';') > 0 or username.count('?') > 0 or username.count('!') > 0 or username.count('@') > 0 or username.count('#') > 0 or username.count('$') > 0 or username.count('%') > 0 or username.count('^') > 0 or username.count('&') > 0 or username.count('*') > 0 or username.count('(') > 0 or username.count(')') > 0 or username.count('=') > 0 or username.count('+') > 0 or username.count('[') > 0 or username.count(']') > 0 or username.count('{') > 0 or username.count('}') > 0 or username.count('|') > 0 or username.count('<') > 0 or username.count('>') > 0 or username.count('`') > 0 or username.count('~') > 0 or username.count("'") > 0 or username.count('"') > 0 or username.count('\n') > 0 or username.count('\t') > 0 or username.count('\r') > 0 or username.count('\f') > 0 or username.count('\v') > 0 or username.count('\b') > 0 or username.count('_') > 1 or username.count('-') > 1)]
        self.usernames = [username for username in self.usernames if len(username) <= 15]

    def write_usernames(self, username, username_status):
        with open(f'results/{username_status}_usernames.txt', 'a') as username_file:
            username_file.write(username + '\n')

    @staticmethod
    def clean_username_list(username):
        with open('username_lists/usernames.txt', 'r+') as current_file:
            lines = current_file.readlines()
            current_file.seek(0)
            current_file.truncate()
            for line in lines:
                if line != username + '\n':
                    current_file.write(line)


if __name__ == '__main__':
    colorama.init(autoreset=True)
    os.system('cls' if sys.platform == 'win32' else 'clear')
    asyncio.get_event_loop().\
        run_until_complete(Snapchat_Username_Checker().startup())