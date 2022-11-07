from pathlib import Path


def _read_input_file_path() -> Path:
    """Reads the input file path from the standard input"""
    return Path(input())


"""The class action provides easy access to an action object. An action object contains action type,
action name, action finish name, action place and action count"""


class Action:
    def __init__(self, actionType, name, time, place, actionCount):
        self.actionType = actionType if actionType == 'ALERT' else 'CANCELLATION'
        self.name = name
        self.time = time
        self.place = place
        self.actionCount = actionCount


def get_the_minimum_index(action):
    """This helper function give the action that needs to be executed from the action list.
    It first finds the least time action. If there are two action with the same time, then cancellation
    goes first. If there are two cancellations, the one with a shorter name goes first."""
    index = 0
    minimum = action[0].time
    for i in range(1, len(action)):
        if action[i].time < minimum:
            index = i
            minimum = action[i].time
        elif action[i].time == minimum:
            if action[i].actionType == 'CANCELLATION' and action[index].actionType == 'ALERT':
                index = i
                minimum = action[i].time
            else:
                if len(action[i].name) < len(action[index].name):
                    index = i
                    minimum = action[i].time
    return index


# line 60-61 of main function is lacking coverage because unresolved reasons.
def main() -> None:
    """Runs the simulation program in its entirety"""
    input_file_path = _read_input_file_path()
    propagateTime = dict()
    deviceCount = 0
    action = []

    try:
        with open(input_file_path, "r") as file:
            for line in file:
                newLine = line.strip()
                if newLine.startswith('#') or len(newLine) == 0:
                    pass
                elif newLine.startswith('DEVICE'):
                    deviceCount += 1
                elif newLine.startswith('PROPAGATE'):
                    tokens = newLine.split(' ')
                    propagateTime[int(tokens[1])] = [int(tokens[2]), int(tokens[3])]
                else:
                    if newLine.startswith('ALERT') or newLine.startswith('CANCEL'):
                        tokens = newLine.split(' ')
                        action.append(Action(tokens[0], tokens[2], int(tokens[3]), int(tokens[1]), 0))

            while True:
                if len(action) == 0:
                    break
                index = get_the_minimum_index(action)
                currentAction = action[index]
                nextPlace = currentAction.place + 1 if currentAction.place + 1 <= deviceCount else 1
                previousPlace = currentAction.place - 1 if currentAction.place - 1 > 0 else deviceCount
                if currentAction.actionCount == 0:
                    print(
                        f"@{currentAction.time} #{currentAction.place}: SENT {currentAction.actionType} TO #{nextPlace}: {currentAction.name}")
                    action[index].time += propagateTime[action[index].place]
                    action[index].actionCount += 1
                    action[index].place = nextPlace
                elif currentAction.actionCount >= deviceCount:
                    print(
                        f"@{currentAction.time} #{currentAction.place}: RECEIVED {currentAction.actionType} FROM #{previousPlace}: {currentAction.name}")
                    action.remove(currentAction)
                else:
                    print(
                        f"@{currentAction.time} #{currentAction.place}: RECEIVED {currentAction.actionType} FROM #{previousPlace}: {currentAction.name}")
                    print(
                        f"@{currentAction.time} #{currentAction.place}: SENT {currentAction.actionType} TO #{nextPlace}: {currentAction.name}")
                    action[index].time += propagateTime[action[index].place]
                    action[index].actionCount += 1
                    action[index].place = nextPlace
    except FileNotFoundError as e:
        print("FILE NOT FOUND")

    # These two lines can not be cover by tests because they can only run in project1 file.


if __name__ == '__main__':
    main()
