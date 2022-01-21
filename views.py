from rest_framework.generics import (ListCreateAPIView,RetrieveUpdateDestroyAPIView,)
from rest_framework.permissions import IsAuthenticated
from .models import userProfile
from .permissions import IsOwnerProfileOrReadOnly
from .serializers import userProfileSerializer

# Create your views here.

class UserProfileListCreateView(ListCreateAPIView):
    permission_classes = (isAuthenticated,)
    queryset=userProfile.objects.all()
    serializer_class=userProfileSerializer
    #permission_classes=[IsAuthenticated]

    def perform_create(self, serializer):
        user=self.request.user
        serializer.save(user=user)


class userProfileDetailView(RetrieveUpdateDestroyAPIView):
    permission_classes = (isAuthenticated,)
    queryset=userProfile.objects.all()
    serializer_class=userProfileSerializer
    #permission_classes=[IsOwnerProfileOrReadOnly,IsAuthenticated]
