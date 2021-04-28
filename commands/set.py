import dotenv
import sys
import os


ENV_FILE = os.path.join('src', os.environ.get('ENV_FILE', '.env'))


def main():
    base64_conf = ''.join(sys.argv[1:])
    dotenv.set_key(ENV_FILE, "RCLONE_CONFIG_BASE64", base64_conf, quote_mode='never')


if __name__ == '__main__':
    main()
