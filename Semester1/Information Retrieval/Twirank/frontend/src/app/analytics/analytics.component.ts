import { Component, OnInit } from '@angular/core';
import { PushBasedService } from '../push-based.service';
import { Observable } from 'rxjs';
@Component({
  selector: 'app-analytics',
  templateUrl: './analytics.component.html',
  styleUrls: ['./analytics.component.css']
})
export class AnalyticsComponent implements OnInit {
  analyticsData$: Observable<{}> = this.pushbased.analyticsData$;
  constructor(private pushbased: PushBasedService) {
    this.pushbased.addQuerySearchVal('');
   }

  ngOnInit(): void {
  }

}
