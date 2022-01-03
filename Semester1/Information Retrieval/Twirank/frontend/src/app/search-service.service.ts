import { Injectable } from '@angular/core';
import { ChartData, queryBased, QueryResults, searchQuery, Tweets } from './search.interface';
import { HttpClient, HttpHeaders, HttpResponse } from '@angular/common/http';
import { Router } from '@angular/router';
import { BehaviorSubject, EMPTY, Subject } from 'rxjs';
@Injectable({
  providedIn: 'root'
})
export class SearchServiceService {
  resultsQuery$ = new Subject<Tweets[]>();
  queryResults: Tweets[];
  queryVal: string;
  constructor(private httpClient: HttpClient, private router: Router) { }
  search(filters: searchQuery) {
    this.queryVal = filters.query;
    let httpHeaders = new HttpHeaders({
      'Content-Type' : 'application/json',
      'Cache-Control': 'no-cache'
    });
    // const query = { "query" : queryVal, "filters": {
    //   "languages": [],
    //   "country": [],
    //   "POI": [],
    //   "verified": []
    // }};
    //if ( filters.filters.poi.length === 0 && filters.filters.country.length === 0 && filters.filters.languages.length === 0 && filters.filters.verified.length === 0) {
      return this.httpClient.post('http://3.145.133.242:9995/search', filters, { headers: httpHeaders });
    // } else {
    //   return this.httpClient.post('http://3.145.133.242:9995/filter', filters, { headers: httpHeaders });
    // }
    
    // this.httpClient.post('http://3.145.133.242:9995/search', query, { headers: httpHeaders }).subscribe(data => {
    //   const parsed_Data = this.parseRawData(data);
    //   //this.setQueryResults(parsed_Data);
    //   this.resultsQuery$.next(parsed_Data);
    //   //this.router.navigate(['/searchresults']);
    // })
    // return this.resultsQuery$.asObservable();
  }
  setQueryResults(queryRes: Tweets[]) {
    this.queryResults = queryRes;
    console.log(this.queryResults);
  }
  parsequerybasedanalytics(data: {}) {
    const countryData : ChartData = {
      type : 'BarChart',
        title : '',
        width : 550,
        height : 400,
        options : {
          pieHole:0.4
        },
        data : []
    };
    let languageData : ChartData = {
      type : 'PieChart',
      title : '',
      width : 400,
      height : 400,
      options : {
        pieHole:0.4
      },
      data : []
      };
      let sentimentData : ChartData= {
        type : 'PieChart',
        title : '',
        width : 400,
        height : 400,
        options : {
        },
        data : []
        };
    for (const i in data ) {
      if ( i !== 'USA' && i !== 'INDIA' && i !== 'MEXICO'  ) {
        const attribute = i.split('_')[0];
        const val2 = i.split('_')[1]; 
        if (attribute === 'lang' ) {
          
            let language = '';
            if ( val2 === 'en') {
              language = 'English';
            } else if ( val2 === 'es') {
              language = 'Spanish';
            } else {
              language = 'Hindi';
            }
              const us = [];
              us.push(language);
              us.push(data[i] as number);
              languageData.title = 'Distribution of Languages in Search Results'
              languageData.data.push(us);
        }
        if (attribute === 'pos' || attribute === 'neg' || attribute === 'neu') {
          let name = '';
          if ( attribute === 'pos') {
            name = 'Positive Tweet';
          }
          else if ( attribute === 'neg') {
            name = 'Negative Tweet';
          }
          else if ( attribute === 'neu') {
            name = 'Neutral Tweet';
          }
          const us = [];
          us.push(name);
          us.push(data[i] as number);
          sentimentData.title = 'Distribution of sentiments in Search Results'
          sentimentData.data.push(us);
        }
      } else {
        
        //countryData['data'] = [];
        countryData['type'] ='BarChart';
        countryData['title'] = 'Number of tweets per country in Search Results';
        countryData['width'] = 400;
        countryData['height'] = 400;
        countryData['options'] = {};
        const arr1 = [];
        arr1.push(i);
        arr1.push(data[i] as number)
        countryData['data'].push(arr1);
        //console.log()
        }
      }
       return { "countryData": countryData, "languageData": languageData, "sentimentData": sentimentData} as queryBased;
    }
    parsePieChartData(data) {
    const temp = {
    type : 'PieChart',
    title : '',
    width : 550,
    height : 400,
    options : {
      pieHole:0.4
    }
    };
    const chartData1 = {
      USA: {...temp},
      India: {...temp},
      Mexico: {...temp}
    };
    chartData1['USA']['data'] = [];
    chartData1['Mexico']['data'] = [];
    chartData1['India']['data'] = [];
    chartData1['USA']['title'] = 'USA ' + chartData1['USA']['title'];
    chartData1['Mexico']['title'] = 'Mexico ' + chartData1['Mexico']['title'];
    chartData1['India']['title'] = 'India ' + chartData1['India']['title'];
    for ( const i in data) {
      var us = [];
      if ( i !== 'USA_Total' && i !== 'Mexico_Total' && i !== 'India_Total') {
      const country = i.split('_')[0];
      const vaccineName = i.split('_')[1];
      us.push(vaccineName);
      us.push(data[i] as number);
      if (country === 'USA') {
        chartData1['USA']['data'].push(us);
      }
      if (country === 'Mexico') {
        chartData1['Mexico']['data'].push(us);
      }
      if (country === 'India') {
        chartData1['India']['data'].push([...us]);
      }
    }
    }
    return chartData1;
  }
  parseRawData(data): Tweets[] {
    const parsedData1: Tweets[] = [];
    for ( const i in data) {
      let dateSent = new Date(data[i]['tweet_date']);
      let currentDate = new Date();
      //dateSent = new Date(dateSent);

      const days = Math.floor((Date.UTC(currentDate.getFullYear(), currentDate.getMonth(), currentDate.getDate()) - Date.UTC(dateSent.getFullYear(), dateSent.getMonth(), dateSent.getDate()) ) /(1000 * 60 * 60 * 24));
      const parsedData = <Tweets>{};
      parsedData.id = data[i]['id'];
      parsedData.mentions = data[i]['mentions'];
      parsedData.tweet_lang = data[i]['tweet_lang'];
      parsedData.hashtags = data[i]['hashtags'];
      parsedData.tweet_date = data[i]['tweet_date'];
      parsedData.verified = data[i]['verified'];
      parsedData.tweet_text = data[i]['tweet_text'];
      parsedData.sentiment = data[i]['sentiment'];
      parsedData.time_ago = days + ' days ago';
      parsedData.urls = data[i]['urls'];
      parsedData1.push(parsedData);
    }
    return parsedData1;
  }
  
  filter() {
    
  }
  
  
}
