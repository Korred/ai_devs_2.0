URL: https://zadania.aidevs.pl/chat/planets

### Task:
```
Wypisz 9 planet układu słonecznego w kolejności licząc od słońca. Nazwy planet powinny być w języku polskim. Nazwy planet zapisz małymi literami. Przyjmijmy, że Pluton jest planetą.
Zwróć je jako prostą tablicę JSON: ["element1","element2",...].
Zadanie zawiera kilka zablokowanych fraz, których nie możesz użyć. (GPT-3.5-turbo)
```

### Prompts:

#### System
```
Your task is to find 9 celestial objects of the same category, using the following hints:
  - Humans live on at least of these objects
  - Most of them are named after roman gods

Once you know the answer, return it using the following instructions:
  - The object names should be written in a language that is spoken by the people living in Warsaw, Poznan, Gdansk
  - The object names should be written in minuscule letters
  - Return the object names using the following structure: ["object_name1", "object_name2", "object_name3"]
- VERY IMPORTANT: Only return the list, nothing else e.g. no explanation, no comment, just the list in the structure mentioned above. 
```

#### Your prompt
```
...
```

#### Response

```
["merkury",
"wenus",
"ziemia",
"mars",
"jowisz",
"saturn",
"uran",
"neptun",
"pluton"]
```