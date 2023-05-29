# Dati Esperimenti
- La cartella _proactive_ contiene i dati ottenuti dallo studio con il **sistema di decisione proattivo**.
- La cartella _random_ contiene i dati ottenuti dallo studio con il **sistema di decisione randomico**.
- Il file _back_end_.py permette di generare il file Excel per l'analisi dei dati:
  - Da installare: 
    - pip install statistics, pandas, pathlib
  - Per eseguire:
    - python back_end.py
- Il file _data_.xlsx contiene:
  - Foglio _Generic_, il quale contiene per ogni partecipante le sequenti colonne:
    - ID: 0 se **sistema di decisione randomico**, 1 	**sistema di decisione Proattivo**
    - Age, Gender, Education: ottenuti dal questionario demografico
    - Conqueror, Manager, Wanderer, Participant: ottenuti dal questionario _DGD_
    - Level, Score, #Mistakes: livello max raggiunto, punteggio ottenuto e numero di errori compiuti
    - #AssistanceTot: numero di assistenza richiesta/ottenuta
    - #AssistanceRequested: numero di assistenze richiesta dal partecipante
    - #AssistanceFromRobot: numero di assistenza ottenuta dal partecipante per intervento del robot
      - Liked, Unliked: numero di gradimento e non gradimento dell'assistenza ricevuta dal robot
    - RB, HLP, TRU, RC, AC, PC, SOC: ottenuti dal questionario _PSI_
    - ServiceProactivity: ottenuto dal questionario _Robotic Service Proactivity_
  - Foglio _Mean_, il quale contiene per ogni condizione sperimentale le sequenti colonne:
    - ID: 0 se **sistema di decisione randomico**, 1 	**sistema di decisione Proattivo**
    - Frequency: numero di partecipanti per quella condizione
    - #Male, #Female: genere dei partecipanti per quella condizione
    - Age, Level, Score, #Mistakes, #AssistanceTot, #AssistanceRequested, #AssistanceFromRobot, Liked, Unliked, RB, HLP, TRU, RC, AC, PC, SOC, ServiceProactivity: valori medi per quella condizione
 
 
