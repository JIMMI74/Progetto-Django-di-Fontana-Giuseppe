from rest_framework import serializers
from .models import RelatedPost

class RelatedpostSerializer(serializers.ModelSerializer):

    class Meta:
        model = RelatedPost
        fields = " _all_"


