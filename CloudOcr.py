# import subprocess

# curlRequest = "curl -X POST -H Authorization: Bearer $(gcloud auth application-default print-access-token) -H" +\
# "Content-Type: application/json; charset=utf-8" +\
# "https://vision.googleapis.com/v1/images:annotate" +\
# "-d @request.json -o response.json"


# checker = subprocess.check_output(hey, shell=True).decode("utf-8")


# print("time to analyse response")