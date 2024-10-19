from csv import DictWriter

from requests import get
from bs4 import BeautifulSoup

from src.ESPNCricInfo import ESPNCricInfo


class Teams(ESPNCricInfo):
    def __init__(self):
        super().__init__()
        self.team_page = self.homepage + "/team"
        self.team_data = dict()


    def get_countries_page(self):
        data = get(self.team_page)
        return data.content

    def parse_data(self):
        data = self.get_countries_page()
        parsed_html = BeautifulSoup(data, 'html.parser')
        teams_data = parsed_html.select('div.ds-p-0')[0]
        team_references = teams_data.select("a")
        for team_reference in team_references:
            team_page = team_reference.get_attribute_list("href")[0]
            team_name = team_reference.select("span")[0].getText()
            team_id = str(team_page).split("-")[-1]
            temp_dict = dict()
            temp_dict['team-name'] = team_name
            temp_dict['team-id'] = team_id
            temp_dict['team-page'] = team_page
            self.team_data[int(team_id)] = temp_dict
        self._sort_team_data()

    def _sort_team_data(self):
        sorted_keys = sorted(self.team_data.keys())
        new_dict = dict()
        for i in sorted_keys:
            new_dict[i] = self.team_data[i]
        self.team_data = new_dict


    def write_csv(self):
        self.parse_data()
        with open("../data/teams.csv", 'w', newline="") as team_data_file:
            headers = ['team-id', 'team-name', 'team-page']
            csv_writer = DictWriter(team_data_file, fieldnames=headers)
            csv_writer.writeheader()
            for team in self.team_data.values():
                csv_writer.writerow(team)


countries = Teams()
countries.write_csv()
