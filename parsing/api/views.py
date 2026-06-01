from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response

from parsing.models import ParserRun
from parsing.services.parser_service import start_books_parser

class StartParserAPIView(APIView):
    def post(self, request):
        run = ParserRun.objects.create(name="Books parser", status="pending",)
        start_books_parser(run.id)

        return Response({"run_id": run.id, "status":"started"}, status.HTTP_201_CREATED)


class PauseParserAPIView(APIView):
    def post(self, request,run_id):
        ParserRun.objects.filter(id=run_id).update(status="paused")
        return Response({"status":"paused"})


class ResumeParserAPIView(APIView):
    def post(self, request,run_id):
        run = ParserRun.objects.get(id=run_id)
        start_books_parser(run.id)
        return Response({"status":"resume"})