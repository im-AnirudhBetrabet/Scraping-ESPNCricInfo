from csv import DictReader, DictWriter

from requests import get
from bs4 import BeautifulSoup
from time import sleep
from src.ESPNCricInfo import ESPNCricInfo


class Players(ESPNCricInfo):
    def __init__(self):
        super().__init__()
        self.players_page = self.homepage +  "/cricketers"
        self.team_data = self._set_team_data()
        self.alphabets = 'abcdefghijklmnopqrstuvwxyz'
        self._headers = ['player-id', 'team-id', 'player-name', 'player-page']
        self._file_name = '../data/Players.csv'
        self._write_headers()


    def _write_headers(self):
        with open(self._file_name, 'w', newline="", encoding="UTF-8") as players_file:
            csv_writer = DictWriter(players_file, fieldnames=self._headers)
            csv_writer.writeheader()


    def write_player_data(self, player_data: dict):
        with open(self._file_name, 'a', newline="", encoding="UTF-8") as players_file:
            csv_writer = DictWriter(players_file, fieldnames=self._headers)
            csv_writer.writerow(player_data)


    def _set_team_data(self):
        with open("../data/teams.csv", 'r') as teams_data_file:
            csv_reader = DictReader(teams_data_file)
            data = dict()
            for team in csv_reader:
                data[team['team-name']] = team
            return data
    def get_page_content(self):
        for team in self.team_data.values():
            for alphabet in self.alphabets:
                url = self.players_page + team['team-page'] + "/alpha-" + alphabet
                print(url)
                sleep(20)
                page = get(url).content
                parsed_data = BeautifulSoup(page, 'html.parser')
                player_divs = parsed_data.select("div.ds-grid")[0].select("div.ds-flex")
                for player_div in player_divs:
                    item = player_div.select("div.ds-flex-col")
                    temp = dict()
                    if len(item) != 0:
                        player_page = item[0].select("a")[0].get_attribute_list("href")[0]
                        temp['player-name'] = str(item[0].select("span")[0].getText())
                        temp['player-id'] = player_page.split("-")[-1]
                        temp['player-page'] = player_page
                        temp['team-id'] = team['team-id']
                        self.write_player_data(temp)


players = Players()
players.get_page_content()
