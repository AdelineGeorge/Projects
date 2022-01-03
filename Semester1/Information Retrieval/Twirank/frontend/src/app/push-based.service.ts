import { Injectable } from '@angular/core';
import { BehaviorSubject, EMPTY, Subject } from 'rxjs';
import { Tweets, QueryResults, initialState, searchQuery } from './search.interface';
import { map, distinctUntilChanged } from "rxjs/operators";
import { SearchServiceService } from './search-service.service';
import { HttpClient, HttpHeaders, HttpResponse } from '@angular/common/http';
import { AnalyticsService } from './analytics.service';
@Injectable({
  providedIn: 'root'
})
export class PushBasedService {

  constructor(private searchService: SearchServiceService, private httpClient: HttpClient, private analyticsSvc: AnalyticsService) {
    this.getAnalyticsData();
   }
  _resultsState = new BehaviorSubject<QueryResults>(initialState);
  queryResults$ = this.state$.pipe(
    map(s => s.tweetsData),
    distinctUntilChanged()
  );
  resultBasedAnalytics$ = this.state$.pipe(
    map(s => s.resultBasedAnalytics),
    distinctUntilChanged()
  );
  resultsAvailable$ = this.state$.pipe(
    map(s => s.resultsAvailable),
    distinctUntilChanged()
  );
  queryVal$ = this.state$.pipe(
    map(s => s.queryText),
    distinctUntilChanged()
  );
  analyticsData$ = this.state$.pipe(
    map(s => s.analyticsData),
    distinctUntilChanged()
  );
  get state() {
    return this._resultsState.getValue();
  }

  setState(newResultsState: QueryResults) {
    this._resultsState.next(newResultsState);
  }

  get state$() {
    return this._resultsState.asObservable();
  }
  addQueryResults( query: searchQuery) {
    
    this.searchService.search(query).subscribe(data=>{
      const q_data = this.searchService.parsequerybasedanalytics(data['q_data']);
      const parsed_Data = this.searchService.parseRawData(data['results']);
      console.log(parsed_Data);
      var resultsAvailable = false;
      if (parsed_Data.length === 0) {
        resultsAvailable = false;
      }
      else {
        resultsAvailable = true;
      }
      const newState = {
        ...this.state,
        queryText: query.query,
        resultsAvailable,
        tweetsData: parsed_Data,
        resultBasedAnalytics: q_data
      } as QueryResults;
  
      this.setState(newState);
    });
    
  }
  getAnalyticsData() {
    
    this.analyticsSvc.getAnalytics().subscribe(data => {
      
      //const tweetCountData= this.analyticsSvc.parseDataTweetCount(data['tweet_count_per_lang']);
      //const countryVaccineCount = this.analyticsSvc.parseCountryWiseDataVaccine(data['countrywise_vaccine_count']);
      //const top5poi = this.analyticsSvc.getTop5POIS();
      //const vaccineforandagainst = this.analyticsSvc.getVaccForAndAgainstData(data['vacc_for_and_against']);
      //const data1 = {tweetCountData: tweetCountData, countryVaccineCount: countryVaccineCount};
      //this.HiText = data
      const newState = {
        ...this.state,
  
        analyticsData: data
      } as QueryResults;
      this.setState(newState);
    });
    
  }
  addQuerySearchVal(newSearchQuery: string) {
    const newState = {
      ...this.state,

      queryText: newSearchQuery
    } as QueryResults;

    this.setState(newState);
  }

}
