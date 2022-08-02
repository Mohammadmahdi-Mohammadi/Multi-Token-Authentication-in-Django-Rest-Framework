from account.models import User
from product.models import Product
from rest_framework import serializers
from product.models import Comment
from rest_framework.exceptions import NotFound

class AddCommentSerializer(serializers.Serializer):
    comment = serializers.CharField(max_length=5000, required=True,allow_blank=False)


    def validate(self, data):
        if data['comment']:
            product = self.context['PID']
            print("PPPP",product)
            product_obj = Product.objects.get(id=product)
            if product:
                Comment.objects.create(product=product_obj,body=data['comment'])
            else:
                raise serializers.ValidationError("product not found!")
        return data


class ListCommentSerializer(serializers.Serializer):
    result=["Comment#"]

    def array_cleaner(self):
        self.result= ["Comment content"]

    def validate(self, data):
        product = self.context['PID']
        product_obj = Product.objects.get(id=product)
        if product:
            comments = Comment.objects.filter(product=product_obj,chech_admin=True)
            for i in range(len(comments)):
                self.result.append(comments[i].body)
        else:
            raise serializers.ValidationError("product not found!")
        return data

class ProductscoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['number_of_voters','rate']