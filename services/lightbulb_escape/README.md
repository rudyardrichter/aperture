```
$ poetry run python -i src/lightbulb_escape/models.py
>>> FlatWithCounter(31).simulate_n_runs(1000)
(953.661, 167.92510258743332)
>>> KTree(31, 5, 20).simulate_n_runs(1000)
(568.82, 217.52927986825128)
>>> FlatWithCounter(91).simulate_n_runs(100)
(8289.79, 971.9051115721122)
>>> KTree(91, 9, 40).simulate_n_runs(1000)
(2533.567, 790.0014376638817)
```
