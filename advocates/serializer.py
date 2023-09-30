from rest_framework import serializers
from userapp.models import UserData, Advocate
from userapp.serializers import UserSerializer
from django.templatetags.static import static


class NormalAdvocateSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    user_id = serializers.PrimaryKeyRelatedField(write_only=True, queryset=UserData.objects.all(), source='user')
    profile_image_url = serializers.SerializerMethodField()
    document_image_url = serializers.SerializerMethodField()
    class Meta:
        model = Advocate
        fields = "__all__"
    def to_representation(self, instance):
        data = super().to_representation(instance)
        if data.get('type_of_user') == 'normal_advocate':
            return data
        return None
    def get_profile_image_url(self, obj):
        request = self.context.get('request')

        if not request:
            return static('main_pro_changing/adh.jpg') 
        
        if obj.profile_image and hasattr(obj.profile_image, 'url'):
            # request = self.context.get('request')
            return request.build_absolute_uri(obj.profile_image.url)
        else:
            default_img_url = static('main_pro_changing/adh.jpg')
            return request.build_absolute_uri(default_img_url)
        
    def get_document_image_url(self, obj):
        request = self.context.get('request')
        if not request:
            return static('main_pro_changing/adh.jpg')
        if obj.document_image and hasattr(obj.document_image, 'url'):
            # request = self.context.get('request')
            return request.build_absolute_uri(obj.document_image.url)
        else:
            default_img_url = static('main_pro_changing/adh.jpg')
            return request.build_absolute_uri(default_img_url)



