# Download_OzFlux_Data_TERN
This repository provides Python script to automate the download of eddy covariance flux tower data of water and carbon fluxes from the Terrestrial Ecosystem Research Network (TERN), specifically from the OzFlux ecosystem observation network.

# Input File
`export_records.csv`
You can obtain this file manually from the TERN data portal by searching for flux datasets and exporting metadata.

It contains metadata fields including:
- Title: Name of the flux data release (e.g., Alice Springs Mulga Flux Data Release 2025_v1)
- Observation period
- Data version: Version of the release


# Requirements
Install dependencies via pip (or any other means):
pip install pandas xarray wget

# How to Run
python Main.py

# Output
Downloaded files are saved in the format:


/path/to/output/

│

├── AliceSpringsMulga_L6.nc

├── AliceSpringsMulga_L6_Daily.nc

├── Warra_L6.nc

├── Warra_L6_Daily.nc

...

# Fallback Naming Logic
TERN's data repository sometimes uses inconsistent site name formats. The script includes a fallback rule that extracts the first capitalized prefix from the site name to retry downloads if a 404 error is encountered (e.g., fallback from CalperumChowilla -> Calperum).
