import boto3

bucketName = "application-tracking-system-test"
Key = '/media/farhaan/New Volume/Masters/database/Data Mining HW1.pdf'
outPutname = "test1.pdf"

s3 = boto3.resource('s3')
# resp = s3.upload_file(Key,bucketName,outPutname)



bucket_location = boto3.client('s3').get_bucket_location(Bucket=bucketName)
object_url = "https://s3-{0}.amazonaws.com/{1}/{2}".format(
    bucket_location['LocationConstraint'],
    bucketName,
    Key,
ACL='public')
print(object_url)









# import boto3
# import botocore
#
# Bucket = "Your S3 BucketName"
# Key = "Name of the file in S3 that you want to download"
# outPutName = "Output file name(The name you want to save after we download from s3)"
#
# s3 = boto3.resource('s3')
# try:
#     s3.Bucket(Bucket).download_file(Key, outPutName)
# except botocore.exceptions.ClientError as e:
#     if e.response['Error']['Code'] == "404":
#         print("The object does not exist.")
#     else:
#         raise