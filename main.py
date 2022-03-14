import pandas as pd
from score_weighting import BM25
from autocorrect import Speller

def recipeData():
    recipe_df = pd.read_csv("source/Food Ingredients and Recipe Dataset with Image Name Mapping.csv", encoding="utf8", encoding_errors="ignore")
    recipe_df = recipe_df.drop_duplicates(subset="Title")
    recipe_df = recipe_df.iloc[:10000]
    recipe_df = recipe_df.iloc[:,1:]
    del recipe_df["Ingredients"]
    recipe_df = recipe_df.dropna()  #drop rows that missing any values
    recipe_df = recipe_df.rename({'Cleaned_Ingredients':'Ingredients'},axis=1)
    recipe_df = recipe_df.reset_index(drop=True)
    recipe_df = recipe_df.reset_index() #add index in first column
    return recipe_df

def searchTitle(query):
    # query = "Mac and cheese"
    recipe_data = recipeData()
    check = Speller(lang='en')
    correct_textqry = check(query)
    bm25 = BM25()
    bm25.fit(recipe_data['Title'])
    result = bm25.transform(correct_textqry, recipe_data['Title'])
    result2 = pd.DataFrame(result)
    result3 = result2.sort_values(by=0, axis=0, ascending=False)
    print(result3)
    result4 = result3.head(10).index
    result5 = recipe_data.iloc[result4]
    result6 = result5.to_dict(orient='records')
    return result6

def searchIngredient(query):
    #query = "chichken"
    recipe_data = recipeData()
    check = Speller(lang='en')
    correct_textqry = check(query)
    bm25 = BM25()
    bm25.fit(recipe_data['Ingredients'])
    result = bm25.transform(correct_textqry, recipe_data['Ingredients'])
    result2 = pd.DataFrame(result)
    result3 = result2.sort_values(by=0, axis=0, ascending=False)
    print(result3)
    result4 = result3.head(10).index
    result5 = recipe_data.iloc[result4]
    result6 = result5.to_dict(orient='records')
    return result6

def listFav(query):
    recipe_data = recipeData()
    print(query)
    print(type(query))
    test = pd.DataFrame(query)
    print(test)
    result = recipe_data.iloc[test['recipe_id']]
    result2 = result.to_dict(orient='records')
    return result2

def search_Fav(fav,query):
    recipe_data = recipeData()
    fav_df_index = pd.DataFrame(fav)
    fav_df = recipe_data.iloc[fav_df_index['recipe_id']]
    check = Speller(lang='en')
    correct_textqry = check(query)
    bm25 = BM25()
    bm25.fit(fav_df['Title'])
    result = bm25.transform(correct_textqry, fav_df['Title'])
    result2 = pd.DataFrame(result)
    result3 = result2.sort_values(by=0, axis=0, ascending=False)
    print(result3)
    result3_5 = result3[result3[0] > 0]
    result4 = fav_df.iloc[result3_5.index]
    print(result4)
    result5 = result4.to_dict(orient='records')
    return result5

def testbackend(text):
    testString = "this is test string with ",text
    return testString

# if __name__ == '__main__':




