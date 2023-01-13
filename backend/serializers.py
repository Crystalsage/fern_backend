from rest_framework import serializers
from .models import Partner

class PartnerSerializer(serializers.ModelSerializer):
    password = serializers.SerializerMethodField()

    class Meta:
        model = Partner
        exclude = ('partner_id',)

    def get_password(self, obj):
        return self.context['request'].data.get('password')
