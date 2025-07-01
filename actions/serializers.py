from rest_framework import serializers

# Serializer for Action model
# This is used to convert the model into a JSON format

class ActionSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    action = serializers.CharField(max_length=255)
    date = serializers.DateField()
    points = serializers.IntegerField()
