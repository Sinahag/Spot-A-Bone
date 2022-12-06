import pyodbc
import spotipy.util as util
from userinfo import SPOTIPY_CLIENT_ID, SPOTIPY_CLIENT_SECRET, SPOTIPY_REDIRECT_URI
import sys

def connect_db():
    ODBC_STR = "Driver={ODBC Driver 18 for SQL Server};Server=tcp:sfucmpt.database.windows.net,1433;Database=cmpt351-spotabone;Uid=sinah;Pwd=CMPT354#;Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;"
    return pyodbc.connect(ODBC_STR)

class database:
    def __init__(self,username):
        self.conn = connect_db()
        self.delete_old_tokens()
        if(username):
            self.username = username
            self.userID=str()
            self.get_user_id()
            self.scope = 'user-top-read user-library-read user-library-modify user-read-private playlist-modify-public user-modify-playback-state user-read-playback-state user-read-currently-playing'
            self.token = str()
            self.get_token()

    def delete_old_tokens(self):
        delete_old_tokens="DELETE FROM SPOTIFYTOKEN WHERE DATEDIFF(SECOND, TIME_CREATED, CURRENT_TIMESTAMP) > 3540"
        cur = self.conn.cursor()
        cur.execute(delete_old_tokens)
        self.conn.commit()

    def set_token(self):
        insert_into_tokens_query = "INSERT INTO SPOTIFYTOKEN (TOKEN,USERNAME) VALUES (?,?);"
        cur = self.conn.cursor()
        cur.execute(insert_into_tokens_query,[self.token, self.userID])
        self.conn.commit()

    def get_token(self):
        if self.token=="":
            get_token_query = "SELECT TOKEN FROM SPOTIFYTOKEN WHERE username=? ORDER BY TIME_CREATED DESC"
            cursor = self.conn.execute(get_token_query,self.userID)

            self.token= cursor.fetchone()
            if self.token:
                self.token = self.token[0]

            self.conn.commit()

        if not self.token:  
            self.token = util.prompt_for_user_token(username=self.userID, 
                                                    scope = self.scope,
                                                    client_id = SPOTIPY_CLIENT_ID,
                                                    client_secret = SPOTIPY_CLIENT_SECRET,
                                                    redirect_uri = SPOTIPY_REDIRECT_URI)
            self.set_token()
        return self.token

    def get_users(self):
        get_users_query = "SELECT username FROM USER_ID"
        cursor = self.conn.execute(get_users_query)

        users = cursor.fetchall()
        filtered_users = list(filter(None, users))

        self.conn.commit()
        return filtered_users

    def get_playlists(self):
        get_playlists_query = "SELECT tagnum FROM NFC_PLAYLIST_URI"
        cursor = self.conn.execute(get_playlists_query)

        playlists = cursor.fetchall()
        filtered_playlists = list(filter(None, playlists))

        for i in range(len(filtered_playlists)):
            filtered_playlists[i] = f"p{filtered_playlists[i]}"

        self.conn.commit()
        return filtered_playlists


    def get_songs(self):
        get_song_query = "SELECT tagnum FROM NFC_URI"
        cursor = self.conn.execute(get_song_query)

        songs = cursor.fetchall()
        filtered_songs = list(filter(None, songs))

        for i in range(len(filtered_songs)):
            filtered_songs[i] = f"s{filtered_songs[i]}"

        self.conn.commit()
        return filtered_songs

    def get_tag_uri(self,tagID):
        get_uri_query = "SELECT uri FROM NFC_URI WHERE tagnum=?"
        cursor = self.conn.execute(get_uri_query,tagID)

        uri= cursor.fetchone()
        uri=uri[0]

        self.conn.commit()

        return uri
    
    def get_playlist_id(self,playlistNum):
        get_uri_query = "SELECT uri FROM NFC_PLAYLIST_URI WHERE tagnum=?"
        cursor = self.conn.execute(get_uri_query,playlistNum)

        uri= cursor.fetchone()
        uri = uri[0]

        self.conn.commit()

        return uri

    def get_user_id(self):
        get_userID_query = "SELECT userID FROM USER_ID WHERE username=?"
        cursor = self.conn.execute(get_userID_query,self.username)

        self.userID = cursor.fetchone()
        
        if not self.userID:
            print("User not registered")
            sys.exit()

        self.userID = self.userID[0]

        self.conn.commit()

        return self.userID

    def cleanup(self):
        self.conn.close()

