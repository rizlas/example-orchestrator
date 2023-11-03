import structlog

from services import netbox
from services.netbox import IPv4_LOOPBACK_PREFIX, IPv6_LOOPBACK_PREFIX

logger = structlog.get_logger(__name__)

initial_objects = [
    netbox.SitePayload(name="Amsterdam", slug="amsterdam", status="active"),
    netbox.SitePayload(name="Paris", slug="paris", status="active"),
    netbox.SitePayload(name="London", slug="london", status="active"),
    netbox.DeviceRolePayload(name="Provider", slug="provider", color="9e9e9e"),
    netbox.DeviceRolePayload(name="Provider Edge", slug="provider-edge", color="ff9800"),
    cisco := netbox.ManufacturerPayload(name="Cisco", slug="cisco"),
    nokia := netbox.ManufacturerPayload(name="Nokia", slug="nokia"),
    netbox.DeviceTypePayload(manufacturer=cisco, model="8812", slug="8812", u_height=21.0),
    netbox.DeviceTypePayload(manufacturer=cisco, model="ASR 903", slug="asr-903", u_height=3.0),
    netbox.DeviceTypePayload(manufacturer=nokia, model="7950 XRS-20", slug="7950-xrs-20", u_height=44.0),
    netbox.DeviceTypePayload(manufacturer=nokia, model="7210 SAS-R6", slug="7210-sas-r6", u_height=3.0),
]


if __name__ == "__main__":
    for initial_object in initial_objects:
        logger.info("add object to Netbox", object=initial_object)
        try:
            netbox.create(initial_object)
        except ValueError:
            # pynetbox already emits a log message
            pass

    for prefix in (IPv4_LOOPBACK_PREFIX, IPv6_LOOPBACK_PREFIX):
        if netbox.netbox.ipam.prefixes.get(prefix=prefix):
            logger.warning("prefix already exists", prefix=prefix)
        else:
            logger.info("add prefix to netbox", prefix=prefix)
            netbox.netbox.ipam.prefixes.create({"prefix": prefix, "description": "loopback addresses"})