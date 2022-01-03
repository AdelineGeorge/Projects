import { Component, HostBinding, OnInit } from '@angular/core';
import { Observable } from 'rxjs';
import { SearchServiceService } from '../search-service.service';
import { Tweets } from '../search.interface';
import { PushBasedService } from '../push-based.service';
@Component({
  selector: 'app-results-page',
  templateUrl: './results-page.component.html',
  styleUrls: ['./results-page.component.css']
})
export class ResultsPageComponent implements OnInit {
  @HostBinding('class') public myClasses = 'myclass';
  queryResults$: Observable<Tweets[]> = this.pushbased.queryResults$;
  resultsAvailable$: Observable<boolean> = this.pushbased.resultsAvailable$;
  constructor(private searchService: SearchServiceService, private pushbased: PushBasedService) { 
    //this.queryResults$ = this.searchService.resultsQuery$;
  }
  //queryResults$: Observable<Tweets[]>;
  ngOnInit(): void {
    //this.queryResults = this.searchService.queryResults;
  }

}
