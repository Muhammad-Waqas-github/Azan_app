from datetime import date
from adhan import adhan
from adhan.methods import KARACHI, ASR_HANAFI

params = {}
params.update(KARACHI)
params.update(ASR_HANAFI)

longitude = -0.119114
latitude = 51.512973

adhan_times = adhan(
    day=date.today(),
    location=(latitude, longitude),
    parameters=params,
    timezone_offset=-4,
)

prayers = {
    "dhuhr": "",
    "asr": "",
    "maghrib": "",
    "isha": "",
    "fajr": "",
}

adhan_times["dhuhr"] = adhan_times["zuhr"]


def find_adhan_times_manually():
    for key in prayers.keys():
        prayers[key] = adhan_times[key].strftime("%I:%M %p")
    return prayers
