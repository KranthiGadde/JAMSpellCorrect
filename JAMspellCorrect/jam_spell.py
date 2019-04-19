from flask import Flask, render_template, request
from textblob import TextBlob
from wordsegment import load, segment

#Creating instance of this Flask class
app = Flask(__name__)

# Decorator for  binding spell_correct() function to spellCorrect URL
@app.route('/spellCorrect')
def spell_correct():
   return render_template('spellcorrect.html')

# Decorator for  binding result() function to result URL
@app.route('/result',methods = ['POST'])
def result():
    if request.method == 'POST':
        auto_corr_word_list=[]
        result = request.form
        input_word = result['word']
        if (result['word'] == ""):
            auto_corr_word_list.append("Empty string Passed")
            return render_template("spellcorrect.html",result = auto_corr_word_list)
        
        #Load unigram and bigram counts from disk
        load()
        
        #Return a list of words that is the best segmenation of input_word
        processed_text = segment(input_word)
        for word in processed_text:
            temp = TextBlob(word.lower())
            auto_corr_word_list.append(temp.correct())
        return render_template("spellcorrect.html",result = auto_corr_word_list)

if __name__ == '__main__':
    app.run(host='0.0.0.0')