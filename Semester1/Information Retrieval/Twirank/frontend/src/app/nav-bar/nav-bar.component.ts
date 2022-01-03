import { Component, Input, OnInit } from '@angular/core';
import { SearchServiceService } from '../search-service.service';
import { PushBasedService } from '../push-based.service';
import { Observable } from 'rxjs';
@Component({
  selector: 'app-nav-bar',
  templateUrl: './nav-bar.component.html',
  styleUrls: ['./nav-bar.component.css']
})
export class NavBarComponent implements OnInit {
  queryVal: string;
  queryVal$: Observable<string> = this.pushbased.queryVal$;
  @Input() name = '';
  constructor(private searchService: SearchServiceService, private pushbased: PushBasedService) { 
    this.queryVal$.subscribe(data=> {
      this.queryVal = data;
    })
  }

  ngOnInit(): void {
    //this.queryVal = this.searchService.queryVal;
  }
  search(queryVal: string){
    const query = { "query" : this.queryVal, "filters": {
      "languages": [],
      "country": [],
      "poi": [],
      "verified": []
    }}
    this.pushbased.addQueryResults(query);
    
    
  }
}
