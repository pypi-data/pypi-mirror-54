# from awsparameter.aws_s3_kms_parameter import Parameters
import boto3
import json
import base64
import logging
logger = logging.getLogger()


def encrypt_text_with_kms(config_dict, kms_key_alias, kms_client=None):
    '''
    :param config_dict: dict of config
                        ex) { key : { key: value} }
    :param kms_key_alias: name of kms
    :param kms_client: boto kms object ex) boto3.clent('kms')
    :return: encrypted ciphertext
    '''
    if kms_client is None:
        kms_client = boto3.client('kms',
                                  aws_access_key_id=None,
                                  aws_secret_access_key=None
                                  )
    config_text = json.dumps(config_dict)
    key = 'alias/%s' % kms_key_alias
    try:
        response = kms_client.encrypt(
            KeyId=key,
            Plaintext=config_text
        )
        encrypted_ciphertext = base64.b64encode(response["CiphertextBlob"])
    except Exception as err:
        logger.error(err)
        raise

    return encrypted_ciphertext


def is_s3_key_list(key_name, key_bucket, s3_client):
    '''
    check same key in s3 bucket
    :param key_name: name of kms key
    :param key_bucket: name fo s3 bucket
    :param s3_client: object of s3 with s3
    :return: boolean
    '''
    try:
        response = s3_client.list_objects(
            Bucket=key_bucket
        )
        res_contents = response.get('Contents', None)
        key_lists = [obj['Key'] for obj in res_contents]
        if key_name in key_lists:
            return False
        else:
            return True
    except Exception as err:
        logger.error(err)
        raise


def upload_s3(key_bucket, kms_key_alias, key_name, encoded_ciphertext, s3_client=None, is_force=False):
    '''
    upload content to s3 bucket
    :param key_bucket: name fo s3 bucket
    :param kms_key_alias: name of kms key
    :param key_name: name of key in s3
    :param encoded_ciphertext: encoded text
    :param s3_client: object of s3 with s3
    :return:
    '''
    if s3_client is None:
        s3_client = boto3.client('s3',
                                 aws_access_key_id=None,
                                 aws_secret_access_key=None
                                 )
    key = 'alias/%s' % kms_key_alias
    if '.json' not in key_name:
        key_name = key_name + '.json'

    if not is_force:
        if not is_s3_key_list(key_name, key_bucket, s3_client):
            raise Exception(key_name+' is already used in '+key_bucket)

    try:
        response = s3_client.put_object(
            ACL='private',
            Body=encoded_ciphertext,
            Bucket=key_bucket,
            ContentType="application/json",
            ServerSideEncryption="aws:kms",
            SSEKMSKeyId=key,
            Key=key_name
        )
    except Exception as err:
        logger.error(err)
        raise
    return response


def get_aws_config_from_bucket(s3_client, ssm_key, key_bucket):
    '''
    get content from bucket
    :param s3_client: object of boto3 with s3
    :param ssm_key: name of key in bucket
    :param key_bucket: name of bucket
    :return:
    '''
    if '.json' not in ssm_key:
        s3_key = ssm_key + '.json'
    else:
        s3_key = ssm_key

    response = s3_client.get_object(
        Bucket=key_bucket,
        Key=s3_key
    )
    decoded_res = response['Body'].read()
    return decoded_res


def decrypt_text_with_kms(key_bucket, saved_bucket_key, kms_client=None, s3_client=None):
    '''
    decrypt content from s3
    :param key_bucket: name of bucket
    :param saved_bucket_key: name of key in bucket
    :param kms_client: object of boto3 with kms
    :param s3_client: object of boto3 with s3
    :return: encoded text
    '''
    if kms_client is None:
        kms_client = boto3.client('kms',
                                  aws_access_key_id=None,
                                  aws_secret_access_key=None
                                  )
    if s3_client is None:
        s3_client = boto3.client('s3',
                                 aws_access_key_id=None,
                                 aws_secret_access_key=None
                                 )

    endcoded_text = get_aws_config_from_bucket(s3_client, saved_bucket_key, key_bucket)
    cipher_text_blob = base64.b64decode(endcoded_text)
    decrypt_text = kms_client.decrypt(
        CiphertextBlob=bytes(cipher_text_blob)
    )
    encoded_txt = json.loads(decrypt_text['Plaintext'])
    return encoded_txt

