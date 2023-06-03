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
      return Response({'error': f'{error.message}'}, status.HTTP_400_BAD_REQUEST)
    except InvalidYearCupError as error:
      return Response({'error': f'{error.message}'}, status.HTTP_400_BAD_REQUEST)
    except ImpossibleTitlesError as error:
      return Response({'error': f'{error.message}'}, status.HTTP_400_BAD_REQUEST)

    team = Team.objects.create(**request.data)

    return Response(model_to_dict(team), status.HTTP_201_CREATED)

