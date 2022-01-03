import { Component } from '@angular/core';
import { HttpClient, HttpHeaders, HttpResponse } from '@angular/common/http';
@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})
export class AppComponent {
  title = 'Search Engine';
  topics;
  serverData: any = { text: 'Not changed yet!'};
  employeeData: any;
  queryVal = '';
  //HiText: any;
  constructor(private httpClient: HttpClient) {
  }
  search(){
    let httpHeaders = new HttpHeaders({
      'Content-Type' : 'application/json',
      'Cache-Control': 'no-cache'
    });
    console.log(this.queryVal);
    const query = { "query" : this.queryVal};
    this.httpClient.post('http://3.145.133.242:9995/search', query, { headers: httpHeaders }).subscribe(data => {
      
    this.serverData = data;
      //this.HiText = data
      console.log(this.serverData);
    })
  }
  sayHi() {
    this.httpClient.get('http://3.145.133.242:9995/').subscribe(data => {
      this.serverData = data;
      //this.HiText = data
      console.log(this.serverData);
    })
}
}
