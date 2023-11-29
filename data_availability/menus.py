from .models import Config

# pylint: disable=W0511
# TODO: Fix config filtering
confs = Config.objects.all()
# if conf:
#     DASHBOARD_VIEW = conf.dashboard_title
# else:
#     DASHBOARD_VIEW = "Dashboard"

MENUS = {
    "NAV_MENU_TOP": [
        {
            "name": "Dashboards",
            "url": "#",
            "submenu": [
                {"name": config.dashboard_title, "url": "lung:dashboard"} for config in confs
            ],
        }
    ]
}
