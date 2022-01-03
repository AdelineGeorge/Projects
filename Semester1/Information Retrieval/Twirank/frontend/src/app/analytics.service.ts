import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders, HttpResponse } from '@angular/common/http';
import { BehaviorSubject, EMPTY, Subject } from 'rxjs';
import {Observable,of, from } from 'rxjs';
@Injectable({
  providedIn: 'root'
})
export class AnalyticsService {
  data: {} = {};
  
  constructor(private httpClient: HttpClient) { }
  getAnalytics() : Observable<any>{
    var subject = new Subject<{}>();
    this.httpClient.get('http://3.145.133.242:9995/getAnalytics').subscribe(data => {
      const covidtweetsByPOI = this.getCovidRelatedTweetsByPOICount(data['POI_covid_tweets']);
      const tweetCountData= this.parseDataTweetCount(data['tweet_count_per_lang']);
      const countryVaccineCount = this.parseCountryWiseDataVaccine(data['countrywise_vaccine_count']);
      const vaccineforandagainst = this.getVaccForAndAgainstData(data['vacc_for_and_against'])
      this.data = {tweetCountData: tweetCountData, countryVaccineCount: countryVaccineCount,
         vaccineforandagainst: vaccineforandagainst,
        covidtweetsByPOI: covidtweetsByPOI};
      subject.next(this.data);
    })
    return subject.asObservable();
  }
  getCovidRelatedTweetsByPOICount(data) {
    const chartData = {};
    chartData['data'] = [];
    chartData['type'] ='ColumnChart';
    chartData['title'] = 'Number of Covid Related Tweets By Each POI';
    chartData['width'] = 1500;
    chartData['height'] = 600;
    chartData['options'] = {};
    for ( const i in data) {
      const arr1 = [];
      arr1.push(i);
      arr1.push(data[i])
      chartData['data'].push(arr1);
    }
    return chartData;
   
  }
  parseDataTweetCount(data) {
    const chartData = {};
    chartData['data'] = [];
    chartData['type'] ='BarChart';
    chartData['title'] = 'Number of tweets per country';
    chartData['width'] = 500;
    chartData['height'] = 400;
    chartData['options'] = {};
    for ( const i in data) {
      const arr1 = [];
      arr1.push(i);
      arr1.push(data[i])
      chartData['data'].push(arr1);
    }
    return chartData;
  }
  
  getVaccForAndAgainstData(data) {
    // "USA_against": 894,
    //     "INDIA_against": 107,
    //     "MEXICO_against": 99,
    //     "USA_for": 7764,
    //     "INDIA_for": 654,
    //     "MEXICO_for": 721
    const chartData = {};
    //chartData['data'] = [];
    chartData['type'] ='PieChart';
    chartData['title'] = 'CountryWise Vaccine Count';
    chartData['width'] = 450;
    chartData['height'] = 400;
    chartData['options'] = {
      pieHole:0.4
    };
    const temp = {
      type : 'PieChart',
      title : 'CountryWise Vaccine Count',
      width : 450,
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
      chartData['data']  = {
        USA: [],
        India: [],
        Mexico: []
      }
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
      const againstorfor = i.split('_')[1];
      us.push(againstorfor.toUpperCase());
      us.push(data[i] as number);
      if (country === 'USA') {
        chartData1['USA']['data'].push(us);
      }
      if (country === 'MEXICO') {
        chartData1['Mexico']['data'].push(us);
      }
      if (country === 'INDIA') {
        chartData1['India']['data'].push([...us]);
      }
    }
    }
    console.log(chartData1);
    return chartData1;
  }
  parseCountryWiseDataVaccine1(data) {
  }
  getTop5POIS() {
    
  }
  parseCountryWiseDataVaccine(data) {
    const chartData = {};
    //chartData['data'] = [];
    chartData['type'] ='PieChart';
    chartData['title'] = 'CountryWise Vaccine Count';
    chartData['width'] = 400;
    chartData['height'] = 400;
    chartData['options'] = {
      pieHole:0.4
    };
    
    const temp = {
    type : 'PieChart',
    title : 'CountryWise Vaccine Count',
    width : 450,
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
    const usa = [];
    const mex = [];
    const ind = [];
    chartData['data']  = {
      USA: [],
      India: [],
      Mexico: []
    }
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
}
