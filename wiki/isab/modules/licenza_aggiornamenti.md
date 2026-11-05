# Licenza, avvio, aggiornamenti

## Avvio

`src/app_launcher.py` è l’entrypoint. In sviluppo la root è la cartella `src/`. In un bundle PyInstaller la root è `_MEIPASS`.

Ordine utile all’agente:

1. `app_logger` prima degli altri import applicativi, così un crash precoce finisce su file.
2. Controllo licenza locale (`license_validator.get_license_info`).
3. GUI principale, oppure utility ROI se l’avvio lo chiede.

`src/main.py` non va lanciato al posto del launcher se serve il controllo licenza iniziale. I test di finestra importano `MainApp` direttamente.

## Licenza

`license_validator.py` legge il file in `Licenza/`, deriva una chiave Fernet e confronta il payload con l’HWID della macchina (seriale disco, normalizzato). `AppController.check_license` pubblica verso la view: validità, cliente, scadenza, HWID, ultimo accesso.

`license_updater.py` è il controllo remoto. `app_launcher.run_app` lo esegue all’avvio, prima della GUI. `AppController.check_license` aggiorna il footer. `start_processing` non ricontrolla la licenza.

La lettura dell’HWID passa da PowerShell con `CREATE_NO_WINDOW` e finestra `SW_HIDE`: la query non apre una console.

Non copiare salt, iterazioni, payload o HWID nella wiki. Il sorgente è la fonte di quei parametri. I test usano fixture locali, non la licenza della macchina.

## Aggiornamenti applicazione

`app_updater.py` confronta la versione in `src/version.py` con il canale web (`version.UPDATE_URL`) e con il canale di rete (`version.NETWORK_UPDATE_PATH`). Privilegia la LAN quando entrambe hanno un setup. L’installer scelto può restare in `_pending_installer_path` ed essere eseguito alla chiusura.

Non riscrivere path UNC o IP nei documenti: citare i simboli.

## Log

`app_logger.py` configura il logging su file all’import. I nomi logger usati nel codice includono `MAIN`, `CONTROLLER`, `Intelleo`.
