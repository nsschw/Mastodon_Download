import pathlib
import time
import threading
import orjson as json

import mastodon
from mastodon.streaming import StreamListener, CallbackStreamListener

import os
from dotenv import load_dotenv


def activate_account(login, email, password):
    nick, domain = login.split("@")
    server_url = f'https://{domain}'
    app_name = f'{nick}_app'
    client_file = f'{nick}_clientcred.secret'
    user_file = f'{nick}_usercred.secret'
    if not pathlib.Path(client_file).exists():
        mastodon.Mastodon.create_app(
            app_name,
            api_base_url=server_url,
            to_file=client_file)
        print(f'>>- Created App for {nick}')
    api = mastodon.Mastodon(client_id=client_file)
    if not pathlib.Path(user_file).exists():
        api.log_in(
            email,
            password,
            to_file=user_file)
        print(f'>>- Created Token for {nick}')
    api = mastodon.Mastodon(access_token=user_file)
    return api

def save_toot(toot, filename):
    with open(f"Data/fediverse-{filename}-toots.log", "ba") as tootfile:
        tootfile.write(json.dumps(toot) + b"\n")


def handle_toot(toot, filename):
    save_toot(toot, filename)


def run_listener(login, email, password):
    api = activate_account(login, email, password)
    filename = login.split("@")[-1]
    listener = CallbackStreamListener(
        update_handler=lambda x: handle_toot(x, filename),
        local_update_handler=lambda x: handle_toot(x, filename),
        status_update_handler=lambda x: handle_toot(x, filename),
    )
    print(f'>>- Streaming {filename}')
    while True:
        try:
            api.stream_public(listener=listener)
        except mastodon.errors.MastodonNetworkError as exc:
            if 'Not Found' in str(exc):
                print(f'>>- Cannot connect to {filename}, aborting')
                return
            print(f'>>- Reconnecting {filename} ...')




if __name__ == "__main__":

    load_dotenv()
        
    accounts = []
    index = 1

    while True:
        username_key = f"ACCOUNTS_USERNAME_{index}"
        email_key = f"ACCOUNTS_EMAIL_{index}"
        password_key = f"ACCOUNTS_PASSWORD_{index}"

        username = os.getenv(username_key)
        email = os.getenv(email_key)
        password = os.getenv(password_key)

        if username and email and password:
            accounts.append((username, email, password))
            index += 1
        else:
            break
    
    print(accounts)
        

    threads = []
    for account in accounts:
        login, email, password = account
        t = threading.Thread(target=run_listener,
                             args=(login, email, password,))
        threads.append(t)
        t.start()
    while True:
        try:
            time.sleep(5)
        except Exception as exc:
            print(f'Quitting: {exc}')
        for t in threads:
            t.join()