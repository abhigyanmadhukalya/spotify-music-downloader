from flask import Flask, redirect, request, url_for, session
from spotipy import SpotifyOAuth, Spotify
from time import time
from download_mp3 import download_mp4_from_titles
from os import getenv
import pandas as pd
import json
import csv


app = Flask(__name__)
app.secret_key = "super secret key"
app.config["SESSION_COOKIE_NAME"] = "spotify-login-session"
TOKEN_INFO = "token_info"


def create_oauth_object():
    return SpotifyOAuth(
        client_id=str(getenv("SPOTIFY_CLIENT_ID")),
        client_secret=getenv("SPOTIFY_CLIENT_SECRET"),
        redirect_uri=url_for("authorise", _external=True),
        scope="user-library-read",
    )


def get_token():
    token_info = session.get(TOKEN_INFO, None)
    if not token_info:
        raise Exception("No token found in session")
    now = int(time())

    is_token_expired = token_info["expires_at"] - now < 60
    if is_token_expired:
        oauth = create_oauth_object()
        token_info = oauth.refresh_access_token(token_info["refresh_token"])

    return token_info


@app.route("/")
def login():
    oauth = create_oauth_object()
    auth_url = oauth.get_authorize_url()
    print(auth_url)
    return redirect(auth_url)


@app.route("/logout")
def logout():
    for key in list(session.keys()):
        session.pop(key)
    return redirect("/")


@app.route("/authorise")
def authorise():
    oauth = create_oauth_object()
    session.clear()
    code = request.args.get("code")
    token_info = oauth.get_access_token(code)
    session[TOKEN_INFO] = token_info
    return redirect("/getTracks")


@app.route("/getTracks")
def get_all_tracks():
    session["token_info"], authorized = get_token()
    session.modified = True
    if not authorized:
        return redirect("/")
    sp = spotipy.Spotify(auth=session.get("token_info").get("access_token"))
    results = []
    iter = 0
    while True:
        offset = iter * 50
        iter += 1
        curGroup = sp.current_user_saved_tracks(limit=50, offset=offset)["items"]
        for idx, item in enumerate(curGroup):
            track = item["track"]
            val = track["name"] + " - " + track["artists"][0]["name"]
            results += [val]
        if len(curGroup) < 50:
            break

    df = pd.DataFrame(results, columns=["song names"])
    df.to_csv("songs.csv", index=False)
    return "done"


if __name__ == "__main__":
    app.run(debug=True)
