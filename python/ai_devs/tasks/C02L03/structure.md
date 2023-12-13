URL: https://zadania.aidevs.pl/chat/structure

### Task:
```
Piszesz klasyfikator problemów użytkownika w dziale pomocy technicznej. Zwróć JSON z kategorią problemu (dostępne kategorie to: pralka/telewizor/zmywarka), nazwę producenta oraz akcję której wymaga klient (zwrot/naprawa). Oczekiwana struktura odpowiedzi zależy od modelu.
Dla GPT-3.5-turbo:
{"kategoria":"pralka","producent":"Whirpool","akcja":"zwrot"}.
Dla GPT-4:
{"kategoria":"pralka","producent":"Whirpool","akcja":"zwrot","data":"20231213"}
UWAGA: Twój prompt wykonuje się jednocześnie na GPT-3.5-turbo i GPT-4!
```

### Prompts:

#### System
```
Your task is to classify/analyze user messages sent to the technical support departement and return them in a valid JSON format that looks like this:
{"kategoria":"pralka","producent":"Whirpool","akcja":"zwrot"}.

For the "kategoria" prop you have the following values to select from: pralka / telewizor / zmywarka

The "producent" stores the product producer

The "akcja" prop stores the request of the user e.g. either a return "zwrot" or a repair "naprawa".


Today is 20231212
Finally add todays date + 1
```

#### Your prompt
```
Dzień dobry zespole wsparcia technicznego!

Kolejny raz zepsuł mi się odbiornik telewizyjny. Tak, to ten sam stary Samsung który ostatnio naprawialiście. Próbowałem włączyć i wyłaczyć go i to nawet trzy razy, ale nadal nie działa. Co robić? jak żyć?! Naprawicie to?
```