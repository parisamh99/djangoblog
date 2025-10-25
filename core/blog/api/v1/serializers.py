from rest_framework import serializers
from blog.models import Post, Category
from accounts.models import Profile

# class PostSerializer(serializers.Serializer):
#     title = serializers.CharField(max_length=250)


class PostSerializer(serializers.ModelSerializer):
    snippet = serializers.ReadOnlyField(source="get_snippet")
    relative_url = serializers.URLField(source="get_absolute_api_url", read_only=True)
    # absolute_url = serializers.SerializerMethodField(source = 'get_absolute_url')
    # category = serializers.SlugRelatedField(many=False,slug_field='name',queryset=Category.objects.all())

    class Meta:
        model = Post
        fields = [
            "id",
            "title",
            "author",
            "content",
            "snippet",
            "status",
            "category",
            "created_date",
            "published_date",
            "relative_url",
        ]  #'absolute_url',]
        read_only_fields = ["author"]

    # def get_absolute_url(self,obj):
    #         request = self.context.get('request')
    #         return request.build_absolute_url(obj)

    def to_representation(self, instance):
        request = self.context.get("request")
        # print(request.__dict__)
        rep = super().to_representation(instance)

        if request.parser_context.get("kwargs").get("pk"):
            rep.pop("snippet", None)
            rep.pop("relative_url", None)
        else:
            rep.pop("content", None)
        rep["category"] = CategorySerializer(
            instance.category, context={"request": request}
        ).data
        return rep

    def create(self, validated_date):
        validated_date["author"] = Profile.objects.get(
            user__id=self.context.get("request").user.id
        )
        return super().create(validated_date)


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["name", "id"]
