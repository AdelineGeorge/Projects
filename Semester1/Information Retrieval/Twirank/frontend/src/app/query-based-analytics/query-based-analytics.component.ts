import { Component, OnInit } from '@angular/core';
import { Observable } from 'rxjs';
import { AnalyticsService } from '../analytics.service';
import { PushBasedService } from '../push-based.service';
@Component({
  selector: 'app-query-based-analytics',
  templateUrl: './query-based-analytics.component.html',
  styleUrls: ['./query-based-analytics.component.css']
})
export class QueryBasedAnalyticsComponent implements OnInit {
  //data = {};
  chartData: any;
  isAvailable = false;
  analyticsData$: Observable<{}> = this.pushbased.resultBasedAnalytics$;
  constructor(private analyticsService: AnalyticsService, private pushbased: PushBasedService) {
   }

  ngOnInit(): void {
    // this.analyticsService.getAnalytics().subscribe(data => {
    //   this.isAvailable = true;
    //   this.chartData = data;
    //   console.log(this.chartData);
    // });
    // console.log('Inside query-based');
  }

}
