# Download OZFlux Data from TERN (Terrestrial Ecosystem Research Network)
# Wriiten by `Pushpendra Raghav`; ppushpendra@ua.edu
# July 10, 2025
import pandas as pd; import re; from urllib.error import HTTPError
import wget; import os; import xarray as xr
export_record = pd.read_csv(r"E:\Asia_OZFlux_TERN_Flux\TERN\export_records.csv")
def extract_site_version(title):
    match = re.match(r"(.+?) Flux Data Release (\d{4})_v(\d+)", title)
    if match:
        site = match.group(1).replace(" ", "")  # Remove spaces
        year = int(match.group(2))
        version = int(match.group(3))
        return pd.Series([site, year, version])
    else:
        return pd.Series([None, None, None])
export_record[['Site', 'Year', 'Version']] = export_record['Title'].apply(extract_site_version)
export_record = export_record.dropna(subset=['Site'])
export_record['Temporal Date From'] = pd.to_datetime(export_record['Temporal Date From'], errors='coerce')
export_record['Temporal Date To'] = pd.to_datetime(export_record['Temporal Date To'], errors='coerce')
export_record['Data_Duration_Years'] = (export_record['Temporal Date To'] - export_record['Temporal Date From']).dt.days / 365.25
export_record = export_record[export_record['Data_Duration_Years'] > 5]
export_record_latest = (
    export_record.sort_values(['Site', 'Year', 'Version'], ascending=[True, False, False])
    .drop_duplicates(subset='Site', keep='first')
)
#print(export_record_latest[['Title', 'Site', 'Year', 'Version', 'Data_Duration_Years']])

# Download Data (Main)
def download_TERN_flux_data(site, year, version, base_url, output_dir, level="L6"):
    def build_url(site_name,fallback_site_name, res="hourly"):
        if res == "hourly":
            return f"{base_url}{site_name}/{year}_v{version}/{level}/default/{fallback_site_name}_{level}.nc"
        else:
            return f"{base_url}{site_name}/{year}_v{version}/{level}/default/{fallback_site_name}_{level}_Daily.nc"
    def get_output_path(site_name, res="hourly"):
        if res == "hourly":
            return os.path.join(output_dir, f"{site_name}_{level}.nc")
        else:
            return os.path.join(output_dir, f"{site_name}_{level}_Daily.nc")
    for res in ["hourly", "daily"]:
        file_url = build_url(site,site, res)
        output_file = get_output_path(site, res)
        # Check if file exists and is valid
        download_flag = True
        if os.path.exists(output_file):
            try:
                xr.open_dataset(output_file).close()
                download_flag = False
            except Exception as e:
                print(f"Corrupt or unreadable file: {output_file}. Reason: {e}")
        if download_flag:
            print(f"Trying to download: {site}")
            try:
                wget.download(file_url, output_file)
                print(f"Done Downloading ({res})")
            except HTTPError as e:
                if e.code == 404:
                    # Try fallback (I observed that filename structure is not consistent in TERN dataset so fallback needed)
                    short_site = re.match(r'^([A-Z][a-z]+)', site)
                    if short_site:
                        fallback_site = short_site.group(1)
                        fallback_url = build_url(site,fallback_site, res)
                        fallback_file = get_output_path(fallback_site, res)
                        print(f"\n404 error. Trying fallback: {fallback_url}")
                        try:
                            wget.download(fallback_url, fallback_file)
                            print(f"Done (fallback: {res})")
                        except Exception as e2:
                            print(f"Fallback failed: {e2}")
                    else:
                        print(f"No fallback pattern found for site: {site}")
                else:
                    print(f"Download failed with error: {e}")

# Basic settings
output_dir = r"E:\Asia_OZFlux_TERN_Flux\TERN"
base_url = "https://dap.tern.org.au/thredds/fileServer/ecosystem_process/ozflux/"
for idx, row in export_record_latest.iterrows():
    site = row['Site']
    year = int(row['Year'])
    version = int(row['Version'])
    download_TERN_flux_data(site, year, version, base_url, output_dir)