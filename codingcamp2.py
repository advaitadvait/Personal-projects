# Analyze words in CEO earnings announcements
def analyze_words(sentence, year):
    positive_words = ['achieve', 'best', 'exceed', 'surpassed']
    negative_words = ['decrease', 'hell', 'lost', 'reduction']
        
    print("In year", year, "Elon Musk said:", sentence, "\n")
    



news1 = "We were in production for the first six months of this year — man, it was hell and then we just managed to sort of climb out of hell basically part way through June. And now our production line is humming."
news2 = "Great. Thank you. So Q1 2021 was a record quarter on many levels. Tesla achieved record production, deliveries and surpassed $1 billion in non-GAAP net income for the first time. We have seen a real shift in customer perception of electric vehicles and our demand is the best we have ever seen. So this is – if you talk about, we are used to seeing a reduction in demand in the first quarter and we saw an increase in demand that exceeded the normal seasonal reduction in demand in Q1."
analyze_words(news1, 2016)
analyze_words(news2, 2021)
