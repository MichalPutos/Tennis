import requests
import json


def match_request_ids():
    burp0_url = "https://sport.pin-up.bet:443/InPlay/GetEventsList"
    burp0_cookies = {"__cfduid": "dff203d9ffe7cb9f07101c0fbf0ca23511562058910", "iOSFix": "sport.pin-up.bet",
                     "_ga": "GA1.2.1012685747.1562058910", "_gid": "GA1.2.1444933814.1562058910", "_gat": "1",
                     "ASP.NET_SesssionId": "jkcaaod55pqmocuxodrcefxi",
                     "__cfruid": "4f5c6f69863ee1f7c6af549797383c6e11ba1cf3-1562066642", "_gat_gtag_UA_106090315_1": "1",
                     "_gat_gtag_UA_133587723_1": "1"}
    burp0_headers = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:60.0) Gecko/20100101 Firefox/60.0",
                     "Accept": "application/json, text/javascript, */*; q=0.01", "Accept-Language": "en-US,en;q=0.5",
                     "Accept-Encoding": "gzip, deflate",
                     "Referer": "https://sport.pin-up.bet/SportsBook/EventView/5125087?game=Facundo-Bagnis-Laurynas-Grigelis",
                     "Content-Type": "application/json; charset=utf-8", "X-Requested-With": "XMLHttpRequest",
                     "Connection": "close"}
    burp0_json = {"langId": 2, "partnerId": 65, "sportId": 3, "stTypes": [1, 702, 2, 3, 37]}
    web_data = requests.post(burp0_url, headers=burp0_headers, cookies=burp0_cookies, json=burp0_json).json()
    return [match_data["Id"] for match_data in web_data]


def request_match_data(event_id):
    burp0_url = "https://sport.pin-up.bet:443/InPlay/GetEventStakes"
    burp0_cookies = {"__cfduid": "dff203d9ffe7cb9f07101c0fbf0ca23511562058910", "iOSFix": "sport.pin-up.bet",
                     "_ga": "GA1.2.1012685747.1562058910", "_gid": "GA1.2.1444933814.1562058910", "_gat": "1",
                     "ASP.NET_SesssionId": "jkcaaod55pqmocuxodrcefxi",
                     "__cfruid": "4f5c6f69863ee1f7c6af549797383c6e11ba1cf3-1562066642", "_gat_gtag_UA_106090315_1": "1",
                     "_gat_gtag_UA_133587723_1": "1"}
    burp0_headers = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:60.0) Gecko/20100101 Firefox/60.0",
                     "Accept": "application/json, text/javascript, */*; q=0.01", "Accept-Language": "en-US,en;q=0.5",
                     "Accept-Encoding": "gzip, deflate",
                     "Referer": "https://sport.pin-up.bet/SportsBook/EventView/5125087?game=Facundo-Bagnis-Laurynas-Grigelis",
                     "Content-Type": "application/json; charset=utf-8", "X-Requested-With": "XMLHttpRequest",
                     "Connection": "close"}
    burp0_json = {"eventNumber": event_id, "langId": 2, "partnerId": 65}
    return requests.post(burp0_url, headers=burp0_headers, cookies=burp0_cookies, json=burp0_json).json()[0]


def parse_responses():
    event_ids = match_request_ids()
    results_list = []
    for event_id in event_ids:
        match_data = request_match_data(event_id)
        sub_results = {"Name": match_data["N"]}  # dict with name of the match to be populated by additional stakes data
        events = {}  # empty dict to be populated with stakes' values
        for stake_type in match_data["StakeTypes"]:
            match_winner = {}
            for k, v in stake_type.items():
                if "N" in k and 'result' in v.lower():
                    # process total result stakes
                    match_winner['1'] = str(stake_type["Stakes"][0]["F"])
                    match_winner['2'] = str(stake_type["Stakes"][1]["F"])
                    events["MatchWinner"] = match_winner
                if "N" in k and "set: winner" in v.lower():
                    # process set winner stakes
                    set_winner_1 = str(stake_type["Stakes"][0]["F"])
                    set_winner_2 = str(stake_type["Stakes"][1]["F"])
                    events[stake_type["N"].replace('Set: Winner', 'Set Winner')] = {"1": set_winner_1, "2": set_winner_2}
                if "N" in k and "game winner" in v.lower():
                    # process game winner stakes
                    game_winner_1 = str(stake_type["Stakes"][0]["F"])
                    game_winner_2 = str(stake_type["Stakes"][1]["F"])
                    events[stake_type["N"]] = {"1": game_winner_1, "2": game_winner_2}
            sub_results["Events"] = events
        results_list.append(sub_results)
    return json.dumps(results_list).replace(': ', ':').replace(', ', ',')


if __name__ == '__main__':
    print(parse_responses())
