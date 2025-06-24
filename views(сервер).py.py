from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.views.decorators.csrf import csrf_exempt
from .models import Device, DeviceState
from .serializers import DeviceSerializer, DeviceStateSerializer

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_devices(request):
    devices = Device.objects.filter(owner=request.user)
    serializer = DeviceSerializer(devices, many=True)
    return Response(serializers.data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_device_state(request, device_id):
    try:
        device = Device.objects.get(id=device_id, owner=request.user)
        state = device.current_state
        serializer = DeviceStateSerializer(state)
        return Response(serializer.data)
    except Device.DoesNotExist:
        return Response({'error': 'Device not found'}, status=404)

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_device_state(request, device_id):
    try:
        device = Device.objects.get(id=device_id, owner=request.user)
        serializer = DeviceStateSerializer(data=request.data)
        if serializer.is_valid():
            # Save new state
            new_state = serializer.save()
            device.current_state = new_state
            device.save()
            
            # Broadcast update to WebSocket clients
            broadcast_state_update(device_id, new_state)
            
            return Response(serializer.data)
        return Response(serializer.errors, status=400)
    except Device.DoesNotExist:
        return Response({'error': 'Device not found'}, status=404)