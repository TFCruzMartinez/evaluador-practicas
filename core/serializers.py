
from rest_framework import serializers
from .models import Registro
from .services import evaluar_postulacion


class RegistroSerializer(serializers.ModelSerializer):
    class Meta:
        model = Registro
        fields = [
            "id",
            "semestre",
            "horas_disponibles",
            "resultado",
            "fecha",
            "eliminado",
            "fecha_eliminacion",
        ]
        read_only_fields = [
            "id",
            "resultado",
            "fecha",
            "eliminado",
            "fecha_eliminacion",
        ]

    def validate_semestre(self, value):
        if value <= 0:
            raise serializers.ValidationError(
                "El semestre debe ser mayor que cero."
            )
        return value

    def validate_horas_disponibles(self, value):
        if value < 0:
            raise serializers.ValidationError(
                "Las horas disponibles no pueden ser negativas."
            )
        return value

    def create(self, validated_data):
        validated_data["resultado"] = evaluar_postulacion(
            validated_data["semestre"],
            validated_data["horas_disponibles"],
        )
        return super().create(validated_data)

    def update(self, instance, validated_data):
        semestre = validated_data.get(
            "semestre", instance.semestre
        )
        horas = validated_data.get(
            "horas_disponibles", instance.horas_disponibles
        )
        validated_data["resultado"] = evaluar_postulacion(
            semestre, horas
        )
        return super().update(instance, validated_data)
