# Monsoon Rainfall Visualization over India (2023)

This project visualizes the progression of monsoon rainfall over India for the year 2023 using satellite precipitation data from CHRS PERSIANN. It generates a time-lapse GIF showing the daily spread of rainfall across the country.

## 🌍 Project Highlights

- Visualizes daily rainfall from CHRS NetCDF data
- Overlays Indian state boundaries (including Jammu & Kashmir)
- Adds annotation and styling for educational and presentation use
- Outputs a smooth animated GIF showing monsoon progression

---
monsoon-rainfall-india-2023/
│
├── Data/                             # Your NetCDF rainfall dataset
│   └── PERSIANN_India_2025-06-04094807pm_2023.nc
│
├── IND_SHP/                          # India shapefile folder
│   └── India_State_Boundary.shp
│   └── (other .shx, .dbf, etc.)
│
├── monsoon_progression.gif          # Final generated GIF
│
├── monsoon_visualization.py        # Your main Python script
│
├── requirements.txt                 # Dependencies
│
└── README.md                        # Project description & usage
