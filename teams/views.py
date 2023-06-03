from rest_framework.views import APIView, status
from exceptions import ImpossibleTitlesError, InvalidYearCupError, NegativeTitlesError
from .models import Team
from django.forms.models import model_to_dict
from rest_framework.response import Response
from rest_framework.request import Request
from utils import data_processing


class TeamView(APIView):
  def get(self, request: Request) -> Response:
    teams = Team.objects.all()
    print(teams)
    teams_list = [model_to_dict(team) for team in teams ]
    return Response(teams_list)
  
  def post(self, request: Request) -> Response:
    try:
      data_processing(request.data)
    except NegativeTitlesError as error:
      return Response({'error': f'{error.args[0]}'}, status.HTTP_400_BAD_REQUEST)
    except InvalidYearCupError as error:
      return Response({'error': f'{error.args[0]}'}, status.HTTP_400_BAD_REQUEST)
    except ImpossibleTitlesError as error:
      return Response({'error': f'{error.args[0]}'}, status.HTTP_400_BAD_REQUEST)

    team = Team.objects.create(**request.data)

    return Response(model_to_dict(team), status.HTTP_201_CREATED)
  

class TeamDetailView(APIView):

  def get_team(self, team_id: int) -> Response:
    try:
      return Team.objects.get(id=team_id)
    except Team.DoesNotExist:
      return Response({'message': 'Team not found'}, status.HTTP_404_NOT_FOUND)

  def get(self, request: Request, team_id: int) -> Response:
  
    team = self.get_team(team_id)
    if isinstance(team, Response):
      return team
    
    return Response(model_to_dict(team), status.HTTP_200_OK)
  
  def patch(self, request: Request, team_id: int):
    
    team = self.get_team(team_id)
    if isinstance(team, Response):
      return team
    
    for key, value in request.data.items():
      if key != 'id':
        setattr(team, key, value)

    team.save()

    return Response(model_to_dict(team))

  def delete(self, request: Request, team_id: int):
    team = self.get_team(team_id)

    if isinstance(team, Response):
      return team
    
    team.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)


