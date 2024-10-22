import  Web_Crawling
import re
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import font_manager
from wordcloud import WordCloud
from collections import Counter
from nltk.util import ngrams


# set font
font_path = "C:/Windows/Fonts/simhei.ttf"
font_prop = font_manager.FontProperties(fname=font_path)

# set font
plt.rcParams['font.family'] = font_prop.get_name()




def count_name_for_character_in_each_chapter(chapters:dict,characters:dict):

    name_frequency_result={name:[] for names in characters.values() for name in names}

    name_frequency_dict={name:0 for names in characters.values() for name in names}#store the frequency of the name for each character for each chapter

    for chapter, text in chapters.items():#traverse all the chapter
        for name,frequency in name_frequency_dict.items():
            frequency=len(re.findall(name,text))
            name_frequency_result[name].append(frequency)

    return  name_frequency_result


def generate_ngrams(text, n):
    tokens = re.findall(r'\w+', text)
    return Counter(ngrams(tokens, n))

def get_visualization_result(chapters:dict,characters:dict):
    # calculate alternative name frequency for each chapter
    name_counts = count_name_for_character_in_each_chapter(chapters, characters)

    # Use dataframe for better visualization
    name_counts_df = pd.DataFrame(name_counts, index=chapters.keys())
    name_counts_df.to_csv([name for name in characters][0])#Save to csv

    print(name_counts_df)  # Dataframe Presentation

    # Visualize Frequency using Stacked bar
    name_counts_df.plot(kind='bar', stacked=True)
    plt.title('NAME FREQUENCY', fontproperties=font_prop)
    plt.xlabel('CHAPTER', fontproperties=font_prop)
    plt.ylabel('FREQUENCY', fontproperties=font_prop)
    plt.xticks(rotation=45, fontproperties=font_prop)
    plt.legend(title='ALTERNATIVE NAME', prop=font_prop)
    plt.tight_layout()
    plt.show()

    # Generate word cloud
    wordcloud = WordCloud(font_path=font_path, width=800, height=400,
                          background_color='white').generate_from_frequencies(
        {name: sum(counts) for name, counts in name_counts.items()})
    plt.figure(figsize=(10, 6))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis('off')
    plt.title('word cloud', fontproperties=font_prop)
    plt.show()


    # 2-grams
    ngram_counts = Counter()
    for chapter in chapters.values():
        ngram_counts.update(generate_ngrams(chapter, 2))
    print("common 2-grams:")
    print(ngram_counts.most_common(10))




if __name__=="__main__":

    crawler = Web_Crawling.web_crawler(25)
    crawler.get_all_chapter_content()
    for a in crawler.content_dict.items():
        print("=====")
        print(a)

    chapters = crawler.content_dict  # Store chapter:text information


    #  Characters and their alternative names, you can set here if you want
    #Just simply put it into  get_visualization_result function
    characters_ALL = {
        "孫悟空": ["齊天大聖", "悟空", "美猴王", "孫悟空", "猴子"],
        "豬八戒": ["豬悟能", "天蓬元帥", "八戒", "猪八戒", "悟能"]
    }
    characters_WUKONG = {
        "孫悟空": ["齊天大聖", "悟空", "美猴王", "孫悟空", "猴子"],
    }
    characters_BAJIE = {
        "豬八戒": ["豬悟能", "天蓬元帥", "八戒", "猪八戒", "悟能"]
    }

    get_visualization_result(chapters,characters_WUKONG)

    get_visualization_result(chapters, characters_BAJIE)

    get_visualization_result(chapters, characters_ALL)






