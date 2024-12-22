"""CS 61A Presents The Game of Hog."""

from dice import six_sided, four_sided, make_test_dice
from ucb import main, trace, interact

## 从.py文件中导入自定义模块

GOAL_SCORE = 100  # The goal of Hog is to score 100 points.
FIRST_101_DIGITS_OF_PI = 31415926535897932384626433832795028841971693993751058209749445923078164062862089986280348253421170679

######################
# Phase 1: Simulator #
######################


def roll_dice(num_rolls, dice=six_sided):
    """
    Simulate rolling the DICE exactly NUM_ROLLS > 0 times. Return the sum of
    the outcomes unless any of the outcomes is 1. In that case, return 1.

    num_rolls:  The number of dice rolls that will be made.
    dice:       A function that simulates a single dice roll outcome.
    """
    
    # These assert statements ensure that num_rolls is a positive integer.
    assert type(num_rolls) == int, 'num_rolls must be an integer.'
    assert num_rolls > 0, 'Must roll at least once.'
    # BEGIN PROBLEM 1
    "*** YOUR CODE HERE ***"
    n= 0
    total=0
    flag=False
    
    while n < num_rolls:
        number = dice() # 投num_rolls次
        total += number # 累加
        n += 1
        if number == 1: # 等于1时做标记
            flag = True
    if flag == True:
        return 1
    return total
    # END PROBLEM 1


def free_bacon(score):
    """
    Return the points scored from rolling 0 dice (Free Bacon).
    score:  The opponent's current score.
    """
    
    assert score < 100, 'The game should be over.'
    pi = FIRST_101_DIGITS_OF_PI
    # pi共101位

    # Trim pi to only (score + 1) digit(s)
    # BEGIN PROBLEM 2
    "*** YOUR CODE HERE ***"
    if(score==0):
        return 6
    digit= pow(10, 100 -score)
    tmp= pi//digit
    # 除去pi从右至左的(100-score)个数, 结果的最后一个数就是Π的小数点后n位
    return tmp%10 + 3
    # END PROBLEM 2
    


def take_turn(num_rolls, opponent_score, dice=six_sided):
    """
    Simulate a turn rolling NUM_ROLLS dice, which may be 0 (Free Bacon).
    Return the points scored for the turn by the current player.
    
    num_rolls:       The number of dice rolls that will be made.
    opponent_score:  The total score of the opponent.
    dice:            A function that simulates a single dice roll outcome.
    """
    
    # Leave these assert statements here; they help check for errors.
    assert type(num_rolls) == int, 'num_rolls must be an integer.'
    assert num_rolls >= 0, 'Cannot roll a negative number of dice in take_turn.'
    assert num_rolls <= 10, 'Cannot roll more than 10 dice.'
    assert opponent_score < 100, 'The game should be over.'
    
    # BEGIN PROBLEM 3
    "*** YOUR CODE HERE ***"
    if num_rolls==0:    # 次数等于0时， free_bacon
        return free_bacon(opponent_score)
    return roll_dice(num_rolls, dice)   # 次数不等于0时一切照旧
    # END PROBLEM 3


def extra_turn(player_score, opponent_score):
    """Return whether the player gets an extra turn."""
    return (pig_pass(player_score, opponent_score) or
            swine_align(player_score, opponent_score))

def swine_align(player_score, opponent_score):
    """
    Return whether the player gets an extra turn due to Swine Align.

    player_score:   The total score of the current player.
    opponent_score: The total score of the other player.

    >>> swine_align(30, 45)  # The GCD is 15.
    True
    >>> swine_align(35, 45)  # The GCD is 5.
    False
    """
    
    # BEGIN PROBLEM 4a
    "*** YOUR CODE HERE ***"
    if min(player_score, opponent_score)<=0:
        return False
    # 两个人的分数不同时为正, 结果为False
    
    a= player_score
    b= opponent_score
    
    # 祖传noj上的gcd算法
    while b!=0:
        tmp= b
        b= a%b
        a= tmp
    
    if a>=10:
        return True
    return False
    # END PROBLEM 4a


def pig_pass(player_score, opponent_score):
    """
    Return whether the player gets an extra turn due to Pig Pass.

    player_score:   The total score of the current player.
    opponent_score: The total score of the other player.

    >>> pig_pass(9, 12)
    False
    >>> pig_pass(10, 12)
    True
    >>> pig_pass(11, 12)
    True
    >>> pig_pass(12, 12)
    False
    >>> pig_pass(13, 12)
    False
    """
    # BEGIN PROBLEM 4b
    "*** YOUR CODE HERE ***"
    if player_score >= opponent_score:
        return False
    if opponent_score-player_score<3:
        return True
    return False
    # END PROBLEM 4b


def other(who):
    """Return the other player, for a player WHO numbered 0 or 1.

    >>> other(0)
    1
    >>> other(1)
    0
    """
    return 1 - who


def silence(score0, score1):
    """Announce nothing (see Phase 2)."""
    return silence


def play(strategy0, strategy1, score0=0, score1=0, dice=six_sided,
         goal=GOAL_SCORE, say=silence):
    """
    Simulate a game and return the final scores of both players, with Player
    0's score first, and Player 1's score second.

    A strategy is a function that takes two total scores as arguments (the
    current player's score, and the opponent's score), and returns a number of
    dice that the current player will roll this turn.

    strategy0:  The strategy function for Player 0, who plays first.
    strategy1:  The strategy function for Player 1, who plays second.
    score0:     Starting score for Player 0
    score1:     Starting score for Player 1
    dice:       A function of zero arguments that simulates a dice roll.
    goal:       The game ends and someone wins when this score is reached.
    say:        The commentary function to call at the end of the first turn.
    """
    who = 0  # Who is about to take a turn, 0 (first) or 1 (second)
    # BEGIN PROBLEM 5
    "*** YOUR CODE HERE ***"
        # 一直循环直到有人的score>=goal
        # 分为who==0和who==1两种情况讨论
    while True:
        if who == 0:
            num_rolls = strategy0(score0, score1)
            score0 += take_turn(num_rolls, score1, dice)    # 累加
            say = say(score0, score1)
            if score0 >= goal or score1 >= goal:        # 判断是否该结束
                break
            if not extra_turn(score0, score1):          # 判断特殊情况
                who = other(who)
        if who == 1:
            num_rolls = strategy1(score1, score0)
            score1 += take_turn(num_rolls, score0, dice)
            say = say(score0, score1)
            if score0 >= goal or score1 >= goal:
                break
            if not extra_turn(score1, score0):
                who = other(who)
    # END PROBLEM 5
    # (note that the indentation for the problem 6 prompt (***YOUR CODE HERE***) might be misleading)
    # BEGIN PROBLEM 6
    "*** YOUR CODE HERE ***"
    # END PROBLEM 6
    return score0, score1


#######################
# Phase 2: Commentary #
#######################


def say_scores(score0, score1):
    """A commentary function that announces the score for each player."""
    print("Player 0 now has", score0, "and Player 1 now has", score1)
    return say_scores


def announce_lead_changes(last_leader=None):
    """Return a commentary function that announces lead changes.

    >>> f0 = announce_lead_changes()
    >>> f1 = f0(5, 0)
    Player 0 takes the lead by 5
    >>> f2 = f1(5, 12)
    Player 1 takes the lead by 7
    >>> f3 = f2(8, 12)
    >>> f4 = f3(8, 13)
    >>> f5 = f4(15, 13)
    Player 0 takes the lead by 2
    """
    def say(score0, score1):
        if score0 > score1:
            leader = 0
        elif score1 > score0:
            leader = 1
        else:
            leader = None
        if leader != None and leader != last_leader:
            print('Player', leader, 'takes the lead by', abs(score0 - score1))
        return announce_lead_changes(leader)
    return say


def both(f, g):
    """Return a commentary function that says what f says, then what g says.

    NOTE: the following game is not possible under the rules, it's just
    an example for the sake of the doctest

    >>> h0 = both(say_scores, announce_lead_changes())
    >>> h1 = h0(10, 0)
    Player 0 now has 10 and Player 1 now has 0
    Player 0 takes the lead by 10
    >>> h2 = h1(10, 8)
    Player 0 now has 10 and Player 1 now has 8
    >>> h3 = h2(10, 17)
    Player 0 now has 10 and Player 1 now has 17
    Player 1 takes the lead by 7
    """
    def say(score0, score1):
        return both(f(score0, score1), g(score0, score1))
    return say


def announce_highest(who, last_score=0, running_high=0):
    """
    Return a commentary function that announces when WHO's score
    increases by more than ever before in the game.

    NOTE: the following game is not possible under the rules, it's just
    an example for the sake of the doctest

    >>> f0 = announce_highest(1) # Only announce Player 1 score gains
    >>> f1 = f0(12, 0)
    >>> f2 = f1(12, 9)
    9 point(s)! The most yet for Player 1
    >>> f3 = f2(20, 9)
    >>> f4 = f3(20, 30)
    21 point(s)! The most yet for Player 1
    >>> f5 = f4(20, 47) # Player 1 gets 17 points; not enough for a new high
    >>> f6 = f5(21, 47)
    >>> f7 = f6(21, 77)
    30 point(s)! The most yet for Player 1
    """
    assert who == 0 or who == 1, 'The who argument should indicate a player.'
    # BEGIN PROBLEM 7
    "*** YOUR CODE HERE ***"
    def announce(score0, score1, last_score=last_score, running_high=running_high):
        if who ==0:     # 玩家0
            if score0-last_score>running_high:  # 迎来骰子上涨最高峰
                print("{0} point(s)! The most yet for Player {1}".format(score0-last_score, who))
                running_high=score0-last_score  # 更新迭代
                 # 更新迭代
            return announce_highest(who, last_score=score0, running_high=running_high)
        
        if who ==1:
            if score1-last_score>running_high:
                print("{0} point(s)! The most yet for Player {1}".format(score1-last_score, who))
                running_high=score1-last_score
            return announce_highest(who, last_score=score1, running_high=running_high)
    return announce
    # END PROBLEM 7


#######################
# Phase 3: Strategies #
#######################


def always_roll(n):
    """Return a strategy that always rolls N dice.

    A strategy is a function that takes two total scores as arguments (the
    current player's score, and the opponent's score), and returns a number of
    dice that the current player will roll this turn.

    >>> strategy = always_roll(5)
    >>> strategy(0, 0)
    5
    >>> strategy(99, 99)
    5
    """
    def strategy(score, opponent_score):
        return n
    return strategy


def make_averaged(original_function, trials_count=1000):
    """
    Return a function that returns the average value of ORIGINAL_FUNCTION
    when called.

    To implement this function, you will have to use *args syntax, a new Python
    feature introduced in this project.  See the project description.

    >>> dice = make_test_dice(4, 2, 5, 1)
    >>> averaged_dice = make_averaged(dice, 1000)
    >>> averaged_dice()
    3.0
    """
    # BEGIN PROBLEM 8
    "*** YOUR CODE HERE ***"
    def calcuate(*args):
        total= 0
        for i in range(trials_count):   # 做循环
            total += original_function(*args)   # 累加
        return total / trials_count
    return calcuate
    # END PROBLEM 8


def max_scoring_num_rolls(dice=six_sided, trials_count=1000):
    """
    Return the number of dice (1 to 10) that gives the highest average turn
    score by calling roll_dice with the provided DICE over TRIALS_COUNT times.
    Assume that the dice always return positive outcomes.

    >>> dice = make_test_dice(1, 6)
    >>> max_scoring_num_rolls(dice)
    1
    """
    # BEGIN PROBLEM 9
    "*** YOUR CODE HERE ***"
    max_roll = 0    # 最大平均结果
    num_of_rolls = 10   # 从10到1的投掷次数
    max_num_of_rolls = 0    # 最优投掷数
    while num_of_rolls > 0:     # 从10到1的投掷次数
        tmp = make_averaged(roll_dice, trials_count)(num_of_rolls, dice)
        # 从10到1的投掷次数, 使用dice=six_sided
        if tmp > max_roll:
            max_roll = tmp
            max_num_of_rolls = num_of_rolls
        num_of_rolls -= 1
    return max_num_of_rolls
    # END PROBLEM 9


def winner(strategy0, strategy1):
    """Return 0 if strategy0 wins against strategy1, and 1 otherwise."""
    score0, score1 = play(strategy0, strategy1)
    if score0 > score1:
        return 0
    else:
        return 1


def average_win_rate(strategy, baseline=always_roll(6)):
    """Return the average win rate of STRATEGY against BASELINE. Averages the
    winrate when starting the game as player 0 and as player 1.
    """
    win_rate_as_player_0 = 1 - make_averaged(winner)(strategy, baseline)
    win_rate_as_player_1 = make_averaged(winner)(baseline, strategy)

    return (win_rate_as_player_0 + win_rate_as_player_1) / 2


def run_experiments():
    """Run a series of strategy experiments and report results."""
    if True:  # Change to False when done finding max_scoring_num_rolls
        six_sided_max = max_scoring_num_rolls(six_sided)
        print('Max scoring num rolls for six-sided dice:', six_sided_max)

    if False:  # Change to True to test always_roll(8)
        print('always_roll(8) win rate:', average_win_rate(always_roll(8)))

    if False:  # Change to True to test bacon_strategy
        print('bacon_strategy win rate:', average_win_rate(bacon_strategy))

    if False:  # Change to True to test extra_turn_strategy
        print('extra_turn_strategy win rate:', average_win_rate(extra_turn_strategy))

    if False:  # Change to True to test final_strategy
        print('final_strategy win rate:', average_win_rate(final_strategy))

    "*** You may add additional experiments as you wish ***"



def bacon_strategy(score, opponent_score, cutoff=8, num_rolls=6):
    """
    This strategy rolls 0 dice if that gives at least CUTOFF points, and
    rolls NUM_ROLLS otherwise.
    """
    
    '''
    # 要求: 投0个骰子时大于cutoff, 否则掷NUM_ROLLS个骰子.
    '''
    # BEGIN PROBLEM 10
    # 如果掷0所得的分数比cutoff大就掷 0 个骰子，else return  num_rolls
    if free_bacon(opponent_score) >= cutoff:
        return 0
    else:
        return num_rolls
    # END PROBLEM 10


def extra_turn_strategy(score, opponent_score, cutoff=8, num_rolls=6):
    """
    This strategy rolls 0 dice when it triggers an extra turn.
    遇到加次的情况就投0
    It also rolls 0 dice if it gives at least CUTOFF points and does not give an extra turn.
    或者如果掷0所得的分数比cutoff大就掷 0 个骰子
    Otherwise, it rolls NUM_ROLLS.
    """
    # BEGIN PROBLEM 11
    if extra_turn(free_bacon(opponent_score) + score, opponent_score):
        return 0
    else:
        return bacon_strategy(score, opponent_score, cutoff, num_rolls)
    # END PROBLEM 11


def final_strategy(score, opponent_score):
    """
    Write a brief description of your final strategy.
    html文件提示是:
    没有必要得分超过 100。检查你是否能通过掷 0、1 或 2 个骰子来获胜。如果你领先，可能会选择减少风险。
    尽量争取额外的回合。
    *** YOUR DESCRIPTION HERE ***
    """
    # BEGIN PROBLEM 12
    skill = free_bacon(opponent_score)
    cutoff = 8
    num_rolls = 6
    if score + skill >= 100:
        return 0
    else:
        return extra_turn_strategy(score,opponent_score,100,num_rolls)
    
    # END PROBLEM 12

##########################
# Command Line Interface #
##########################

# NOTE: Functions in this section do not need to be changed. They use features
# of Python not yet covered in the course.


@main
def run(*args):
    """Read in the command-line argument and calls corresponding functions."""
    import argparse
    parser = argparse.ArgumentParser(description="Play Hog")
    parser.add_argument('--run_experiments', '-r', action='store_true',
                        help='Runs strategy experiments')

    args = parser.parse_args()

    if args.run_experiments:
        run_experiments()
