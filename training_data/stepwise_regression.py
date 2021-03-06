from pandas import read_csv, read_html
from statsmodels.api import add_constant, OLS
from tqdm import tqdm

df = read_csv('clean_data_set.csv', sep=',', header=0, index_col=['Date/Time', 'Year', 'Month', 'Day', 'Time'])
# print("Finished import")

predictors = list()
with open('temp_relevant_features_2.txt', 'r') as f:
    predictors = [line.strip() for line in f]

# print(predictors)
df = df[['Temp (°C)'] + predictors]

X = add_constant(df[predictors]) 
Y = df['Temp (°C)']
# print(x.ix[:5, :5])

alpha = 0.05

model = OLS(Y, X).fit()

results = model.summary()
results_as_html = results.tables[1].as_html()
results_df = read_html(results_as_html, header=0, index_col=0)[0].T
results_fit = False
while not results_fit:
    results_fit = True
    max_p_val = alpha
    max_key = None
    for x in tqdm(results_df.columns[1:]):
        # if results_df[x]['P>|t|'] > max_p_val:
        #     max_p_val = results_df[x]['P>|t|']
        #     max_key = x
        #     results_fit = False
        if results_df[x]['P>|t|'] > alpha:
            # max_p_val = results_df[x]['P>|t|']
            # max_key = x
            results_fit = False
            results_df = results_df.drop(x, axis=1)
            X = X.drop(x, axis=1)
    if not results_fit:
        # print(max_key)
        # X = X.drop(max_key, axis=1)
        # results_df = results_df.drop(max_key, axis=1)
        model = OLS(Y, X).fit()
        results = model.summary()
        results_as_html = results.tables[1].as_html()
        resutls_df = read_html(results_as_html, header=0, index_col=0)[0].T
print(model.summary())
X = X.drop('const', axis=1)
print(X)
X.to_csv('final_clean_training_set_temp_2.csv')