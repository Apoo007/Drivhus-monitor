# Handles threshold logic and email notifications.
import yagmail
from datetime import datetime
from config import THRESHOLDS, EMAIL

sent_warnings = set()

def is_daytime():
    now = datetime.now().time()
    return datetime.strptime("05:00", "%H:%M").time() <= now <= datetime.strptime("22:00", "%H:%M").time()

def get_temp_thresholds():
    if is_daytime():
        return THRESHOLDS["TEMP_DAY_MIN"], THRESHOLDS["TEMP_DAY_MAX"]
    else:
        return THRESHOLDS["TEMP_NIGHT_MIN"], THRESHOLDS["TEMP_NIGHT_MAX"]

def analog_to_vwc(raw):
    # Convert raw analog value (0–1023) to approximate VWC %
    vwc = 100 * (1023 - raw) / (1023 - 300)
    return max(0, min(vwc, 100))

def send_email(subject, value):
    yag = yagmail.SMTP(user=EMAIL["sender"], password=EMAIL["password"])
    body = f"{subject}. Målt værdi: {value}"
    yag.send(to=EMAIL["receiver"], subject=subject, contents=body)

def check_and_notify(data):
    alerts = []
    soil_raw = int(data['soil'])
    vwc = analog_to_vwc(soil_raw)
    if vwc < THRESHOLDS["SOIL_MIN"]:
        alerts.append(("Jordfugtighed for lav", f"{vwc:.1f}% (rå værdi: {soil_raw})", "SOIL_LOW"))
    elif vwc > THRESHOLDS["SOIL_MAX"]:
        alerts.append(("Jordfugtighed for høj", f"{vwc:.1f}% (rå værdi: {soil_raw})", "SOIL_HIGH"))

    light = float(data['light'])
    if is_daytime() and light < THRESHOLDS["LIGHT_MIN"]:
        alerts.append(("Lysintensitet for lav", f"{light:.1f} LUX", "LIGHT"))

    temp = float(data['temp'])
    tmin, tmax = get_temp_thresholds()
    if temp < tmin:
        alerts.append(("Temperatur for lav", f"{temp:.1f}°C", "TEMP_LOW"))
    elif temp > tmax:
            alerts.append(("Temperatur for høj", f"{temp:.1f}°C", "TEMP_HIGH"))

    hum = float(data['hum'])
    if hum < THRESHOLDS["HUM_MIN"]:
        alerts.append(("Luftfugtighed for lav", f"{hum:.1f}%", "HUM_LOW"))
    elif hum > THRESHOLDS["HUM_MAX"]:
        alerts.append(("Luftfugtighed for høj", f"{hum:.1f}%", "HUM_HIGH"))

    for subject, value, key in alerts:
        if key not in sent_warnings:
            send_email(subject, value)
            sent_warnings.add(key)

