from rest_framework import serializers
from .models import ModuleRecord

class ModuleRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = ModuleRecord
        fields = '__all__'
