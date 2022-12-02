
from sklearn.preprocessing import MinMaxScaler
from plotly.colors import sample_colorscale
import pandas as pd
import numpy as np
import math
from wordcloud import WordCloud
from sklearn.decomposition import PCA
from factor_analyzer import Rotator
from scipy.stats import zscore
def wordcloud_(loadings):
    """
    This function generates a wordcloud from the loadings of a topic model.
    Args:
        loadings (pandas.DataFrame): The loadings of a topic model.
    Returns:
        im (PIL.Image.Image): The wordcloud image.
    """
    unscaledloadings = loadings.sort_values(ascending=False)
    scaledloadings = MinMaxScaler().fit_transform(unscaledloadings.values.reshape(-1, 1)).flatten().round(4)
    scaledloadings_col = (
        MinMaxScaler(feature_range=(-10, 10)).fit_transform(unscaledloadings.values.reshape(-1, 1)).round(4)
    )
    scaledloadings_col = (
        pd.DataFrame(scaledloadings_col.T)
        .apply(lambda x: 1 / (1 + math.exp(-x)))
        .to_numpy()
    )
    colours = sample_colorscale("RdBu", samplepoints=scaledloadings_col)
    colour_dict = {x.split("_")[0]: y for x, y in zip(unscaledloadings.index, colours)}
    absolutescaledloadings = np.where(
        scaledloadings < 0.5, 1 - scaledloadings, scaledloadings
    )
    rescaledloadings = (
        MinMaxScaler().fit_transform(absolutescaledloadings.reshape(-1, 1)).flatten()
    )
    freq_dict = {
        x.split("_")[0]: y for x, y in zip(unscaledloadings.index, rescaledloadings)
    }

    def color_func(
        word, *args, **kwargs
    ):  # colour function to supply to wordcloud function.. don't ask !
        return colour_dict[word]

    wc = WordCloud(
        background_color="white",
        color_func=color_func,
        width=400,
        height=400,
        prefer_horizontal=1,
        min_font_size=8,
        max_font_size=200,
    )
    # generate wordcloud from loadings in frequency dict
    wc = wc.generate_from_frequencies(freq_dict)
    im = wc.to_image()
    return im

data = pd.read_csv('Analysis/output.csv')
data = data.drop(["Participant #","Runtime_mod","Gradient 1","Gradient 2","Gradient 3"],axis=1)
Taskindices = data["Task_name"]
data_ = data.drop(["Task_name"],axis=1).apply(lambda x: zscore(x),axis=0)


PCAdata = data_.apply(lambda x: zscore(x),axis=0)  # zscore the dataframe to normalise it.)
PCAmodel = PCA(n_components=4)
rot = Rotator()

PCAmodel.fit(PCAdata)

loadings = PCAmodel.components_
loadings = rot.fit_transform(PCAmodel.components_.T).T
#lods = rot.transform(PCAmodel.components_.T)
names = PCAdata.columns
#loadings = PCAmodel.components_
loadings = pd.DataFrame(
    np.round(loadings.T, 3),
    index=names,
    columns=[f"Component {x}" for x in range(4)],
)
PCAresults = np.dot(PCAdata,loadings).T
pcres = pd.DataFrame(PCAresults.T,index=Taskindices,columns=loadings.columns)
for z in loadings.columns:
    wdc = wordcloud_(loadings[z])
    wdc.save(f'{z}.jpeg')
PCR = pcres.groupby("Task_name").mean()
fl = pd.read_csv('file.csv',header=None,index_col=0)
from scipy.stats import pearsonr
corr = loadings.corr(fl[1])
print('e')