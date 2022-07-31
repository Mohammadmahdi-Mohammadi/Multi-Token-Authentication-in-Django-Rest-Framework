from django.core.exceptions import BadRequest
from rest_framework import serializers
from rest_framework.exceptions import NotFound

from .models import Product, Comment


class ProductListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'

class AddRateSerializer(serializers.ModelSerializer):
    rate = serializers.IntegerField(required=True)
    # url = request.build_absolute_uri()
    # index_item = url.split('/')[-2]

    class Meta:
        model = Product
        fields = ['rate','id' ]

    def get_alternate_data(self,):
        rate = self.context["rate"]
        product_id = self.context["product_id"]
        username = self.context["username"]
        print(rate)
        print(product_id)
        print(username)
        product = Product.objects.filter(id=product_id)
        old_rate = product.first().rate
        old_users = product.first().user
        old_users_number = product.first().number_of_voters
        new_user = old_users + '#]/!.!/[#' + username
        new_rate = int(old_rate) + int(rate)
        if username in old_users:
            raise serializers.ValidationError("You have already voted for this product!")
        product = Product.objects.filter(id=product_id).update(rate=new_rate,user=new_user,number_of_voters=old_users_number+1)



    def validate(self,data):
        self.get_alternate_data()
        var = data['rate']
        if var > 5 or var <0 :
            raise serializers.ValidationError("enter validate rate 0 to 5")
        return data

#
class AllCommentsserilizer(serializers.ModelSerializer):
    # rate = serializers.IntegerField(required=True)
    # print("FFFFFFFFFFFFFFF")

    class Meta:
        model = Comment
        fields = ['body', 'product', 'id', 'date_add' ]



class CheckCommentSerializer(serializers.Serializer):
    ids = serializers.ListField(child=serializers.IntegerField(), required=True, allow_null=False, min_length=1)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._comments = None

    def validate_ids(self, value):
        comments = Comment.objects.filter(id__in=value)
        if len(comments) != len(value):
            raise NotFound()
        self._comments = comments
        return value

    @property
    def validated_data(self):
        _validated_data = super().validated_data
        _validated_data['comments'] = self._comments
        return _validated_data

class AddToCartSerializer(serializers.Serializer):
    ids = serializers.ListField(child=serializers.IntegerField(), required=True, allow_null=False, min_length=1)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._tokens = None

    def validate_ids(self, value):
        products = Product.objects.filter(id__in=value)
        if len(products) != len(value):
            raise BadRequest("wrong ids")
        self._products = products
        return value

    @property
    def validated_data(self):
        _validated_data = super().validated_data
        _validated_data['products'] = self._products
        return _validated_data