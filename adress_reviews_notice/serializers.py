from rest_framework import serializers
from .models import *
 

#  =================== hostel rating serializer ======================== 
class HotelRatingSerializer(serializers.ModelSerializer):
    hotel=serializers.SlugRelatedField(slug_field='name',read_only=True)
    user=serializers.SlugRelatedField(slug_field='username',read_only=True)
    class Meta:
        model = HotelRating
        fields =["id","rating","hotel","user","created_at"]
    def validate_rating(self,value):
        if value < 1 or value > 5:
            raise serializers.ValidationError("Rating must be between 1 and 5")
        return value



# ===================================   hostel review serializer ========================

class HostelReviewSerializer(serializers.ModelSerializer):
    hostel=serializers.SlugRelatedField(slug_field='name',read_only=True)
    user=serializers.SlugRelatedField(slug_field='username',read_only=True)
    class Meta:
        model = Hostel_review
        fields = ["id","content","hostel","user","created_at"]
    def validate_content(self,value):
        if len(value) < 10:
            raise serializers.ValidationError("Content must be at least 10 characters long")
        return value



# ==================================== notice serializer ========================

class NoticeSerializer(serializers.ModelSerializer):
    hostel=serializers.SlugRelatedField(slug_field='name',read_only=True)
    class Meta:
        model = Notice
        fields = ["id","hostel","title","content","is_global","created_at"]
    def validate_title(self,value):
        if len(value) < 10:
            raise serializers.ValidationError("Title must be at least 10 characters long")
        return value
    def validate_content(self,value):
        if len(value) < 20:
            raise serializers.ValidationError("Content must be at least 20 characters long")
        return value



# ============================= Hostel address serializers ===================


class HostelAddressSerializer(serializers.ModelSerializer):
    hostel=serializers.SlugRelatedField(slug_field='name',read_only=True)
    class Meta:
        model = Hostel_address 
        fields = ["id","hostel","division","district","thana","created_at"]
        read_only_fields = ["created_at"] 



# ============================= Hostel coordinate serializers ===================
 

class HostelCoordinateSerializer(serializers.ModelSerializer):
    hostel=serializers.SlugRelatedField(slug_field='name',read_only=True) 
    class Meta:
        model = Hostel_coordinate
        fields = ["id","hostel","lat","lng","created_at"]
        read_only_fields = ["created_at"]