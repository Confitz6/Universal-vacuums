import logging
from homeassistant.core import HomeAssistant
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import Platform
from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)

# Explicitly defining the platform as a list of Platform objects
PLATFORMS: list[Platform] = [Platform.VACUUM]

async def async_setup(hass: HomeAssistant, config: dict) -> bool:
    """Set up the Universal Vacuums component (Legacy/Global Setup)."""
    # This must return True for the Config Flow to even start
    return True

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up Universal Vacuums from a config entry."""
    hass.data.setdefault(DOMAIN, {})
    
    # New 2026.3 requirement: forward setups and await them
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    
    return True

async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    # Updated to use the plural 'platforms' helper for 2026 stability
    unload_ok = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
    
    if unload_ok:
        hass.data[DOMAIN].pop(entry.entry_id, None)

    return unload_ok
