import pandas as pd
from geopy.distance import geodesic

def analisis_banjir(df):
    if df.empty: return df
    
    df['Waktu'] = pd.to_datetime(df['Waktu_Str'])
    
    def cek_status(row):
        hujan = row['Curah_Hujan_mm']
        kode = row['Kode_Cuaca']
        
        if hujan > 5.0 or kode >= 95:
            return "BAHAYA (Potensi Banjir/ Hujan Badai)"
        elif hujan > 1.0 or (60 <= kode <= 65):
            return "WASPADA (Hujan)"
        else:
            return "AMAN (Berawan/Cerah)"
            
    df['Status_Risiko'] = df.apply(cek_status, axis=1)
    return df

def hitung_jarak(df, user_lat, user_lon):
    if df.empty: return df
    user = (user_lat, user_lon)
    
    kota_unique = df[['Kota', 'Latitude', 'Longitude']].drop_duplicates()
    
    def hitung(row):
        return round(geodesic(user, (row['Latitude'], row['Longitude'])).km, 1)
        
    kota_unique['Jarak_KM'] = kota_unique.apply(hitung, axis=1)
    
    return pd.merge(df, kota_unique[['Kota', 'Jarak_KM']], on='Kota', how='left')