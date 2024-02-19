import requests, json, schedule
from time import sleep


USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:123.0) Gecko/20100101 Firefox/123.0"

def main():
    
    with requests.Session() as sess:
        
        sess.headers = {
            'User-Agent': USER_AGENT
        }
        
        with open('./usernames.txt', 'r') as file:
            USERNAMES = [username.lower().split(":") for username in file.read().split('\n')]
        
        for username in USERNAMES:
        
            # To get the needed cookies
            sess.get("https://u.gg")

            payload = {"operationName":"UpdatePlayerProfile","variables":{"regionId":f"{username[0]}1","riotUserName":username[1],"riotTagLine":username[2]},"query":"query UpdatePlayerProfile($regionId: String!, $riotUserName: String!, $riotTagLine: String!) {\n  updatePlayerProfile(\n    regionId: $regionId\n    riotUserName: $riotUserName\n    riotTagLine: $riotTagLine\n  ) {\n    success\n    errorReason\n    __typename\n  }\n}"}
            
            req = sess.post(
                "https://u.gg/api",
                headers={
                    'Content-Type': "application/json",
                    "Content-Length": str(len(json.dumps(payload))),
                    "User-Agent": USER_AGENT,
                    "Accept-Language": "en-US,en;q=0.5",
                    "Accept-Encoding": "gzip, deflate, br",
                    "Host": "u.gg"
                },
                data=json.dumps(payload)
            )
            
            data = req.json()
            
            if data['data']['updatePlayerProfile']['success'] is True:
                print(f"Sucessfully updated {username[1]}'s profile")
            else:
                print(f"Failed to updated {username[1]}'s profile, reason => {data['data']['updatePlayerProfile']['errorReason']}")


schedule.every(20).minutes.do(main)

while True:
    schedule.run_pending()
    sleep(1)