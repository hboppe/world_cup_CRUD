from exceptions import NegativeTitlesError, InvalidYearCupError, ImpossibleTitlesError

from datetime import datetime


def data_processing(team_info: dict):
  current_year = datetime.now().year

  def get_first_cup_year():
    first_cup_date = datetime.strptime(team_info["first_cup"], "%Y-%m-%d")
    first_cup_year = first_cup_date.year

    return first_cup_year

  def check_first_year_cup():
    first_cup_date = datetime.strptime(team_info["first_cup"], "%Y-%m-%d")
    first_cup_year = first_cup_date.year
    years_difference = first_cup_year - 1930

    return years_difference

  first_cup_year = get_first_cup_year()
  cup_years_difference = check_first_year_cup()

  if team_info["titles"] < 0:
    raise NegativeTitlesError()

  if cup_years_difference % 4 != 0 or cup_years_difference < 0:
    raise InvalidYearCupError()

  number_of_cups = (current_year - first_cup_year) // 4

  if number_of_cups < team_info["titles"]:
    raise ImpossibleTitlesError()
