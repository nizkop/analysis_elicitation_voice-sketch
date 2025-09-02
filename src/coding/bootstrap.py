import numpy as np

from src.color_codes import global_colors
from src.statistical_settings import alpha
from src.plt_settings import my_plt, figure_width, default_height, save_my_figures


def bootstrap_valbjoern(agreement_rates: list, description:str):
    # ### Valbjörn's python code:
    # n = 2000
    # np.random.seed(1337)
    # bootstrap_means = np.zeros(n)
    #
    # for i in range(n):
    #     bootstrap_sample = np.random.choice(agreement_rates, size=len(agreement_rates), replace=True)
    #     bootstrap_means[i] = np.mean(bootstrap_sample)
    #
    # alpha = 0.05
    # lower_bound = np.percentile(bootstrap_means, 100 * (alpha / 2))
    # upper_bound = np.percentile(bootstrap_means, 100 * (1 - alpha / 2))
    #
    # print(f"Bootstrap Mean: {np.mean(bootstrap_means):.3f}")
    # print('Original mean:', np.mean(agreement_rates))
    # print(f"95% Confidence Interval: [{lower_bound:.3f}, {upper_bound:.3f}]")
    #
    # plt.hist(bootstrap_means, bins=50, edgecolor='k', color='royalblue', alpha=0.7)
    # plt.axvline(np.mean(agreement_rates), color='red', linestyle='--', label=f'Original Mean ({np.mean(agreement_rates):.4f})')
    # plt.axvline(np.mean(bootstrap_means), color='orange', linestyle='--', label=f'Bootstrap Mean ({np.mean(bootstrap_means):.4f})')
    # plt.axvline(lower_bound, color='black', linestyle='--', label=f'Lower conf. ({lower_bound:.3f})')
    # plt.axvline(upper_bound, color='black', linestyle='--', label=f'Upper conf. ({upper_bound:.3f})')
    # plt.xlabel('Mean Agreement Rate')
    # plt.ylabel('Frequency')
    # plt.legend(bbox_to_anchor=(0.5, -0.15), loc='upper center', ncol=3, fontsize=10)
    # plt.savefig(f"bootstrap_mean_{description}.pdf", bbox_inches="tight")
    # plt.show()
    # plt.close()

    n = 2000
    np.random.seed(1337)
    bootstrap_means = np.zeros(n)

    for i in range(n):
        bootstrap_sample = np.random.choice(agreement_rates, size=len(agreement_rates), replace=True)
        bootstrap_means[i] = np.mean(bootstrap_sample)

    lower_bound = np.percentile(bootstrap_means, 100 * (alpha / 2))
    upper_bound = np.percentile(bootstrap_means, 100 * (1 - alpha / 2))

    print(f"Bootstrap Mean: {np.mean(bootstrap_means):.3f}")
    print('Original mean:', np.mean(agreement_rates))
    print(f"95% Confidence Interval: [{lower_bound:.3f}, {upper_bound:.3f}]")

    fig, ax = my_plt.subplots(figsize=(figure_width, default_height*0.75))
    ax.hist(bootstrap_means, bins=50, edgecolor='k', color=global_colors[description], alpha=0.5 if "LESS" in description else 1)
    ax.axvline(np.mean(agreement_rates), color='red', linestyle='--', label=f'Original Mean ({np.mean(agreement_rates):.4f})')
    ax.axvline(np.mean(bootstrap_means), color='orange', linestyle='--', label=f'Bootstrap Mean ({np.mean(bootstrap_means):.4f})')
    ax.axvline(lower_bound, color='black', linestyle='--', label=f'Lower conf. ({lower_bound:.3f})')
    ax.axvline(upper_bound, color='black', linestyle='--', label=f'Upper conf. ({upper_bound:.3f})')
    ax.set_xlabel('Mean Agreement Rate [ ]')
    ax.set_ylabel('Frequency [ ]')
    legend = ax.legend(bbox_to_anchor=(0.5, -0.15), loc='upper center', ncol=3)
    save_my_figures(f"bootstrap_mean_{description}", bbox_extra_artists=[legend])
    fig.show()
    my_plt.close()




# if __name__ == '__main__':
#     agreement_rates_kravac = [0.590476190476191,
#                                 0.427807486631016,
#                                 0.387301587301587,
#                                 0.366366366366366,
#                                 0.361904761904762,
#                                 0.329411764705882,
#                                 0.328571428571429,
#                                 0.310099573257468,
#                                 0.303174603174603,
#                                 0.290476190476191,
#                                 0.284615384615385,
#                                 0.231746031746032,
#                                 0.226984126984127,
#                                 0.223809523809524,
#                                 0.223328591749644,
#                                 0.220720720720721,
#                                 0.215053763440860,
#                                 0.164705882352941,
#                                 0.157142857142857,
#                                 0.119327731092437]
#
#
#     print(round(np.mean(agreement_rates_kravac),4) )
#     # assert round(np.mean(agreement_rates_kravac),4) == 0.2880
#
#
#
#     data = (np.array(agreement_rates_kravac),)  # data MUST be a tuple of arrays
#
#     res = bootstrap(data, statistic=np.mean, method='percentile', confidence_level=0.95)
#     bootstrap_mean = np.mean(res.bootstrap_distribution)
#     ci_low, ci_high = res.confidence_interval
#
#     print(f"Mean: {bootstrap_mean:.4f} \t\t\t\t({round(bootstrap_mean, 4) == 0.2888})")
#     print(f"95% CI: [{ci_low:.3f}, {ci_high:.3f}]\t\t({round(ci_low, 3) == 0.245} and {round(ci_high, 3) == 0.338})")
#     print()
#
#     bootstrap_valbjoern(agreement_rates_kravac)

