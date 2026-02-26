Idee: Alle Banks in eine Klasse Bank
- Alles was geladen werden muss wird in einer Datei oder so definiert
- Durch diese durch iterieren um alle zu laden 
- Dann vllt static

Bei dieser Idee müsste man also globale Parameter und instanzparam beachten
ich bräuchte damit eine Liste der zuordnung welcher Parameter zu welcher Instanz
gehört bzw. ob er global ist.
Wenn die funktion set param(name, value) aufgerufen wird, muss erstens sicher sein,
dass es keine zwei parameter mit dem gleichen namen gibt, das wäre SEHR problematisch
der name müsste dann mit der liste abgeglichen werden und je nach parametername würde dann
entweder studio_system.set_parameter_by_name oder event_instance.set...

Aus den Bank dateien könnten die entsprechenden Parameter rausgelesen werden und überprüft
werden ob sie global oder zum event gehören.

Diese Idee würde den Vorteil bringen, dass die Bank Klasse praktisch nicht mehr
"gepflegt" werden müsste, sondern alles automatisiert abläuft, durch skripte, die man bspw.
in der main aufgerufen werden.
Die Bank klasse könnte eine Methode haben wie "set_banks" und "receive_param" um alles nötige
zu erhalten.

Erstmal mit verschiedenen Bank klassen probieren und dann mal refactorn und schauen

Es könnte interessant sein, folgende Werte zu publishen
| Event                     | Wert                 | Beschreibung                                                             |
| ------------------------- | -------------------- | ------------------------------------------------------------------------ |
| `event_started`           | Event-Name oder ID   | Signalisiert, dass ein Sound-Event gestartet wurde                       |
| `event_stopped`           | Event-Name oder ID   | Signalisiert, dass ein Event gestoppt wurde                              |
| `event_error`             | Fehlermeldung        | Wenn FMOD einen Fehler wirft                                             |
| `event_parameter_changed` | Parametername + Wert | Falls du dynamische Parameter im Event setzt                             |
| `bank_loaded`             | Bankname             | Optional, falls Monitoring benötigt                                      |
| `studio_updated`          | Timestamp / Counter  | Optional, falls Subscriber wissen wollen, dass Studio aktualisiert wurde |