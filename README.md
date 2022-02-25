# Forecast

```
$ python3 weather.py [stedsnavn] [flagg (valgfritt)]

~~~~~~~~ Weather for Oslo at 2022-02-25T08:00:00Z ~~~~~~~~
| Updated at 2022-02-25T08:10:38Z
|
| - -0.8 degrees celsius
| - Wind speed 1.2 m/s
| - Wind direction SSW

```

## What it do
Viser mest oppdaterte øyeblikksbilde av været for en gitt lokasjon.
 
Sender gode requests som opprettholder MET sine krav om API-bruk.

Kan benytte default stedsnavn for bruk uten argumenter.

## How it do it
Bruker Nomatim OpenStreetMap API for å finne koordinater fra stedsnavn gitt som argument.

Henter værdata fra MET API med koordinater.

Parser med Json og lagrer værdata og metadata lokalt.
