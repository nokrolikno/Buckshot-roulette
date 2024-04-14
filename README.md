# Buckshot-roulette

This project implements the Buckhot Roulette game engine in python

In engine/engine.py the engine itself and the abstract class ```Player Abstract``` are located.
It is necessary to inherit from ```PlayerAbstract``` and implement the method of the class ```make_move```.
Then you can use the engine as in the example in ```main.py ```.

Original game: https://mikeklubnika.itch.io/buckshot-roulette

Now on steam: https://store.steampowered.com/app/2835570/Buckshot_Roulette/
<p>
<3

For those who wants to support project, there are some help with development:
<p>
Project runs on python > 3.10

```commandline
pip install -r requirements.txt
```
Before push
```commandline
ruff check .
```
Also you can run to format code by using
```commandline
black .
ruff format .
```
