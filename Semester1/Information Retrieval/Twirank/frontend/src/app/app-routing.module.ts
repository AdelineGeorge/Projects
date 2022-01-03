import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';
import { ResultsPageComponent } from './results-page/results-page.component';
import { MainSearchComponent } from './main-search/main-search.component';
import { MainResultsPageComponent } from './main-results-page/main-results-page.component';
import { AnalyticsComponent } from './analytics/analytics.component';
//const routes: Routes = [];
const routes: Routes = [
  {path: '', component: MainSearchComponent},
  { path: 'searchresults', component: MainResultsPageComponent },
  { path: 'analytics', component: AnalyticsComponent },
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { 
  
}
