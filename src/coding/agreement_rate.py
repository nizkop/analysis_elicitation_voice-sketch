

def agreement_rate(s: dict, information: str=dict):
    """
          SUM( (1/2) * |S_t,c| (|S_t,c| - 1)  )
    at = ---------------------------------------
                (1/2) * |S_t| (|S_t| - 1 )
    :param s:
    :return:
    """
    if len(s.values())==1:
        return 0
    at = 0
    st = sum(s.values())
    print(f"agreement_rate: number of task solutions = {st}")
    nenner = 0.5 * st * (st - 1)
    for category, amount_of_usages in s.items():
        zaehler = 0.5 * amount_of_usages * (amount_of_usages - 1)
        at += zaehler
        participants_using_this_code = information[category] if category in information.keys() else ""
        print("\t", amount_of_usages, "* ", [category],
              "-->", zaehler, "/", nenner,
              "\tfor", participants_using_this_code)
    # print("nenner", nenner)
    # print("-> agreement:", at / nenner)
    return at/nenner
#
#
# def collect_information_about_agreement_rate(s: dict, information:str=dict):
#
#
#
#
