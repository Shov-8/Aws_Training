import boto3

from flask import Flask, render_template

app = Flask(__name__)


def fetchData():
    session = boto3.Session(profile_name="Shov8")
    s3_client = session.client("s3")
    bucket_name = "tiger-mle-pg"
    # Get all the subfolder names
    response = s3_client.list_objects_v2(
        Bucket=bucket_name, Prefix="home/shovit.mittra/", Delimiter="/"
    )
    subfolders = []
    for o in response.get("CommonPrefixes"):
        subfolders.append(o.get("Prefix"))
    # Print the files within each subfolder
    s3 = session.resource("s3")
    my_bucket = s3.Bucket(bucket_name)
    dic = {}
    for subfolder in subfolders:
        for object_summary in my_bucket.objects.filter(Prefix=subfolder):
            if object_summary.key != subfolder:
                dic[subfolder] = object_summary.key.replace(subfolder, "")
    return dic


@app.route("/")
def home():
    posts = fetchData()
    return render_template("index.html", posts=posts)


# added port 8085 and made debug=True to check for bugs
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8085, debug=True)
