from account.models import User
from .models import Cart
from   product.models import Product
from rest_framework import serializers,exceptions
from rest_framework.exceptions import NotFound
from .models import CartItem

class add_product_serilizer(serializers.Serializer):
    # print("##########################################")
    response_array = [["None","None","No massage"]]
    binary_saver = serializers.ListField(child=serializers.ListField(child=serializers.IntegerField(), required=True,allow_null=False,min_length=1,max_length=2),required=True, allow_null=False,min_length=1)
    # print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")


    def validate(self, data):
        print("222222222222222222222222222222222222222222")
        # user = self.context['request'].user
        user = self.context["user_request"]
        print("user::::::::::::::", user)
        print("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$")

        user_main = User.objects.get(id=user)
        print(user_main)
        # user_main = User.objects.filter(id=user).first()
        user_cart = Cart.objects.get_or_create(user=user_main.id)
        print(data['binary_saver'])
        for i in range(len(data['binary_saver'])):
            print("iteration number: ", i)
            print("iteration numbers: ", len(data['binary_saver'] ))
            product = data['binary_saver'][i][0]
            count = data['binary_saver'][i][1]
            last_count_obj = CartItem.objects.filter(product=product)
            if last_count_obj:
                last_count = last_count_obj.first().count
            else:
                last_count = 0
            # if (count > last_count):
            current_count = last_count + count
            # this_item = CartItem.objects.filter(cart=user_cart)
            if last_count_obj:
                CartItem.objects.filter(product=product).update(count=current_count)
            else:
                new_item = CartItem.objects.create(cart=user_cart, product=product,
                                                   count=current_count)
                new_item.save()
        return data



    def validate(self, data):
        for i in range(len(data['binary_saver'])):
            # print("iteration number: ", i)
            # print("iteration numbers: ", len(data['binary_saver']))
            product = data['binary_saver'][i][0]
            count = data['binary_saver'][i][1]
            # print("p&d is: ", product , " - ", count)
            check_product = Product.objects.filter(id=product).first()
            if not check_product:
                raise serializers.ValidationError("this product dosnt exist!: ",product)

            if check_product.count < count:
                self.response_array.append([product,"unsuccessful","there is no enough product for yor request"])
            else:
                self.response_array.append([product,"successful","your request successfully completed"])

        # ____________________________________________________________________________________________________


        # user = self.context['request'].user
        user = self.context["user_request"]
        user_main = User.objects.get(id=user)
        # print(user_main)
        # user_main = User.objects.filter(id=user).first()
        Cart.objects.get_or_create(user=user_main)

        for i in range(len(data['binary_saver'])):
            # print("iteration number: ", i)
            # print("iteration numbers: ", len(data['binary_saver'] ))
            product = data['binary_saver'][i][0]
            count = data['binary_saver'][i][1]
            # print("********************************************************")
            print(user_main)
            print(user_main.id)
            cart = Cart.objects.get(user=user_main.id)
            print("********************************************************")

            current_product = Product.objects.get(id=product)
            last_count_obj = CartItem.objects.filter(cart=cart, product=current_product).first()
            print("last count obj: ", last_count_obj)
            if last_count_obj:
                last_count = last_count_obj.count
            else:
                last_count = 0

            current_count = last_count + count
            print("summary: ", current_count,count,last_count)
            print(product)
            print("********************************************************")


            remain_count = current_product.count

            if last_count_obj:
                print("Current count 1: ", current_count)
                print("remain_count: ",remain_count)
                Product.objects.filter(id=product).update(count=(remain_count - current_count))
            else:
                print("$$$$$$$")
                print("Current count 2: ", current_count)
                print("remain_count: ",remain_count)
                new_item = CartItem.objects.create(cart=cart, product=current_product,
                                                   count=current_count)

                new_item.save()
        return data












