import jwt
from django.http import JsonResponse
from django.contrib.auth import authenticate
from django.shortcuts import render, get_object_or_404

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer, TokenRefreshSerializer
from decouple import config

from .serializers import *



class JWTSignupView(APIView):
    serializer_class = UserJWTSignupSerializer

    def post(self, request):
        data = request.data.copy()
        data.pop('password2', None)
        
        serializer = UserJWTSignupSerializer(data=data)
        if serializer.is_valid(raise_exception=False):
            user = serializer.save()
            # jwt 토큰 접근
            token = TokenObtainPairSerializer.get_token(user)
            refresh_token = str(token)
            access_token = str(token.access_token)
            res = Response(
                {
                    "user": serializer.data,
                    "message": "register successs"
                },
                status=status.HTTP_200_OK,
            )        

            # jwt 토큰 => 쿠키에 저장
            res.set_cookie("access", access_token)
            res.set_cookie("refresh", refresh_token, httponly=True)
            return res
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class JWTLoginView(APIView):
    # 유저 정보 확인
    def get(self, request):
        try:
            # access token을 decode 해서 유저 id 추출 => 유저 식별
            access = request.COOKIES['access']
            SECRET_KEY = config('SECRET_KEY')
            payload = jwt.decode(access, SECRET_KEY, algorithms=['HS256'])
            id = payload.get('user_id')
            user = get_object_or_404(User, id=id)
            serializer = UserJWTLoginSerializer(instance=user)
            return Response(serializer.data, status=status.HTTP_200_OK)

        except(jwt.exceptions.ExpiredSignatureError):
            # 토큰 만료 시 토큰 갱신
            data = {'refresh': request.COOKIES.get('refresh', None)}
            serializer = TokenRefreshSerializer(data=data)
            if serializer.is_valid(raise_exception=True):
                access = serializer.data.get('access', None)
                refresh = serializer.data.get('refresh', None)
                payload = jwt.decode(access, SECRET_KEY, algorithms=['HS256'])
                id = payload.get('user_id')
                user = get_object_or_404(User, id=id)
                serializer = UserJWTLoginSerializer(instance=user)
                res = Response(serializer.data, status=status.HTTP_200_OK)
                res.set_cookie('access', access)
                res.set_cookie('refresh', refresh, httponly=True)
                return res
            raise jwt.exceptions.InvalidTokenError

        except(jwt.exceptions.InvalidTokenError):
            # 사용 불가능한 토큰일 때
            return Response(status=status.HTTP_400_BAD_REQUEST)

    # 로그인
    def post(self, request):
    # 유저 인증
        user = authenticate(
            email=request.data.get("email"), password=request.data.get("password")
        )
        # 이미 회원가입 된 유저일 때
        if user is not None:
            serializer = UserJWTLoginSerializer(user)
            # jwt 토큰 접근
            token = TokenObtainPairSerializer.get_token(user)
            refresh_token = str(token)
            access_token = str(token.access_token)
            res = Response(
                {
                    "user": serializer.data,
                    "message": "login success"
                },
                status=status.HTTP_200_OK,
            )
            # jwt 토큰 => 쿠키에 저장
            res.set_cookie("access", access_token)
            res.set_cookie("refresh", refresh_token, httponly=True)
            return res
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)

    # 로그아웃
    def delete(self, request):
        # 쿠키에 저장된 토큰 삭제 => 로그아웃 처리
        response = Response({
            "message": "Logout success"
            }, status=status.HTTP_202_ACCEPTED)
        response.delete_cookie("access")
        response.delete_cookie("refresh")
        return response

class JWTRefreshView(APIView):
    def get(self, request):
        refresh_token = request.COOKIES.get('refresh')
        
        if refresh_token is None:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        
        try:
            # refresh 토큰을 사용하여 새로운 access 토큰 생성
            serializer = TokenRefreshSerializer(data={'refresh': refresh_token})
            
            if serializer.is_valid(raise_exception=True):
                access_token = serializer.validated_data['access']
                res = Response({
                    'access': access_token
                })
                res.set_cookie('access', access_token)
                return res
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)

#=========================================================

from rest_framework import viewsets, mixins
from datetime import datetime, timedelta

class UserNameViewSet(viewsets.GenericViewSet, mixins.RetrieveModelMixin):
    queryset = User.objects.all()
    serializer_class = UserNameSerializer

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        user_id = print(kwargs['pk'])
        target_user_log_ = request.COOKIES.get('target_user_log_')
        res = Response()

        if target_user_log_ is None:
            now = datetime.now()
            
            # 3시간 후의 시간
            expires = now + timedelta(hours=3)

            res.set_cookie("target_user_log_", user_id, expires=expires)
            instance.view_cnt += 1

        else:
            if user_id == target_user_log_:
                pass
            else:
                now = datetime.now()
            
                # 3시간 후의 시간
                expires = now + timedelta(hours=3)
                res.set_cookie("target_user_log_", user_id, expires=expires)

        instance.save()
        serializer = self.serializer_class(instance)
        res.data = serializer.data
        return res