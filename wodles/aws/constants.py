from os import path

# AWS Bucket
MAX_AWS_BUCKET_RECORD_RETENTION = 500
AWS_BUCKET_DB_DATE_FORMAT = "%Y%m%d"

DEFAULT_AWS_BUCKET_DATABASE_NAME = "s3_cloudtrail"

RETRY_CONFIGURATION_URL = 'https://documentation.wazuh.com/current/amazon/services/prerequisites/' \
                          'considerations.html#Connection-configuration-for-retries'

INVALID_CREDENTIALS_ERROR_CODE = "SignatureDoesNotMatch"
INVALID_REQUEST_TIME_ERROR_CODE = "RequestTimeTooSkewed"
THROTTLING_EXCEPTION_ERROR_CODE = "ThrottlingException"

INVALID_CREDENTIALS_ERROR_MESSAGE = "Invalid credentials to access S3 Bucket"
INVALID_REQUEST_TIME_ERROR_MESSAGE = "The server datetime and datetime of the AWS environment differ"
THROTTLING_EXCEPTION_ERROR_MESSAGE = "The '{name}' request was denied due to request throttling. " \
                                     "If the problem persists check the following link to learn how to use " \
                                     f"the Retry configuration to avoid it: '{RETRY_CONFIGURATION_URL}'"

AWS_BUCKET_MSG_TEMPLATE = {'integration': 'aws',
                           'aws': {'log_info': {'aws_account_alias': '', 'log_file': '', 's3bucket': ''}}}

# Cloudtrail
AWS_CLOUDTRAIL_DYNAMIC_FIELDS = ['additionalEventData', 'responseElements', 'requestParameters']

# Guarduty
GUARDDUTY_URL = 'https://documentation.wazuh.com/current/amazon/services/supported-services/guardduty.html'
GUARDDUTY_DEPRECATED_MESSAGE = 'The functionality to process GuardDuty logs stored in S3 via Kinesis was deprecated ' \
                               'in {release}. Consider configuring GuardDuty to store its findings directly in an S3 ' \
                               'bucket instead. Check {url} for more information.'

# AWS Service
DEFAULT_AWS_SERVICE_DATABASE_NAME = "aws_services"
DEFAULT_AWS_SERVICE_TABLENAME = "aws_services"

# AWS Tools
DEFAULT_AWS_CONFIG_PATH = path.join(path.expanduser('~'), '.aws', 'config')
AWS_CREDENTIALS_URL = 'https://documentation.wazuh.com/current/amazon/services/prerequisites/credentials.html'
DEPRECATED_MESSAGE = 'The {name} authentication parameter was deprecated in {release}. ' \
                     'Please use another authentication method instead. Check {url} for more information.'
SECURITY_LAKE_IAM_ROLE_AUTHENTICATION_URL = 'https://documentation.wazuh.com/current/cloud-security/amazon/services/' \
                                        'supported-services/security-lake.html#configuring-an-iam-role'

ALL_REGIONS = (
    'af-south-1', 'ap-east-1', 'ap-northeast-1', 'ap-northeast-2', 'ap-northeast-3', 'ap-south-1', 'ap-south-2',
    'ap-southeast-1', 'ap-southeast-2', 'ap-southeast-3', 'ap-southeast-4', 'ca-central-1', 'eu-central-1',
    'eu-central-2', 'eu-north-1', 'eu-south-1', 'eu-south-2', 'eu-west-1', 'eu-west-2', 'eu-west-3', 'il-central-1',
    'me-central-1', 'me-south-1', 'sa-east-1', 'us-east-1', 'us-east-2', 'us-west-1', 'us-west-2'
)

RETRY_ATTEMPTS_KEY: str = "max_attempts"
RETRY_MODE_CONFIG_KEY: str = "retry_mode"
RETRY_MODE_BOTO_KEY: str = "mode"