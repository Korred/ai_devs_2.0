URL: https://zadania.aidevs.pl/chat/fixit

### Task:
```
Spraw, aby ChatGPT poprawił poniższy kod tak, aby poprawnie zwracał zadaną liczbę ciągu Fibonnacciego. Kod jest napisany w PHP 8.1. Limit czasu wykonania funkcji to 2 sekundy. W przypadku jakichkolwiek błędów, zwracaną wartością z funkcji powinno być zero. Weź pod uwagę, że wyliczanie elementów ciągu Fibbonaciego jest BARDZO zasobożerne pod względem pamięci. Może warto pomyśleć o jakimś usprawnieniu? (GPT-4)
```

### Prompts:

#### System
```
Masz dany poniższy kod. Wszystkie moje polecenia dotyczą właśnie jego. W odpowiedziach zwracaj tylko gotowy kod bez żadnych wyjaśnień i komentarzy.

###

function fib($n) {
    if ($n > 2) return $n
    return fib($n-1) + fib($n-2)
}
```

#### Your prompt
```
Rewrite the Fibonacci function (fib) so that:
- it uses an iterative approach instead of a recursive one
- it has some error handling if the provided variable is invalid e.g. not a number, a negative number, a float, etc.; in that case return 0
```

#### Reply
```
function fib($n) {
    if (!is_int($n) || $n < 0 ) {
        return 0;
    }
    $fib = [0, 1];
    for($i = 2; $i <= $n; $i++){
        $fib[$i] = $fib[$i-1] + $fib[$i-2];
    }
    return $fib[$n];
}

Test01 (małe liczby) = OK
Test02 (liczby ujemne) = OK
Test03 (tekst jako input) = OK
Test04 (duża liczba) = OK
```