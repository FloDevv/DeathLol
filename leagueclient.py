import requests
import logging

class LeagueClient:
    def __init__(self):
        self.base_url = "https://127.0.0.1:2999/liveclientdata"
        self.playerlist_url = f"{self.base_url}/playerlist"
        self.gamedata_url = f"{self.base_url}/gamestats"
        self.allgamedata_url = f"{self.base_url}/allgamedata"
        self.summoner_name = None
        self.last_state = False

    def is_game_active(self):
        try:
            response = requests.get(self.allgamedata_url, verify=False, timeout=2)
            if response.status_code == 200:
                data = response.json()
                if 'activePlayer' in data:
                    self.summoner_name = data['activePlayer'].get('summonerName')
                    logging.info(f"Game is active, found summoner: {self.summoner_name}")
                    return True
            return False
        except:
            return False

    def get_player_state(self):
        try:
            if not self.is_game_active():
                logging.info("Waiting for active game...")
                return False

            response = requests.get(self.playerlist_url, verify=False, timeout=2)
            data = response.json()

            for player in data:
                is_local = (
                    player.get('summonerName') == self.summoner_name or
                    player.get('isLocalPlayer', False)
                )

                if is_local:
                    current_state = player.get('isDead', False)
                    if current_state != self.last_state:
                        logging.info(f"Death state changed: {current_state}")
                        self.last_state = current_state
                    return current_state

            logging.warning(f"Player {self.summoner_name} not found in player list")
            return False

        except requests.exceptions.RequestException as e:
            logging.error(f"Error connecting to League client: {str(e)}")
            return False
        except Exception as e:
            logging.error(f"Unexpected error: {str(e)}")
            return False
