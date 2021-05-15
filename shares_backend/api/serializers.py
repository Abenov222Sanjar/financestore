from rest_framework import serializers
from api import models

import logging
logger = logging.getLogger(__name__)

class BaseSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField()

    def validate(self, data):
        if data['id'] < 0:
            logger.error('Error at id validation')
            raise serializers.ValidationError({ "error": "Id should be a positive number" })
        return data


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Category
        fields = 'id', 'name'
    def validate(self, data):
        if data['id'] < 0:
            logger.error('Error at id validation')
            raise serializers.ValidationError({ "error": "Id should be a positive number" })
        return data

class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Company
        fields = 'id', 'name'
    def validate(self, data):
        if data['id'] < 0:
            logger.error('Error at id validation')
            raise serializers.ValidationError({ "error": "Id should be a positive number" })
        return data

class SubCategorySerializer(BaseSerializer):
    category = CategorySerializer()

class BrokerSerializer(BaseSerializer):
    phone = serializers.CharField()
    amount_of_trades = serializers.IntegerField()

    def validate(self, data):
        if data['amount_of_trades'] < 0:
            logger.error('Error at amount of trades validation')
            raise serializers.ValidationError({ "error": "Amount_of_trades may not be negative" })
        return data

class ShareSerializer(BaseSerializer):
    category = CategorySerializer()
    subcategory = SubCategorySerializer()
    company = CompanySerializer()
    description = serializers.CharField()
    image = serializers.CharField()
    price = serializers.FloatField()

    def validate(self, data):
        if data['price'] < 500:
            raise serializers.ValidationError({ "error": "Price should be higher than 500" })
        return data


class OrderSerializer(BaseSerializer):
    phone = serializers.CharField()
    status = serializers.CharField()
    share = ShareSerializer()
    attached_broker = BrokerSerializer()

    def validate(self, data):
        if data['status'] not in ['completed', 'declined', 'in_progress']:
            raise serializers.ValidationError({ "error": "Status is unacceptable" })
        return data
    