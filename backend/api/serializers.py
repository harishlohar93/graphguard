from rest_framework import serializers
from .models import Account , Alert , AuditLog, Cluster

class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = '__all__'
        
        
class AlertSerializer(serializers.ModelSerializer):
    class Meta:
        model = Alert
        fields = '__all__'  
        
class AuditLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = AuditLog
        fields = '__all__'      
             
class ClusterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cluster
        fields = '__all__'
        