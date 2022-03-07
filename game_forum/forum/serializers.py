from rest_framework.serializers import ModelSerializer

from forum.models import *


class GameSerializer(ModelSerializer):
    class Meta:
        model = Game
        fields = '__all__'


class CompanySerializer(ModelSerializer):
    class Meta:
        model = Company
        fields = '__all__'


class DeveloperSerializer(ModelSerializer):
    class Meta:
        model = Developer
        fields = '__all__'


class PublisherSerializer(ModelSerializer):
    class Meta:
        model = Publisher
        fields = '__all__'


class SponsorSerializer(ModelSerializer):
    class Meta:
        model = Sponsor
        fields = '__all__'


class GenreSerializer(ModelSerializer):
    class Meta:
        model = Genre
        fields = '__all__'


class AwardSerializer(ModelSerializer):
    class Meta:
        model = Award
        fields = '__all__'
