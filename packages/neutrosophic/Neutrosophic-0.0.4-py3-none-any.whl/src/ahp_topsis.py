# بسم الله الرحمن الرحيم

from math import sqrt

from .ahp import AHP

from .ahp_helper import(
    plot_saaty_scale,
    initialize_ahp_environment, 
    plot_pie, 
    deneutrosophy_matrix, 
    normalize_matrix
    )

class AHPTopsis(AHP):
    
    def __init__(self, no_criteria, no_dec_makers, no_alternatives, log_enabled=True):
        AHP.__init__(self, no_criteria, no_dec_makers, no_alternatives, log_enabled=True)
        self.TDM = None
        self.norm_TDM = None
        self.norm_TDM_cw = None
        self.best_value = None
        self.worst_value = None
        self.n_DM_w_d = None

    def norm_deneut_norm_DMs(self, *args):
        '''
        ## Step 05.01: Normalize DM Vector (by Column)

        ### Step 05.01.01: Calculate Square Root of (Column Summation of Squared value for each cell)
        '''
        self.TDM = args[0]
        for i in range(len(args)):
            if i == 0:
                continue
            # Build Aggregate DM Matrix
            self.TDM += args[i]
        # Add this dilemma to the paper as an example of the Package need
        # Deneutrosophy, them sum, then divide
        # sum, then deneutrosophy, then divide
        # sum, then divide, then deneutrosophy
        # Can you notice the difference?
        # This is why most papers immediately deneutrosophy
        # Which is not the correct behaviour
        # Necessity: Google Rank, Score, etc. and add it here
        # Normalize Aggregate DM Matrix
        self.TDM = self.TDM.div(self.no_dec_makers)
        self.TDM = deneutrosophy_matrix(self.TDM)
        self.norm_TDM = normalize_matrix(self.TDM, by_col=False)
        return self.TDM, self.norm_TDM

    def calc_weighted_sum(self, criteria_weights=None):
        '''
        ## Step 05.02: Multiply Weights of each Criteria by the Corresponding Cell
        ### Paper Contribution here: we used Neutrosophic AHP to calculate Criteria Weights
        ### that will be used with TOPSIS to find ideal candidate
        # In this example, criteria weights are given
        # In AHP-TOPSIS, we use Neutrosophic AHP to obtain Criteria Weights
        '''
        if criteria_weights is None:
            criteria_weights = self.normalized_criteria_weights
        # Weighted Matrix
        # Normalized DM multiplied by Criteria Weights 
        self.norm_TDM_cw = self.norm_TDM.mul(criteria_weights)
        # norm_DM_cw
        return self.norm_TDM_cw

    
    def calc_ideal_best(self, beneficial=None):
        '''
        ## Step 05.03: Calculate Ideal Best and Ideal Worst

        - Note: Here, we use the normalized matrix multiplied by critiera weights
        - if the criteria is **beneficial** we take the maximum value
        - if the criteria is **non-beneficial** we take the minimum value
        '''
        if beneficial is None:
            criteria_category = self.no_criteria * [1]
        else:
            criteria_category = beneficial
        # Identify Beneficial and Non-Beneficial Criteria
        # 0 - used for non-beneficial criteria
        # 1 - used for beneficial criteria
        # critieria_idx = 0
        # critieia_category = [1,1,1]
        self.best_value = self.no_criteria * [0]

        for idx in range(self.norm_TDM_cw.shape[1]):
            if criteria_category[idx]:
                self.best_value[idx] = self.norm_TDM_cw.max()[idx]
            else:
                self.best_value[idx] = self.norm_TDM_cw.min()[idx]

        return self.best_value


    def calc_ideal_worst(self, beneficial=None):
        if beneficial is None:
            criteria_category = self.no_criteria * [1]
        else:
            criteria_category = beneficial

        # critieria_idx = 0
        self.worst_value = self.no_criteria * [0]

        for idx in range(self.norm_TDM_cw.shape[1]):
            if criteria_category[idx]:
                self.worst_value[idx] = self.norm_TDM_cw.min()[idx]
            else:
                self.worst_value[idx] = self.norm_TDM_cw.max()[idx]

        return self.worst_value

    def calc_distance(self):
        '''
        ## Step 05.04: For each row (alternative) - Calculate Distance from Ideal Best and Ideal Worst
        '''
        # norm DM with Distance
        self.n_DM_w_d = self.norm_TDM_cw.copy()

        self.n_DM_w_d.loc[:, 's_pos'] = 0

        for row in range(self.n_DM_w_d.shape[0]):
            for col in range(self.n_DM_w_d.shape[1] - 1):
                self.n_DM_w_d.iloc[row, self.no_criteria] += pow(self.n_DM_w_d.iloc[row,col] - self.best_value[col],2)
            self.n_DM_w_d.iloc[row, self.no_criteria] = sqrt(self.n_DM_w_d.iloc[row,self.no_criteria])

        self.n_DM_w_d.loc[:, 's_neg'] = 0

        for row in range(self.n_DM_w_d.shape[0]):
            for col in range(self.n_DM_w_d.shape[1] - 2):
                self.n_DM_w_d.iloc[row, self.no_criteria + 1] += pow(self.n_DM_w_d.iloc[row,col] - self.worst_value[col],2)
            self.n_DM_w_d.iloc[row, self.no_criteria + 1] = sqrt(self.n_DM_w_d.iloc[row,self.no_criteria + 1])

        # n_DM_w_d

        self.n_DM_w_d.loc[:, 'p'] = 0

        for row in range(self.n_DM_w_d.shape[0]):
            for col in range(self.n_DM_w_d.shape[1] - 3):
                self.n_DM_w_d.iloc[row, self.no_criteria + 2] = self.n_DM_w_d.iloc[row, self.no_criteria + 1] / (self.n_DM_w_d.iloc[row, self.no_criteria ] + self.n_DM_w_d.iloc[row, self.no_criteria + 1])


        return self.n_DM_w_d

    def rank_alternatives(self):
        return self.n_DM_w_d.sort_values(by=['p'], ascending=False)

    def plot_rank(self):
        plot_pie(data=self.n_DM_w_d['p'],pie_labels=self.n_DM_w_d.index)