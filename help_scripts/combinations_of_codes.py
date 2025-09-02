import itertools



def get_all_categories(codes):
    all_combinations = []
    for r in range(1, len(codes)+1):
        comb_r = list(itertools.combinations(codes, r))
        all_combinations.extend(comb_r)

    print(all_combinations)
    print("Number of combinations:", len(all_combinations))


if __name__ == '__main__':
    codes_operation = ['WORDS', 'SYMBOL']
    get_all_categories(codes_operation)

    codes_operation = ['WORDS', 'SYMBOL']
    get_all_categories(codes_operation)

    codes_location = ["POINTING", "ADDRESS", "ENTRY"]
    get_all_categories(codes_location)

    get_all_categories(codes_location+codes_operation)