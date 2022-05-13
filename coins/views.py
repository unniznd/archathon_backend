from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status

from django.contrib.auth.models import User

import json
import requests


class MarketLiveView(ListAPIView):
    permission_classes = [IsAuthenticated,]

    def get(self, request, id = None, *args, **kwargs):
        key = "https://api.binance.com/api/v3/ticker/price?symbol="
        if id:
            res = requests.get(key+id)
            data = res.json()
            return Response({"price":round(float(data['price']),3)})

        symbols  = {"BitCoin":"BTCUSDT","Etherium":"ETHUSDT","Polkadot":"DOTUSDT","Dogecoin":"DOGEUSDT"}
        result = []
        for sym in symbols.keys():
            res = requests.get(key+symbols[sym])
            data = res.json()
            result.append({
                "name":sym,
                "short":symbols[sym].replace('USDT',''),
                "price":round(float(data['price']),3),
                "logo":"/media/"+symbols[sym].replace('USDT','')+".png"
            })
        

        return Response({"data":result})


class Login(ObtainAuthToken):

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user_id': user.pk,
        })

class Register(ListAPIView):
    def post(self, request, *args, **kwargs):

        username = request.data.get("username")
        password = request.data.get("password")
        email = request.data.get("email")
        
        user = User(username = username,email = email)
        user.set_password(password)

        try:
            user.save()
            token, created = Token.objects.get_or_create(user=user)
            return Response({
                "status":True,
                'token': token.key,
                'user_id': user.pk,
            })
        
        except:
            return Response({"status":False,"details":"User already exists"},status=status.HTTP_406_NOT_ACCEPTABLE)

