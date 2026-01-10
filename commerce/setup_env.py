import os
import secrets
import string

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def generate_secret_key():
    #generate a random string as secret key
    chars = string.ascii_letters + string.digits + string.punctuation
    return ''.join(secrets.choice(chars) for i in range(50))


def setup():
    env_file = os.path.join(BASE_DIR, '.env')
    example_file = os.path.join(BASE_DIR, '.env.example')

    if os.path.exists(env_file):
        print(f" {env_file} already exists. No changes made.")
        return

    print(f" Creating {env_file} file...")

    secret_key = generate_secret_key()

    # try to  read template from  .env.example
    if os.path.exists(example_file):
        with open(example_file, 'r') as f:
            content = f.read()
        content = content.replace('SECRET_KEY=', f'SECRET_KEY={secret_key}')
    else:
        content = f"SECRET_KEY={secret_key}\nDEBUG=True\n"

    with open(env_file, 'w') as f:
        f.write(content)

    print(f" Successfully generated {env_file} with a fresh SECRET_KEY!")


if __name__ == "__main__":
    setup()