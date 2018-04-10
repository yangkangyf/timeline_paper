#!/usr/bin/env python
import sys
from scipy.stats import pearsonr
import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA

corr={}
for f1 in sys.argv[1:]:
	sampleA=f1.split(".")[0].split("-")[1]+"_"+f1.split(".")[0].split("-")[3]
	for f2 in sys.argv[1:]:
		sampleB=f2.split(".")[0].split("-")[1]+"_"+f2.split(".")[0].split("-")[3]
		
		if sampleA == sampleB:
			if sampleA not in corr: corr[sampleA]={}
			corr[sampleA][sampleB]=1
			continue

		a=[]
		b=[]
		for line in open(f1): a.append(float(line.strip()))
		for line in open(f2): b.append(float(line.strip()))
	
		r,p = pearsonr(a,b)
		if sampleA not in corr: corr[sampleA]={}
		corr[sampleA][sampleB]=r

df = pd.DataFrame.from_dict(corr)



pca = PCA(n_components=2)
principalComponents = pca.fit_transform(df)
principalDf = pd.DataFrame(data = principalComponents, columns = ['component_1', 'component_2'])

df = df.reset_index()
finalDf = pd.concat([principalDf, df[["index"]]], axis = 1)


var = pca.explained_variance_ratio_

fig = plt.figure(figsize = (5,5))
ax = fig.add_subplot(1,1,1) 
ax.set_xlabel('Principal Component 1 (variance explained = '+ str(var[0]*100)[:4]+"%", fontsize = 10)
ax.set_ylabel('Principal Component 2 (variance explained = '+ str(var[1]*100)[:4]+"%", fontsize = 10)

colors = {"2014": 'r', "2015":'g', "2016":'b', "2017":'c'}
for i in finalDf.index:
	x = finalDf["component_1"][i]
	y = finalDf["component_2"][i]
	sample = finalDf["index"][i].split("_")[0]
	color=colors[sample]
	if finalDf["index"][i].split("_")[1]=="1": ax.scatter(x, y, c=color, s=50, label=sample)	
	else: ax.scatter(x, y, c=color, s=50)

ax.legend()
ax.grid()


plt.show()






