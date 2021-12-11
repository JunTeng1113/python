import numpy as np
import pandas as pd

np.random.seed(123456)
names = ['Allen', 'Alan', 'Ann', 'Bob', 'Cathy', 'David', 'Ellen', 'Ford', 'Giny', 'Hans']
grades = np.random.randint(50, 101, len(names))
scores = pd.DataFrame({'Name': names, 'Grade': grades})
print(scores)

score_bins = [0, 59, 62, 66, 69, 72, 76, 79, 82, 86, 89, 92, 99, 100]
letter_grades = ['F', 'D-', 'D', 'D+', 'C-', 'C', 'C+', 'B-', 'B', 'B+', 'A-', 'A', 'A+']
letter_cat = pd.cut(scores.Grade, score_bins, labels=letter_grades)
scores['Letter'] = letter_cat
print(scores)




# np.random.seed(123456)
# names = ['Allen','Alan','Ann','Bob','Cathy','David',"Ellen",'Ford','Giny','Hans']
# grades = np.random.randint(50,101, len(names))
# scores = pd.DataFrame({'Name':names,'Grade':grades})
# print(scores)
# score_bins = [0,59,62,66,69,72,76,79,82,86,89,92,99,100]
# letter_grades = ['F','D-','D','D+','C-','C','C+','B-','B','B+','A-','A','A+']
# letter_cat = pd.cut(scores.Grade, score_bins, labels=letter_grades)
# scores['Letter'] = letter_cat
# print(scores)
# print(letter_cat)
# print(scores.Letter.value_counts())
# print(scores.sort_values(by=['Letter'], ascending=False))