from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.generics import ListAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status

from django.contrib.auth.models import User
from coins.serializer import ProfileSerializer, WatchListSerializer

from coins.models import ProfileModel, WatchListModel

import requests

class Register(APIView):
    

    def post(self, request, *args, **kwargs):

        username = request.data.get("username")
        password = request.data.get("password")
        email = request.data.get("email")
        
        user = User(username = username,email = email)
        user.set_password(password)

        try:
            user.save()
            token, created = Token.objects.get_or_create(user=user)
            profile = ProfileModel(user=user,cash_in_hand = 100)
            profile.save()

            return Response({
                "status":True,
                'token': token.key,
                'user_id': user.pk,
            })
        
        except:
            return Response({"status":False,"details":"User already exists"},status=status.HTTP_406_NOT_ACCEPTABLE)


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


class ProfileView(ListAPIView):
    permission_classes = [IsAuthenticated,]
    def get(self, request, *args, **kwargs):
        user = Token.objects.get(key=request.auth.key).user
        profile = ProfileModel.objects.filter(user=user).first()
        profile_serial = ProfileSerializer(profile)
        return Response(profile_serial.data)


class MarketLiveView(ListAPIView):
    permission_classes = [IsAuthenticated,]

    def get(self, request, id = None, *args, **kwargs):
        key = "https://api.binance.com/api/v3/ticker/price?symbol="
        if id:
            res = requests.get(key+id)
            data = res.json()
            print(data)
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



class WatchList(ListAPIView):
    permission_classes = [IsAuthenticated,]

    def get(self, request, *args, **kwargs):
        user = Token.objects.get(key=request.auth.key).user
        watchlist = WatchListModel.objects.filter(user=user)
        watchlist_serial = WatchListSerializer(watchlist, many=True)
        return Response(watchlist_serial.data)