export interface Tweets {

    id: number;
    country: string;
    mentions: string[];
    tweet_lang: string;
    tweet_en: string;
    tweet_hi: string;
    tweet_de: string;
    hashtags: string[];
    tweet_text: string;
    verified: boolean;
    tweet_date: string;
    urls: string[];
    time_ago: string;
    sentiment: string;
}
export interface CheckboxType {
    name: string;
    checked: Boolean;
}
export interface searchQuery {
    query: string,
    filters: filters
}
export interface filters {
    
        languages: string[],
        country: string[],
        poi: string[],
        verified: string[],
    

}
export interface ChartData {
    data: any[];
    type:string;
    title : string;
    width : number;
    height : number;
    options : {};
}
export interface queryBased {
    countryData: ChartData;
    languageData: ChartData;
    sentimentData: ChartData;
}
export interface QueryResults {
    tweetsData: Tweets[];
    queryText: string;
    resultsAvailable: boolean;
    resultBasedAnalytics: queryBased;
    analyticsData: {};
    filters: filters;
}
export const initialState: QueryResults = {
    tweetsData: [],
    queryText : '',
    resultBasedAnalytics: null,
    resultsAvailable: false,
    analyticsData: null,
    filters: null
  };
// {
//     "_version_": 1711642805707735000,
//     "country": "USA",
//     "id": "1440805434646929410",
//     "mentions": [
//         "bravotweety",
//         "Winslow20Don",
//         "POTUS"
//     ],
//     "score": 9.271122,
//     "text_en": "There is no covid,there is no vaccine, there is no vaccine for covid! The virus",
//     "tweet_date": "2021-09-22T22:29:19Z",
//     "tweet_lang": "en",
//     "tweet_text": "@bravotweety @Winslow20Don @POTUS There is no covid,there is no vaccine, there is no vaccine for covid!  The virus… https://t.co/Ua7POw9Jhz",
//     "urls": [
//         "https://t.co/Ua7POw9Jhz"
//     ],
//     "verified": false
// }