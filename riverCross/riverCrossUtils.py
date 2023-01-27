def finish(observation):
    if win(observation):
        print("Felicitaciones, ganaste!")
    else:
        print("Perdiste")

def win(observation):
    win = {"farmerSide": 1,
            "cabbageSide": 1,
            "goatSide": 1,
            "wolfSide": 1,
            }
    
    return observation == win
    
def ask_input(text):
    ret = input(text)
    return ret

def parse_action(direction, passenger):

    charToPassenger = {
        "C": "0",
        "F": "3",
        "G": "1",
        "W": "2"
    }
    charToDirection = {
        "R": "0",
        "L": "1",
    }
    input_status = True
    d = 0
    p = 0
    try:
        p = int(charToPassenger[passenger])
    except Exception:
        print("Codigo de pasajero desconocido.")
        input_status = False

    try:
        d = int(charToDirection[direction])
    except Exception:
        print("Codigo de direccion desconocida.")
        input_status = False

    ret = {
        "direction": d,
        "passenger": p
    }
    return ret, input_status


def input_action():

    input_status = False

    while(not(input_status)):
        user_input_passenger = ask_input("Ingrese el pasajero (F,C,G,W):")
        user_input_direction = ask_input("Ingrese la dirección (L,R):")
        action, input_status = parse_action(
            user_input_direction, user_input_passenger)

    return action
