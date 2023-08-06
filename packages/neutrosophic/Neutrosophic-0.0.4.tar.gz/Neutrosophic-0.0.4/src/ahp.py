# بسم الله الرحمن الرحيم

from .svtnn import svtnn
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from math import sqrt, pow
import pandas as pd
import datetime

from .ahp_helper import(
    ratio_index, 
    generate_pie_labels,
    log,
    plot_pie,
    plot_correlation,
    find_largest_preference,
    deneutrosophy_matrix,
    initialize_ahp_environment,
    svtnn_list,
    svtnn_inverse_list,
    normalize_matrix, 
    pandas_plot_correlation)

class AHP:
    '''
    '''
    
    def __init__(self, no_criteria, no_dec_makers, no_alternatives, log_enabled=True):
        self.no_criteria = no_criteria
        self.no_dec_makers = no_dec_makers
        self.no_alternatives = no_alternatives
        self.ratio_index = ratio_index(self.no_criteria)
        self.pie_labels = generate_pie_labels(self.no_criteria)
        self.log_enabled = log_enabled
        self.consistent = False
        self.fix_suggestion_exists = False
        # New
        self.consistency_ratio = 0.0
        self.criteria_weights = []
        self.normalized_criteria_weights = []
        # End New
        
    def calculate_aggregate_pairwise(self, aggregate=True, *args):
        ''' This function accepts Pandas Data Frame in args'''
        if aggregate:
            self.aggregate_pairwise_comparison = args[0]
        else:
            self.DMs = args
            self.aggregate_pairwise_comparison = args[0].copy()
            for arg in args:
                self.aggregate_pairwise_comparison += arg
            self.aggregate_pairwise_comparison -= args[0]
            self.aggregate_pairwise_comparison = self.aggregate_pairwise_comparison.div(self.no_dec_makers)


    def calculate_criteria_weights(self):
        self.aggregate_pairwise_sum_by_col = self.aggregate_pairwise_comparison.sum(axis=0)
        self.normalized_aggregate_pairwise_comparison = self.aggregate_pairwise_comparison.div(self.aggregate_pairwise_sum_by_col)
        self.criteria_weights = self.normalized_aggregate_pairwise_comparison.sum(axis=1).div(self.no_criteria)
        return self.criteria_weights

    def calculate_normalized_criteria_weights(self):
        self.normalized_criteria_weights = normalize_matrix(deneutrosophy_matrix(self.criteria_weights))

    # Check Consistency
    # Two cases: for aggregate pairwise, and for individual matrices
    # Here, focus will be on Aggregate
    def check_consistency(self, aggregate=True, log_enabled=True):
        # sum by row https://www.youtube.com/watch?v=ecckslwG3xk
        if aggregate:
            # check following index
            self.consistency_ratio = (self.aggregate_pairwise_comparison.mul(deneutrosophy_matrix(self.criteria_weights)).sum(axis=0)).div(self.criteria_weights)
            self.lambda_max = deneutrosophy_matrix(self.consistency_ratio).mean()
            self.consistency_index = (self.lambda_max - self.no_criteria)/(self.no_criteria - 1)
            self.consistency_ratio = self.consistency_index / self.ratio_index

            if self.consistency_ratio - 0.1 > 0.01:
                if log_enabled:
                    log(f'Consistency Repair is needed, {self.consistency_ratio}')
                    print(f'Consistency Repair is needed, Consistency Ratio = {self.consistency_ratio}')
                self.induced_matrix = (self.aggregate_pairwise_comparison.mul(self.aggregate_pairwise_comparison)) - (self.aggregate_pairwise_comparison.mul(self.no_criteria))
                self.largest_preference_info = find_largest_preference(deneutrosophy_matrix(self.induced_matrix))
                self.inconsistent_row_vector = self.induced_matrix.iloc[self.largest_preference_info[0]]
                self.inconsistent_col_vector_transpose = self.induced_matrix.iloc[:, self.largest_preference_info[1]:self.largest_preference_info[1]+1].transpose()
                self.prejudice_vector = self.inconsistent_row_vector.mul(self.inconsistent_col_vector_transpose.squeeze().array)
                self.b_01 = self.prejudice_vector - self.aggregate_pairwise_comparison.iat[self.largest_preference_info[0],self.largest_preference_info[1]]
                if log_enabled:
                    log(f'Row {self.largest_preference_info[0] + 1} needs attention')
                self.to_modify = []
                for idx, item in enumerate(self.b_01):
                    if item.a1 > 0 or item.a2 > 0 or item.a3 > 0:
                        self.to_modify.append(idx)
                # New
                if len(self.to_modify) == 0:
                    self.to_modify.append(self.largest_preference_info[1])
                # End New
                if log_enabled:
                    for c in self.to_modify:
                        print(f'Please update value of item [{self.largest_preference_info[0] + 1},{c + 1}]')
                        log(f'Please update value of item [{self.largest_preference_info[0] + 1},{c + 1}]')
            else:
                self.consistent = True
                if log_enabled:
                    log('Consistency Ratio is Accepted')
                    print('Consistency Ratio is Accepted')
        return self.consistency_ratio

    def suggest_fix(self):
        self.log_enabled = False
        if self.consistency_ratio - 0.1 > .0:
            self.log_enabled = False
            for c in self.to_modify:
                for idx,num in enumerate(svtnn_list):
                    if idx == 0:
                        continue
                    apc = self.aggregate_pairwise_comparison.copy()
                    inner_ahp = AHP(self.no_criteria, self.no_dec_makers, self.no_alternatives, log_enabled=False)
                    apc.iat[self.largest_preference_info[0],c] = num
                    apc.iat[c, self.largest_preference_info[0]] = svtnn_inverse_list[idx]
                    inner_ahp.calculate_aggregate_pairwise(True, apc)
                    inner_ahp.calculate_criteria_weights()
                    if inner_ahp.check_consistency(log_enabled=False) - 0.1 < 0.1:
                        self.log_enabled = False
                        self.fix_suggestion = [self.largest_preference_info[0], c, idx, num]
                        self.fix_suggestion_exists = True
                        print(f'Suggestion: Modify item [{self.largest_preference_info[0] + 1},{c + 1}] to be {num} so Consistency Ratio becomes {inner_ahp.check_consistency(log_enabled=False)}')
                        log(f'Suggestion: Modify item [{self.largest_preference_info[0] + 1},{c + 1}] to be {num} so Consistency Ratio becomes {inner_ahp.check_consistency(log_enabled=False)}')
                        return
            log('No suggestions found!')
            print('No suggestions found!')
        else:
            pass
#             log('Consistency Ratio is really good!')
#             print('Consistency Ratio is really good!')


    def apply_suggestion(self):
        self.aggregate_pairwise_comparison.iat[self.largest_preference_info[0],self.fix_suggestion[1]] = self.fix_suggestion[3]
        self.aggregate_pairwise_comparison.iat[self.fix_suggestion[1], self.largest_preference_info[0]] = self.fix_suggestion[3]
        # self.calculate_aggregate_pairwise(True, self.aggregate_pairwise_comparison)
        self.calculate_criteria_weights()
        self.calculate_normalized_criteria_weights()
        plot_pie(self.pie_labels, self.normalized_criteria_weights)
        self.fix_suggestion = []
        self.fix_suggestion_exists = False


    def plot_my_correlation(self):
        plot_correlation(normalize_matrix(deneutrosophy_matrix(self.normalized_aggregate_pairwise_comparison.sum(axis=1))), self.no_criteria)
        
    
    def plot_pandas_correlation(self):
        pandas_plot_correlation(deneutrosophy_matrix(self.normalized_aggregate_pairwise_comparison))
        pandas_plot_correlation(deneutrosophy_matrix(self.normalized_aggregate_pairwise_comparison), corr_type='pearson')