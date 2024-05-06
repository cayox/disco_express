# Disco Express
Eine App zur Informationsanzeige und Eingabe von Musikwünschen.

Die App kommuniziert mit dem Disco Express Server via HTTP.

## Einstellungen
Alle Einstellungen können über die Config Datei und die dazugehörigen Dateien gemacht
werden. Dazu erstellt das Programm unter ``~/disco_express`` einen Ordner mit allen
nötigen Dateien und Verzeichnissen. 

### Default Config Datei
Die standard Config Datei sieht wie folgt aus:
```toml
[general]
# Debug modus, sollte "false" sein
debug = false

# Titel der app am oberen Bildschirmrand
app_name = "Disco Express"

# Dateien relativ zum ~/disco_express ordner
classics_file = "data/classics.csv"
charts_file = "data/charts.csv"
current_charts = "data/current_charts.csv"
slurs_file = "data/slurs.txt"

# Log Ordner relativ zum ~/disco_express ordner
log_directory = "logs"
# Documents Ordner relativ zum ~/disco_express ordner
# hier werden die Dokumente vom Server heruntergeladen und gespeichert
documents_directory = "documents"

# Automatisches Schließen der Dokumente oder Charts menü
auto_close_time = 300  # in seconds
# Abfrageintervall an den Disco Express Server. Demnach auch Aktualisierungszeit bei Serverseitigen Einstellungen.
server_refresh_interval = 10  # in seconds
# Delay das eingestellt wird wenn ein Musikwunsch abgeschickt wird.
wish_sending_time = 10 # in seconds
# interval in welchem das banner um einen Buschstaben weiter rückt
banner_speed = 100 # in millisekunden

# maximale Eingabelänge bei Musikwunschfeldern
max_input_length = 32
# maximale Eingabelänge bei dem Message Musikwunschfeld
max_input_length_message = 64


######### SCREEN SAVER
#screen_saver_images = "screen_saver"
#screen_saver_rotation_speed = 5 # seconds
#screen_saver_start_time = 5 # seconds


######### ICONS

[icons]
artist_icon = "icons/artist.svg"
song_icon = "icons/song.svg"
file_icon = "icons/file.svg"
error_icon = "icons/error.svg"
home_icon = "icons/home.svg"
charts_plays_icon = "icons/chart.svg"
unavailable_icon = "icons/unavailable.svg"
zoom_in_icon = "icons/zoom-in.svg"
zoom_out_icon = "icons/zoom-out.svg"

######### NETWORK

[network]
# hier die IP adresse vom Server eintragen
server_ip = "localhost"
# Port muss beim Server und Client gleich sein. Standard ist 8080
server_port = 8080

######### COLORS
[style]
# Pfad zum Hintergrundbild relartiv zu ~/disco_express
background_image = "img/jukebox_comic.jpg"
# Wie stark das Bild abgedunkelt werden soll [1 keine abdunklung, 0 Schwarz]
background_darkness_factor = 0.7

# Glow stärke für UI (Knöpfe und so) und Text
# je stärker der glow (neon) desto schlechter ist die performance
ui_glow_strength = 128
text_glow_strength = 128

[style.colors]
background_color = "#f5ebe0"

accent1_glow = "#80ffdb"
accent1 = "#48bfe3"
accent1_dark = "#4895ef"

highlight_glow = "#ff0a54"
highlight = "#ff7096"
off_highlight = "#e01e37"

icon_color = "#f5ebe0"

white = "#f5ebe0"
red = "#e01e37"

disabled_light = "#ced4da"
disabled = "#adb5bd"
disabled_dark = "#6c757d"

######### LANGUAGES

[[languages]]
# Name der Sprache für interne Identifikation
language_name = "german"
# Bild der Sprache relativ zu ~/disco_express
language_icon = "icons/de.svg"

heading_music_wish = "Geben Sie einen Musikwunsch an. Sie können diesen Musikwunsch auch an eine Person richten!"
heading_home = "Willkommen beim Disco Express. Hier können Sie sich ein Lied wünschen oder Informationen zum Fahrgeschäft erhalten."
heading_information = "Wählen Sie eines der Dokumente um mehr zu erfahren."

home_info_btn = "Information"
home_music_wish_btn = "Musik Wunsch"

music_title = "Musik Titel"
music_interpret = "Interpret"
music_sender = "Von"
music_receiver = "Für"
music_message = "Nachricht"

btn_quick_selection = "Schnelle Auswahl"
btn_send = "Anfrage Senden"

error_no_title = "Kein Titel angegeben!"
error_no_interpret = "Kein Interpret angegeben!"
# hier wird bei {} der eingegebene Text eingefügt
error_slur_found = "{} enthält eine Beleidigung!"
error_dj_unavailable = "Der DJ nimmt momentan keine neuen Musikwünsche an. Bitte versuche es später erneut."
error_network = "Anfrage konnte nicht gesendet werden! Bitte wende dich an einen Admin"
error_no_connection_to_server = "Server unerreichbar! Bitte kontaktieren Sie einen Administrator"

classics_artist_description = "Interpret"
classics_song_description = "Musik Titel"

# Hier kann eine liste von Texten angegeben werden, welche beim Laden nacheinander angezeigt werden.
loading_description = ["Suche CD heraus ...", "Lege CD ein ...", "Packe deinen Song in die Warteschlange ..."]
loading_success = "Musikwunsch erfolgreich versendet!"


[[languages]]
# Name der Sprache für interne Identifikation
language_name = "english"
# Bild der Sprache relativ zu ~/disco_express
language_icon = "icons/gb.svg"

heading_music_wish = "Enter a music wish. You can also direct this wish to someone!"
heading_home = "Welcome to the Disco Express, make a music wish or retrieve some infotmation about us!"
heading_information = "Choose a document to learn more."

home_info_btn = "Information"
home_music_wish_btn = "Music Wish"

music_title = "Music Title"
music_interpret = "Artist"
music_sender = "From"
music_receiver = "For"
music_message = "Message"

btn_quick_selection = "Quick Selection"
btn_send = "Send Request"

error_no_title = "No Title entered!"
error_no_interpret = "No Interpret entered!"
# hier wird bei {} der eingegebene Text eingefügt
error_slur_found = "{} contains a slur!"
error_dj_unavailable = "The DJ does currently not accept wishes. Please try later again."
error_network = "Request could not be sent! Please refer to an Admin"
error_no_connection_to_server = "Server unavailable! Please contact an Admin"

classics_artist_description = "Artist"
classics_song_description = "Music Title"

# Hier kann eine liste von Texten angegeben werden, welche beim Laden nacheinander angezeigt werden.
loading_description = ["Finding Disc ...", "Inserting Disc ...", "Putting song in queue ..."]
loading_success = "Your music wish was sent sucessfully!"
```

## UI

Das Programm beinhaltete eine Home Seite, wo zwischen "Musikwunsch" und "Information"
gewählt werden kann. 

### Musikwunsch
Hier kann ein User einen Musikwunsch eingeben. Dabei sind Titel und Interpret Pflichteingaben.
Alle Felder werden nach Beleidigungen überprüft. Die Beleidigungen können in der Datei 
"slurs_file" aus der Config eingesehen und editiert werden.

Es gibt auch die Möglichkeit eine Schnellauswahl zu treffen, durch den Knopf "Schnellauswal".
Dort gibt es Classics ("classics_file"), meistgewünschte Charts ("charts_file") und aktuelle
Charts/Radio ("current_charts").

Der Musikwunsch wird sofort gesendet, beim Betätigen des entsprechenden Knopfes.
Allerdings wird, um Spameingaben zu vermeiden, ein Ladebalken von 10 Sekunden (Config -> wish_sending_time) angezeigt.
Danach wird man automatisch wieder auf die Home Seite weitergeleitet.

### Information
Der Server stellt Informationsdateien zur Verfügung, welche Disco Express herunterladen kann.
Diese werden dann pro Datei aufgelistet in der Informationsansicht. Unterstützte Formate
sind dabei PDFs und Bilddateien.


## Entwickler Hinweise
Das Programm wurde mittels Python 3.11.6 entwickelt. Für das Dependeny Management wird poetry verwendet:

```pip install poetry```

Sobald poetry installiert ist, können die Abhängigkeiten installiert werden:

```poetry install```

Die App kann als ausfürbare Datei gebaut werden mittels. Die erstellte App befindet sich
dann im "dist" ordner.

```poetry run poe build```


Diese Datei kann als PDF generiert werden durch:

```poetry run poe docs```

# Pflichtangaben
Icons von [Fontawesome](https://fontawesome.com/)

App Icon von [Flaticon](https://www.flaticon.com/free-icon/jukebox_1026050?term=jukebox&page=1&position=1&origin=tag&related_id=1026050)


