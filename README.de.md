# Goethe Programmiersprache

[toc]

## Anforderungen

- Python  3.8+
## Sprachspezifikation

Die Goethe Programmiersprache baut auf den Silben der jeweiligen Verse eines Gedichtes auf. Je nach Anzahl der Silben wird ein entsprechender Befehl ausgeführt. Eine Liste der verfügbaren Befehle findet sich in der unten stehenden Tabelle.

### Silben pro Vers

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

___

### Stilmittel

Neben der Silbenanzahl ist es auch möglich, mit bestimmten Stilmitteln Aktionen ausführen.

#### Anapher

Eine Anapher ist die Wiederholung eines Wortes oder einer Wortgruppe zu Beginn aufeinanderfolgender Verse.

##### Effekt

Die Anzahl der Silben zweier <u>aufeinanderfolgender</u> Verse mit Anaphern wird addiert.

> _**Wer** nie sein Brot mit Tränen aß,_ <small>(8 Silben)</small><br>
> _**Wer** nie die kummervollen Nächte_ <small>(9 Silben)</small><br>_Auf seinem Bette weinend saß.“_ <small>(8 Silben)</small>

<sub>(Johann Wolfgang von Goethe: Wer nie sein Brot mit Tränen aß...)</sub>



Das obige Beispiel führt zu folgenden Zahlenfolge: `[17, 8]`.

#### Epiphora / Epipher 

Die Epiphora bezeichnet die Wiederholung eines Wortes oder einer Wortgruppe am Ende aufeinanderfolgender Verse.

##### Effekt

Die Anzahl der Silben zweier <u>aufeinanderfolgender</u> Verse mit Epiphora wird subtrahiert.

> _Sturm und Meeresgefährde trifft **nie**_ <small>(9 Silben)</small><br>
> _Dich den Klugen, der geschifft **nie**;_ <small>(8 Silben)</small><br>
> _Wer in Furcht sogar den Wein scheut,_ <small>(8 Silben)</small><br>_trinkt das eingemischte Gift nie._ <small>(8 Silben)</small>

<sub>(August von Platen)</sub>

