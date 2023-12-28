URL: https://zadania.aidevs.pl/chat/format

### Task:
```
Napisz parser nowego języka formatowania tekstu podanego przez użytkownika. Język ten składa się ze znaczników zapisywanych jako !slowo! i bazuje na dziwnych wyrażeniach jednego z afrykańskich plemion. Twój prompt powinien zamienić go na kod HTML (GPT-3.5-turbo)
```

### Prompts:

#### System
```
Translate the provided code into valid HTML code. The provided code will contain strange tags that should be replaced by their HTML counterparts.

The rules are:
1. Replace the !tumba! pair with a paragraph
2. Replace the !zabzila! pair with a bold tag
3. Replace a list of !kurak! elements with
a html list with bulletpoints
```

#### Your prompt
```
!tumba!to jest !zabzila!pogrubiony napis!zabzila! w środku paragrafu!tumba!

!kukak! punkt pierwszy
!kukak! punkt drugi
!kukak! punkt trzeci
```

#### Response

```
<p>To jest <b>pogrubiony napis</b> w środku paragrafu</p>

<ul>
<li>punkt pierwszy</li>
<li>punkt drugi</li>
<li>punkt trzeci</li>
</ul>

<p><img src="fotka_lwa.jpg"></p>

<h1>Nagłówek pierwszego stopnia</h1>
<p>To jest paragraf. Może być <b>długi</b>, może być krótki... ten język ogarnia wszystko</p>x`x`
```