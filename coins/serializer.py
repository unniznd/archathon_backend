from coins.models import WatchListModel, ProfileModel
from rest_framework import serializers

class ProfileSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username')
    wallet_id = serializers.IntegerField(source = 'user.pk')
    class Meta:
        model = ProfileModel
        exclude = ('user','id')

class WatchListSerializer(serializers.ModelSerializer):
    class Meta:
        model = WatchListModel
        exclude = ('id',)