# corecproj
A project to collect and display aggregated purdue Corec usage data.

## Usage
If you're trying to reproduce this, I used Python 3.8.10 and the packages in requirements.txt.
To run the collection script after cloning:

for windows:
```
python3 --version
python3 -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python3 get_usage_data_v2.py usage_data_out.csv
```
for linux:
```
python3 --version
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python3 get_usage_data_v2.py usage_data_out.csv
```
