import logging
from homeassistant.core import HomeAssistant
from homeassistant.config_entries import ConfigEntry
from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)

# List the platforms your integration supports (just vacuum for now)
PLATFORMS = ["vacuum"]

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up Universal Vacuums from a config entry."""
    hass.data.setdefault(DOMAIN, {})
    
    # This line tells HA to go look at your vacuum.py file
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    
    return True

async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    unload_ok = await hass.config_entries.async_forward_entry_unload(entry, "vacuum")
    if unload_ok:
        hass.data[DOMAIN].pop(entry.entry_id, None)

    return unload_ok
