from gxdltk.header import *


def calc_acc(pred: list, label: list) -> float:
    """
    calc accuracy
    :param pred:
    :param label:
    :return:
    """
    assert len(pred) == len(label), "length of arg#1 must be equal to arg#2"
    p = np.array(pred)
    l = np.array(label)
    return np.sum(p == l) / len(label)


def sum_loss(loss_arr: list) -> float:
    loss_ar = np.array(loss_arr)
    return loss_ar.sum()
