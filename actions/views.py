from django.shortcuts import render

import json
from django.http import JsonResponse
from rest_framework import status
from rest_framework.decorators import api_view
from .serializers import ActionSerializer
from datetime import date

ACTIONS_FILE = 'actions/actions.json'


def read_actions():
    """
    Read actions data from JSON file.

    Returns:
        list: List of action dictionaries loaded from JSON file
    """
    with open(ACTIONS_FILE, 'r') as f:
        return json.load(f)


def write_actions(actions):
    """
    Write actions data to JSON file with date serialization support.

    Args:
        actions (list): List of action dictionaries to write to file
    """
    def convert(o):
        # Convert date objects to ISO format for JSON serialization
        if isinstance(o, date):
            return o.isoformat()
        return o

    with open(ACTIONS_FILE, 'w') as f:
        json.dump(actions, f, indent=4, default=convert)


@api_view(['GET', 'POST'])
def action_list(request):
    """
    Handle GET and POST requests for actions list.

    GET: Returns all actions
    POST: Creates a new action

    Args:
        request: Django request object

    Returns:
        JsonResponse: Serialized actions data or error response
    """
    actions = read_actions()

    if request.method == 'GET':
        serializer = ActionSerializer(actions, many=True)
        return JsonResponse(serializer.data, safe=False)

    elif request.method == 'POST':
        data = request.data
        new_id = max([a['id'] for a in actions], default=0) + 1
        data['id'] = new_id

        # Validate and serialize the new action data
        serializer = ActionSerializer(data=data)
        if serializer.is_valid():
            # Add new action to list and save to file
            actions.append(serializer.data)
            write_actions(actions)
            return JsonResponse(serializer.data, status=status.HTTP_201_CREATED)
        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PUT', 'PATCH', 'DELETE'])
def action_detail(request, id):
    """
    Handle PUT, PATCH, and DELETE requests for individual actions.

    PUT: Replace entire action
    PATCH: Update partial action data
    DELETE: Remove action

    Args:
        request: Django request object
        id (int): Action ID to operate on

    Returns:
        JsonResponse: Updated action data, success message, or error response
    """
    actions = read_actions()
    # Find action by ID, return None if not found
    action = next((a for a in actions if a['id'] == id), None)

    if not action:
        return JsonResponse({'error': 'Not found'}, status=status.HTTP_404_NOT_FOUND)

    if request.method in ['PUT', 'PATCH']:
        serializer = ActionSerializer(
            action, data=request.data, partial=(request.method == 'PATCH'))
        if serializer.is_valid():
            updated_action = serializer.validated_data
            updated_action['id'] = id  # Ensure ID stays correct

            # Update the action in the list and save to file
            actions = [a if a['id'] != id else updated_action for a in actions]
            write_actions(actions)
            return JsonResponse(updated_action)
        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        actions = [a for a in actions if a['id'] != id]
        write_actions(actions)
        return JsonResponse({'message': 'Deleted'}, status=status.HTTP_204_NO_CONTENT)
