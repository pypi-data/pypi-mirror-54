python-kuorma
=============

Käyttö:
------

Tuotantokoodi:
```python
# projekti/tuotanto.py

from kuorma import toteutus
...
class Tuotantoluokka:
  ...
  @toteutus
  def vakiometodi(self, a, b, c):
    return a + b + c
  ...
  def muodosta_aineistot(self):
    return [
      self.vakiometodi(1, 2, 3),
      self.vakiometodi(4, 5, 6),
    ]
  ...
```

Asiakaskohtainen tms. ylikuormitussovellus:
```python
# asiakas/ylikuormitus.py

from kuorma import toteutus

@toteutus('projekti.tuotanto:Tuotantoluokka.vakiometodi')
def mukautettu_metodi(self, *args):
  return mukautettu_metodi.oletus(*args[:3]) * sum(args[3:])
```

Käyttöliittymän muodostus:
```python
# sovellus/kayttoliittyma.py

from projekti.tuotanto import Tuotantoluokka

class Nakyma:
  ...
  def ajossa_olevat_ylikuormitukset(self):
    return Tuotantoluokka.vakiometodi.toteutukset()
```

Lisätietoja, ks. `kuorma/testit.py`.
