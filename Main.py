from Arena import Arena
from MinionGroup import MinionGroup


from TrainingRoom import TrainingRoom


class Main():
    def __init__(self):
        pass

def battle():
    alpha = MinionGroup(0,True,grp_name="Alpha")
    beta = MinionGroup(0,True,grp_name="Beta")
    alpha1 = alpha.minionList[2]
    beta1 = beta.minionList[4]
    tourne = Arena(alpha1.name.lower() + ".png",beta1.name.lower() + ".png")
    tourne.fight(alpha1, beta1)
def training(n_min,n_gen):
    alpha = MinionGroup(n_min)
    beta = MinionGroup(n_min)
    alpha_room = TrainingRoom(alpha)
    beta_room = TrainingRoom(beta)
    alpha_room.mass_train(n_gen)
    beta_room.mass_train(n_gen)
    alpha1 = alpha.minionList[0]
    alpha1.name = "Edek"
    beta1 = beta.minionList[0]
    beta1.name = "Beniek"
    alpha1.show_params()
    beta1.show_params()
    alpha_room.save_best("Alpha")
    tourne = Arena()
    tourne.fight(alpha1,beta1)

if __name__ == "__main__":
    training(20,100)

