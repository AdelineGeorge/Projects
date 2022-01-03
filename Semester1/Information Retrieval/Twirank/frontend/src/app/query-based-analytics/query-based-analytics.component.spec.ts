import { ComponentFixture, TestBed } from '@angular/core/testing';

import { QueryBasedAnalyticsComponent } from './query-based-analytics.component';

describe('QueryBasedAnalyticsComponent', () => {
  let component: QueryBasedAnalyticsComponent;
  let fixture: ComponentFixture<QueryBasedAnalyticsComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ QueryBasedAnalyticsComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(QueryBasedAnalyticsComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
