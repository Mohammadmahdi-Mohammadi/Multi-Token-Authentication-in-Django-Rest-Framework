from account.models import User
from .models import Cart,Shopping
from   product.models import Product
from rest_framework import serializers,exceptions
from rest_framework.exceptions import NotFound
from .models import CartItem


class add_product_serilizer(serializers.Serializer):
    response_array = [["Product_ID", "operation_status", "massage"]]
    binary_saver = serializers.ListField(child=serializers.ListField(child=serializers.IntegerField(), required=True,allow_null=False,min_length=1,max_length=2),required=True, allow_null=False,min_length=1)

    def array_cleaner(self):
        self.response_array = [["Product_ID","operation_status","massage"]]

    def validate(self, data):
        for i in range(len(data['binary_saver'])):
            # self.response_array = [["Product_ID","operation_status","massage"]]
            product = data['binary_saver'][i][0]
            count = data['binary_saver'][i][1]
            check_product = Product.objects.filter(id=product).first()
            if not check_product:
                raise serializers.ValidationError("this product dosnt exist!: ",product)
            if check_product.count < count:
                self.response_array.append([product,"unsuccessful","there is no enough product for yor request"])
            else:
                self.response_array.append([product,"successful","your request successfully completed"])
        # ____________________________________________________________________________________________________
        user = self.context["user_request"]
        user_main = User.objects.get(id=user)
        Cart.objects.get_or_create(user=user_main)
        for i in range(len(data['binary_saver'])):
            product = data['binary_saver'][i][0]
            count = data['binary_saver'][i][1]
            cart = Cart.objects.get(user=user_main.id, ordered=False)
            current_product = Product.objects.get(id=product)
            last_count_obj = CartItem.objects.filter(cart=cart, product=current_product).first()
            if last_count_obj:
                last_count = last_count_obj.count
            else:
                last_count = 0
            current_count = last_count + count
            remain_count = current_product.count
            if last_count_obj and remain_count >= current_count:
                Product.objects.filter(id=product).update(count=(remain_count - current_count))
            elif not (last_count_obj) and remain_count >= current_count:
                new_item = CartItem.objects.create(cart=cart, product=current_product,
                                                   count=(remain_count - current_count))
                new_item.save()
            else:
                # print("there isn't enough product and nothing dosnt apply to database")
                pass

        # self.response_array = [["Product_ID","operation_status","massage"]]
        return data


class CartDetailllllViewSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = '__all__'


class CartViewSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = ['id', 'product', 'count']


class RemoveFromCartSerializer(serializers.Serializer):
    ids = serializers.ListField(child=serializers.CharField(), required=True, allow_null=False, min_length=1)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._remove_list = None

    def validate_ids(self, value):
        if len(value) == 1 and value[0] == 'all':
            user = self.context["user_request"]
            objects = Cart.objects.filter(user=user)
            remove_list = CartItem.objects.filter(cart__in=objects)
        else:
            remove_list = CartItem.objects.filter(id__in=value)
            if len(remove_list) != len(value):
                raise NotFound()
        self._remove_list = remove_list
        return value

    @property
    def validated_data(self):
        _validated_data = super().validated_data
        _validated_data['ramove_list'] = self._remove_list
        return _validated_data


class TrackListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Shopping
        fields = ['tracking_id', ]


class CartDetailViewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields = '__all__'


class TrackDetailSerializer(serializers.ModelSerializer):
    cart = serializers.HyperlinkedIdentityField(view_name='cartdetail')

    class Meta:
        model = Shopping
        fields = '__all__'











