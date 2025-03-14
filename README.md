# Texas Hold'em AI
## 1 Players
+ defaut player: randomly choose action [raise,call,fold].   
+ never fold player: randomly choose action from [raise,call]. 
+ rule based player: decide based on situation.   

## 2 How to change players
In main.py,evaluate method,define two players like this:
+ Bob = Player(name='Bob', chips=1000)
+ Bob = NeverFold(name='Bob', chips=1000)
+ Alice = RuleBased(name='Alice', chips=1000)

## 3 How to evaluate 
In main.py, there are two ways to evaluate the players:
+ oneRound: The two players play only one round of the game, and the player with the higher chips at the end wins.
+ fight_to_the_last_chip: The two players start with a certain amount of initial chips and play multiple rounds until one player runs out of chips, ending the game.   

To change the evaluation method, update the code in main.py, evaluate method,choose one:  
```
name2cnt[fight_to_the_last_chip([Alice,Bob])] += 1  
name2cnt[oneRound([Alice,Bob])] += 1  
```
Warning: for oneRound, it is ok to set round as 10000; for fight_to_the_last_chip, 100 round is enough.
