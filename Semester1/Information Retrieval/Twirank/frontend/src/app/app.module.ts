import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';
import {FormsModule, ReactiveFormsModule} from '@angular/forms'
import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { HttpClientModule } from '@angular/common/http';
import { RouterModule } from '@angular/router';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';
import { ResultsPageComponent } from './results-page/results-page.component';
import { MainSearchComponent } from './main-search/main-search.component';
import { SearchServiceService } from './search-service.service';
import { NavBarComponent } from './nav-bar/nav-bar.component';
import { AnalyticsComponent } from './analytics/analytics.component';
import { NewsArticlesComponent } from './news-articles/news-articles.component';
import { QueryBasedAnalyticsComponent } from './query-based-analytics/query-based-analytics.component';
import { MainResultsPageComponent } from './main-results-page/main-results-page.component';
import { FiltersComponent } from './filters/filters.component';
import { GoogleChartsModule } from 'angular-google-charts';
@NgModule({
  declarations: [
    AppComponent,
    ResultsPageComponent,
    MainSearchComponent,
    NavBarComponent,
    AnalyticsComponent,
    NewsArticlesComponent,
    QueryBasedAnalyticsComponent,
    MainResultsPageComponent,
    FiltersComponent,
  ],
  imports: [
    BrowserModule,
    AppRoutingModule,
    HttpClientModule,
    BrowserAnimationsModule,
    FormsModule,
    GoogleChartsModule,
    ReactiveFormsModule,
    RouterModule.forRoot([
      {path: '', component: MainSearchComponent},
      {path: 'searchresults', component: ResultsPageComponent},
    ],{useHash:true}),
  ],
  providers: [
    SearchServiceService
  ],
  bootstrap: [AppComponent]
})
export class AppModule { }