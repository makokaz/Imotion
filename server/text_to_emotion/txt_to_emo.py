# Using the trained model for making predictions
import pandas as pd
from nltk.corpus import stopwords
from textblob import Word
import pickle
from flask import Flask, request, render_template,jsonify
from flask_cors import CORS


# # tweets = pd.DataFrame(['I am really happy today!',
# # 'The sunset is so beatiful',
# # 'The cup broke off, I feel sad now',
# # 'The dog is excited to play',
# # 'This hackathon is really fun!',
# # 'I feel lonely and sad',
# # 'I hate banana',
# # 'I am super excited!'])

# # tweets = pd.DataFrame(['a group of happy people are playing a video game',
# # 'a group of nice people holding umbrellas in the rain',
# # 'a close up of some very tasty food on a table',
# # 'a nice man is riding a motorcycle down a busy street', 
# # 'a nice man is riding a great wave on a surfboard',
# # 'a group of stupid people playing nintendo wii in a living room',
# # 'a lonely train pulling into a train station',
# # 'a plate of disgusting food on a table',
# # 'a close up of a lazy cat laying on a bed'])

file = 'count_vector.sav'
count_vect = pickle.load(open(file, 'rb'))

filename = 'finalized_model.sav'
loaded_model = pickle.load(open(filename, 'rb'))

tweets = pd.DataFrame(['She seems very happy in the picture, and you want to know\n what what is behind the smile.',
'This woman has really knotty hands which makes her look like she has arthritis.', 
'When looking at this woman, I am filled with curiosity about what \nshe is thinking about with her elbow on the table and a very emotionless face.', 
'A woman looking at ease, peaceful, and satisfied amongst her books makes me feel content.',
'She looks like a lady from that past that might have been a teacher (books).\nShe looks tired and I wondered how hard it must have been for them back then.',
'The bright colors make a very unique scene for the interesting shapes.',
'The way the image is presented, with large chunks of paint used to depict each of the subjects,\nmakes for a slight amount of confusion and an unsureness on the part of the viewer: what, exactly, was Kandinsky trying to depict during Autumn?'])
print(tweets)

# Doing some preprocessing on the text
tweets[0] = tweets[0].str.replace('[^\w\s]',' ')
from nltk.corpus import stopwords
stop = stopwords.words('english')
tweets[0] = tweets[0].apply(lambda x: " ".join(x for x in x.split() if x not in stop))
# from textblob import Word
tweets[0] = tweets[0].apply(lambda x: " ".join([Word(word).lemmatize() for word in x.split()]))
# Extracting Count Vectors feature from our tweets
tweet_count = count_vect.transform(tweets[0])

######################################################################

# t = str(input('Please input some text: '))
# tweets = pd.DataFrame([t], columns=['str'])
# print(tweets)

# # Doing some preprocessing on these tweets as done before
# tweets['str'] = tweets['str'].str.replace('[^\w\s]',' ')

# stop = stopwords.words('english')
# tweets['str'] = tweets['str'].apply(lambda x: " ".join(x for x in x.split() if x not in stop))

# tweets['str'] = tweets['str'].apply(lambda x: " ".join([Word(word).lemmatize() for word in x.split()]))
# # Extracting Count Vectors feature from our tweets
# tweet_count = count_vect.transform(tweets['str'])

#########################################################################

#Predicting the emotion of the tweet using our already trained linear SVM
tweet_pred = loaded_model.predict(tweet_count)
print(tweet_pred)

def preprocess(txt):
    t = str(txt)
    tweets = pd.DataFrame([t], columns=['str'])
    print(tweets)

    # Doing some preprocessing on these tweets as done before
    tweets['str'] = tweets['str'].str.replace('[^\w\s]',' ')

    stop = stopwords.words('english')
    tweets['str'] = tweets['str'].apply(lambda x: " ".join(x for x in x.split() if x not in stop))

    tweets['str'] = tweets['str'].apply(lambda x: " ".join([Word(word).lemmatize() for word in x.split()]))
    # Extracting Count Vectors feature from our tweets
    tweet_count = count_vect.transform(tweets['str'])
    tweet_pred = loaded_model.predict(tweet_count)
    return tweet_pred

def generate_emo(txt):
    res = []
    for i in txt:
        if i==4:
            print('Happiness')
            res.append('Happy')
        elif i==6:
            print('Sadness')
            res.append('Sad')
        elif i==8:
            print('Enthusiasm')
            res.append('Surprise')
        elif i==5:
            print('Hate')
            res.append('Anger')
    
    return res

app = Flask(__name__)
CORS(app, supports_credentials=True)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/res', methods=['GET'])
def txt_to_emo():
    text = 'She seems very happy in the picture, and you want to know\n what what is behind the smile.'
    preds = preprocess(text)
    response = generate_emo(preds)
    return jsonify(result=response)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)