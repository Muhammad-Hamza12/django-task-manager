from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Task
from .serializers import TaskSerializer
from django.db import connection
from datetime import timedelta

# Create your views here.

@api_view(['POST'])
def create_task(request):
    if request.method == 'POST':
        title = request.data.get('title')
        duration = request.data.get('duration')

        # Ensure user is authenticated
        if not title or not duration:
            return Response({"error": "Title and duration are required"}, status=status.HTTP_400_BAD_REQUEST)

        task = Task.objects.create(
            title=title,
            duration=timedelta(minutes=int(duration)),
            user=request.user
        )
        serializer = TaskSerializer(task)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

@api_view(['GET'])
def get_tasks(request):
    if request.method == 'GET':
        tasks = Task.objects.filter(user=request.user).order_by('-created_at')[:4]
        serializer = TaskSerializer(tasks, many=True)
        return Response(serializer.data)

@api_view(['GET'])
def retrieve_task(request, pk):
    if request.method == 'GET':
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM tasks_task WHERE id = %s AND user_id = %s", [pk, request.user.id])
            row = cursor.fetchone()

        if row:
            task = {
                'id': row[0],
                'title': row[1],
                'duration': row[2],
                'created_at': row[3],
                'updated_at': row[4],
            }
            return Response(task)
        else:
            return Response({"error": "Task not found or not authorized"}, status=status.HTTP_404_NOT_FOUND)

@api_view(['PUT'])
def update_task(request, pk):
    if request.method == 'PUT':
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM tasks_task WHERE id = %s AND user_id = %s", [pk, request.user.id])
            row = cursor.fetchone()

        if row:
            title = request.data.get('title')
            if title:
                with connection.cursor() as cursor:
                    cursor.execute("UPDATE tasks_task SET title = %s WHERE id = %s AND user_id = %s", [title, pk, request.user.id])
                return Response({"message": "Task updated successfully"})
            else:
                return Response({"error": "Title is required"}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"error": "Task not found or not authorized"}, status=status.HTTP_404_NOT_FOUND)


@api_view(['DELETE'])
def delete_task(request, pk):
    """
    Delete a task if it belongs to the logged-in user.
    Only tasks created by the logged-in user can be deleted.
    """
    if request.method == 'DELETE':
        # Check if the task exists and belongs to the logged-in user
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM tasks_task WHERE id = %s AND user_id = %s", [pk, request.user.id])
            row = cursor.fetchone()

        if row:
            # If the task exists, delete it
            with connection.cursor() as cursor:
                cursor.execute("DELETE FROM tasks_task WHERE id = %s AND user_id = %s", [pk, request.user.id])
            return Response({"message": "Task deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
        else:
            # If the task does not exist or does not belong to the logged-in user
            return Response({"error": "Task not found or not authorized to delete"}, status=status.HTTP_404_NOT_FOUND)