import pandas as pd
from pycountry import countries

# List of Non-Annex I countries as of May 16, 2023
non_annex_countries = [
    "Afghanistan", "Albania", "Algeria", "Andorra", "Angola", "Antigua and Barbuda", "Argentina",
    "Armenia", "Azerbaijan", "Bahamas", "Bahrain", "Bangladesh", "Barbados", "Belize", "Benin", "Bhutan",
    "Bolivia (Plurinational State of)", "Bosnia and Herzegovina", "Botswana", "Brazil", "Brunei Darussalam",
    "Burkina Faso", "Burundi", "Cabo Verde", "Cambodia", "Cameroon", "Central African Republic", "Chad",
    "Chile", "China", "Colombia", "Comoros", "Congo", "Cook Islands", "Costa Rica", "Côte d'Ivoire", "Cuba",
    "Democratic People's Republic of Korea", "Democratic Republic of the Congo", "Djibouti", "Dominica",
    "Dominican Republic", "Ecuador", "Egypt", "El Salvador", "Equatorial Guinea", "Eritrea", "Eswatini",
    "Ethiopia", "Fiji", "Gabon", "Gambia", "Georgia", "Ghana", "Grenada", "Guatemala", "Guinea",
    "Guinea-Bissau", "Guyana", "Haiti", "Holy See", "Honduras", "India", "Indonesia", "Iran (Islamic Republic of)",
    "Iraq", "Israel", "Jamaica", "Jordan", "Kazakhstan", "Kenya", "Kiribati", "Kuwait", "Kyrgyzstan",
    "Lao People's Democratic Republic", "Lebanon", "Lesotho", "Liberia", "Libya", "Madagascar", "Malawi",
    "Malaysia", "Maldives", "Mali", "Marshall Islands", "Mauritania", "Mauritius", "Mexico", "Micronesia (Federated States of)",
    "Mongolia", "Montenegro", "Morocco", "Mozambique", "Myanmar", "Namibia", "Nauru", "Nepal", "Nicaragua",
    "Niger", "Nigeria", "Niue", "North Macedonia", "Oman", "Pakistan", "Palau", "Panama", "Papua New Guinea",
    "Paraguay", "Peru", "Philippines", "Qatar", "Republic of Korea", "Republic of Moldova", "Rwanda",
    "Saint Kitts and Nevis", "Saint Lucia", "Saint Vincent and the Grenadines", "Samoa", "San Marino",
    "Sao Tome and Principe", "Saudi Arabia", "Senegal", "Serbia", "Seychelles", "Sierra Leone", "Singapore",
    "Solomon Islands", "Somalia", "South Africa", "South Sudan", "Sri Lanka", "State of Palestine", "Sudan",
    "Suriname", "Syrian Arab Republic", "Tajikistan", "Thailand", "Timor-Leste", "Togo", "Tonga", "Trinidad and Tobago",
    "Tunisia", "Turkmenistan", "Tuvalu", "Uganda", "United Arab Emirates", "United Republic of Tanzania", "Uruguay",
    "Uzbekistan", "Vanuatu", "Venezuela (Bolivarian Republic of)", "Viet Nam", "Yemen", "Zambia", "Zimbabwe"
]

# Creating DataFrame and adding ISO3 codes
data = []

for country in non_annex_countries:
    try:
        # Match country name to ISO3 code
        iso3_code = countries.lookup(country).alpha_3
    except LookupError:
        iso3_code = "N/A"
    
    data.append({"Country": country, "ISO3": iso3_code})

# Creating DataFrame
df = pd.DataFrame(data)

# Saving DataFrame to Excel
output_path = "/mnt/data/non_annex_1_countries.xlsx"
df.to_excel(output_path, index=False)

output_path