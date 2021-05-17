import dotenv
import base64
from string import Template
import os


ENV_FILE = os.path.join('src', os.environ.get('ENV_FILE', '.env'))


def get_digital_ocean_endpoint():
    location = os.environ.get('AWS_LOCATION')
    endpoint = f'{location}.digitaloceanspaces.com'

    return endpoint


def get_aws_endpoint():
    location = os.environ.get('AWS_LOCATION')
    endpoint = f's3.{location}.amazonaws.com'

    return endpoint


OPTIONS = {
    'DigitalOcean': get_digital_ocean_endpoint(),
    'AWS': get_aws_endpoint(),
}


def main():
    with open('./.rclone.conf') as f:
        template = Template(f.read())

    provider = os.environ.get('AWS_PROVIDER')
    if provider not in OPTIONS:
        raise ValueError(
            f'{provider} is not allowed. available providers are: {", ".join(OPTIONS.keys())}'
        )

    endpoint = OPTIONS[provider]
    vars = os.environ.copy()
    vars['AWS_ENDPOINT'] = endpoint

    substituted = template.safe_substitute(**vars)
    base64_conf = base64.b64encode(substituted.encode()).decode()
    dotenv.set_key(ENV_FILE, 'RCLONE_CONFIG_BASE64', base64_conf, quote_mode='never')
    dotenv.set_key(ENV_FILE, 'AWS_ENDPOINT', endpoint, quote_mode='never')


if __name__ == '__main__':
    main()
