from homeassistant.components.vacuum import StateVacuumEntity, VacuumEntityFeature, Segment
from typing import Any

class UniversalVacuums(StateVacuumEntity):
    def __init__(self):
        self._attr_name = "Universal Vacuums"
        self._attr_unique_id = "univ_vac_2026_pro"
        self._attr_supported_features = (
            VacuumEntityFeature.CLEAN_AREA | 
            VacuumEntityFeature.START | 
            VacuumEntityFeature.STOP |
            VacuumEntityFeature.RETURN_HOME |
            VacuumEntityFeature.REMOTE_POSITION |
            VacuumEntityFeature.STATE
        )

    async def async_get_segments(self) -> list[Segment]:
        """Exposes your rooms to the Home Assistant UI for mapping"""
        return [
            Segment(id="1", name="Kitchen (Tapo)"),
            Segment(id="16", name="Living Room (Tikom)"),
            Segment(id="Bedroom", name="Bedroom (Wyze)")
        ]

    async def async_clean_segments(self, segment_ids: list[str], **kwargs: Any) -> None:
        """The core translation engine for the 2026.3 Area Clean service"""
        for segment in segment_ids:
            if segment == "1":
                await self.hass.services.async_call("tapo", "vacuum_clean_room", {"entity_id": "vacuum.tapo_rv20_max_plus", "room_id": 1})
            elif segment == "16":
                await self.hass.services.async_call("vacuum", "send_command", {"entity_id": "vacuum.tikom_6000pa", "command": "app_segment_clean", "params": [16]})
            elif segment == "Bedroom":
                await self.hass.services.async_call("vacuum", "send_command", {"entity_id": "vacuum.wyze_200s", "command": "sweep_rooms", "params": {"rooms": ["Bedroom"]}})

    async def async_send_command(self, command: str, params: dict[str, Any] | None = None, **kwargs: Any) -> None:
        """Manual Remote Control Forward/Left/Right for your robots"""
        for entity in ["vacuum.tapo_rv20_max_plus", "vacuum.tikom_6000pa"]:
            await self.hass.services.async_call("vacuum", "send_command", {"entity_id": entity, "command": command})