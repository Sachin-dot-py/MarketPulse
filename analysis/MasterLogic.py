

def master_input(master_input_df):
    from sklearn.pipeline import make_pipeline
    from sklearn.preprocessing import StandardScaler
    from sklearn.linear_model import LinearRegression
    import numpy as np
    import pandas as pd
    import spacy
    from spacy.matcher import PhraseMatcher
    from spacy.tokens import Span
    from spacy.language import Language
    nlp = spacy.load('en_core_web_sm')

    df = pd.read_excel('stocksGood.xlsx')
    firms = list(df['Column3'])

    def better_name(firm_name):
        return firm_name.replace("Inc.", "").replace('Holdings', '').replace('Corp.', '').replace('Solutions','').replace('Services','').replace("Corporation", "").replace(",", "").replace("PLC", "").replace("Ltd.", "").replace('Platforms', '').replace('News','').replace('Institution','').replace('research','').replace('Replace','').replace('news','').replace('advantage','').strip().lower()

    name_to_ticker = df.assign(Column4 = df['Column3'].apply(better_name)).set_index('Column4')

    def n_to_t(lst):
        return_lst = []
        lst = [x.lower() for x in lst]
        def helper(x):
            try:
                a = name_to_ticker.loc[x]['Column2']
                if (isinstance(a, str)):
                    if ((a!='RSSS') & (a!='BPOP') & (a!='PINC') & (a!='AWRE') & (a!='NICE') & (a!='ADV') & (a!='BKNG') & (a!='DALN') & (a!='STHO')):
                        return a
                    else:
                            return False
                else:
                    return name_to_ticker.loc[x]['Column2'][-1]
            except:
                return False

        return_lst = list(map(lambda x: helper(x), lst))
        return return_lst
    

    def remove_rubbish(df):
        def remove_false(lst):
            try:
                if (False in lst):
                    while False in lst:
                        lst.remove(False)
                    return lst
                else:
                    return lst
            except:
                return lst
        try:
            df['ticker'] = df['ticker'].apply(remove_false)
            df = df.dropna(axis='index', how='any')
            return df
        except:
            return None

    company_names = firms
    def preprocess_company_names(company_names):
        processed_names = []
        for name in company_names:
        
            core_name = name.replace("Inc.", "").replace('Holdings', '').replace('Corp.', '').replace('Solutions','').replace('Services','').replace("Corporation", "").replace(",", "").replace("PLC", "").replace("Ltd.", "").replace('Platforms', '').replace('News','').replace('Institution','').replace('research','').replace('Replace','').replace('news','').strip()
            processed_names.append(core_name)
        try:
            return list(set(processed_names))
        except:
            return None
    core_company_names = preprocess_company_names(company_names)

    matcher = PhraseMatcher(nlp.vocab, attr="LOWER")


    patterns = list(nlp.pipe(core_company_names))
    matcher.add("COMPANY", patterns)

    @Language.component("company_ner_component")
    def company_ner_component(doc):
        matches = matcher(doc)
        spans = []
        for match_id, start, end in matches:
            span = Span(doc, start, end, label="COMPANY")
            spans.append(span)

     
        doc.ents = spacy.util.filter_spans(spans)
        return doc

    nlp.add_pipe("company_ner_component", last=True)

    def find_companies(text):
        doc = nlp(text)
        detected_firms = set()
        for ent in doc.ents:
            if (ent.label_ == "COMPANY"):
                detected_firms.add(ent.text)
        if (len(detected_firms) == 0):
            return None
        return list(detected_firms)


    #Sachin CSV here
    financial_news = master_input_df
    #b = financial_news[financial_news['title'].str.contains('Amazon')]

    financial_news = financial_news.assign(firms = financial_news['title'].apply(find_companies))
    financial_news = financial_news.dropna(axis='index', how='any')
    financial_news = financial_news.assign(ticker = financial_news['firms'].apply(n_to_t))

    financial_news= remove_rubbish(financial_news)

    test_data = financial_news.explode('ticker')

    test_data = test_data.dropna(axis='index', how='any')

    test_data['combined'] = test_data.apply(lambda row: [row['ticker'], row['publish_date']], axis=1)

    def clean_time(tim):
        if (tim[-6:]=='-05:00'):
            return tim[:-6]
        return tim

    test_data['publish_date'] = test_data['publish_date'].apply(clean_time)

    from datetime import datetime, timedelta
    import yfinance as yf
    import pandas as pd

    def round_down_datetime(dt, period_minutes=60):
       
        if not isinstance(dt, datetime):
            try:
                dt = datetime.strptime(dt, "%Y-%m-%d %H:%M:%S")
            except:
                dt = datetime.now()

     
        period_seconds = period_minutes * 60
        seconds_since_midnight = (dt - datetime.combine(dt.date(), datetime.min.time())).total_seconds()
        rounded_seconds = (seconds_since_midnight // period_seconds) * period_seconds

        return dt.replace(hour=0, minute=0, second=0, microsecond=0) + timedelta(seconds=rounded_seconds)


    def calculate_cumulative_sum(df, up_to_time):
      
        if not isinstance(df.index, pd.DatetimeIndex):
            raise ValueError("The DataFrame index must be a DatetimeIndex.")
        filtered_df = df.between_time("00:00", up_to_time)
        cumulative_daily_sum = filtered_df.groupby(filtered_df.index.date).cumsum()
        return cumulative_daily_sum


    from functools import cache

    @cache
    def download_data_from_datetime(ticker, start_datetime=None, end_datetime=None, interval="60m"):
    
        if start_datetime is None and end_datetime is None:
            end_dt = round_down_datetime(datetime.now(),period_minutes=60)
            start_dt = end_dt - timedelta(days=31)
        elif start_datetime is not None and end_datetime is not None:

            end_dt = end_datetime
            start_dt = start_datetime
            pass
        else:

            raise ValueError("You must provide both start_datetime and end_datetime, or neither.")
     
        df = yf.download(ticker, start=start_dt, end=end_dt, interval=interval)
        return df

    def ticker_vol_price_df(ticker, days_before=31, end_datetime=None):
        if end_datetime is None:
            end_datetime = datetime.now()

        try:
            rounded_down_dt = round_down_datetime(end_datetime)
            print(rounded_down_dt)

            start_datetime_obj = rounded_down_dt - timedelta(days=days_before)
            start_datetime = start_datetime_obj
            end_datetime = rounded_down_dt

            df = download_data_from_datetime(ticker, start_datetime=start_datetime, end_datetime=end_datetime, interval="60m")
            cumulative_sum_df = calculate_cumulative_sum(df, up_to_time=end_datetime.time())
            ticker_price_df = cumulative_sum_df.groupby(cumulative_sum_df.index.date).tail(1)
            return ticker_price_df
        except:
            return None

    def give_vol(lst):
        if (isinstance(lst[0], str) == False):
            return None
        ticker = lst[0]
        end_datetime = lst[1]
        try:
            df = ticker_vol_price_df(ticker, days_before=31,end_datetime=end_datetime)['Volume']
            return (df.tail(1)/(df[-30:-1].mean())).values[0][0]
        except:
            return None
        
    def price_change(lst):
        if (isinstance(lst[0], str) == False):
            return None
        ticker = lst[0]
        end_datetime = lst[1]
        end_dt = round_down_datetime(end_datetime).date()
        start_dt = end_dt - timedelta(days=2)
        df = download_data_from_datetime(ticker, start_dt, end_dt, interval="1d")
        try:
            return df['Close'].pct_change().values[1][0]
        except:
            return None
        
    test_data1 = test_data.assign(vol_prop = test_data['combined'].apply(give_vol))
    test_data2 = test_data1.dropna().assign(price_percent = test_data1.dropna()['combined'].apply(price_change))

    from transformers import pipeline
    pipe1 = pipeline("text-classification", model="ProsusAI/finbert")
    def finbert(text):
            
        text = text[:1500]
        d = pipe1(text)[0]
        if (d['label']=='neutral'):
            return 0
        elif (d['label']=='positive'):
            return d['score']
        else:
            return -d['score']
        
    test_data3 = test_data2.dropna().assign(finbert_score = test_data2.dropna()['text'].apply(finbert))

    import joblib

    loaded_model = joblib.load('regression_model_2.pkl')

    title = test_data3['title'] 
    vol_prop = test_data3['vol_prop']

    input_predict = pd.DataFrame({
        'title': title,
        'vol_prop': vol_prop
    })
    prediction = loaded_model.predict(input_predict)

    test_data3 = test_data3.assign(predicted = prediction)
    test_data3 = test_data3.set_index('title')

    return test_data3

# import pandas as pd
# master_input(pd.read_csv('all-scraped-news-articles.csv').iloc[:20])