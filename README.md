# Goethe Programmiersprache

Die Goethe Programmiersprache ist eine dynamische Programmiersprache, so entworfen, dass Programme in Gedichtform geschrieben werden können.

### Wozu das ganze?

In der heutigen Welt der Programmiersprachen sehen fast alle Programme gleich aus. Dem Code
fehlt es an eigenem Charakter und Charme. Die Individualität eines einzelnen Programmierers
lässt sich nicht in den niedergeschriebenen Zeilen wiederfinden.

Dabei ist Programmieren doch ein höchst kreativer Prozess. Man könnte fast sagen, Programmieren ist wie das Schreiben eines Gedichtes. Mit jeder Zeile Code wächst des Programmierers Komposition um einen weiteren Vers.

Die Goethe Programmiersprache löst das geschilderte Problem: Sie befreit den Entwickler von den ihm auferlegten lyrischen Fesseln.



___



## 1. Installation

Zur Installation wird Python 3.8+ benötigt.

```bash
git clone git@github.com:mxschll/goethe.git
cd goethe
python3 setup.py install
```

Unter Umständen muss unter Linux `sudo` zur Installation verwendet werden.



## 2. Benutzung

```bash
goethe [-h] (-i INPUT | -e)
```

Mit `goethe -h` werden alle verfügbaren Optionen aufgelistet:

```bash
usage: goethe [-h] (-i INPUT | -e)

Python interpreter for the Goethe programming language.

optional arguments:
  -h, --help            	show this help message and exit
  -i INPUT, --input INPUT	Input file (.goethe)
  -e, --editor          	Open the editor
```

Im folgenden Beispiel wird ein Goethe Programm in der Konsole ausgeführt:

```bash
> goethe -i examples/hello.goethe 
Hello World!
```



## 3. Sprachspezifikation

Die Goethe Programmiersprache baut auf den Silben der jeweiligen Verse eines Gedichtes auf. Je nach Anzahl der Silben wird ein entsprechender Befehl ausgeführt. Eine Liste der verfügbaren Befehle findet sich in der unten stehenden Tabelle.

### 3.1 Silben pro Vers

In jedem Vers werden die Silben gezählt und in einen entsprechenden Befehl umgewandelt:

| Silben | Befehl   | Beschreibung                                                 |
| ------ | -------- | ------------------------------------------------------------ |
| 0      | `PASS`   | Führe keine Aktion aus.                                      |
| 1      | `LOOP`   | Springe zum entsprechenden `POOL`, wenn der aktuelle Speicherwert 0 ist. |
| 2      | `POOL`   | Springe zum entsprechenden `LOOP`, wenn der aktuelle Speicherwert != 0 ist. |
| 3      | `INCVAL` | Erhöhe den aktuellen Speicherwert um 1.                      |
| 4      | `DECVAL` | Verringere den aktuellen Speicherwert um 1.                  |
| 5      | `INCPTR` | Erhöhe den Programmzeiger um 1.                              |
| 6      | `DECPTR` | Verringere den Programmzeiger um 1.                          |
| 7      | `OUT`    | Gib den aktuellen Speicherwert als ASCII aus.                |
| 8      | `IN`     | Lese die Benutzereingabe zeichenweise und schreibe sie in den Speicher. |
| 9      | `RND`    | Schreibe eine Zufallszahl zwischen 0 und 255 in den Speicher. |

Die Anzahl der Silben `n` wird immer `n mod 10` genommen. Hat ein Vers beispielsweise 13 Silben, so wird dieser wie folgt umgewandelt: `13 mod 10 = 3 -> INCVAL`.



### 3.2 Stilmittel

Neben der Silbenanzahl ist es auch möglich, mit bestimmten Stilmitteln Aktionen ausführen.

#### 3.2.1 Anapher

Eine Anapher ist die Wiederholung eines Wortes oder einer Wortgruppe zu Beginn aufeinanderfolgender Verse.

##### Effekt

Die Anzahl der Silben zweier <u>aufeinanderfolgender</u> Verse mit Anaphern wird addiert.

> _**Wer** nie sein Brot mit Tränen aß,_ <small>(8 Silben)</small><br>
> _**Wer** nie die kummervollen Nächte_ <small>(9 Silben)</small><br>_Auf seinem Bette weinend saß.“_ <small>(8 Silben)</small>

<sub>(Johann Wolfgang von Goethe: Wer nie sein Brot mit Tränen aß...)</sub>



Das obige Beispiel führt zu folgenden Zahlenfolge: `[17, 8]`.

#### 3.2.2 Epiphora / Epipher 

Die Epiphora bezeichnet die Wiederholung eines Wortes oder einer Wortgruppe am Ende aufeinanderfolgender Verse.

##### Effekt

Die Anzahl der Silben zweier <u>aufeinanderfolgender</u> Verse mit Epiphora wird subtrahiert.

> _Sturm und Meeresgefährde trifft **nie**_ <small>(9 Silben)</small><br>
> _Dich den Klugen, der geschifft **nie**;_ <small>(8 Silben)</small><br>
> _Wer in Furcht sogar den Wein scheut,_ <small>(8 Silben)</small><br>_trinkt das eingemischte Gift nie._ <small>(8 Silben)</small>

<sub>(August von Platen)</sub>



Das obige Beispiel führt zu folgender Zahlenfolge: `[1, 8, 8]`.

#### 3.2.3 Alliteration

Die Alliteration bezeichnet die Verwendung von Wörtern mit gleichen Anfangsbuchstaben kurz hintereinander in einem Satz.

Eine Alliteration wird erkannt, wenn mehr als 60% der verwendeten Wörter mit demselben Anfangsbuchstaben anfangen und ein Vers aus mehr als 3 Wörtern besteht.

##### Effekt

Ein Vers mit Alliteration wird als 7 gezählt. Die Silben des Verses werden nicht beachtet.

> _**W**ir **w**anken in **w**ohnsamer **W**iege,_ <small>(9 Silben)</small><br>
> _Wind weht wohl ein Federlein los,_ <small>(8 Silben, nicht als Alliteration erkannt, da W < 60%)</small><br>
> _**W**ie's **w**ehe, **w**ie's fliege, **w**ie's liege,_ <small>(9 Silben)</small><br>
> _Fein fiel es und spielt es dem Vater im Schoß._ <small>(11 Silben)</small>

<sub>(Clemens Brentano: Rheinmärchen)</sub>



Das obige Beispiel führt zu folgender Zahlenfolge: `[7, 8, 7, 1]`.

#### 3.2.4 Assonanz

Die Assonanz bezeichnet den sich auf die Vokale beschränkenden Gleichklang zwischen mehreren Wörtern.

##### Effekt

Ein Vers mit Assonanz wird als 9 gezählt. Die Silben des Verses werden nicht beachtet.

> _Die M**e**nschen g**e**ben und n**e**hmen **e**ben,_ <small>(10 Silben)</small><br>
> _So ist nun mal das Leben._ <small>(7 Silben)</small>



Das obige Beispiel führt zu folgender Zahlenfolge: `[9, 7]`.
