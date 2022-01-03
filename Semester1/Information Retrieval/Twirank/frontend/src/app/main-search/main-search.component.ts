import { Component, OnInit } from '@angular/core';
import { SearchServiceService } from '../search-service.service';
import { Router } from '@angular/router';
import { PushBasedService } from '../push-based.service';
@Component({
  selector: 'app-main-search',
  templateUrl: './main-search.component.html',
  styleUrls: ['./main-search.component.css']
})
export class MainSearchComponent implements OnInit {
  queryVal: string;
  serverData: any;
  constructor(private searchService: SearchServiceService,  private router: Router, private pushbased: PushBasedService) { }

  ngOnInit(): void {
  }
  search(){
    const query = { "query" : this.queryVal, "filters": {
      "languages": [],
      "country": [],
      "poi": [],
      "verified": []
    }}
    this.pushbased.addQueryResults(query);
    // let httpHeaders = new HttpHeaders({
    //   'Content-Type' : 'application/json',
    //   'Cache-Control': 'no-cache'
    // });
    // console.log(this.queryVal);
    //this.searchService.search(this.queryVal).subscribe(data=>{
      //const parsed_Data = this.searchService.parseRawData(data);
     // this.searchService.setQueryResults(data);
     // this.router.navigate(['/searchresults']);
    //});
    // const query = { "query" : this.queryVal};
    // this.httpClient.post('http://3.145.133.242:9995/search', query, { headers: httpHeaders }).subscribe(data => {
    //   this.serverData = data;
    //   const parsed_Data = this.searchService.parseRawData(data);
    //   this.searchService.setQueryResults(parsed_Data);
      
    //   this.router.navigate(['/searchresults']);
    // })
  }
}
