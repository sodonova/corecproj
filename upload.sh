DATE=$(date -Is)
FILENAME=usage_data_$DATE.csv
/homes/sodonova/corecproj/env2/bin/python /homes/sodonova/corecproj/get_corec_usage_v2.py /homes/sodonova/corecproj/tempData/$FILENAME
/homes/sodonova/corecproj/aws-bin/aws s3 cp /homes/sodonova/corecproj/tempData/$FILENAME s3://corecbucket/$FILENAME
rm /homes/sodonova/corecproj/tempData/$FILENAME

FILENAME=napi_data_$DATE.csv
/homes/sodonova/corecproj/env2/bin/python /homes/sodonova/corecproj/get_corec_usage.py /homes/sodonova/corecproj/tempData/$FILENAME
/homes/sodonova/corecproj/aws-bin/aws s3 cp /homes/sodonova/corecproj/tempData/$FILENAME s3://corecbucket/$FILENAME
rm /homes/sodonova/corecproj/tempData/$FILENAME
