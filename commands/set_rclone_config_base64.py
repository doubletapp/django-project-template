import dotenv
import base64
from string import Template
import os


ENV_FILE = os.path.join('src', os.environ.get('ENV_FILE', '.env'))


def main():
    with open('./.rclone.conf') as f:
        template = Template(f.read())

    substituted = template.safe_substitute(**os.environ)
    base64_conf = base64.b64encode(substituted.encode()).decode()
    dotenv.set_key(ENV_FILE, "RCLONE_CONFIG_BASE64", base64_conf, quote_mode='never')


if __name__ == '__main__':
    main()
