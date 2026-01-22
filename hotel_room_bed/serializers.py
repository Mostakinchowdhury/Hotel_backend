from rest_framework import serializers
from .models import *


# =================== hostel bed serializer  ==============


class HostelBedSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hostel_bed
        fields = '__all__'

# =================== hostel images serializer  ==============


class HostelImagesSerializer(serializers.ModelSerializer):
    file_url = serializers.SerializerMethodField()
    class Meta:
        model = Hostel_images
        fields = ['id','file','hostel','created_at','is_image','is_video',"file_url"]
        read_only_fields = ['is_image','is_video',"file_url"] 

    def validate_file(self, file):
        # 200MB limit
        max_size = 200 * 1024 * 1024  

        if file.size > max_size:
            raise serializers.ValidationError(
                "File size must be less than or equal to 200MB."
            )

        return file

    def get_file_url(self,obj):
        rq=self.context.get("request")
        return rq.build_absolute_uri(obj.file.url) if obj.file else None




# =================== hostel room serializer  ==============


class HostelRoomSerializer(serializers.ModelSerializer):
    beds=HostelBedSerializer(many=True,read_only=True)
    class Meta:
        model = HostelRoom
        fields = [
          "id","hostel","room_no","created_at","bed_capacity","beds"
        ]
        read_only_fields=["beds"]



# =================== hostel serializer  ==============


class HostelSerializer(serializers.ModelSerializer):
    rooms=HostelRoomSerializer(many=True,read_only=True)
    files=HostelImagesSerializer(many=True,read_only=True)
    monitor = serializers.SlugRelatedField(
    slug_field="username",
    read_only=True)
    class Meta:
        model = Hostel
        fields = [
          "id","monitor","created_at","updated_at","rooms","name","description","benefits","is_verified","files","hostel_type"
        ]
        read_only_fields = ['monitor',"created_at","updated_at","rooms","files"]

