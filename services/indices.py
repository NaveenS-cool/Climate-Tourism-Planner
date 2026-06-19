import numpy

def rate_CIA(tmean, rhmean):       
        if 22 <= tmean <= 28 and 55 <= rhmean <= 80:
                return 5
        elif 20 <= tmean <= 30 and 40 <= rhmean <= 88:
                return 4
        elif 17 <= tmean <= 32:
                return 3
        elif 13 <= tmean <= 35:
                return 2
        return 1

def rate_CID(tmax, rhmin):
        if 22 <= tmax <= 30 and 50 <= rhmin <= 75:
                return 5
        elif 20 <= tmax <= 33 and 35 <= rhmin <= 85:
                return 4
        elif 18 <= tmax <= 35 and 25 <= rhmin <= 90:
                return 3
        elif 15 <= tmax <= 38:
                return 2
        return 1
def precipitation_rating(rain_mm):
        if rain_mm < 2:
                return 5
        elif rain_mm < 8:
                return 4
        elif rain_mm < 20:
                return 3
        elif rain_mm < 40:
                return 2
        return 1

def sunshine_rating(sunshine_hours):

        if sunshine_hours > 9:
                return 5
        elif sunshine_hours > 7:
                return 4
        elif sunshine_hours > 5:
                return 3
        elif sunshine_hours > 3:
                return 2
        return 1
 
 
def wind_rating(wind_kmh):
        if 8 <= wind_kmh <= 20:
                return 5
        elif (5 <= wind_kmh < 8) or (20 < wind_kmh <= 28):
                return 4
        elif 28 < wind_kmh <= 38:
                return 3
        elif 38 < wind_kmh <= 50:
                return 2
        return 1
 
 
def monsoon_penalty(rain_mm, rhmean):
        if rain_mm >= 20 and rhmean >= 85:
                return -6
        return 0

def compute_tci(tmax, tmean, rhmin, rhmean, rain_mm, sunshine_hours, wind_kmh):

        CID = rate_CIA(tmax, rhmin)
        CIA = rate_CID(tmean, rhmean)
        P   = precipitation_rating(rain_mm)
        S   = sunshine_rating(sunshine_hours)
        W   = wind_rating(wind_kmh)
        MP  = monsoon_penalty(rain_mm, rhmean)
 
        raw_tci = 2 * (4 * CID + CIA + 2 * P + 2 * S + W)
        final_tci = round(max(0.0, raw_tci + MP), 2)

        return final_tci
