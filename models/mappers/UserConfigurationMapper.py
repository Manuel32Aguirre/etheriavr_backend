from models.dto.request.UserConfigurationRequest import UserConfigurationRequest
from models.dto.request.UserCreateRequest import UserCreateRequest
from models.dto.response.UserConfigurationResponse import UserConfigurationResponse
from models.entities.UserConfiguration import UserConfiguration
from models.enums.AudienceIntensity import AudienceIntensity


class UserConfigurationMapper:
    @staticmethod
    def toEntity(request: UserCreateRequest) -> UserConfiguration:
        return UserConfiguration(
            midi_device_name=request.midi_device_name,
            audience_intensity=request.audience_intensity or AudienceIntensity.MEDIO
        )

    @staticmethod
    def toEntityFromRequest(user_id: int, request: UserConfigurationRequest) -> UserConfiguration:
        return UserConfiguration(
            user_id=user_id,
            midi_device_name=request.midi_device_name,
            audience_intensity=request.audience_intensity or AudienceIntensity.MEDIO
        )

    @staticmethod
    def toDto(entity: UserConfiguration) -> UserConfigurationResponse:
        if not entity:
            return None

        return UserConfigurationResponse(
            user_id=entity.user_id,
            midi_device_name=entity.midi_device_name,
            audience_intensity=entity.audience_intensity.value
        )