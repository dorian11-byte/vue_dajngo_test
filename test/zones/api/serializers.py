from rest_framework import serializers

from zones.models import Zone, Distribution


class DistributionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Distribution
        fields = ['id', 'percentage']


class ZoneSerializer(serializers.ModelSerializer):
    distributions = DistributionSerializer(many=True)
    updated_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S")  # Agregamos el campo aquí
    distributions_count = serializers.SerializerMethodField()  # Agregamos el campo aquí

    class Meta:
        model = Zone
        fields = ['id', 'name', 'distributions', 'updated_at', 'distributions_count']  # Incluimos 'distributions_count' aquí

    def get_distributions_count(self, zone):
        return Distribution.objects.filter(zone=zone).count()  # Cambiamos 'obj' por 'zone' aquí
