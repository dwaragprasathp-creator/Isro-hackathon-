import cdsapi
from pathlib import Path

client = cdsapi.Client()

output = Path("data/raw/era5")
output.mkdir(parents=True, exist_ok=True)

outfile = output / "era5_hyderabad.nc"

client.retrieve(
    "reanalysis-era5-single-levels",
    {
        "product_type": "reanalysis",
        "variable": [
            "2m_temperature",
            "2m_dewpoint_temperature",
            "10m_u_component_of_wind",
            "10m_v_component_of_wind",
        ],
        "year": "2024",
        "month": "05",
        "day": "29",

        "time": [
            "00:00","01:00","02:00","03:00",
            "04:00","05:00","06:00","07:00",
            "08:00","09:00","10:00","11:00",
            "12:00","13:00","14:00","15:00",
            "16:00","17:00","18:00","19:00",
            "20:00","21:00","22:00","23:00"
        ],

        "format":"netcdf",

        "area":[
            17.7,
            78.2,
            17.2,
            78.8
        ]
    },

    str(outfile)
)

print("ERA5 Download Completed")